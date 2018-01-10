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

        self.mainplot.set_xticks([])
        self.mainplot.set_yticks([])

        self.vsfreq_curves=[]
        self.curves=[]
        self.dots=[]

        PlotSmith(self.mainplot)

        parent.bind('<Up>',self.test)

        self.settings={'centerfreq':2.0e9,
                       'lowerfreq':1.5e9,
                       'upperfreq':2.5e9,
                       'stepsize':0.1e9,
                       'SmithImpedance':50.0,
                       'InputImpedance':50,
                       'LoadImpedance':50}

        #Menu
        menu=Tk.Menu(self.master)
        self.master.config(menu=menu)
        File=Tk.Menu(menu)
        menu.add_cascade(label="File",menu=File)
        menu.add_cascade(label="Plotting",menu=File)
        menu.add_cascade(label="Settings",menu=File)
        menu.add_cascade(label="Help",menu=File)
        
        #SLIDER FRAME
        Slider_Frame=Tk.Frame(root)
        Slider_Frame.grid(row=0,column=0,sticky=Tk.S)
        
        slider_canvas=Tk.Canvas(Slider_Frame)
        slider=SliderFrame(slider_canvas,self.callback)

        #COMPONENT CONTROL BUTTON FRAMES (i.e. delete, edit)
        CmpCntrl = Tk.Frame()
        CmpCntrl.grid(row=1,column=0,padx=5,pady=10,sticky=Tk.S)
        button_del=Tk.Button(CmpCntrl,width=10,text="Delete",command=self.delete_element)
        button_del.grid(row=2,column=0,padx=5,pady=1)
        button_edit=Tk.Button(CmpCntrl,width=10,text="Edit",command=self.edit_element)
        button_edit.grid(row=2,column=1,padx=5,pady=10)

        ser_c_icon=Tk.PhotoImage(file="./icons/button_Cse.gif")
        #button_ser_c=Tk.Button(CmpCntrl,image=ser_c_icon,command=self.add_series_c)#command=self.add_series_c,image=series_c_photo
        button_ser_c=Tk.Button(CmpCntrl,width=10,text="Series C",command=self.add_series_c)#command=self.add_series_c,image=series_c_photo
        button_ser_c.grid(row=0,column=0)
        button2=Tk.Button(CmpCntrl,width=10,text="Shunt C", command=self.add_shunt_c)
        button2.grid(row=0,column=1)
        button3=Tk.Button(CmpCntrl,width=10,text="Series L", command=self.add_series_l)
        button3.grid(row=1,column=0)
        button4=Tk.Button(CmpCntrl,width=10,text="Shunt L", command=self.add_shunt_l)
        button4.grid(row=1,column=1)
        CmpCntrl.config(background="white")

        #PLOT FRAME
        PlotFrame = Tk.Frame()
        PlotFrame.grid(row=1,column=1)
        self.pltcanvas = FigureCanvasTkAgg(fig, master=PlotFrame)
        self.pltcanvas.get_tk_widget().grid(row=1,column=1)

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
        self.im_size=100
        SchemFrame = Tk.Frame(root)
        SchemFrame.grid(row=2,column=0,columnspan=6,sticky=Tk.N+Tk.S+Tk.W+Tk.E)
        self.Schem = SchematicFrame(SchemFrame,self.net,self.draw_plot,slider) #Pass re-draw function to schematic ########
        #Schem.grid(row=0,column=0)

        #Draw
        #self.center_freq=2.0e9
        self.draw_plot()

    def callback(self,**kargs):
        """Not really implemented -- in hindsight, this would have been a better way
            of managing interface"""
        unit_map={'u':1e-6,'n':1e-9,'p':1e-12,'f':1e-15}

        if 'image_selection' in kargs:
            i=self.Schem.image_selection-1
            self.draw_plot(selection=i)
        if 'values' in kargs:
            if 'cur' in kargs['values']:
                i=self.Schem.image_selection-1
                scale=unit_map[self.net.element_array[i].val['unit'][0]]
                self.net.element_array[i].set_val(kargs['values']['cur']*scale)
                #print i,kargs['values']['cur']
                #self.Schem.draw_schematic()
                self.draw_plot(selection=i)


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
        
    def draw_plot(self,selection=None):

        nodeZ=self.net.compute_node_impedances(self.settings['centerfreq'])

        for i in range(len(self.curves)):
            self.curves.pop(0).remove()

        for i in range(len(self.dots)):
            self.dots.pop(0).remove()

        for i in range(len(self.vsfreq_curves)):
            self.vsfreq_curves.pop(0).remove()
    
        for i in range(len(nodeZ)-1):
            if self.net.element_array[i].orientation==0:
                curve_data=ConstImpedCurve(nodeZ[i],nodeZ[i+1],100)
                self.curves.extend(self.mainplot.plot(curve_data[0],curve_data[1],lw=3,color='b'))
            elif self.net.element_array[i].orientation==1:
                curve_data=ConstAdmitCurve(nodeZ[i],nodeZ[i+1],100)
                self.curves.extend(self.mainplot.plot(curve_data[0],curve_data[1],lw=3,color='b'))

        vsfreq_curve=[]
        for freq in SSS(self.settings['lowerfreq'],self.settings['upperfreq'],self.settings['stepsize']):
            gam=ZtoGamma(self.net.compute_node_impedances(freq)[-1])
            vsfreq_curve.append([gam.real,gam.imag])

        #print vsfreq_curve
        vsfreq_curve=zip(*vsfreq_curve)
        self.vsfreq_curves.extend(self.mainplot.plot(vsfreq_curve[0],vsfreq_curve[1],lw=2,color='k',linestyle='--'))

        
        if selection!=None:
            self.curves[selection].set_color('g')

        for i in range(len(nodeZ)):
            Gam=ZtoGamma(nodeZ[i])
            #print Gam
            self.dots.extend(self.mainplot.plot(Gam.real,Gam.imag,'or'))


        self.pltcanvas.draw()


if __name__=='__main__':

    print "OK"

    
    root=Tk.Tk()
    root.configure(background='white')
    root.wm_title("Impedance Matching Tool")
    
    a=MainWindow(root)
    root.mainloop()
