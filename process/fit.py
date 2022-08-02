#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:03:30 2022

@author: jsewell
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
from iminuit.cost import LeastSquares
from iminuit import Minuit, __version__
import tools

file_path = input("Enter file path: ")

ds = pd.read_csv(
    f"{file_path}",
)

size_data = input('Enter integer index of column with size data: ')
size_data = int(size_data)

def getsize(ds):
    vals = ds.iloc[:,size_data]
    sizes = []
    for x in vals:
       if x not in sizes:
           sizes.append(x)
    return sizes

def main():
    plot_dir  = "process_plots"
    tools.makeDir(plot_dir)
    
    sl = getsize(ds)
    sl = np.array(sl,dtype = 'd')
    
    index_num = input("Enter integer index of column with data to be plotted: ")
    index_num = int(index_num)
    
    title_name = input("Enter title of plot: ")
    
    fit_style = input("Fit style? (lin/exp/quad): ")
    
    output_name = "{0}/{1}.pdf".format(plot_dir, title_name)
    
    dl = ds.groupby(ds.iloc[:,size_data].name)[ds.iloc[:,index_num].name].apply(list)# select column to be plotted by integer index
    
    numlen = len(sl)
    
    means = [np.array(dl[sl[x]]).mean() for x in range(numlen)]

    errlist = [(np.std(dl[sl[x]]))/np.sqrt(len(dl[sl[x]])) for x in range(numlen)] 
    TAP0err = np.array(errlist,dtype = 'd')
#------------------------------------------------------------------------------------
### end of options ###
#------------------------------------------------------------------------------------  
    if (fit_style == 'quad'):
        print('iminuit version', __version__)
    
        def line(x, a, b, c): # model for fit line
            return a + b*x + c * x**2
         
        least_squares = LeastSquares(sl,means,TAP0err,line)  #(data_x,data_y,yerr,form)
    
        m = Minuit(least_squares,0,0,0)  #(0,0,0 == initial values)
        m.migrad()  # finds minimum of least_squares function
        m.hesse()  # computes errors
        
        ### total differential of fit model

        a, b, c, x= sym.symbols('a b c x')

        def f(x):
            return a + b * x + c * x**2

        f = f(x)

        dfda = sym.diff(f,a)
        dfdb = sym.diff(f,b)
        dfdc = sym.diff(f,c)

        def z(i):
            
          r = sym.sqrt((dfda**2 * (m.errors[0])**2 + dfdb**2 * (m.errors[1])**2 + dfdc**2 * (m.errors[2])**2))
          
          return r.subs(x,i)

        vals = np.array([])
        for i in np.linspace(0.35,2.3):
            vals = np.append(vals,z(i))
            vals = vals.astype(float)
            
        ### plotting all the lines

        x = np.linspace(0.35,2.3)
        err1 = vals + line(np.linspace(0.35,2.3), *m.values)
        err2 = line(np.linspace(0.35,2.3), *m.values) - vals


        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        ax1.fill_between(x,err1,err2,alpha = 0.4)
        #delta f lines
        ax1.plot(np.linspace(0.35,2.3,len(vals)),err1,color = 'royalblue',ls = '--',label = '$\\delta$ f')#plots fit error
        ax1.plot(np.linspace(0.35,2.3,len(vals)),err2,color = 'royalblue',ls = '--')#plots fit error
        #fit line and errorbar points
        ax1.errorbar(sl,means,yerr = TAP0err, fmt = "s",color = "royalblue", ecolor = "k",elinewidth = 3, capsize = 5) #plots errorbars and points
        ax1.plot(np.linspace(0.35,2.3), line(np.linspace(0.35,2.3), *m.values),'-', label= 'f [a + bx + cx\N{SUPERSCRIPT TWO}]',color = 'darkorange')  #plots line
        
        ### legend and console info
   
        r = m.fval / (len(means) - len(m.parameters))
        
        fit_info = [ 
        f"$\\chi^2$ / $n_\\mathrm{{dof}}$ = {r:.2f}", 
        ]
    
        for p, v, e in zip(m.parameters, m.values, m.errors):
            fit_info.append(f"{p} = ${v:.0f} \\pm {e:.0f}$")
    
        plt.legend(title="\n".join(fit_info));
        print(' ') 
        print(' Fitting parameters') 
        for p in m.parameters: 
            print("{} = {} +- {}".format(p,m.values[p], m.errors[p]))
    
        print(' ') 
        print('chi squared:', m.fval) 
        print('number of degrees of freedom', (len(means)-len(m.parameters))) 
        print('reduced chi squared:', m.fval / (len(means) - len(m.parameters)) )
        plt.title(f"{title_name}")
        plt.ylim(75,400)
        plt.xlim(0,2.3)
        plt.ylabel('Average TAP0 for BERT = 10E-11')
        plt.xlabel('Length (m)')
        plt.savefig(output_name)
#------------------------------------------------------------------------------------     
    elif (fit_style == 'lin'):
        print('iminuit version', __version__)
    
        def line(x, a, b): # model for fit line
            return a + b * x
         
        least_squares = LeastSquares(sl,means,TAP0err,line)  #(data_x,data_y,yerr,form)
    
        m = Minuit(least_squares,0,0)  #(0,0,0 == initial values)
        m.migrad()  # finds minimum of least_squares function
        m.hesse()  # computes errors
        
        ### total differential of fit model

        a, b, x= sym.symbols('a b x')

        def f(x):
            return a + b * x 

        f = f(x)

        dfda = sym.diff(f,a)
        dfdb = sym.diff(f,b)

        def z(i):
            
          r = sym.sqrt((dfda**2 * (m.errors[0])**2 + dfdb**2 * (m.errors[1])**2))
          
          return r.subs(x,i)

        vals = np.array([])
        for i in np.linspace(0.35,2.3):
            vals = np.append(vals,z(i))
            vals = vals.astype(float)
            
        ### plotting all the lines

        x = np.linspace(0.35,2.3)
        F_errP = vals + line(np.linspace(0.35,2.3), *m.values)
        F_errN = line(np.linspace(0.35,2.3), *m.values) - vals

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        ax1.fill_between(x,err1,err2,alpha = 0.4)
        #delta f lines
        ax1.plot(np.linspace(0.35,2.3,len(vals)),F_errP,color = 'royalblue',ls = '--',label = '$\\delta$ f')#plots fit error
        ax1.plot(np.linspace(0.35,2.3,len(vals)),F_errN,color = 'royalblue',ls = '--')#plots fit error
        #fit line and errorbar points
        ax1.errorbar(sl,means,yerr = TAP0err, fmt = "s",color = "royalblue", ecolor = "k",elinewidth = 3, capsize = 5) #plots errorbars and points
        ax1.plot(np.linspace(0.35,2.3), line(np.linspace(0.35,2.3), *m.values),'-', label= 'a + bx',color = 'darkorange')  #plots line
        
        ### legend and console info
    
        r = m.fval / (len(means) - len(m.parameters))
    
        fit_info = [ 
        f"$\\chi^2$ / $n_\\mathrm{{dof}}$ = {r:.2f}", 
        ]
    
        for p, v, e in zip(m.parameters, m.values, m.errors):
            fit_info.append(f"{p} = ${v:.0f} \\pm {e:.0f}$")
    
    
        plt.legend(title="\n".join(fit_info));
        print(' ') 
        print(' Fitting parameters') 
        for p in m.parameters: 
            print("{} = {} +- {}".format(p,m.values[p], m.errors[p]))
    
        print('') 
        print('chi squared:', m.fval) 
        print('number of degrees of freedom', (len(means)-len(m.parameters))) 
        print('reduced chi squared:', f"{r:.2f}" )
        plt.title(f"{title_name}")
        plt.ylim(75,400)
        plt.xlim(0,2.3)
        plt.ylabel('Average TAP0 for BERT = 10E-11')
        plt.xlabel('Length (m)')
        plt.savefig(output_name)
#------------------------------------------------------------------------------------
    elif (fit_style == 'exp'):
        
        print('iminuit version', __version__)
    
        def line(x, a, b, c): # model for fit line
            return a + b * np.exp(x*c)
         
        least_squares = LeastSquares(sl,means,TAP0err,line)  #(data_x,data_y,yerr,form)
    
        m = Minuit(least_squares,0,0,0)  #(0,0,0 == initial values)
        m.migrad()  # finds minimum of least_squares function
        m.hesse()  # computes errors
    
        ### total differential of fit model

        a, b, c, x= sym.symbols('a b c x')
 
        def f(x):
            return a + b * sym.exp(x * c)
 
        f = f(x)
 
        dfda = sym.diff(f,a)
        dfdb = sym.diff(f,b)
        dfdc = sym.diff(f,c)
 
        def z(i):
            
          r = sym.sqrt((dfda**2 * (m.errors[0])**2 + dfdb**2 * (m.errors[1])**2 + dfdc**2 * (m.errors[2])**2))
          r = r.subs([(b,m.values[1]),(c,m.values[2])])# subs in best values of b & c
          return r.evalf(subs={x: i})
 
        vals = np.array([])
        for i in np.linspace(0.35,2.3):
            vals = np.append(vals,z(i))
            vals = vals.astype(float)
            
        ### plotting all the lines 

        x = np.linspace(0.35,2.3)
        err1 = vals + line(np.linspace(0.35,2.3), *m.values)
        err2 = line(np.linspace(0.35,2.3), *m.values) - vals

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        ax1.fill_between(x,err1,err2,alpha = 0.4)
        #delta f lines
        ax1.plot(np.linspace(0.35,2.3,len(vals)),err1,color = 'royalblue',ls = '--',label = '$\\delta$ f')#plots fit error
        ax1.plot(np.linspace(0.35,2.3,len(vals)),err2,color = 'royalblue',ls = '--')#plots fit error
        #fit line and errorbar points
        ax1.errorbar(sl,means,yerr = TAP0err, fmt = "s",color = "royalblue", ecolor = "k",elinewidth = 3, capsize = 5) #plots errorbars and points
        ax1.plot(np.linspace(0.35,2.3), line(np.linspace(0.35,2.3), *m.values),'-', label= "a + b$\mathregular{e^{cx}}$",color = 'darkorange')  #plots line
        
        ### legend and console info       
    
        r = m.fval / (len(means) - len(m.parameters))
    
        fit_info = [ 
        f"$\\chi^2$ / $n_\\mathrm{{dof}}$ = {r:.2f}", 
        ]
    
        for p, v, e in zip(m.parameters, m.values, m.errors):
            fit_info.append(f"{p} = ${v:.0f} \\pm {e:.0f}$")
    
    
        plt.legend(title="\n".join(fit_info));
        print(' ') 
        print(' Fitting parameters') 
        for p in m.parameters: 
            print("{} = {} +- {}".format(p,m.values[p], m.errors[p]))
    
        print('') 
        print('chi squared:', m.fval) 
        print('number of degrees of freedom', (len(means)-len(m.parameters))) 
        print('reduced chi squared:', f"{r:.2f}" )
        plt.title(f"{title_name}")
        plt.ylim(75,400)
        plt.xlim(0,2.3)
        plt.ylabel('Average TAP0 for BERT = 10E-11')
        plt.xlabel('Length (m)')
        plt.savefig(output_name)
        
if __name__ == "__main__":
    main()


