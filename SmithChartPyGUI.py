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

class SchematicFrame(Tk.Frame):
    def im_reorder(self,event,old,new):
        self.canvas1.move(self.item_arr[new], (old-new)*self.im_x_size, 0)
        self.item_arr[old], self.item_arr[new] = self.item_arr[new], self.item_arr[old]
        
        self.image_selection=new

    def down_click(self,event):
        #global image_selection

        self.image_selection=int(event.x/self.im_x_size)
        
        self.canvas1.delete(self.box)
        self.draw_box(self.canvas1,event.x/self.im_x_size)    

        #self.canvas1.tag_raise(self.image_selection)
        #self.canvas1.tag_raise(self.box)
        
    def follow_mouse(self,event):
        #global imag_selection
        #global drag
        
        new_x, new_y = event.x, event.y
        old_x, old_y = self.canvas1.coords(self.item_arr[self.image_selection])
        
        self.canvas1.move(self.item_arr[self.image_selection], new_x-old_x, new_y-old_y)

        if int(new_x/self.im_x_size) != int(old_x/self.im_x_size):
            self.im_reorder(event,int(old_x/self.im_x_size),int(new_x/self.im_x_size))
            item_n=int(new_x/self.im_x_size)

        self.drag=True
        
    def draw_box(self,canvas,n):
        w=2
        self.box = canvas.create_rectangle((n)*self.im_x_size+w, w ,(n+1)*self.im_x_size-w/2, self.im_y_size-w/2,
                                           width=w,dash='.')
        self.canvas1.tag_raise(self.box)

    def reposition_image(self,event):
        #global drag
        
        new_x, new_y = event.x, event.y
        
        if self.drag==True:
            self.canvas1.move(self.item_arr[int(new_x/self.im_x_size)],-new_x%self.im_x_size-0.5*self.im_x_size,-new_y+0.5*self.im_y_size)
            self.drag=False

    def __init__(self,parent):
        self.im_y_size=150
        self.im_x_size=100

        self.box=None
        self.drag=False
        self.image_selection=0
        
        self.parent=parent
        Tk.Frame.__init__(self,parent)
        
        self.canvas1 = Tk.Canvas(parent,width=850, height=150)#,scrollregion=(0,0,1000,150)
        self.canvas1.grid(row=3,column=0,columnspan=3,sticky=Tk.W)
        self.canvas1.configure(background='white')
        
        capse = "icons/Cseries2.gif"
        capsh = "icons/Cshunt2.gif"
        self.CapIconSe = Tk.PhotoImage(file=capse)
        self.CapIconSh = Tk.PhotoImage(file=capsh)
        
        indse = "icons/Lseries2.gif"
        indsh = "icons/Lshunt2.gif"
        self.IndIconSe = Tk.PhotoImage(file=indse)
        self.IndIconSh = Tk.PhotoImage(file=indsh)
        
        Match=[{'type':self.CapIconSh},{'type':self.CapIconSe},{'type':self.IndIconSe},{'type':self.IndIconSh}]

        self.item_arr=[]
        x = (self.im_x_size)/2.0
        y = (self.im_y_size)/2.0
        for n,elem in enumerate(Match):
            self.item_arr.append(self.canvas1.create_image(x+100*n, y, image=elem['type']))

        self.draw_box(self.canvas1,0)

        self.canvas1.bind('<Button-1>', self.down_click)
        ##canvas1.bind('<Button-3>', right_click)
        self.canvas1.bind('<B1-Motion>', self.follow_mouse)
        self.canvas1.bind('<ButtonRelease-1>', self.reposition_image)


class MainWindow(Tk.Frame):
    def __init__(self,parent):
        Tk.Frame.__init__(self,parent)
        fig = Figure(figsize=(7, 7), dpi=100)
        fig.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99)
        mainplot = fig.add_subplot(111,aspect=1)

        PlotSmith(mainplot)

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
        
        ##NavigationToolbar2TkAgg uses pack internally, so grid cannot be used
        ##Frame used to get around this.
        #NavBarFrame=Tk.Frame(root)
        #NavBarFrame.grid(row=2,column=1,sticky=Tk.W)
        #plttoolbar = NavigationToolbar2TkAgg(pltcanvas, NavBarFrame)
        #plttoolbar.pack()

        #SCHEMATIC FRAME
        self.im_size=150
        SchemFrame = Tk.Frame(root)
        SchemFrame.grid(row=2,column=0,columnspan=2,sticky=Tk.W)
        Schem = SchematicFrame(SchemFrame)
        #Schem.grid(row=0,column=0)

        self.net=network()

        #TEST CASE -- matching 50.0 Ohms to ~5.0 Ohms at 2 GHz
 
        L1=ind(0.80e-9)
        C1=cap(6.3e-12,shunt=1)    
        L2=ind(2.0e-9)
        C2=cap(1.6e-12,shunt=1)

        self.net.element_array.append(C2)
        self.net.element_array.append(L2)
        self.net.element_array.append(C1)
        self.net.element_array.append(L1)

        #Draw
        self.center_freq=2.0e9
        curves=[]
        nodeZ=self.net.compute_node_impedances(self.center_freq)
        for i in range(len(nodeZ)-1):
            if self.net.element_array[i].orientation==0:
                curves.append(ConstImpedCurve(nodeZ[i],nodeZ[i+1],100))
                mainplot.plot(curves[i][0],curves[i][1],lw=3,color='b')
            elif self.net.element_array[i].orientation==1:
                curves.append(ConstAdmitCurve(nodeZ[i],nodeZ[i+1],100))
                mainplot.plot(curves[i][0],curves[i][1],lw=3,color='b')
                
        for i in range(len(nodeZ)):
            Gam=ZtoGamma(nodeZ[i])
            #print Gam
            mainplot.plot(Gam.real,Gam.imag,'or')

        

root=Tk.Tk()
root.wm_title("Impedance Matching Tool")
MainWindow(root)
root.mainloop()

