"""
Author: Joel Rieger

October 29, 2016

Description: Schematic frame for Smith Chart matching tool
"""

import Tkinter as Tk

class manual_event(object):
    def __init__(x,y):
        self.x=x
        self.y=y

def nearest_ind(item_list,val):
    """Return index of nearest val in item_list"""
    error_arr=[abs(tmp-val) for tmp in item_list]
    error_min=min(error_arr)

    return error_arr.index(error_min)


class SchematicFrame(Tk.Frame):

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
        self.item_positions=[]
        
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


    def im_reorder(self,event,old,new):
        self.canvas1.move(self.item_arr[new], (old-new)*self.im_x_size, 0)

        self.item_arr[old], self.item_arr[new] = self.item_arr[new], self.item_arr[old]
        self.net.element_array[old], self.net.element_array[new] = self.net.element_array[new], self.net.element_array[old]
        
        self.image_selection=new
        self.draw_plot()

    def down_click(self,event):
        self.image_selection=int(event.x/self.im_x_size)
        #print "down_click, ", self.image_selection

        #TODO
        #1) Up-Date Slider, Min, Max, Cur, Unit, Step, etc.
        #2)
        i=self.image_selection

        #Make this more elegant...
        if self.net.element_array[i].name=='cap':
            valname='C'
        elif self.net.element_array[i].name=='ind':
            valname='L'

        unit_map={'u':1e-6,'n':1e-9,'p':1e-12,'f':1e-15}
        scale_letter=self.net.element_array[i].val['unit'][0]
        scale=unit_map[scale_letter]
        
        self.slider.update_slider(values={'min':self.net.element_array[i].val['min']/scale,
                                          'cur':self.net.element_array[i].val[valname]/scale,
                                          'max':self.net.element_array[i].val['max']/scale,
                                          'step':0.1,
                                          'unit':self.net.element_array[i].val['unit']})

        self.slider.update_slider_position()
        
        self.canvas1.delete(self.box)
        self.draw_box(self.canvas1,self.image_selection)#event.x/self.im_x_size)
        self.draw_plot()


    def follow_mouse(self,event):
        new_x, new_y = event.x, event.y
        old_x, old_y = self.canvas1.coords(self.item_arr[self.image_selection])

        num_items=len(self.item_arr)        
        position_num=nearest_ind(self.item_positions,new_x)

        self.canvas1.move(self.item_arr[self.image_selection], new_x-old_x, new_y-old_y)
        self.drag=True

        if int(new_x/self.im_x_size) != int(old_x/self.im_x_size):
            self.im_reorder(event,self.image_selection,position_num)


    def draw_box(self,canvas,n):
        w=2        
        self.box = canvas.create_rectangle((n)*self.im_x_size+w, 2*w ,(n+1)*self.im_x_size-w/2, self.im_y_size-w/2,
                                           width=w,dash='.')
        canvas.tag_raise(self.box)

    def new_position(self,x):
        #valid
        return max(min(int(new_x/self.im_x_size)),0)
        
    def reposition_image(self,event):
        new_x, new_y = event.x, event.y

        position_num=nearest_ind(self.item_positions,new_x)
        nearest_valid_x=self.item_positions[position_num]
        print new_x, position_num, nearest_valid_x
        if (self.drag==True&(position_num<=len(self.item_arr))):
            self.canvas1.move(self.item_arr[position_num],
                              nearest_valid_x-new_x,
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
            self.item_positions=[]

        x = (self.im_x_size)/2.0
        y = (self.im_y_size)/2.0
        for n,elem in enumerate(self.Match):
            self.item_arr.append(self.canvas1.create_image(x+self.im_x_size*n, y, image=elem['type']))
        self.item_positions=[n*self.im_x_size+0.5*self.im_x_size for n in range(len(self.item_arr))]

    def update_icons(self):
        pass 

if __name__=='__main__':

    from network_class import *
    
    net=network()
    L1=ind(0.80e-9)
    C1=cap(6.3e-12,shunt=1)    
    L2=ind(2.0e-9)
    C2=cap(1.6e-12,shunt=1)

    net.element_array.append(C2)
    net.element_array.append(L2)
    net.element_array.append(C1)
    net.element_array.append(L1)
    
    class slider(object):
        def __init__(self):
            pass
        def update_slider(self,values={}):
            print values
        def draw_plot(self):
            print "draw_plot() called"
        def update_slider_position(self):
            print "update_slider_position() called"


    class MainWindow(Tk.Frame):
        def __init__(self,parent):
            Tk.Frame.__init__(self,parent)
            
    net=network()
    slide=slider()
    def draw_plot():
            print "draw_plot() called"

    root = Tk.Tk()
    
    Frame=Tk.Canvas(root)
    Frame.grid(row=0,column=0)
    Slider=SchematicFrame(Frame,net,draw_plot,slide)
    Slider.grid(row=0,column=0)

    root.mainloop()
