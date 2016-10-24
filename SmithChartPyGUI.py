from Tkinter import *
root = Tk()
im_size=150

box=None
drag=False
image_selection=0

def down_click(event):
    global image_selection

    image_selection=int(event.x/im_size)
    
    canvas1.delete(box)
    draw_box(canvas1,event.x/im_size)    


def draw_box(canvas,n):
    global box
    w=3
    box = canvas.create_rectangle((n)*im_size+w, w ,(n+1)*im_size-w/2, 150-w,
                                  width=w,dash='.')
    canvas1.tag_raise(box)


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


capse = "icons/C.gif"
capsh = "icons/Csh.gif"
CapIconSe = PhotoImage(file=capse)
CapIconSh = PhotoImage(file=capsh)

indse = "icons/Lse.gif"
indsh = "icons/Lsh.gif"
IndIconSe = PhotoImage(file=indse)
IndIconSh = PhotoImage(file=indsh)


Match=[{'type':CapIconSh},{'type':IndIconSe},{'type':CapIconSe},{'type':IndIconSh}]

canvas1 = Canvas(width=1000, height=150,scrollregion=(0,0,1000,1000))
canvas1.pack(expand=1, fill=BOTH)
canvas2 = Canvas(width=1000, height=150,scrollregion=(0,0,1000,1000))
canvas2.pack(expand=1, fill=BOTH)

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

root.mainloop()
