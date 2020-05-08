from abc import ABC, abstractmethod
from queue import Queue
import ast
import classes.Pipe


class Filter(ABC):

    def __init__(self, forward_pipe: classes.Pipe):
        self.taskQueue = Queue(maxsize=0)
        self.exit_pipe = forward_pipe

    @abstractmethod
    def execute(self) -> None:  # here we get items from the queue & confinue our task
        pass

    # invoked by the pipe to send data & tasks
    def receive_task(self, task: str):
        try:

            task_object = ast.literal_eval(task)
            self.taskQueue.put(task_object)

        except:
            pass

    # transferer le donnés au pipe de sortie pour les prochains filtres
    def send_task_done(self, result: dict):
        self.exit_pipe.broad_cast_new_task(result.__str__())
