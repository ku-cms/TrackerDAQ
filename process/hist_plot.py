#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 13:43:09 2022

@author: jsewell
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
import warnings
import tools

warnings.filterwarnings("ignore")

def main():
    plot_dir  = "process_plots"
    tools.makeDir(plot_dir)
    file_path = input("Enter file path: ")

    ds = pd.read_csv(
        f"{file_path}",
    )

    index_num = input("Enter integer index of column with data to be plotted: ")
    index_num = int(index_num)
    x_data = ds.iloc[:,index_num].name

    plot_type = input("Plot distribution by type? (y/n): ")

    title_name = input("Title of plot: ")

    output_name = "{0}/{1}.pdf".format(plot_dir, title_name)

    mean = ds.loc[:,x_data].mean()
    std = np.std(ds.loc[:,x_data])

    if (plot_type == 'y'):
        
        index_num2 = input("Enter integer index of column with type data: ")
        index_num2 = int(index_num2)
        
        def gettype(ds):
            vals = ds.iloc[:,index_num2]
            types = []
            for x in vals:
               if x not in types:
                   types.append(x)
            return types
        
        sl = gettype(ds)
        sl = np.array(sl,dtype = 'd')
        dl = ds.groupby(ds.iloc[:,0].name)[ds.iloc[:,index_num].name].apply(list)
        
        sl_mean = [np.array(dl[sl[i]]).mean() for i in range(0,len(sl))]
        sl_std = [np.std(dl[sl[i]]) for i in range(0,len(sl))]
        
        type_data = ds.iloc[:,index_num2].name
        
        fig, g = plt.subplots()
        g = sns.displot(
            data = ds,
            x = x_data,
            kind = "hist",
            aspect = 1.4,
            hue = type_data,
            multiple = "stack",
            palette = 'Dark2',
            element = 'bars',
            binwidth = 10,
            legend = False,
        )
    
        g.fig.suptitle(f'{title_name}',color = 'k',fontsize = '21')
        plt.xlabel(f'{x_data}',fontsize = '16')
        plt.xticks(fontsize = '15')
        plt.ylabel('Count',fontsize = '16')
        plt.yticks(fontsize = '15')
    
        g.refline(x = mean + std,color = "k",label= "$\\sigma$",alpha = 0.5)
        g.refline(x = mean - std,color = "k",alpha = 0.5)
        g.refline(x = mean, color = "k", ls = "-",label = "$\\mu$",alpha = 0.8)
    
        first_legend = plt.legend(title = f'Total $\\sigma$ & $\\mu$', labels = ['_n', f"$\\sigma$ = {std:.0f}" , f"$\\mu$ = {mean:.0f}"], loc='upper right',bbox_to_anchor=(1,1.165))
    
        plt.gca().add_artist(first_legend)
                                                                                                                                                                                                                                    
        g.fig.legend(title = f"Cable Length (m)\n                 [$\\mu$,$\\sigma$]", labels = ['_n','_n',"_n",f'2.0 [{sl_mean[6]:.0f} , {sl_std[6]:.0f}]',f'1.8 [{sl_mean[5]:.0f} , {sl_std[5]:.0f}]',f'1.6 [{sl_mean[4]:.0f} , {sl_std[4]:.0f}]',f'1.4 [{sl_mean[3]:.0f} , {sl_std[3]:.0f}]',f'1.0 [{sl_mean[2]:.0f} , {sl_std[2]:.0f}]',f'0.8 [{sl_mean[1]:.0f} , {sl_std[1]:.0f}]',f'0.35 [{sl_mean[0]:.0f} , {sl_std[0]:.0f}]'],loc = "center right", bbox_to_anchor=(1,0.65),fontsize = '11');
        
        plt.savefig(output_name)
        
    elif (plot_type == 'n'):
        fig, g = plt.subplots()
        
        g = sns.displot(
            data = ds,
            x = x_data,
            kind = "hist",
            aspect = 1.4,
            color = "royalblue",
            palette = "Dark2",
            binwidth = 10,
            legend = False)
        
        g.fig.suptitle(f'{title_name}',color = 'k',fontsize = '21')
        plt.xlabel(f'{x_data}',fontsize = '16')
        plt.xticks(fontsize = '15')
        plt.ylabel('Count',fontsize = '16')
        plt.yticks(fontsize = '15')
    
        g.refline(x = mean + std,color = "orange",label= f"$\\sigma$ = {std:.0f}")
        g.refline(x = mean - std,color = "orange")
        g.refline(x = mean, color = "orange", ls = "-",label = f"$\\mu$ = {mean:.0f}")
    
        g.fig.legend(title="",fontsize = '16', loc = 'center right',bbox_to_anchor=(1,.8));
        
        plt.savefig(output_name)


if __name__ == "__main__":
    main()


