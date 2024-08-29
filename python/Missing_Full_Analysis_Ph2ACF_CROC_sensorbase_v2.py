##############################################################################
# Author: M.Antonello 
# Date: 29/07/2023
# Input: 1 physics root file of a X-Ray scan + 1 Thr root file + the relative txt file 
# Usage: python3 Missing_Full_Analysis_Ph2ACF_CROC.py -scurve Run000083 -noise Run000088 -outpath ADVCAM -sensor ADV_W_8_64 -bias 30 -vref 785
# Output: png plots with the main results
# Variables to change: Sensor, Thr, VMAX (only if hot pixels are present) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
import os
from scipy.optimize import curve_fit
import ROOT; ROOT.gErrorIgnoreLevel = ROOT.kWarning; ROOT.gROOT.SetBatch(True) 
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mplhep as hep; hep.style.use("CMS")
import argparse

# Arguments --------------------
parser = argparse.ArgumentParser(description='Do the XRay analysis')
parser.add_argument('-scurve','--scurve', help = 'The name of the SCurve.root (and txt) file', default = 'Run000083', type = str)
parser.add_argument('-noise','--noise', help = 'The name of the Noise.root file', default = 'Run000088', type = str)
parser.add_argument('-outpath','--outpath', help = 'The name of the folder to be creaated in results', default = 'ADVCAM', type = str)
parser.add_argument('-sensor','--sensor', help = 'The name of the sensor', default = 'ADV_W_8_64', type = str)
parser.add_argument('-thr_missing','--thr_missing', help = 'The threshold to classify the missing bumps [Hits]', default = 100, type = int)
parser.add_argument('-thr_strange','--thr_strange', help = 'The threshold to classify the problematic bumps [Hits]', default = 1000, type = int)
parser.add_argument('-bias','--bias', help = 'The bias of the sensor [V]', default = '120', type = str)
parser.add_argument('-vref','--vref', help = 'The VRef_ADC [mV]', default = 800, type = int)
parser.add_argument('-ntrg','--ntrg', help = 'The total # of triggers in the xml', default = 1e6, type = int)
parser.add_argument('-nbx','--nbx', help = 'The total # of bunch crossing for each trigger in the xml', default = 10, type = int)
args = parser.parse_args()

Sensor=args.sensor; thr_data_file='data/'+args.scurve+'_SCurve.root'; Path='results/'+args.outpath+'/'
analyzed_data_file='data/'+args.noise+'_NoiseScan.root'; analyzed_txt_file='data/'+args.scurve+'_CMSIT_RD53B.txt'
Thr=args.thr_missing; Thr_strange=args.thr_strange; Voltage_1=args.bias; 
V_adc=args.vref; nTrg=args.ntrg; nBX=args.nbx

####### PARAMETERS TO BE CHANGED MANUALLY: ###################################  
H_ID='0'; C_ID='15'; num_rows = 336; num_cols = 432; FIT=True
el_conv=V_adc/162; Noise_MAX=65*el_conv; Thr_MAX=600*el_conv 
step_noise=0.1*el_conv; step_thr=2*el_conv; YMAX=100000; step=10; VMAX=7000; 
##############################################################################

if not os.path.exists(Path+Sensor): os.makedirs(Path+Sensor)

def GetMaskFromTxt(file_path,num_rows,num_cols):
    array_2d = np.zeros((num_rows,num_cols))
    col=-1
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("COL "): col+=1
            if line.startswith("ENABLE "):
                enable_row = line.replace("ENABLE ", "").strip().split(',')
                for row,value in enumerate(enable_row): array_2d[row,col]=int(value)
    return array_2d.T

def Ph2_ACFRootExtractor(infile,Scan_n,type):
    canvas = infile.Get("Detector/Board_0/OpticalGroup_0/Hybrid_"+H_ID+"/Chip_"+str(int(C_ID))+"/D_B(0)_O(0)_H("+H_ID+")_"+Scan_n+"_Chip("+str(int(C_ID))+")")
    map_r = canvas.GetPrimitive("D_B(0)_O(0)_H("+H_ID+")_"+Scan_n+"_Chip("+str(int(C_ID))+")")
    if "2D" in type:
        # Convert the TH2F histogram to np array (NB: bin numbering in root starts from 1, numpy from 0)
        map = np.zeros((map_r.GetNbinsX(), map_r.GetNbinsY()))
        for i in range(1, map_r.GetNbinsX()+1):
            for j in range(1, map_r.GetNbinsY()+1):
                map[i-1][j-1] = map_r.GetBinContent(i, j)
        map=map.T
    else:
        map = map_r.GetEntries()
    return map

def ExtractThrData():
    inFile = ROOT.TFile.Open(thr_data_file,"READ")
    ThrMap=Ph2_ACFRootExtractor(inFile,'Threshold2D','2D')
    ThrMap=To25x100SensorCoordinates(ThrMap)
    NoiseMap=Ph2_ACFRootExtractor(inFile,'Noise2D','2D')
    NoiseMap=To25x100SensorCoordinates(NoiseMap)
    ToTMap=Ph2_ACFRootExtractor(inFile,'ToT2D','2D')
    ToTMap=To25x100SensorCoordinates(ToTMap)
    ReadoutErrors=Ph2_ACFRootExtractor(inFile,'ReadoutErrors','Entries')
    FitErrors=Ph2_ACFRootExtractor(inFile,'FitErrors','Entries')
    inFile.Close()
    Noise_L=NoiseMap.flatten(); Thr_L=ThrMap.flatten(); 
    return ThrMap, NoiseMap, ToTMap, ReadoutErrors, FitErrors, Noise_L, Thr_L

def gaus(X,A,X_mean,sigma): return A*np.exp(-(X-X_mean)**2/(2*sigma**2))
def GAUSS_FIT(x_hist,y_hist,color):
    mean = sum(x_hist*y_hist)/sum(y_hist)               
    sigma = sum(y_hist*(x_hist-mean)**2)/sum(y_hist)
    #Gaussian least-square fitting process
    param_optimised,param_covariance_matrix = curve_fit(gaus,x_hist,y_hist,p0=[1,mean,sigma])#,maxfev=5000)
    x_hist_2=np.linspace(np.min(x_hist),np.max(x_hist),500)
    plt.plot(x_hist_2,gaus(x_hist_2,*param_optimised),color,label='FIT: $\mu$ = '+str(round(param_optimised[1],1))+' e$^-$ $\sigma$ = '+str(abs(round(param_optimised[2],1)))+' e$^-$')

def XRayAnalysis(nTrg,nBX):
    Mask_before = GetMaskFromTxt(analyzed_txt_file,num_rows,num_cols) # 0 in Mask_before means MASKED, 1 Good
    Disabled=np.where(Mask_before==0)
    
    inFile = ROOT.TFile.Open(analyzed_data_file,"READ")
    Data=Ph2_ACFRootExtractor(inFile,'PixelAlive','2D')
    ToTMapX=Ph2_ACFRootExtractor(inFile,'ToT2D','2D')
    Data=Data*nTrg*nBX
    ReadoutErrorsXRay=Ph2_ACFRootExtractor(inFile,'ReadoutErrors','Entries')
    inFile.Close()
    Data_L=Data.flatten()
    
    # MASK FROM MY THR
    Mask_XRay=np.ones((num_cols,num_rows))+1
    Cut=np.where(Data<Thr)
    Mask_XRay[Cut[1],Cut[0]]=0 # 0 in Mask_XRays means MASKED, 2 Good
    # Adding strange pixels
    Mask_strange=np.ones((num_cols,num_rows))+1
    Cut_strange=np.where((Data<Thr_strange) & (Data>=Thr))
    Mask_strange[Cut_strange[1],Cut_strange[0]]=0 # 0 in Mask_Strange means MASKED, 2 Good

    # FIND MISSING BUMPS
    Missing_mat=Mask_before+Mask_XRay # 0=MASKED 1=MISSING 2=ERRORS 3=GOOD
    Missing=np.where(Missing_mat==1)
    Perc_missing=float("{:.4f}".format((Missing[0].size/((num_rows*num_cols)-Disabled[0].size))*100))
    # Adding strange pixels
    Missing_mat_strange=Mask_strange+Mask_before # 0=MASKED 1=STRANGE 2=ERRORS 3=GOOD -1= STRANGE
    Missing_strange=np.where(Missing_mat_strange==1)
    Perc_missing_strange=float("{:.4f}".format((Missing_strange[0].size/((num_rows*num_cols)-Disabled[0].size))*100))
    # 0=MASKED 1=MISSING 2=ERRORS 3=GOOD -1= STRANGE
    Missing_mat[Missing_strange[0],Missing_strange[1]]=-1 #IMPORTANT TO REMOVE FOR PLOTS IF NO STRANGE
    
    Data=To25x100SensorCoordinates(Data)
    Missing_mat=To25x100SensorCoordinates(Missing_mat.T) #traspose for the same reason... consider that as output I wil lprovide the Transpose again so it should be fine
    ToTMapX=To25x100SensorCoordinates(ToTMapX)

    return Disabled[0].size, Data, Data_L, Missing_mat.T, Missing[0].size, Missing_strange[0].size, ReadoutErrorsXRay, Perc_missing, Perc_missing_strange, ToTMapX

def Plots(ToTMap, NoiseMap, Noise_L, ThrMap, Thr_L, Data, Data_L, Missing_mat, Missing, Missing_strange, Perc_missing, Perc_missing_strange, Disabled, ToTMapX, FitErrors):
    # Noise Map
    fig1 = plt.figure()
    ax = fig1.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(NoiseMap*el_conv, vmax=Noise_MAX) #150vmax
    ax.set_aspect(0.25)
    bar1=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
    fig1.savefig(Path+Sensor+'/'+Voltage_1+'V_Noise_Map.png', format='png', dpi=300)

    #Histogram
    fig2 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig2.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    h_S=plt.hist(Noise_L*el_conv,color='black',bins = np.arange(0,Noise_MAX,step_noise),label='Noise',histtype='step')
    if FIT: GAUSS_FIT(h_S[1][:-1],h_S[0],'red')
    ax.set_ylim([0.1, 10000])
    ax.set_yscale('log')
    ax.set_xlabel('electrons')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper right')
    fig2.savefig(Path+Sensor+'/'+Voltage_1+'V_Noise_Hist.png', format='png', dpi=300)

    # Threshold Map
    fig3 = plt.figure()
    ax = fig3.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(ThrMap*el_conv, vmax=Thr_MAX, vmin=1200) #3500 vmax
    ax.set_aspect(0.25)
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
    fig3.savefig(Path+Sensor+'/'+Voltage_1+'V_Threshold_Map.png', format='png', dpi=300)

    # ToT Map
    fig7 = plt.figure()
    ax = fig7.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(ToTMap)
    ax.set_aspect(0.25)
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='ToT')
    fig7.savefig(Path+Sensor+'/'+Voltage_1+'V_ToT_Map.png', format='png', dpi=300)

    # ToT Map XRay
    fig10 = plt.figure()
    ax = fig10.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(ToTMapX)
    ax.set_aspect(0.25)
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='ToT')
    fig10.savefig(Path+Sensor+'/'+Voltage_1+'V_ToT_Map_XRay.png', format='png', dpi=300)


    #Histogram
    fig4 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig4.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    h_L=plt.hist(Thr_L*el_conv,color='black',bins = np.arange(0,Thr_MAX,step_thr),label='Threshold',histtype='step')
    if FIT: GAUSS_FIT(h_L[1][:-1],h_L[0],'red')
    ax.set_ylim([0.1, YMAX])
    ax.set_xlim([0, Thr_MAX])
    ax.set_yscale('log')
    ax.set_xlabel('electrons')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper left')
    fig4.savefig(Path+Sensor+'/'+Voltage_1+'V_Threshold_Hist.png', format='png', dpi=300)

    # XRAY PART
    # HITS/PXL HISTOGRAM WITH X-RAYS
    fig5 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
    ax = fig5.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    ax.set_yscale('log')
    h_LIN=plt.hist(Data_L,color='black',bins = range(0,int(VMAX*3.0),step),label='Hits/pixel',histtype='step')
    ax.plot([Thr,Thr],[0,2e3],'--r',linewidth=2)
    ax.plot([Thr_strange,Thr_strange],[0,2e3],'--r',linewidth=2)
    ax.set_xlabel('Number of total Hits/pixel')
    ax.set_ylabel('entries')
    ax.legend(prop={'size': 14}, loc='upper right')
    fig5.savefig(Path+Sensor+'/'+Voltage_1+'V_Hist_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)

    # Raw Hit Map from XRay alone
    fig8 = plt.figure()
    ax = fig8.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(Data, vmax=VMAX)
    ax.set_aspect(0.25)
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='Hits')
    fig8.savefig(Path+Sensor+'/'+Voltage_1+'_XRay_Hits_Map.png', format='png', dpi=300)

    # Raw Hit Map from XRay alone
    fig9 = plt.figure()
    ax = fig9.add_subplot(111)
    ax.spines["bottom"].set_linewidth(1); ax.spines["left"].set_linewidth(1); ax.spines["top"].set_linewidth(1); ax.spines["right"].set_linewidth(1)
    imgplot = ax.imshow(Data[0:35,0:15], vmax=VMAX)
    ax.set_aspect(0.25)
    bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='Hits')
    fig9.savefig(Path+Sensor+'/'+Voltage_1+'_XRay_Hits_Map_zoom.png', format='png', dpi=300)

    # MISSING BUMPS FINAL MAPS
    fig6, (ax1, ax2) = plt.subplots(1,2, figsize=(13, 7.5))
    plt.rcParams.update({'font.size': 16})
    fig6.suptitle("Sensor "+Sensor+" -- Masked pixels: "+str(Disabled)+" -- Fit errors: "+str(FitErrors)+"\nMissing bumps (<"+str(Thr)+" hits): "+str(Missing)+" ("+str(Perc_missing)+"%) -- Problematic bumps (<"+str(Thr_strange)+" hits): "+str(Missing_strange)+" ("+str(Perc_missing_strange)+"%)")
    imgplot = ax1.imshow(Data, vmax=VMAX)
    ax1.set_title("Hit Map (Z Lim: %s hits)" % str(VMAX))
    ax1.set_aspect(0.25)
    ax1.spines["bottom"].set_linewidth(1); ax1.spines["left"].set_linewidth(1); ax1.spines["top"].set_linewidth(1); ax1.spines["right"].set_linewidth(1)
    bar1=plt.colorbar(imgplot, orientation='horizontal',ax=ax1, extend='max', label='Hits', shrink=1)
    bar1.cmap.set_over('red')
    cmap = matplotlib.colors.ListedColormap(['orange','blue', 'red', 'white'])
    bounds = [-1,0,0.9, 1.9, 2.9]
    norm =matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    imgplot2 = ax2.imshow(Missing_mat.T,cmap=cmap,norm=norm)
    ax2.set_title("Missing Map")
    ax2.set_aspect(0.25)
    ax2.spines["bottom"].set_linewidth(1); ax2.spines["left"].set_linewidth(1); ax2.spines["top"].set_linewidth(1); ax2.spines["right"].set_linewidth(1)
    bar2=plt.colorbar(imgplot2, ticks=bounds, orientation='horizontal', label='Problematic   Masked      Missing       Good      ',  spacing='proportional', shrink=1)
    bar2.set_ticks([])
    fig6.savefig(Path+Sensor+'/'+Voltage_1+'V_Missing_Bumps_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)
    return

def TerminalInfos(FitErrors,ReadoutErrors,Disabled,ReadoutErrorsXRay,Missing,Missing_strange,Perc_missing,Perc_missing_strange,Missing_mat):
    print('##############################################################\n INFO\n##############################################################')
    print('Failed fits (thr):\t'+str(FitErrors))
    print('Readout Errors (thr):\t'+str(ReadoutErrors))
    print('Readout Errors (xray):\t'+str(ReadoutErrorsXRay))
    print('Masked before:\t\t'+str(Disabled))
    print('Missing (<'+str(Thr)+'):\t\t'+str(Missing)+' ('+str(Perc_missing)+'%)')
    print('Strange (<'+str(Thr_strange)+'):\t'+str(Missing_strange)+' ('+str(Perc_missing_strange)+'%)')
    print('Check from Final matrix:')
    print('Masked before:\t\t'+str(np.where(Missing_mat==0)[0].size))
    print('Missing:\t\t'+str(np.where(Missing_mat==1)[0].size))
    print('Strange:\t\t'+str(np.where(Missing_mat==-1)[0].size))
    print('Errors:\t\t\t'+str(np.where(Missing_mat==2)[0].size))
    print('Good:\t\t\t'+str(np.where(Missing_mat==3)[0].size))
    print('Sum is: \t\t'+str(np.where(Missing_mat==0)[0].size+np.where(Missing_mat==1)[0].size+np.where(Missing_mat==2)[0].size+np.where(Missing_mat==3)[0].size+np.where(Missing_mat==-1)[0].size))
    print('Total # of pixels:\t'+str(num_cols*num_rows))
    print('##############################################################\n')
    return

def To25x100SensorCoordinates(npArray):
    new_rows=num_rows*2; new_cols=num_cols//2
    NewArray=np.zeros((new_rows,new_cols), dtype=npArray.dtype)
    for i in range(num_cols):
        for j in range(num_rows):
            #Conversion from CMSIT coverter plugin for 25x100r0c0 of Mauro
            row = 2*j+(i%2)
            col = int(i/2)
            NewArray[row,col]=npArray[j,i]
    return NewArray
    
def main():
    ThrMap, NoiseMap, ToTMap, ReadoutErrors, FitErrors, Noise_L, Thr_L = ExtractThrData()
    Disabled, Data, Data_L, Missing_mat, Missing, Missing_strange, ReadoutErrorsXRay, Perc_missing, Perc_missing_strange, ToTMapX = XRayAnalysis(nTrg,nBX)
    Plots(ToTMap, NoiseMap, Noise_L, ThrMap, Thr_L, Data, Data_L, Missing_mat, Missing, Missing_strange, Perc_missing, Perc_missing_strange, Disabled, ToTMapX,FitErrors)
    TerminalInfos(FitErrors,ReadoutErrors,Disabled,ReadoutErrorsXRay,Missing, Missing_strange,Perc_missing,Perc_missing_strange, Missing_mat)

if __name__ == "__main__":
	main()
