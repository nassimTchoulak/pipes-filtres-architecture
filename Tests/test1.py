import unittest
from classes.Filter import Filter
from classes.Pipe import Pipe
from classes.GuiFilter import GuiFilter
from classes.CalculeFilter import CalculeFilter


class MyTestCase(unittest.TestCase):

    def test_Pipe(self):
        pip = Pipe()
        fl = GuiFilter(pip)
        fl.receive_task("{'action':'test'}")
        self.assertEqual(fl.taskQueue.get(block=True)['action'], "test")  # block locks the thread until new value !!!

    def test_Pipe_empty(self):
        pip = Pipe()
        fl = GuiFilter(pip)
        fl.receive_task("{'action:'test'}")  # false value
        self.assertEqual(fl.taskQueue.empty(), True)

    def test_Pipe_empty_clacule(self):
        pip = Pipe()
        fl = CalculeFilter(pip)
        fl.receive_task("{'action:'test'}")  # false value
        self.assertEqual(fl.taskQueue.empty(), True)



    def test_pipe_sending(self):
        # declare pipes
        pip_in = Pipe()
        pip_out = Pipe()

        # declare filtres using created pipes
        fl = GuiFilter(pip_out)

        # link pipes with thier destination
        pip_in.add_in_broadcast_list(fl)  # ajouter pip_in en entré our fl

        pip_in.broad_cast_new_task("{'action':'test'}")
        self.assertEqual(fl.taskQueue.get(block=True)['action'], "test")






if __name__ == '__main__':
    unittest.main()
