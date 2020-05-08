

class Pipe:
    def __init__(self):
        self.broad_cast_list = []  # list of target filters
        # sender holds a copy of pipe instance

    def broad_cast_new_task(self, task: str):
        for i in self.broad_cast_list:
            i.receive_task(task)

    def add_in_broadcast_list(self, filtre):
        self.broad_cast_list.append(filtre)
