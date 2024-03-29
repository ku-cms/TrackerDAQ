##############################################################################
# Author: M.Antonello 
# Date: 15/03/2023
# Input: 1 interpreted.h5 file of a X-Ray scan (the noise scan) + 1 threshold file
# Output: png plots with the main results
# Variables to change: chip, Thr, VMAX (only if hot pixels are present) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################

import os
import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import mplhep as hep
import csv

# print border line
def printBorderLine():
    print('--------------------------------------------------------------')

# creates directory if it does not exist
def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

# Gaussian function
def gauss(X,A,X_mean,sigma):
    return A*np.exp(-(X-X_mean)**2/(2*sigma**2))

# Gaussian fit
def gauss_fit(x_hist,y_hist,color):
    mean = sum(x_hist*y_hist)/sum(y_hist)               
    sigma = sum(y_hist*(x_hist-mean)**2)/sum(y_hist)
    #Gaussian least-square fitting process
    #param_optimised,param_covariance_matrix = curve_fit(gauss,x_hist,y_hist,p0=[1,mean,sigma])
    param_optimised,param_covariance_matrix = curve_fit(gauss,x_hist,y_hist,p0=[1,mean,sigma],maxfev=1000000)
    x_hist_2=np.linspace(np.min(x_hist),np.max(x_hist),500)
    plt.plot(x_hist_2,gauss(x_hist_2,*param_optimised),color,label='FIT: $\mu$ = '+str(round(param_optimised[1],1))+' e$^-$ $\sigma$ = '+str(abs(round(param_optimised[2],1)))+' e$^-$')

# analyze data for one chip
def analyze_chip_data(module_path, chip, xray_data_file, thr_data_file):
    if module_path[-1] != "/":
        module_path += "/"
    
    chip_path = module_path + chip 
    #data_dir = "data"
    hep.style.use("CMS")
    
    ####### Parameters: ############## 
    #Thr=100; Thr_strange=1000; VMAX=5000
    
    Thr=50; Thr_strange=200; VMAX=2000
    #Thr=70; Thr_strange=200; VMAX=2000
    #Thr=100; Thr_strange=200; VMAX=2000
    #Thr=100; Thr_strange=500; VMAX=2000
    #Thr=100; Thr_strange=1000; VMAX=2000
    
    ####### THR PART  ###################
    #FIT=True; Voltage_1='120V'; el_conv=10.4; Noise_MAX=25*el_conv; Thr_MAX=400*el_conv 
    FIT=True; Voltage_1='25V'; el_conv=10.4; Noise_MAX=25*el_conv; Thr_MAX=400*el_conv 
    
    make_dir(module_path)
    make_dir(chip_path)
    
    # Load Thr data
    with tb.open_file(thr_data_file, 'r') as infile:
        data1 = infile.get_node('/HistOcc')[:].T
        Chi2in = infile.get_node('/Chi2Map')[:].T
        mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        ThrMap = infile.get_node('/ThresholdMap')[:].T
        NoiseMap = infile.get_node('/NoiseMap')[:].T
    
    #Mask
    Mask_before=np.zeros((192,400))
    Enabled=np.where(mask1)
    Mask_before[Enabled[0],Enabled[1]]=1
    
    Failed_Chi2_Map=np.zeros((192,400))+2
    Failed_fits=np.where((Chi2in==0) | (Chi2in>49))
    Failed_Chi2_Map[Failed_fits[0],Failed_fits[1]]=0
    
    New_Failed_Map=Failed_Chi2_Map+Mask_before #0 = masked alreday, 1 = Failed fit, 2 ERROR, 3 GOOD
    printBorderLine()
    print("THR SCAN")
    printBorderLine()
    print('Masked before: '+str(np.where(New_Failed_Map==0)[0].size))
    print('New failed fits: '+str(np.where(New_Failed_Map==1)[0].size))
    print('Errors: '+str(np.where(New_Failed_Map==2)[0].size))
    print('Good: '+str(np.where(New_Failed_Map==3)[0].size))
    print('Check: (must be 0) '+str(400*192-(np.where(New_Failed_Map==3)[0].size+np.where(New_Failed_Map==2)[0].size+np.where(New_Failed_Map==1)[0].size+np.where(New_Failed_Map==0)[0].size)))
    
    #### NOISE: #####################
    Noise_S=NoiseMap[:,0:127].flatten()*el_conv; Noise_L=NoiseMap[:,128:263].flatten()*el_conv; Noise_D=NoiseMap[:,264:399].flatten()*el_conv
    Legend=['SYNCH','LIN','DIFF']; step=0.1*el_conv
    
    # Map
    fig1 = plt.figure()
    #plt.rcParams.update({'font.size': 16})
    ax = fig1.add_subplot(111)
    imgplot = ax.imshow(NoiseMap*el_conv, vmax=Noise_MAX-10*el_conv) #150vmax
    bar1=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
    fig1.savefig(chip_path+'/'+Voltage_1+'_Noise_Map.png', format='png', dpi=300)
    
    #Histogram
    fig2 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig2.add_subplot(111)
    h_S=plt.hist(Noise_S,color='red',bins = np.arange(0,Noise_MAX,step),label=Legend[0],histtype='step')
    if FIT: gauss_fit(h_S[1][:-1],h_S[0],'r')
    h_D=plt.hist(Noise_D,color='blue',bins = np.arange(0,Noise_MAX,step),label=Legend[2],histtype='step')
    if FIT: gauss_fit(h_D[1][:-1],h_D[0],'blue')
    h_L=plt.hist(Noise_L,color='green',bins = np.arange(0,Noise_MAX,step),label=Legend[1],histtype='step')
    if FIT: gauss_fit(h_L[1][:-1],h_L[0],'green')
    ax.set_ylim([0.1, 3000])
    ax.set_yscale('log')
    ax.set_xlabel('electrons')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper right')
    fig2.savefig(chip_path+'/'+Voltage_1+'_Noise_Hist.png', format='png', dpi=300)
    
    #### THRESHOLDS: #####################
    Thr_S=ThrMap[:,0:127].flatten()*el_conv+180; Thr_L=ThrMap[:,128:263].flatten()*el_conv+180; Thr_D=ThrMap[:,264:399].flatten()*el_conv+180
    Legend=['SYNCH','LIN','DIFF']; step=5*el_conv; YMAX=100000
    
    # Map
    fig3 = plt.figure()
    #plt.rcParams.update({'font.size': 16})
    ax = fig3.add_subplot(111)
    imgplot = ax.imshow(ThrMap*el_conv+180, vmax=Thr_MAX-10*el_conv, vmin=1200) #3500 vmax
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
    fig3.savefig(chip_path+'/'+Voltage_1+'_Threshold_Map.png', format='png', dpi=300)
    
    #Histogram
    fig4 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig4.add_subplot(111)
    h_S=plt.hist(Thr_S,color='red',bins = np.arange(0,Thr_MAX,step),label=Legend[0],histtype='step')
    if FIT: gauss_fit(h_S[1][:-1],h_S[0],'r')
    h_D=plt.hist(Thr_D,color='blue',bins = np.arange(0,Thr_MAX,step),label=Legend[2],histtype='step')
    if FIT: gauss_fit(h_D[1][15:-1],h_D[0][15:],'blue')
    h_L=plt.hist(Thr_L,color='green',bins = np.arange(0,Thr_MAX,step),label=Legend[1],histtype='step')
    if FIT: gauss_fit(h_L[1][15:-1],h_L[0][15:],'green')
    ax.set_ylim([0.1, YMAX])
    ax.set_xlim([0, Thr_MAX])
    ax.set_yscale('log')
    ax.set_xlabel('electrons')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper left')
    fig4.savefig(chip_path+'/'+Voltage_1+'_Threshold_Hist.png', format='png', dpi=300)
    
    ####### X-RAY PART  #################
    step=10 
    with tb.open_file(xray_data_file, 'r') as infile:
        data1 = infile.get_node('/HistOcc')[:].T
        mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
    
    # MASKED BEFORE
    Mask_before=np.zeros((192,400))
    Enabled=np.where(mask1)
    Mask_before[Enabled[0],Enabled[1]]=1
    Mask_before[:,0:128]=0 #Removing SYNCH
    Disabled=((400-128)*192)-Enabled[0].size
    Enabled_Lin=np.where(mask1[:,128:264])
    Enabled_Diff=np.where(mask1[:,264:400])
    
    # MASK FROM MY THR
    Mask=np.ones((192,400))+1
    Data=np.array(data1[0])
    Data[:,0:128]=0 #Removing SYNCH
    Cut=np.where(Data<Thr)
    Mask[Cut[0],Cut[1]]=0
    # Adding strange pixels
    Mask_strange=np.ones((192,400))+1
    Cut_strange=np.where((Data<Thr_strange) & (Data>Thr))
    Mask_strange[Cut_strange[0],Cut_strange[1]]=0
    
    Data_L=Data[:,128:264]
    Data_D=Data[:,264:400]
    Data_F=Data[Enabled[0],Enabled[1]].flatten()
    Data_LIN=Data_L[Enabled_Lin[0],Enabled_Lin[1]].flatten()
    Data_DIFF=Data_D[Enabled_Diff[0],Enabled_Diff[1]].flatten()
    
    printBorderLine()
    print("X-RAY SCAN")
    printBorderLine()
    print('CHECK Disabled bdaq: %i' % (400*192-Enabled[0].size))
    print('CHECK < Thr (must be >=): %i' %Cut[0].size )
    print('# of pixels < Thr: %i'% (-(128*192)+np.where(Mask==0)[0].size))
    print('# of pixels < Thr_strange: %i'% (np.where(Mask_strange==0)[0].size))
    
    # FIND MISSING BUMPS
    Neglet_mat=Mask+Mask_before # 0=MASKED + SYNCH 1=MISSING 2=ERRORS 3=GOOD
    Missing=np.where(Neglet_mat==1)
    Missing_L=np.where(Neglet_mat[:,128:264]==1)
    # Adding strange pixels
    Neglet_mat_strange=Mask_strange+Mask_before # 0=MASKED + SYNCH 1=MISSING 2=ERRORS 3=GOOD -1= STRANGE
    Missing_strange=np.where(Neglet_mat_strange==1)
    Missing_L_strange=np.where(Neglet_mat_strange[:,128:264]==1)
    Neglet_mat[Missing_strange[0],Missing_strange[1]]=-1 #IMPORTANT TO REMOVE FOR PLOTS IF NO STRANGE
    
    print('# of masked by bdaq (enable mask): %i' % Disabled)
    print('# of masked by Analysis (Occ. map): %i' % (-(128*192)+np.where(Neglet_mat==0)[0].size))
    print('# of errors: %i' % (np.where(Neglet_mat==2)[0].size))
    print('# of missing: %i' % Missing[0].size)
    print('# of missing LIN: %i' % Missing_L[0].size)
    print('# of strange: %i' % Missing_strange[0].size)
    print('# of strange LIN: %i' % Missing_L_strange[0].size)
    print('CHECK: Sum of pixels: '+str(np.where(Neglet_mat==0)[0].size+np.where(Neglet_mat==-1)[0].size+np.where(Neglet_mat==1)[0].size+np.where(Neglet_mat==3)[0].size)+' of '+str(400*192)+' total pixels')
    
    Mask_Failed_check=np.zeros((192,400))
    Mask_Failed_check_where=np.where(New_Failed_Map==1)
    Mask_Failed_check[Mask_Failed_check_where[0],Mask_Failed_check_where[1]]=1
    Mask_Failed_check[Missing[0],Missing[1]]+=1
    Mask_Failed_check[Missing_strange[0],Missing_strange[1]]+=3
    printBorderLine()
    print("FINAL RESULTS")
    printBorderLine()
    print('# of masked by bdaq (enable mask): %i' % Disabled)
    print('# of failed fits: '+str(Mask_Failed_check_where[0].size))
    print('# of missing: '+str(Missing[0].size)+' ('+str(np.where(Mask_Failed_check==2)[0].size)+' failed fits)')
    print('# of strange: '+str(Missing_strange[0].size)+' ('+str(np.where(Mask_Failed_check==4)[0].size)+' failed fits)')
    printBorderLine()
    
    Missing_mat=np.zeros((192,400))
    Missing_mat[Missing[0],Missing[1]]=1
    Perc=float("{:.4f}".format((Missing[0].size/((400-128)*192-Disabled))*100))
    Missing_mat_strange=np.zeros((192,400))
    Missing_mat_strange[Missing_strange[0],Missing_strange[1]]=1
    Perc_strange=float("{:.4f}".format((Missing_strange[0].size/((400-128)*192-Disabled))*100))
    
    # HITS/PXL HISTOGRAM WITH X-RAYS
    fig3 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig3.add_subplot(111)
    ax.set_yscale('log')
    h_DIFF=plt.hist(Data_DIFF,color='blue',bins = range(0,VMAX,step),label='DIFF',histtype='step')
    h_LIN=plt.hist(Data_LIN,color='green',bins = range(0,VMAX,step),label='LIN',histtype='step')
    ax.plot([Thr,Thr],[0,2e3],'--k',linewidth=2)
    ax.plot([Thr_strange,Thr_strange],[0,2e3],'--k',linewidth=2)
    ax.set_xlabel('Number of total Hits/pixel')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper right')
    fig3.savefig(chip_path+'/Hist_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)
    
    # MISSING BUMPS FINAL MAPS
    fig , (ax1, ax2) = plt.subplots(1,2, figsize=(20, 6))
    plt.rcParams.update({'font.size': 16})
    fig.suptitle("chip "+chip+" -- Missing bumps: "+str(Missing[0].size)+" ("+str(Perc)+"%) ("+str(np.where(Mask_Failed_check==2)[0].size)+" failed fits) -- Masked pixels: "+str((400-128)*192-Enabled[0].size)+" -- Problematic bumps: "+str(Missing_strange[0].size)+" ("+str(Perc_strange)+"%) ("+str(np.where(Mask_Failed_check==4)[0].size)+" failed fits)")
    imgplot = ax1.imshow(Data, vmax=VMAX)
    ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(VMAX))
    bar1=plt.colorbar(imgplot, orientation='horizontal',ax=ax1, extend='max', label='Hits')
    bar1.cmap.set_over('red')
    cmap = mpl.colors.ListedColormap(['orange','white', 'red', 'green'])
    bounds = [-1,0,0.9, 1.9, 2.9]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    imgplot2 = ax2.imshow(Neglet_mat,cmap=cmap,norm=norm)
    ax2.set_title("Missing Map (Cut: < %s hits)" % str(Thr))
    bar2=plt.colorbar(imgplot2, ticks=bounds, orientation='horizontal', label='Problematic             Masked               Missing                   Good          ',  spacing='proportional')
    bar2.set_ticks([])
    fig.savefig(chip_path+'/Missing_Bumps_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)

    # close all figures to avoid memory issues:
    plt.close('all')

# analyze all chips in a module
def analyze_module(module_path, dataMap):
    printBorderLine()
    print("Analyzing module; module_path = {0}".format(module_path))
    printBorderLine()
    for chip in dataMap:
        print(" - Analyzing chip: {0}".format(chip))
        xray_data_file  = dataMap[chip]['xray_data_file']
        thr_data_file   = dataMap[chip]['thr_data_file']
        analyze_chip_data(module_path, chip, xray_data_file, thr_data_file)

# run analysis over all modules; define chips to analyze for each module
def run_analysis():
    # results directory
    results_path = 'analysis_results'
    make_dir(results_path)

    # Module_ZH0024
    """ module_path = '{0}/Module_ZH0024'.format(results_path)

    dataMap = {}
    dataMap['ROC0'] = {}
    dataMap['ROC0']['xray_data_file'] = 'output_data/module_0_xray_run_7/chip_0/20230417_144719_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC0']['thr_data_file']  = 'output_data/module_0_xray_run_7/chip_0/20230417_143501_threshold_scan_interpreted.h5'
    dataMap['ROC1'] = {}
    dataMap['ROC1']['xray_data_file'] = 'output_data/module_0_xray_run_7/chip_1/20230417_153820_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC1']['thr_data_file']  = 'output_data/module_0_xray_run_7/chip_1/20230417_152739_threshold_scan_interpreted.h5'
    dataMap['ROC2_original'] = {}
    dataMap['ROC2_original']['xray_data_file'] = 'output_data/module_0_xray_run_7/chip_2/20230417_160928_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2_original']['thr_data_file']  = 'output_data/module_0_xray_run_7/chip_2/20230417_160037_threshold_scan_interpreted.h5'
    dataMap['ROC2_2p0cm'] = {}
    dataMap['ROC2_2p0cm']['xray_data_file'] = 'output_data/module_ZH0024_xray_run_1/chip_2/20230420_141506_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2_2p0cm']['thr_data_file']  = 'output_data/module_ZH0024_xray_run_1/chip_2/20230420_140710_threshold_scan_interpreted.h5'
    dataMap['ROC2_2p5cm'] = {}
    dataMap['ROC2_2p5cm']['xray_data_file'] = 'output_data/module_ZH0024_xray_run_1/chip_2/20230427_120227_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2_2p5cm']['thr_data_file']  = 'output_data/module_ZH0024_xray_run_1/chip_2/20230427_115533_threshold_scan_interpreted.h5'
    dataMap['ROC3'] = {}
    dataMap['ROC3']['xray_data_file'] = 'output_data/module_0_xray_run_7/chip_3/20230417_164701_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC3']['thr_data_file']  = 'output_data/module_0_xray_run_7/chip_3/20230417_163833_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap) 
    
    # Module_ZH0022
    module_path = '{0}/Module_ZH0022'.format(results_path)

    #dataMap = {}
    #dataMap['ROC1'] = {}
    #dataMap['ROC1']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_1/chip_1/20230418_115040_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC1']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_1/chip_1/20230418_114015_threshold_scan_interpreted.h5'
    #dataMap['ROC2'] = {}
    #dataMap['ROC2']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_1/chip_2/20230418_130837_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC2']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_1/chip_2/20230418_125845_threshold_scan_interpreted.h5' 
    #dataMap['ROC3'] = {}
    #dataMap['ROC3']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_1/chip_3/20230420_114212_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC3']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_1/chip_3/20230420_110751_threshold_scan_interpreted.h5' 
    
    dataMap = {}
    dataMap['ROC1'] = {}
    dataMap['ROC1']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_2/chip_1/20230427_153604_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC1']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_2/chip_1/20230427_152633_threshold_scan_interpreted.h5'
    dataMap['ROC2'] = {}
    dataMap['ROC2']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_2/chip_2/20230427_162130_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_2/chip_2/20230427_161235_threshold_scan_interpreted.h5'
    dataMap['ROC3'] = {}
    dataMap['ROC3']['xray_data_file'] = 'output_data/module_ZH0022_xray_run_2/chip_3/20230427_170337_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC3']['thr_data_file']  = 'output_data/module_ZH0022_xray_run_2/chip_3/20230427_165527_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap)
    

    #Module_ZH0023
    module_path = '{0}/Module_ZH0023'.format(results_path)

    dataMap = {}
    dataMap['ROC0'] = {}
    dataMap['ROC0']['xray_data_file'] = 'output_data/module_ZH0023_xray_run_0/chip_0/20230511_171828_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC0']['thr_data_file']  = 'output_data/module_ZH0023_xray_run_0/chip_0/20230511_170535_threshold_scan_interpreted.h5'
    dataMap['ROC1'] = {}
    dataMap['ROC1']['xray_data_file'] = 'output_data/module_ZH0023_xray_run_0/chip_1/20230511_174624_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC1']['thr_data_file']  = 'output_data/module_ZH0023_xray_run_0/chip_1/20230511_173158_threshold_scan_interpreted.h5'
    dataMap['ROC2'] = {}
    dataMap['ROC2']['xray_data_file'] = 'output_data/module_ZH0023_xray_run_0/chip_2/20230511_180727_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2']['thr_data_file']  = 'output_data/module_ZH0023_xray_run_0/chip_2/20230511_180113_threshold_scan_interpreted.h5'
    dataMap['ROC3'] = {}
    dataMap['ROC3']['xray_data_file'] = 'output_data/module_ZH0023_xray_run_0/chip_3/20230511_182952_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC3']['thr_data_file']  = 'output_data/module_ZH0023_xray_run_0/chip_3/20230511_182339_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap)"""

    #Module_ZH0036
    #module_path = '{0}/Module_ZH0036'.format(results_path)

    #dataMap = {}
    #dataMap['ROC0'] = {}
    #dataMap['ROC0']['xray_data_file'] = 'output_data/module_ZH0036/chip_0/20230710_134647_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC0']['thr_data_file']  = 'output_data/module_ZH0036/chip_0/20230710_133310_threshold_scan_interpreted.h5'
    #dataMap['ROC1'] = {}
    #dataMap['ROC1']['xray_data_file'] = 'output_data/module_ZH0036/chip_1/20230710_132124_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC1']['thr_data_file']  = 'output_data/module_ZH0036/chip_1/20230710_131449_threshold_scan_interpreted.h5'
    #dataMap['ROC2'] = {}
    #dataMap['ROC2']['xray_data_file'] = 'output_data/module_ZH0036/chip_2/20230710_124452_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC2']['thr_data_file']  = 'output_data/module_ZH0036/chip_2/20230710_123826_threshold_scan_interpreted.h5'
    #dataMap['ROC3'] = {}
    #dataMap['ROC3']['xray_data_file'] = 'output_data/module_ZH0036/chip_3/20230710_114935_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC3']['thr_data_file']  = 'output_data/module_ZH0036/chip_3/20230710_114312_threshold_scan_interpreted.h5'
    
    #analyze_module(module_path, dataMap)

    #Module_ZH0034
    module_path = '{0}/Module_ZH0034'.format(results_path)

    dataMap = {}
    #dataMap['ROC0'] = {}
    #dataMap['ROC0']['xray_data_file'] = 'output_data/module_ZH0036/chip_0/20230710_134647_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC0']['thr_data_file']  = 'output_data/module_ZH0036/chip_0/20230710_133310_threshold_scan_interpreted.h5'
    dataMap['ROC1'] = {}
    dataMap['ROC1']['xray_data_file'] = 'output_data/module_ZH0034/chip_1/20230720_114857_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC1']['thr_data_file']  = 'output_data/module_ZH0034/chip_1/20230720_114127_threshold_scan_interpreted.h5'
    dataMap['ROC2'] = {}
    dataMap['ROC2']['xray_data_file'] = 'output_data/module_ZH0034/chip_2/20230718_162508_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC2']['thr_data_file']  = 'output_data/module_ZH0034/chip_2/20230718_161900_threshold_scan_interpreted.h5'
    dataMap['ROC3'] = {}
    dataMap['ROC3']['xray_data_file'] = 'output_data/module_ZH0034/chip_3/20230718_160514_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC3']['thr_data_file']  = 'output_data/module_ZH0034/chip_3/20230718_155509_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap)

    #Module_MJ321
    #module_path = '{0}/Module_MJ321_v2'.format(results_path)

    #dataMap = {}
    #dataMap['ROC0'] = {}
    #dataMap['ROC0']['xray_data_file'] = 'output_data/single_chip_modules_v2/20230621_153826_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC0']['thr_data_file']  = 'output_data/single_chip_modules_v2/20230621_153234_threshold_scan_interpreted.h5'
    
    #analyze_module(module_path, dataMap)

    #Module_MJ322
    #module_path = '{0}/Module_MJ322_v2'.format(results_path)

    #dataMap = {}
    #dataMap['ROC0'] = {}
    #dataMap['ROC0']['xray_data_file'] = 'output_data/single_chip_modules_v2/20230621_160631_noise_occupancy_scan_interpreted.h5'
    #dataMap['ROC0']['thr_data_file']  = 'output_data/single_chip_modules_v2/20230621_155833_threshold_scan_interpreted.h5'
    
    #analyze_module(module_path, dataMap)

    '''#Module_MJ321
    module_path = '{0}/Module_MJ321'.format(results_path)

    dataMap = {}
    dataMap['ROC0'] = {}
    dataMap['ROC0']['xray_data_file'] = 'output_data/module_MJ321/20230619_142233_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC0']['thr_data_file']  = 'output_data/module_MJ321/20230619_141624_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap)

     #Module_MJ322
    module_path = '{0}/Module_MJ322'.format(results_path)

    dataMap = {}
    dataMap['ROC0'] = {}
    dataMap['ROC0']['xray_data_file'] = 'output_data/module_MJ322/20230619_144523_noise_occupancy_scan_interpreted.h5'
    dataMap['ROC0']['thr_data_file']  = 'output_data/module_MJ322/20230619_143857_threshold_scan_interpreted.h5'
    
    analyze_module(module_path, dataMap)'''


def main():
    run_analysis()

if __name__ == "__main__":
    main()

