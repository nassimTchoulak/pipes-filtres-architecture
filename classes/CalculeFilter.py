from .Filter import Filter
from .Pipe import Pipe
from .Trace import Trace
import math


class CalculeFilter(Filter):
    def __init__(self, forward_pipe: Pipe):
        super().__init__(forward_pipe)
        self.task_switcher = {"calculer_somme": self.somme,
                              "calculer_produit": self.produit,
                              "calculer_factoriel": self.factoriel}

    def somme(self, payload: str):
        try:
            params = payload.split("-")
            nbs = []
            for i in params:
                nbs.append(int(i))

            res = nbs[0] + nbs[1]

            res1 = {'action': 'update_result', 'payload': res.__str__()}
            res2 = {'action': 'trace_in',
                    # 'payload': "calcule filtre a fait " + params[0] + "+" + params[1] + "=" + res.__str__()}
                    'payload': Trace(' calcule Filtre', 'somme', payload, res.__str__()).__str__()}

            self.send_task_done(res1)  # pour la mise a jour action
            self.send_task_done(res2)  # pour garder la trace de l'operation

        except:
            pass
        return 0

    def produit(self, payload: str):
        params = payload.split("-")
        nbs = []
        for i in params:
            nbs.append(int(i))

        res = nbs[0] * nbs[1]
        res1 = {'action': 'update_result', 'payload': res.__str__()}
        res2 = {'action': 'trace_in',
                'payload': Trace(' calcule Filtre', 'somme', payload, res.__str__()).__str__()}
        self.send_task_done(res1)
        self.send_task_done(res2)

    def factoriel(self, payload: str):
        nb = int(payload)

        res = math.factorial(nb)
        res1 = {'action': 'update_result', 'payload': res.__str__()}
        res2 = {'action': 'trace_in',
                'payload': Trace(' calcule Filtre', 'factoriel', payload, res.__str__()).__str__()}
        self.send_task_done(res1)
        self.send_task_done(res2)

    def execute(self) -> None:
        # create out

        while True:

            task = self.taskQueue.get(block=True)  # block the thread if no task available & unlock when new inserted

            try:
                # select the task from action attribute !! if doesnt exist then key error
                func = self.task_switcher[task['action']]
                # execute with payload
                func(task['payload'])

            except:
                pass
