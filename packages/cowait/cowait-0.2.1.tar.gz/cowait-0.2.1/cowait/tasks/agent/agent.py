from datetime import datetime, timezone
from cowait.tasks import Task, TaskDefinition, sleep, rpc
from cowait.network import Conn, get_local_connstr
from cowait.tasks.status import DONE, FAIL
from cowait.tasks.messages import TASK_INIT, TASK_STATUS, TASK_FAIL
from .tasklist import TaskList
from .subscriptions import Subscriptions
from .api import Dashboard, TaskAPI


class Agent(Task):
    def init(self):
        self.tasks = TaskList(self)
        self.subs = Subscriptions(self)

        # subscriber events
        async def send_state(conn: Conn) -> None:
            """" sends the state of all known tasks """
            for task in self.tasks.values():
                await conn.send({
                    'type': TASK_INIT,
                    'id':   task.id,
                    'task': task.serialize(),
                })
        self.subs.on('subscribe', send_state)

        self.token = self.meta['http_token']

        # create http server
        self.node.http.add_routes(TaskAPI(self).routes('/api/1/tasks'))
        self.node.http.add_routes(Dashboard().routes())
        self.node.http.auth.add_token(self.token)

    async def run(self, **inputs) -> dict:
        if '/' in self.routes:
            url = self.routes['/']['url']
            print('Agent ready. Dashboard available at:')
            print(f'{url}?token={self.token}')
        else:
            print('Warning: No route set for /, dashboard not available.')

        # monitor tasks
        while True:
            running_tasks = self.cluster.list_all()
            for id, task in self.tasks.items():
                # skip tasks that are done or failed
                if task.status == DONE or task.status == FAIL:
                    continue

                # ensure task is still in the list of running tasks
                # if not, consider it lost.
                if id not in running_tasks:
                    # compute task age
                    since = datetime.now(timezone.utc) - task.created_at
                    error = f'Task lost after {since}'

                    # update task state record
                    await self.tasks.on_status(None, id=id, status=FAIL)
                    await self.tasks.on_fail(None, id=id, error=error)

                    # emulate failure messages to parent
                    await self.node.parent.msg(type=TASK_STATUS, id=id, status=FAIL)
                    await self.node.parent.msg(type=TASK_FAIL, id=id, error=error)

                    # emulate failure messages to subscribers
                    await self.subs.forward(None, id=id, type=TASK_FAIL, error=error)
                    await self.subs.forward(None, id=id, type=TASK_STATUS, status=FAIL)

            await sleep(5.0)

        return {}

    @rpc
    async def destroy(self, task_id) -> None:
        self.cluster.destroy(task_id)

    @rpc
    async def destroy_all(self) -> None:
        self.cluster.destroy_all()

    @rpc
    async def list_tasks(self) -> list:
        return self.cluster.list_all()

    @rpc
    async def get_agent_url(self) -> str:
        url = get_local_connstr()
        return f'{url}?token={self.token}'

    @rpc
    async def spawn(
        self,
        name: str,
        image: str,
        id: str = None,
        ports: dict = {},
        routes: dict = {},
        inputs: dict = {},
        meta: dict = {},
        env: dict = {},
        cpu: str = '0',
        memory: str = '0',
        owner: str = '',
        **kwargs: dict,
    ) -> dict:
        if not isinstance(name, str) and issubclass(name, Task):
            name = name.__module__

        # todo: throw error if any input is a coroutine

        task = self.cluster.spawn(TaskDefinition(
            id=id,
            name=name,
            image=image,
            upstream=get_local_connstr(),
            meta=meta,
            ports=ports,
            routes=routes,
            env=env,
            cpu=cpu,
            memory=memory,
            owner=owner,
            inputs={
                **inputs,
                **kwargs,
            },
        ))

        # authorize id
        self.node.http.auth.add_token(id)

        # register with subtask manager
        self.subtasks.watch(task)

        return task.serialize()
