from plot_funcs import *
from canvas_slider import *
from network_class import *

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as Tk
             
class SchematicFrame(Tk.Frame):
    def im_reorder(self,event,old,new):
        self.canvas1.move(self.item_arr[new], (old-new)*self.im_x_size, 0)

        self.item_arr[old], self.item_arr[new] = self.item_arr[new], self.item_arr[old]
        self.net.element_array[old], self.net.element_array[new] = self.net.element_array[new], self.net.element_array[old]
        
        self.image_selection=new
        self.draw_plot()

    def down_click(self,event):
        self.image_selection=int(event.x/self.im_x_size)
        print "down_click, ", self.image_selection

        #TODO
        #1) Up-Date Slider, Min, Max, Cur, Unit, Step, etc.
        #2) 

        self.canvas1.delete(self.box)
        self.draw_box(self.canvas1,self.image_selection)#event.x/self.im_x_size)




    def follow_mouse(self,event):
        new_x, new_y = event.x, event.y
        old_x, old_y = self.canvas1.coords(self.item_arr[self.image_selection])

        num_items=len(self.item_arr)        
        position_num=int(new_x/self.im_x_size)

        #Move image to follow mouse
        if ((new_x>0)&(new_x<self.im_x_size*num_items)):
            self.canvas1.move(self.item_arr[self.image_selection], new_x-old_x, new_y-old_y)
            self.drag=True
        else:
            pass
            #reposition image -- but now this will fail

        #Dynamically move icons while dragging
        if ((position_num<num_items)&(new_x>0.0)&(old_x<num_items*self.im_x_size)): #Only if move if within region of circuit
            if int(new_x/self.im_x_size) != int(old_x/self.im_x_size):
                self.im_reorder(event,int(old_x/self.im_x_size),int(new_x/self.im_x_size))
                item_n=int(new_x/self.im_x_size)

    def draw_box(self,canvas,n):
        w=2        
        self.box = canvas.create_rectangle((n)*self.im_x_size+w, 2*w ,(n+1)*self.im_x_size-w/2, self.im_y_size-w/2,
                                           width=w,dash='.')
        canvas.tag_raise(self.box)

    def reposition_image(self,event):
        new_x, new_y = event.x, event.y
        
        position_num=int(new_x/self.im_x_size)
        if (self.drag==True&(position_num<=len(self.item_arr))&(new_x>0.0)):
            self.canvas1.move(self.item_arr[int(new_x/self.im_x_size)],
                              -new_x%self.im_x_size-0.5*self.im_x_size,
                              -new_y+0.5*self.im_y_size)
        self.drag=False

    def draw_schematic(self):
        capse = "icons/C.gif"
        capsh = "icons/Csh.gif"
        self.CapIconSe = Tk.PhotoImage(file=capse)
        self.CapIconSh = Tk.PhotoImage(file=capsh)

        indse = "icons/Lse.gif"
        indsh = "icons/Lsh.gif"
        self.IndIconSe = Tk.PhotoImage(file=indse)
        self.IndIconSh = Tk.PhotoImage(file=indsh)

        self.Match=[]
        for elem in self.net.element_array:
            if elem.name == 'cap':
                if elem.orientation==1:
                    self.Match.append({'type':self.CapIconSh})
                elif elem.orientation==0:
                    self.Match.append({'type':self.CapIconSe})
            elif elem.name =='ind':
                if elem.orientation==1:
                    self.Match.append({'type':self.IndIconSh})
                elif elem.orientation==0:
                    self.Match.append({'type':self.IndIconSe})

        for elem in self.item_arr:
            self.canvas1.delete(elem)
            self.item_arr=[]

        x = (self.im_x_size)/2.0
        y = (self.im_y_size)/2.0
        for n,elem in enumerate(self.Match):
            self.item_arr.append(self.canvas1.create_image(x+self.im_x_size*n, y, image=elem['type']))

    def update_icons(self):
        pass 

    def __init__(self,parent,network,draw_plot,slider):
        Tk.Frame.__init__(self,parent)
        self.parent=parent
        
        self.net=network
        self.draw_plot=draw_plot
        self.slider=slider
        self.Match=[]
        
        self.im_y_size=150
        self.im_x_size=150

        self.box=None
        self.drag=False
        self.image_selection=0

        self.item_arr=[] #contains canvas item index

        self.canvas1 = Tk.Canvas(parent,width=850, height=150)#,scrollregion=(0,0,1000,150)
        self.canvas1.grid(row=3,column=0,columnspan=3,sticky=Tk.W)
        self.canvas1.configure(background='white')

        #print self.item_arr
        self.update_icons()
        self.draw_schematic()
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

        a=Tk.Canvas(Palette,width=50)
        a.grid(row=2,column=0,columnspan=2,sticky=Tk.N+Tk.W)
        slider=SliderFrame(a)
        #b.grid(row=2,column=0)
        
        entry1=Tk.Entry(Palette,width=5)
        entry1.grid(row=2,column=0,sticky=Tk.S)

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
