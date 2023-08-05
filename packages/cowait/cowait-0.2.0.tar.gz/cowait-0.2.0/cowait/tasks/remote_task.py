from __future__ import annotations
import asyncio
from concurrent.futures import Future
from cowait.types import type_from_description
from .errors import TaskError
from .definition import TaskDefinition
from .status import WAIT, WORK, FAIL, DONE


class RemoteTask(TaskDefinition):
    def __init__(self, taskdef: TaskDefinition, cluster):
        kwargs = taskdef.serialize()
        super().__init__(**kwargs)
        self.conn = None
        self.nonce = 0
        self.cluster = cluster
        self.future = Future()
        self.awaitable = asyncio.wrap_future(self.future)
        self.status = WAIT
        self.error = None
        self.result = None

    def __await__(self):
        return self.awaitable.__await__()

    @property
    def done(self) -> bool:
        return self.future.done()

    def destroy(self) -> None:
        self.cluster.destroy(self.id)

    def set_status(self, status: str) -> None:
        # sanity checks
        if self.status == FAIL and status == DONE:
            raise RuntimeError('Cant complete a failed task')

        if self.status == DONE and status == FAIL:
            raise RuntimeError('Cant fail a failed completed')

        # update status
        self.status = status

    def set_error(self, error: str) -> None:
        self.set_status(FAIL)
        self.error = error
        if not self.future.done():
            self.future.set_exception(TaskError(error))

    def set_result(self, result: any, result_type: any = 'any') -> None:
        # unpack type & deserialize result
        result_type = type_from_description(result_type)
        result = result_type.deserialize(result)

        self.set_status(DONE)
        self.result = result
        if not self.future.done():
            self.future.set_result(result)

    async def wait_for_init(self, timeout=30) -> None:
        if self.status != WAIT:
            raise RuntimeError(f'Cant await task with status {self.status}')

        slept = 0
        interval = 0.2
        while True:
            if self.status == WORK:
                return
            if self.status == FAIL:
                raise RuntimeError(
                    f'Awaited task failed with error: {self.error}')

            if slept > timeout:
                raise TimeoutError('Task took to long to initialize')

            await asyncio.sleep(interval)
            slept += interval

    async def call(self, method, args={}):
        if self.status != WORK:
            await self.wait_for_init()
            # raise RuntimeError(
            #     f'RPC is only available when status = WORK, was {self.status}. '
            #     f'Attempted to call {method}')

        return await self.conn.rpc.call(method, args)

    async def stop(self):
        # special case RPC - it always causes a send exception
        await self.call('stop')

    def __getattr__(self, method):
        async def magic_rpc(**kwargs):
            return await self.call(method, kwargs)
        return magic_rpc
