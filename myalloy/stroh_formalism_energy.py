
# schematic:
# https://ars.els-cdn.com/content/image/1-s2.0-S1359645416305808-fx2_lrg.jpg
  


import scipy as sc
import numpy as np
from scipy import integrate


# integrate each return of f 
def myint(f, x1, x2):
    nf = len(f(0))   # number of returns of f 

    F = np.array([])
    for i in np.arange(nf):  
        def g(x):
            return f(x)[i]

        temp = integrate.quad(g, x1, x2 )
        F = np.append(F, temp[0])

    return F






def calc_Ec(stroh_u1s1, stroh_u2s2, r0, R0, X1, Y1, X2, Y2):

    # energy contributions
    def fec(x, y, n0):
        u1 = stroh_u1s1(x=x, y=y)[0] 
        s1 = stroh_u1s1(x=x, y=y)[1] 
        u2 = stroh_u2s2(x=x, y=y)[0] 
        s2 = stroh_u2s2(x=x, y=y)[1] 

        ec1 = ((s1 @ n0).T @ u1 ) / 2.0
        ec2 = ((s1 @ n0).T @ u2 ) / 2.0
        ec3 = ((s2 @ n0).T @ u1 ) / 2.0
        ec4 = ((s2 @ n0).T @ u2 ) / 2.0
        
        return ec1, ec2, ec3, ec4




    Ec = np.zeros([4,5])

# S(C1) ===============================
    def fec_C1(alpha):
        x = X1+r0*np.cos(alpha)
        y = Y1+r0*np.sin(alpha)
        n0 = np.array([[-np.cos(alpha)], [-np.sin(alpha)], [0.]])
        return fec(x, y, n0)  
   
    Ec[:,0] = myint(fec_C1, 0, 2*np.pi)*(r0)
   

 
# S(R) ===============================
    def fec_R(alpha):
        x = R0*np.cos(alpha)
        y = R0*np.sin(alpha)
        n0 = np.array([[-np.cos(alpha)], [-np.sin(alpha)], [0.]])
        return fec(x, y, n0)
    
    Ec[:,1]  = myint(fec_R, 0, 2.0*np.pi)*(R0) 



# S(C2) ===============================
    def fec_C2(alpha):
        x = X2+r0*np.cos(alpha)
        y = Y2+r0*np.sin(alpha)
        n0 = np.array([[-np.cos(alpha)],[-np.sin(alpha)],[0.]])
        return fec(x, y, n0)
    
    Ec[:,2]  = myint(fec_C2, 0, 2.0*np.pi)*(r0) 



# S(1) ===============================
    def fec_1(x):
        n1 = [[0.],[1.],[0.]]
        return fec(x, Y1+1e-100, n1) + fec(x, Y1-1e-100, n1)
    
    Ec[:,3]  = myint(fec_1, -sc.sqrt(R0**2-Y1**2), X1-r0 )



# S(2) ===============================
    def fec_2(x):
        n1 = [[0.],[1.],[0.]]
        return fec(x, Y2+1e-100, n1) + fec(x, Y2-1e-100, n1)
    
    Ec[:,4]  = myint(fec_2, X2+r0, sc.sqrt(R0**2-Y2**2) )


    return Ec 




