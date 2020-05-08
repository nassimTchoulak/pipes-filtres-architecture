from tkinter import *
from tkinter.ttk import *
from threading import Thread, Event
from queue import Queue
from time import sleep, time
from classes.CalculeFilter import CalculeFilter
from classes.Pipe import Pipe
from classes.GuiFilter import GuiFilter
from classes.TraceFilter import TraceFilter

# declare pipes
pipe_gui_out = Pipe()  # pipe de sortie de Gui et entré de Calcule

pipe_calcule_out = Pipe()  # pipe de sortie de Calcule et entré vers Gui et Trace

pipe_trace_out = Pipe()  # pipe de sortie de Trace et entré vers Gui /get trace

# declare filters with their defined forwarding pipes
gui: GuiFilter = GuiFilter(pipe_gui_out)
calcule: CalculeFilter = CalculeFilter(pipe_calcule_out)
trace: TraceFilter = TraceFilter(pipe_trace_out)

# link pipes with their destination filters
pipe_gui_out.add_in_broadcast_list(calcule)
pipe_gui_out.add_in_broadcast_list(trace)

pipe_calcule_out.add_in_broadcast_list(gui)
pipe_calcule_out.add_in_broadcast_list(trace)

pipe_trace_out.add_in_broadcast_list(gui)

# main thread handels gui rest 2 handels calcule et trace

th1 = Thread(target=calcule.execute)

th2 = Thread(target=trace.execute)

th1.start()
th2.start()

gui.execute()
