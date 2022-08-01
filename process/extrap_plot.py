# BERT_Plot.py

import matplotlib.pyplot as plt
import numpy as np
from tools import makeDir
# import sympy as sym
from iminuit.cost import LeastSquares
from iminuit import Minuit, __version__
from tools import ToErrRate, Xtrap

def plot(plot_dir, output_file, x_values, y_values,name,min_value, x_label="TAP0 DAC", y_label="Bit error rate", setLogY=True, y_errors=[]):

    useXKCDStyle = False
    test = True
    
    makeDir(plot_dir)
    table = []
    size_list = [[0.35, 100], [0.35, 101], [0.8, 102], [0.8, 103], [1, 104], [1.6, 106], [1.6, 107],  [0.35, 134], [0.35, 135], [0.35, 137], [0.35, 138], [0.8, 139], [0.8, 141], [0.8, 142], [0.8, 143], [1.0, 144], [1.0, 145], [1.0, 146], [1.0, 147], [1.0, 148], [1.4, 149], [1.4, 150], [1.4, 151], [1.4, 152], [1.4, 153], [1.6, 154], [1.6, 155], [1.6, 156], [1.6, 157], [1.6, 158], [1.6, 159], [1.6, 160], [1.6, 161], [1.6, 162], [1.6, 163], [1.6, 164], [1.6, 165], [1.8, 167], [1.8, 168], [1.8, 169], [1.8, 170], [1.8, 172], [1.8, 175], [1.8, 176], [2.0, 179], [2.0, 180], [2.0, 181], [1.4,207], [0.35,300], [0.35,301], [0.35,302], [0.35,303], [0.35,304], [0.35,305]]
    
    if useXKCDStyle:
        plt.xkcd()
        
    if not test:  
        if len(y_values) > 2:
            
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            
            # model for fit line
            def line(x, b, c): 
                return b * np.exp(c*x)
                
            
            #(x_data,y_data,yerr,fit_model)
            least_squares = LeastSquares(x_values,y_values,y_errors,line)  
            
            m = Minuit(least_squares,b = 0.1,c = 0)  #initial values for fit params
            m.migrad()  # finds minimum of least_squares function
            m.hesse()  # computes errors
            NewBer = Xtrap(m) #extrapolate BER to E-14
            
            
            if setLogY:
                ax1.set_yscale('log')
            ax1.set_title(f"E-link {name}",  fontsize=20)
            ax1.set_xlabel(x_label,          fontsize=16)
            ax1.set_ylabel(y_label,          fontsize=16)
            ax1.tick_params(axis='both', which='major', labelsize=10)
            ax1.tick_params(axis='both', which='minor', labelsize=8)
            plt.ylim(1E-14,1E-3)
            
            x = np.linspace(x_values[0],500)
            #plots fit line
            ax1.plot(x, line(x, *m.values),'-',label= "b$\mathregular{e^{cx}}$",color = 'darkorange')
            
            #plots points
            ax1.errorbar(x_values,y_values,y_errors, fmt = "s",color = "royalblue", ecolor = "k",elinewidth = 3, capsize = 5)
            
            if len(y_values) > len(m.parameters):
                
                r = m.fval / (len(y_values) - len(m.parameters))
                table.append([min_value,NewBer,name,r])
                
                fit_info = [ 
                f"$\\chi^2$ / $n_\\mathrm{{dof}}$ = {r:.2f}", 
                ]
            
                for p, v, e in zip(m.parameters, m.values, m.errors):
                    fit_info.append(f"{p} = ${v:.6f} \\pm {e:.6f}$")
                
                
                fit_info.append(f"TAP0 for BER(-10) = {min_value:.0f}")
                fit_info.append(f"TAP0 for BER(-14) = {NewBer:.0f}")
                
                ax1.legend(title="\n".join(fit_info));
                
                # output_png = "{0}/{1}.png".format(plot_dir, output_file)
                # output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
                
                # plt.savefig(output_png, bbox_inches='tight')
                # plt.savefig(output_pdf, bbox_inches='tight')
                
                # #close to avoid memory warning 
                # plt.close('all')
                
    elif test:
        if len(y_values) > 2:
            
        
        # model for fit line
            def line(x, b, c): 
                return b * np.exp(c*x)
                # return a + b*x + c * x**2
                
            #(x_data,y_data,yerr,fit_model)
            least_squares = LeastSquares(x_values,y_values,y_errors,line)  
            
            m = Minuit(least_squares,b = 0.1,c = 0)  #initial values for fit params
            m.migrad()  # finds minimum of least_squares function
            m.hesse()  # computes errors
            NewBer = Xtrap(m) #extrapolate BER to E-14
            r = m.fval / (len(y_values) - len(m.parameters)) #reduced chi^2
            table_list = [min_value,NewBer,name,r]
            for i in size_list:
                if int(i[1]) == int(name):
                    table_list.append(i[0])
                    table.append(table_list)
                
               
    return table
    
def plotMultiple(plot_dir, output_file, inputs, xlim, ylim, x_label="TAP0 DAC", y_label="Bit errors per 10 seconds", setLogY=True, alpha=None, setBERY=False):
    useXKCDStyle = False
    makeDir(plot_dir)
    if useXKCDStyle:
        plt.xkcd()
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = [
                "xkcd:cherry red",
                "xkcd:apple green",
                "xkcd:bright blue",
                "xkcd:tangerine",
                "xkcd:electric purple",
                "xkcd:aqua blue",
                "xkcd:grass green",
                "xkcd:lilac",
                "xkcd:coral",
                "xkcd:fuchsia"
    ]
    
    for i, item in enumerate(inputs):
        x_values = item["x_values"]
        y_values = item["y_values"]
        label    = item["label"]
        color    = colors[i]
        x_values = np.array(x_values)
        y_values = np.array(y_values)
        if setBERY:
            # note: using this order of operations to fix floating point issue for 1e-11
            y_values = 1e-10 * y_values
            for i in range(len(y_values)):
                if y_values[i] == 0.0:
                    y_values[i] = 1e-11
        if "y_errors" in item:
            y_errors = item["y_errors"]
            plt.errorbar(x_values, y_values, yerr=y_errors, fmt='o', label=label, color=color, alpha=alpha)
        else:
            plt.plot(x_values, y_values, 'o', label=label, color=color, alpha=alpha)

    if setLogY:
        ax.set_yscale('symlog')
    if setBERY:
        ax.set_yscale('log')
    
    legend_font_size = 12
    #legend_font_size = 16
    ax.legend(loc='upper right', prop={'size': legend_font_size})
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title("BERT TAP0 Scan", fontsize=20)
    ax.set_xlabel(x_label,         fontsize=16)
    ax.set_ylabel(y_label,         fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    
    #plt.rcParams.update({'axes.labelsize': 'large'}) 
    
    # output_png = "{0}/{1}.png".format(plot_dir, output_file)
    # output_pdf = "{0}/{1}.pdf".format(plot_dir, output_file)
    
    # plt.savefig(output_png, bbox_inches='tight')
    # plt.savefig(output_pdf, bbox_inches='tight')
    
    # # close to avoid memory warning 
    # plt.close('all')

def main():
    plot_dir    = "plots"
    output_file = "BERT_example"
    x_values = [100, 110, 120,130,140]
    y_values = [179652,112632, 9469, 192,24]
    y_values = ToErrRate(y_values)
    plot(plot_dir, output_file, x_values, y_values)

if __name__ == "__main__":
    main()
    
    
   
        
        

    
        
        
        
            
    
        
        

