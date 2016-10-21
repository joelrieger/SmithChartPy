"""
Author: Joel Rieger

October 29, 2016

Description: Functions to perform basic network calculations.
"""

#The next three functions will be repeated,
#they should be moved into their own file.
def SSS(start,stop,step):
    return [start+step*i for i in range(int((stop-start)/step))]


def ZtoGamma(Z,Z0=50.0):
    return (Z-Z0)/(Z+Z0)


def GammatoZ(Gamma,Z0=50.0):
    return -Z0*(Gamma+1)/(Gamma-1)


def PlotSmith(plt):
    plt.axes().set_aspect('equal')
    for R in [0.0,0.3,1.0,3.0]:
        Y=[]
        for x in SSS(-50,50,0.05):
            Z=R+x*1j
            Y.append(ZtoGamma(Z,Z0=1.0))

        x=[tmp.real for tmp in Y]
        y=[tmp.imag for tmp in Y]
        plt.plot(x,y,'gray')

    for R in [-2.0,-1.0,-0.5,-0.25,0.0,0.25,0.5,1.0,2.0]:
        Y=[]
        for x in SSS(0,80.0,0.1):
            Z=x+R*1j
            Y.append(ZtoGamma(Z,Z0=1.0))

        x=[tmp.real for tmp in Y]
        y=[tmp.imag for tmp in Y]
        plt.plot(x,y,'gray')


def ConstImpedCurve(start,stop,pnts):
    step=(stop.imag-start.imag)/pnts
    Zarray=[start.real+imag*1j for imag in SSS(start.imag,stop.imag,step)]
    GamArray=[ZtoGamma(tmp) for tmp in Zarray]
    real=[tmp.real for tmp in GamArray]
    imag=[tmp.imag for tmp in GamArray]
    return [real,imag]


def ConstAdmitCurve(start,stop,pnts):
    Ystart=1.0/start
    Ystop=1.0/stop
    step=(Ystop.imag-Ystart.imag)/pnts
    Yarray=[Ystart.real+imag*1j for imag in SSS(Ystart.imag,Ystop.imag,step)]
    Zarray=[1/tmp for tmp in Yarray]
    GamArray=[ZtoGamma(tmp) for tmp in Zarray]
    real=[tmp.real for tmp in GamArray]
    imag=[tmp.imag for tmp in GamArray]
    return [real,imag]

