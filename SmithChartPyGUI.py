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

######################################################
#SCHEM SETUP
im_size=150
box=None
drag=False
image_selection=0

def draw_box(canvas,n):
    global box
    w=3
    box = canvas.create_rectangle((n)*im_size+w, w ,(n+1)*im_size-w/2, 150-w,
                                  width=w,dash='.')
    canvas1.tag_raise(box)

def down_click(event):
    global image_selection

    image_selection=int(event.x/im_size)
    
    canvas1.delete(box)
    draw_box(canvas1,event.x/im_size)   

def im_reorder(event,old,new):
    global image_selection
    
    canvas1.move(item_arr[new], (old-new)*im_size, 0)
    item_arr[old], item_arr[new] = item_arr[new], item_arr[old]
    
    image_selection=new


def follow_mouse(event):
    global imag_selection
    global drag
    
    new_x, new_y = event.x, event.y
    old_x, old_y = canvas1.coords(item_arr[image_selection])
    
    canvas1.move(item_arr[image_selection], new_x-old_x, new_y-old_y)

    if int(new_x/im_size) != int(old_x/im_size):
        im_reorder(event,int(old_x/im_size),int(new_x/im_size))
        item_n=int(new_x/im_size)

    drag=True


def reposition_image(event):
    global drag
    
    new_x, new_y = event.x, event.y
    
    if drag==True:
        canvas1.move(item_arr[int(new_x/im_size)],-new_x%im_size-0.5*im_size,-new_y+0.5*im_size)
        drag=False


######################################################
root = Tk.Tk()
root.wm_title("Embedding in TK")

fig = Figure(figsize=(6, 6), dpi=100)
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


    
#PALETTE FRAME
Palette = Tk.Frame(root)
Palette.grid(row=1,column=0,sticky=Tk.N)
button1=Tk.Button(Palette,text="SeriesC")
button1.grid(row=0,column=0)
button1=Tk.Button(Palette,text="ShuntC")
button1.grid(row=0,column=1)
button1=Tk.Button(Palette,text="SeriesL")
button1.grid(row=1,column=0)
button1=Tk.Button(Palette,text="SeriesL")
button1.grid(row=1,column=1)
entry1=Tk.Entry(Palette,width=5)
entry1.grid(row=2,column=0)

#PLOT FRAME
PlotFrame = Tk.Frame(root)
PlotFrame.grid(row=1,column=1)
pltcanvas = FigureCanvasTkAgg(fig, master=PlotFrame)
pltcanvas.get_tk_widget().grid(row=1,column=1)
#NavigationToolbar2TkAgg uses pack internally, so grid cannot be used
#Frame used to get around this.
#NavBarFrame=Tk.Frame(root)
#NavBarFrame.grid(row=1,column=1,sticky=Tk.W)
#plttoolbar = NavigationToolbar2TkAgg(pltcanvas, NavBarFrame)
#plttoolbar.pack()

############################################################
#SCHEMATIC FRAME
SchemFrame = Tk.Frame(root)
SchemFrame.grid(row=3,column=0,columnspan=2,sticky=Tk.W)

capse = "icons/C.gif"
capsh = "icons/Csh.gif"
CapIconSe = Tk.PhotoImage(file=capse)
CapIconSh = Tk.PhotoImage(file=capsh)

indse = "icons/Lse.gif"
indsh = "icons/Lsh.gif"
IndIconSe = Tk.PhotoImage(file=indse)
IndIconSh = Tk.PhotoImage(file=indsh)

Match=[{'type':CapIconSh},{'type':IndIconSe},{'type':CapIconSe},{'type':IndIconSh}]

canvas1 = Tk.Canvas(SchemFrame,width=750, height=150)#,scrollregion=(0,0,1000,1000)
canvas1.grid(row=0,column=0)

item_arr=[]
x = (im_size)/2.0
y = (im_size)/2.0
for n,elem in enumerate(Match):
    item_arr.append(canvas1.create_image(x+150*n, y, image=elem['type']))

draw_box(canvas1,0)

canvas1.bind('<Button-1>', down_click)
#canvas1.bind('<Button-3>', right_click)
canvas1.bind('<B1-Motion>', follow_mouse)
canvas1.bind('<ButtonRelease-1>', reposition_image)

#########################
############################################################
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
