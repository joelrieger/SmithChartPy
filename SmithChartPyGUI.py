"""
Author: Joel Rieger

October 29, 2016

Description: Smith Chart matching tool
"""

from plot_funcs import *
from canvas_slider import *
from network_class import *
from schematic_frame import *

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as Tk

class MainWindow(Tk.Frame):
    def __init__(self,parent):
        Tk.Frame.__init__(self,parent)
        fig = Figure(figsize=(7, 7), dpi=100)
        fig.subplots_adjust(left=0.01, bottom=0.01, right=0.99, top=0.99)
        self.mainplot = fig.add_subplot(111,aspect=1)

        self.curves=[]
        self.dots=[]

        PlotSmith(self.mainplot)

        parent.bind('<Up>',self.test)

        #fig.draw(0)

        self.settings={'centerfreq':2.0e9,
                       'lowerfreq':1.5e9,
                       'upperfreq':2.5e9,
                       'SmithImpedance':50.0,
                       'InputImpedance':50+0*1j,
                       'LoadImpedance':50+0*1j}

        #PALETTE FRAME
        Palette = Tk.Frame(root)
        Palette.grid(row=1,column=0,sticky=Tk.N)
        
        button1=Tk.Button(Palette,text="SeriesC", command=self.add_series_c)
        button1.grid(row=0,column=0)
        button1=Tk.Button(Palette,text="ShuntC", command=self.add_shunt_c)
        button1.grid(row=0,column=1)
        button1=Tk.Button(Palette,text="SeriesL", command=self.add_series_l)
        button1.grid(row=1,column=0)
        button1=Tk.Button(Palette,text="ShuntL", command=self.add_shunt_l)
        button1.grid(row=1,column=1)

        slider_canvas=Tk.Canvas(Palette,width=50)
        slider=SliderFrame(slider_canvas)
        slider.grid(row=2,column=0)

        #COMPONENT CONTROL BUTTON FRAMES (i.e. delete, edit)
        CmpCntrl = Tk.Frame(root)
        CmpCntrl.grid(row=1,column=0,sticky=Tk.S)
        button1=Tk.Button(CmpCntrl,text="Delete",command=self.delete_element)
        button1.grid(row=0,column=0)
        button1=Tk.Button(CmpCntrl,text="Edit",command=self.edit_element)
        button1.grid(row=0,column=1)
        
        #PLOT FRAME
        PlotFrame = Tk.Frame(root)
        PlotFrame.grid(row=1,column=1)
        self.pltcanvas = FigureCanvasTkAgg(fig, master=PlotFrame)
        self.pltcanvas.get_tk_widget().grid(row=1,column=1)
        
        ##NavigationToolbar2TkAgg uses pack internally, so grid cannot be used
        ##Frame used to get around this.
        #NavBarFrame=Tk.Frame(root)
        #NavBarFrame.grid(row=2,column=1,sticky=Tk.W)
        #plttoolbar = NavigationToolbar2TkAgg(pltcanvas, NavBarFrame)
        #plttoolbar.pack()

        self.net=network()
        
        L1=ind(0.80e-9)
        C1=cap(6.3e-12,shunt=1)    
        L2=ind(2.0e-9)
        C2=cap(1.6e-12,shunt=1)
        L3=ind(5e-9,shunt=1)

        self.net.element_array.append(C2)
        self.net.element_array.append(L2)
        self.net.element_array.append(C1)
        self.net.element_array.append(L1)
        
        self.net.element_array.append(L3)

        #TEST CASE -- matching 50.0 Ohms to ~5.0 Ohms at 2 GHz
        
        #SCHEMATIC FRAME
        self.im_size=150
        SchemFrame = Tk.Frame(root)
        SchemFrame.grid(row=2,column=0,columnspan=2,sticky=Tk.W)
        self.Schem = SchematicFrame(SchemFrame,self.net,self.draw_plot,slider) #Pass re-draw function to schematic ########
        #Schem.grid(row=0,column=0)

        #Draw
        #self.center_freq=2.0e9
        self.draw_plot()

    def test(self,event):
        print "OK"
        
    def edit_element(self):
        pass

    def delete_element(self):
        n=self.Schem.image_selection
        self.net.element_array.pop(n)

        self.Schem.draw_schematic()
        self.draw_plot()
        
    def add_shunt_c(self):
        C=cap(1.0e-12,shunt=1)
        self.net.element_array.append(C)
        self.Schem.draw_schematic()
        self.draw_plot()
        
    def add_series_c(self):
        C=cap(1.0e-12,shunt=0)
        self.net.element_array.append(C)
        self.Schem.draw_schematic()
        self.draw_plot()

    def add_shunt_l(self):
        L=ind(1.0e-9,shunt=1)
        self.net.element_array.append(L)
        self.Schem.draw_schematic()
        self.draw_plot()

    def add_series_l(self):
        L=ind(1.0e-9,shunt=0)
        self.net.element_array.append(L)
        self.Schem.draw_schematic()
        self.draw_plot()
        
    def draw_plot(self):

        nodeZ=self.net.compute_node_impedances(self.settings['centerfreq'])

        for i in range(len(self.curves)):
            self.curves.pop(0).remove()

        for i in range(len(self.dots)):
            self.dots.pop(0).remove()
            
        for i in range(len(nodeZ)-1):
            if self.net.element_array[i].orientation==0:
                curve_data=ConstImpedCurve(nodeZ[i],nodeZ[i+1],100)
                self.curves.extend(self.mainplot.plot(curve_data[0],curve_data[1],lw=3,color='b'))
            elif self.net.element_array[i].orientation==1:
                curve_data=ConstAdmitCurve(nodeZ[i],nodeZ[i+1],100)
                self.curves.extend(self.mainplot.plot(curve_data[0],curve_data[1],lw=3,color='b'))

        for i in range(len(nodeZ)):
            Gam=ZtoGamma(nodeZ[i])
            #print Gam
            self.dots.extend(self.mainplot.plot(Gam.real,Gam.imag,'or'))

        self.pltcanvas.draw()



if __name__=='__main__':

    print "OK"

    
    root=Tk.Tk()
    
    root.wm_title("Impedance Matching Tool")
    
    a=MainWindow(root)
    root.mainloop()
