##############################################################################
# Author: M.Antonello 
# Date: 15/03/2023
# Input: 1 interpreted.h5 file of a X-Ray scan (the noise scan) + 1 threshold file
# Output: png plots with the main results
# Variables to change: Sensor, Thr, VMAX (only if hot pixels are present) 
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
hep.style.use("CMS")

####### TO BE CHANGED: ############## 
Thr=100; Thr_strange=1000; VMAX=5000
####### KIT MODULES:   ##############
#Path='results/KIT/'
#Sensor='33196-06-21'; analyzed_data_file='20221014_155339_noise_occupancy_scan_interpreted.h5'; thr_data_file='20221014_154421_threshold_scan_interpreted.h5'
#Sensor='33196-06-21_40c'; analyzed_data_file='20230324_153834_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230324_152646_threshold_scan_interpreted.h5'
#Sensor='33196-06-13'; analyzed_data_file='20221014_130846_noise_occupancy_scan_interpreted.h5'; thr_data_file='20221014_091826_threshold_scan_interpreted.h5'
#Sensor='33196-06-13_30c'; analyzed_data_file='20230324_162150_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230324_161103_threshold_scan_interpreted.h5'
#Sensor='KIT_5'; analyzed_data_file='20230313_102807_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230313_101757_threshold_scan_interpreted.h5'
#Sensor='KIT_8'; analyzed_data_file='20230313_155958_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230313_154703_threshold_scan_interpreted.h5'
#Sensor='KIT_9'; analyzed_data_file='20230308_143817_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230308_142339_threshold_scan_interpreted.h5'
#Sensor='KIT_13'; analyzed_data_file='20230314_111149_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230314_105849_threshold_scan_interpreted.h5'
#Sensor='KIT_14'; analyzed_data_file='20230314_145516_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230314_144336_threshold_scan_interpreted.h5'
####### IZM MODULES:   ##############
Path='results/IZM/'
#Sensor='614'; analyzed_data_file='20230314_145516_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230314_144336_threshold_scan_interpreted.h5'
#Sensor='615'; analyzed_data_file='20230321_150829_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230321_145813_threshold_scan_interpreted.h5'
#Sensor='615_10c'; analyzed_data_file='20230322_120957_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230322_115814_threshold_scan_interpreted.h5'
#Sensor='615_40c'; analyzed_data_file='20230324_145848_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230324_144731_threshold_scan_interpreted.h5'
Sensor='618_30c'; analyzed_data_file='20230324_171010_noise_occupancy_scan_interpreted.h5'; thr_data_file='20230324_165756_threshold_scan_interpreted.h5'
#####################################

if not os.path.exists(Path+Sensor): os.makedirs(Path+Sensor)

####### THR PART  ###################
FIT=True; Voltage_1='120V'; el_conv=10.4; Noise_MAX=25*el_conv; Thr_MAX=400*el_conv 
# Load Thr data
with tb.open_file('data/'+thr_data_file, 'r') as infile:
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
print('##############################################################\n THR SCAN\n##############################################################')
print('Masked before: '+str(np.where(New_Failed_Map==0)[0].size))
print('New failed fits: '+str(np.where(New_Failed_Map==1)[0].size))
print('Errors: '+str(np.where(New_Failed_Map==2)[0].size))
print('Good: '+str(np.where(New_Failed_Map==3)[0].size))
print('Check: (must be 0) '+str(400*192-(np.where(New_Failed_Map==3)[0].size+np.where(New_Failed_Map==2)[0].size+np.where(New_Failed_Map==1)[0].size+np.where(New_Failed_Map==0)[0].size)))

# GAUSS FIT ##########################################
def gaus(X,A,X_mean,sigma): return A*np.exp(-(X-X_mean)**2/(2*sigma**2))
def GAUSS_FIT(x_hist,y_hist,color):
    mean = sum(x_hist*y_hist)/sum(y_hist)               
    sigma = sum(y_hist*(x_hist-mean)**2)/sum(y_hist)
    #Gaussian least-square fitting process
    param_optimised,param_covariance_matrix = curve_fit(gaus,x_hist,y_hist,p0=[1,mean,sigma])#,maxfev=5000)
    x_hist_2=np.linspace(np.min(x_hist),np.max(x_hist),500)
    plt.plot(x_hist_2,gaus(x_hist_2,*param_optimised),color,label='FIT: $\mu$ = '+str(round(param_optimised[1],1))+' e$^-$ $\sigma$ = '+str(abs(round(param_optimised[2],1)))+' e$^-$')

######################################################

#### NOISE: #####################
Noise_S=NoiseMap[:,0:127].flatten()*el_conv; Noise_L=NoiseMap[:,128:263].flatten()*el_conv; Noise_D=NoiseMap[:,264:399].flatten()*el_conv
Legend=['SYNCH','LIN','DIFF']; step=0.1*el_conv
#################################

# Map
fig1 = plt.figure()
#plt.rcParams.update({'font.size': 16})
ax = fig1.add_subplot(111)
imgplot = ax.imshow(NoiseMap*el_conv, vmax=Noise_MAX-10*el_conv) #150vmax
bar1=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
fig1.savefig(Path+Sensor+'/'+Voltage_1+'_Noise_Map.png', format='png', dpi=300)

#Histogram
fig2 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
ax = fig2.add_subplot(111)
h_S=plt.hist(Noise_S,color='red',bins = np.arange(0,Noise_MAX,step),label=Legend[0],histtype='step')
if FIT: GAUSS_FIT(h_S[1][:-1],h_S[0],'r')
h_D=plt.hist(Noise_D,color='blue',bins = np.arange(0,Noise_MAX,step),label=Legend[2],histtype='step')
if FIT: GAUSS_FIT(h_D[1][:-1],h_D[0],'blue')
h_L=plt.hist(Noise_L,color='green',bins = np.arange(0,Noise_MAX,step),label=Legend[1],histtype='step')
if FIT: GAUSS_FIT(h_L[1][:-1],h_L[0],'green')
ax.set_ylim([0.1, 3000])
ax.set_yscale('log')
ax.set_xlabel('electrons')
ax.set_ylabel('entries')
ax.legend(prop={'size': 14}, loc='upper right')
fig2.savefig(Path+Sensor+'/'+Voltage_1+'_Noise_Hist.png', format='png', dpi=300)

#### THRESHOLDS: #####################
Thr_S=ThrMap[:,0:127].flatten()*el_conv+180; Thr_L=ThrMap[:,128:263].flatten()*el_conv+180; Thr_D=ThrMap[:,264:399].flatten()*el_conv+180
Legend=['SYNCH','LIN','DIFF']; step=5*el_conv; YMAX=100000
#################################

# Map
fig3 = plt.figure()
#plt.rcParams.update({'font.size': 16})
ax = fig3.add_subplot(111)
imgplot = ax.imshow(ThrMap*el_conv+180, vmax=Thr_MAX-10*el_conv, vmin=1200) #3500 vmax
bar2=plt.colorbar(imgplot, orientation='horizontal', extend='max', label='electrons')
fig3.savefig(Path+Sensor+'/'+Voltage_1+'_Threshold_Map.png', format='png', dpi=300)

#Histogram
fig4 = plt.figure(figsize=(1050/96, 750/96), dpi=96)
ax = fig4.add_subplot(111)
h_S=plt.hist(Thr_S,color='red',bins = np.arange(0,Thr_MAX,step),label=Legend[0],histtype='step')
if FIT: GAUSS_FIT(h_S[1][:-1],h_S[0],'r')
h_D=plt.hist(Thr_D,color='blue',bins = np.arange(0,Thr_MAX,step),label=Legend[2],histtype='step')
if FIT: GAUSS_FIT(h_D[1][15:-1],h_D[0][15:],'blue')
h_L=plt.hist(Thr_L,color='green',bins = np.arange(0,Thr_MAX,step),label=Legend[1],histtype='step')
if FIT: GAUSS_FIT(h_L[1][15:-1],h_L[0][15:],'green')
ax.set_ylim([0.1, YMAX])
ax.set_xlim([0, Thr_MAX])
ax.set_yscale('log')
ax.set_xlabel('electrons')
ax.set_ylabel('entries')
ax.legend(prop={'size': 14}, loc='upper left')
fig4.savefig(Path+Sensor+'/'+Voltage_1+'_Threshold_Hist.png', format='png', dpi=300)


####### X-RAY PART  #################
step=10 
with tb.open_file('data/'+analyzed_data_file, 'r') as infile:
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

print('##############################################################\n X-RAY SCAN\n##############################################################')
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
print('\n\n##############################################################\n FINAL RESULTS\n##############################################################')
print('# of masked by bdaq (enable mask): %i' % Disabled)
print('# of failed fits: '+str(Mask_Failed_check_where[0].size))
print('# of missing: '+str(Missing[0].size)+' ('+str(np.where(Mask_Failed_check==2)[0].size)+' failed fits)')
print('# of strange: '+str(Missing_strange[0].size)+' ('+str(np.where(Mask_Failed_check==4)[0].size)+' failed fits)')
print('##############################################################\n')

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
fig3.savefig(Path+Sensor+'/'+analyzed_data_file[0:-3]+'_Hist_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)

# MISSING BUMPS FINAL MAPS
fig , (ax1, ax2) = plt.subplots(1,2, figsize=(20, 6))
plt.rcParams.update({'font.size': 16})
fig.suptitle("Sensor "+Sensor+" -- Missing bumps: "+str(Missing[0].size)+" ("+str(Perc)+"%) ("+str(np.where(Mask_Failed_check==2)[0].size)+" failed fits) -- Masked pixels: "+str((400-128)*192-Enabled[0].size)+" -- Problematic bumps: "+str(Missing_strange[0].size)+" ("+str(Perc_strange)+"%) ("+str(np.where(Mask_Failed_check==4)[0].size)+" failed fits)")
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
fig.savefig(Path+Sensor+'/'+analyzed_data_file[0:-3]+'_Missing_Bumps_Thr_'+str(Thr)+'_'+str(Thr_strange)+'.png', format='png', dpi=300)

