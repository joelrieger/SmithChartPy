from plot_funcs import *
from network_classes import *

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")


fig = Figure(figsize=(8, 8), dpi=100)
fig.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99)
mainplot = fig.add_subplot(111,aspect=1)
#t = arange(0.0, 3.0, 0.01)
#s = sin(2*pi*t)

PlotSmith(mainplot)
#mainplot.plot(t, s)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

pltcanvas = FigureCanvasTkAgg(fig, master=root)
pltcanvas.get_tk_widget().grid(row=1,column=1)
plttoolbar = NavigationToolbar2TkAgg(pltcanvas, root)
plttoolbar.grid(row=2,column=1,sticky=Tk.W)

#########################
net=network()

#TEST CASE -- matching 50.0 Ohms to ~5.0 Ohms at 2 GHz
    
L1=ind(0.80e-9)
C1=cap(6.3e-12,shunt=1)    
L2=ind(2.0e-9)
C2=cap(1.6e-12,shunt=1)

net.element_array.append(C2)
net.element_array.append(L2)
net.element_array.append(C1)
net.element_array.append(L1)

#Draw
freq=2.0e9
curves=[]
nodeZ=net.compute_node_impedances(freq)
for i in range(len(nodeZ)-1):
    if net.element_array[i].orientation==0:
        curves.append(ConstImpedCurve(nodeZ[i],nodeZ[i+1],100))
        mainplot.plot(curves[i][0],curves[i][1],lw=3,color='b')
    elif net.element_array[i].orientation==1:
        curves.append(ConstAdmitCurve(nodeZ[i],nodeZ[i+1],100))
        mainplot.plot(curves[i][0],curves[i][1],lw=3,color='b')
        
for i in range(len(nodeZ)):
    Gam=ZtoGamma(nodeZ[i])
    print Gam
    mainplot.plot(Gam.real,Gam.imag,'or')

##########################
    
Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.
