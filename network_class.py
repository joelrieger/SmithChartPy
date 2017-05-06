"""
Author: Joel Rieger

October 29, 2016

Description: Classes and functions to perform basic network abstraction and plotting
"""

from numpy import pi as pi

class network(object):
    """Class for one dimension network (i.e. a matching network)."""

    element_array=[]

    def __init__(self):
        
        self.ZP2=lambda freq: 50.0 #Network termination on output
        self.ZP1=lambda freq: 50.0 #Network termination on output
    
    def compute_node_impedances(self,freq):
        """Calculate impedances at each node walking back from the output impedance, Zp2"""

        Zarr=[self.ZP2(freq)]
        for elem in self.element_array:
            if elem.orientation==0: #series
                Zarr.append(Zarr[-1]+elem.Z(freq))
            elif elem.orientation==1: #shunt
                Zarr.append(1.0/(1.0/Zarr[-1]+elem.Y(freq)))

        #Zarr.reverse()
        return Zarr

    def print_net(self):
        for elem in self.element_array:
            print elem.name, elem.val

    def move_element(self,n_a,n_b):
        """
        Moves element to new index shifting other elements accordingly.
        Simplies drag-drop action of components
        """
        self.element_array.insert(n_b,self.element_array.pop(n_a))

    
class element(object):
    """Class for a single impedance/admittance element (i.e. capacitor, indcutor, etc.)."""
    
    def __init__(self,*args,**kargs):
        self.name=''
        self.icon=''
        self.orientation=0
        
        if kargs.has_key('shunt'):
            self.orientation=kargs['shunt'] # 0: Series, 1:Shunt
        self.val={}

        self.Zfunc=lambda self,x: 1e-14 #function to define series impedance
        self.Yfunc=lambda self,x: 1e14 #function to define admittance

    def __setval__(self,val):
        self.val=val
        
    def Z(self,freq):
        return self.Zfunc(self,freq)

    def Y(self,freq):
        return self.Yfunc(self,freq)


class cap(element):
    """Modification of element class to model an ideal capacitor"""

    def __init__(self,*args,**kargs):
        element.__init__(self,*args,**kargs)
        self.name='cap'

        if 'min' in kargs:
            self.val['min']=kargs['min']
        else:
            self.val['min']=1e-12

        if 'max' in kargs:
            self.val['max']=kargs['max']
        else:
            self.val['max']=12.1e-12

        if 'step' in kargs:
            self.val['step']=kargs['step']
        else:
            self.val['step']=0.1e-12

        self.val['unit']='pF' #Unit not used to scale value variable
                
        if len(args)!=1:
            print "ERROR: cap(element) requires 1 argument"
        else:
            self.val['C']=args[0]

        #self.Zfunc=lambda self,freq: 1j/(2*pi*freq*self.val['C']) #function to define series impedance
        self.Yfunc=lambda self,freq: (1j*2*pi*freq*self.val['C']) #function to define admittance
        self.Zfunc=lambda self,freq: 1.0/self.Yfunc(self,freq)


class ind(element):
    """Modification of element class to model an ideal capacitor"""

    def __init__(self,*args,**kargs):
        element.__init__(self,*args,**kargs)
        self.name='ind'

        if 'min' in kargs:
            self.val['min']=kargs['min']
        else:
            self.val['min']=1e-9

        if 'max' in kargs:
            self.val['max']=kargs['max']
        else:
            self.val['max']=12.1e-9

        if 'step' in kargs:
            self.val['step']=kargs['step']
        else:
            self.val['step']=0.1e-9

        self.val['unit']='nH' #Unit not used to scale value variable
        
        if len(args)!=1:
            print "ERROR: ind(element) requires 1 argument"
        else:
            self.val['L']=args[0]

        self.Zfunc=lambda self,freq: 1j*2*pi*freq*self.val['L'] #function to define series impedance
        self.Yfunc=lambda self,freq: 1.0/self.Zfunc(self,freq)


class indQ(element):
    """Modification of element class to model an capacitor with a fixed Q"""

    def __init__(self,*args,**kargs):
        element.__init__(self)
        self.name='indQ'

        if len(args)!=2:
            print "ERROR: indQ(element) requires 2 arguments"
        else:
            self.val['L']=args[0]
            self.val['Q']=args[1]

        #function to define series impedance
        self.Zfunc=lambda self,freq: 2*pi*freq*self.val['L']/self.val['Q']+1j*2*pi*freq*self.val['L']
        #function to define admittance
        self.Yfunc=lambda self,freq: 1.0j/self.Zfunc(self,x) 


class capQ(element):
    """Modification of element class to model an capacitor with a fixed L"""

    def __init__(self,*args,**kargs):
        element.__init__(self)
        self.name='capQ'
        
        if len(args)!=2:
            print "ERROR: capQ(element) requires 2 arguments"
        else:
            self.val['C']=args[0]
            self.val['Q']=args[1]

        #function to define series impedance
        self.Zfunc=lambda self,freq: (1.0/(2*pi*freq*self.val['C']))/self.val['Q']+1.0j/(2*pi*freq*self.val['C'])
        #function to define admittance
        self.Yfunc=lambda self,freq: 1.0/self.Zfunc(self,x)


if __name__=='__main__':

    net=network()

    #TEST CASE -- matching 50.0 Ohms to ~5.0 Ohms at 2 GHz
    
    L1=ind(0.75e-9)
    C1=cap(6.3e-12,shunt=1)    
    L2=ind(2.0e-9)
    C2=cap(1.6e-12,shunt=1)

    net.element_array.append(C2)
    net.element_array.append(L2)
    net.element_array.append(C1)
    net.element_array.append(L1)

    print net.compute_node_impedances(2.0e9)
    
    
