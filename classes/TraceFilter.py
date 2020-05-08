from .Filter import Filter
from .Pipe import Pipe


class TraceFilter(Filter):
    def __init__(self, forward_pipe: Pipe):
        super().__init__(forward_pipe)
        self.traces = []

        # dictionnaire des actions => leur function
        self.swith_task = {'trace_in': self.trace_save, 'trace_out': self.trace_out}

    def trace_save(self, value: str):
        self.traces.append(value)

    def trace_out(self, extra: str):
        result = ""
        for i in self.traces:
            result = result + i + " \n "

        res1 = {'action': 'update_trace', 'payload': result}

        self.send_task_done(res1)

    def execute(self) -> None:
        while True:

            task = self.taskQueue.get(block=True)  # block the thread if no task available & unlock when new inserted

            try:
                # select the task from action attribute !! if doesnt exist then key error
                func = self.swith_task[task['action']]
                # execute with payload
                func(task['payload'])


            except:
                pass
