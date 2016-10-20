"""
Author: Joel Rieger

October 29, 2016

Description: Classes and functions to perform basic network abstraction and plotting.
"""

from numpy import pi as pi

class network(object):
    """Class for one dimension network (i.e. a matching network)."""
    element_array=[]

    def __init__(self,*args):
        pass
    
    def compute_node_impedances(self,Zp2,freq):
        """Calculate impedances at each node walking back from the output impedance, Zp2"""
        pass

    def move_element(self,n_a,n_b):
        """
        Moves element to new index shifting other elements accordingly.
        Simplies drag-drop action of components
        """
        self.element_array.insert(n_b,self.element_array.pop(n_a))

    
class element(object):
    """Class for a single impedance/admittance element (i.e. capacitor, indcutor, etc.)."""
    name=''
    icon=''
    orientation=0
    val={'C':1e-12}

    Zfunc=lambda self,x: 1e-14 #function to define series impedance
    Yfunc=lambda self,x: 1e14 #function to define admittance
    
    def __init__(self,*args):
        pass

    def Z(self,freq):
        return self.Zfunc(freq)

    def Y(self,freq):
        return self.Yfunc(freq)


class cap(element):
    """Modification of element class to model an ideal capacitor"""
    
    Zfunc=lambda self,freq: 1.0j/(2*pi*freq*self.val['C']) #function to define series impedance
    Yfunc=lambda self,freq: (2*pi*freq*self.val['C']) #function to define admittance


class ind(element):
    """Modification of element class to model an ideal capacitor"""

    Zfunc=lambda self,freq: 2*pi*freq*self.val['L']*1j #function to define series impedance
    Yfunc=lambda self,freq: 1.0j/(2*pi*freq*self.val['L']) #function to define admittance


class indQ(element):
    """Modification of element class to model an capacitor with a fixed Q"""
    
    Zfunc=lambda self,freq: 2*pi*freq*self.val['L']/self.val['Q']+2*pi*freq*self.val['L']*1j #function to define series impedance
    Yfunc=lambda self,freq: 1.0j/self.Zfunc(self,x) #function to define admittance


class capQ(element):
    """Modification of element class to model an capacitor with a fixed L"""
 
    Zfunc=lambda self,freq: 1e-12 #function to define series impedance
    Yfunc=lambda self,freq: 1.0/self.Zfunc(self,x) #function to define admittance


if __name__=='__main__':

    net=network()
    
    L1=ind()
    L1.val['L']=1.9e-9
    print L1.Z(2.0e9)
    
    L2=indQ()
    L2.val={'L':1.9e-9,'Q':30.0}
    print L2.Z(2.0e9)
    
