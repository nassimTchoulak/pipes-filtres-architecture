from .Filter import Filter
from .Pipe import Pipe
from tkinter import *
from tkinter.ttk import *
from threading import Thread, Event
from queue import Queue
from time import sleep, time


class GuiFilter(Filter):
    def __init__(self, forward_pipe: Pipe):
        super().__init__(forward_pipe)
        self.task_switch = {
            "update_trace": self.update_trace,
            "update_result": self.update_result
        }
        self.lbl_result: Label
        self.lbl_trace: Label

        self.txt_op1: Entry
        self.txt_op2: Entry

    def update_result(self, payload: str):
        self.lbl_result.configure(text=payload)

    def update_trace(self, payload: str):

        self.lbl_trace.configure(text=payload)

    def send_trace_request(self):  # send the first data request to trace
        print(' give trace invoked ')
        self.send_task_done({'action': 'trace_out', 'payload': 'not used'})

    def send_calcule_somme(self):
        print({'action': 'calculer_somme', 'payload': self.txt_op1.get() + "-" + self.txt_op2.get()})
        self.send_task_done({'action': 'calculer_somme', 'payload': self.txt_op1.get() + "-" + self.txt_op2.get()})

    def send_calculer_produit(self):
        print({'action': 'calculer_produit', 'payload': self.txt_op1.get() + "-" + self.txt_op2.get()})
        self.send_task_done({'action': 'calculer_produit', 'payload': self.txt_op1.get() + "-" + self.txt_op2.get()})

    def send_caculer_factoriel(self):
        print({'action': 'calculer_produit', 'payload': self.txt_op1.get()})
        self.send_task_done({'action': 'calculer_factoriel', 'payload': self.txt_op1.get()})

    def backgroud_update_capture(self):
        while True:
            print(" back started ")
            task = self.taskQueue.get(block=True)  # block the thread if no task available & unlock when new inserted
            print(" back continues ")
            try:
                # select the task from action attribute !! if doesnt exist then key error
                func = self.task_switch[task['action']]
                # execute with payload
                func(task['payload'])

            except:
                pass

    def execute(self) -> None:

        # run sync data in diffrent thread
        th1 = Thread(target=self.backgroud_update_capture)
        th1.start()

        root = Tk()
        root.geometry('1000x800')
        style = Style()
        style.configure('TButton', font=('calibri', 15, 'normal'), foreground='#002148', borderwidth=0,
                        highlightthickness=0)
        style.configure('TLabel', font=('calibri', 20, 'bold'), foreground='#000000', borderwidth=0,
                        highlightthickness=0)
        style.configure('TEntry', font=('calibri', 18, 'normal'), foreground='#000000', borderwidth=0,
                        highlightthickness=0)

        titre_all = Label(root, text="Le Programme de Trace ", style="TLabel")
        titre_all.grid(row=0, column=0, padx=10, pady=10)

        label_op1 = Label(root, text="Oprand 1 :", font=("Helvetica", 16))
        label_op1.grid(row=1, column=1, padx=10, pady=10)

        self.txt_op1 = Entry(root, width=30, style="TEntry")
        self.txt_op1.grid(row=2, column=1, padx=10, pady=10)

        label_op2 = Label(root, text="Oprand 2 :", font=("Helvetica", 16))
        label_op2.grid(row=3, column=1, padx=10, pady=10)

        self.txt_op2 = Entry(root, width=30, style="TEntry")
        self.txt_op2.grid(row=4, column=1, padx=10, pady=10)

        label_op_res = Label(root, text="Résultat :", font=("Helvetica", 16))
        label_op_res.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_result = Label(root, text=" * * ", font=("Helvetica", 16))
        self.lbl_result.grid(row=6, column=1, padx=10, pady=10)

        btn_somme = Button(root, text=" la somme ", style="TButton", command=self.send_calcule_somme)
        btn_somme.grid(row=1, column=0, padx=10, pady=10)

        btn_produit = Button(root, text=" le produit ", style="TButton", command=self.send_calculer_produit)
        btn_produit.grid(row=3, column=0, padx=10, pady=10)

        btn_facto = Button(root, text=" Factoriel ", style="TButton", command=self.send_caculer_factoriel)
        btn_facto.grid(row=5, column=0, padx=10, pady=10)

        btn_trace = Button(root, text=" La trace ", style="TButton" , command=self.send_trace_request )
        btn_trace.grid(row=7, column=0, padx=10, pady=10)

        label_trace = Label(root, text="Trace:", font=("Helvetica", 16))
        label_trace.grid(row=1, column=2, padx=100, pady=10)

        self.lbl_trace = Label(root, text="res trace", font=("Helvetica", 12))
        self.lbl_trace.grid(row=2, column=2, padx=100, pady=10)

        root.mainloop()
