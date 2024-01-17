# Port Card BERT TAP0 Scan Instructions (2023)

For the port card BERT TAP0 scans, we use an RD53B SCC (CROCv1) with optical readout, an optical FMC, and a port card.
To test Type 5K e-links, there is a custom red adapter board (with jumpers) that is used to connect a display port (DP) cable on one side and the 15-pin paddle board of the e-link on the other side.

1. Connect a desired e-link between RD53B chip and port card! Make sure kucms desktop, power supplies, and FC7 are all on and running.

![Full readout chain](Full_Readoutchain_with_SMA_cables.jpg)

2. The top power supply must be set to 10.16 volts and .8 amps. The bottom power supply must be set too 1.6 volts and 2 amps (make sure you follow these paramaters to the upmost or else the hardware could be fried!) once verified press the synchronos on/off switch

Power Supply output off:

![Power Supply output off](Power_Supply_output_off.jpg)

 Power Supply output on:

![Power Supply output on](Power_Supply_output_on.jpg)

Power Supply Readout mode:

![Power Supply Readout mode](Power_Supply_Readoutmode.jpg)

3. If you want to run the scan to your laptop you must ssh into the desktop with this command: ssh -Y kucms@kucms-01.phsx.ku.edu (usefull to set up an alias to make this step faster  ‘kucms’)
to add an alias we need to locate .bashrc file (in home directory) open .bashrc file with text editor and add an alias to the bottom of it. the format is: alias kucms='ssh -Y kucms@kucms.phsx.ku.edu'
4. The firmware must be set up for the FC7 after each reboot. instructions in this read me will provide the set up for the firmware for the FC7 https://github.com/ku-cms/TrackerDAQ. Further explained below 
5. To check connectivity between the desktop and the FC7 use this command: ping fc7 -c 3
6. Run these commands in order. 
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF
```
 CD- "change directorty" PH2_ACF- "phase 2 ACF"
 changed directory to the phase 2 ACF 
 ```
 source setup.sh
 ```
 this runs the setup script for fc7 firmware and tap0 software, this gives us access to the following commands we are gong to run
 ```
 cd DAQSettings_v3
 ```
 changes directory to DAQ settings v3 

 ```
 fpgaconfig -c CMSIT_RD53B_Optical.xml -i IT-L8-OPTO_CROC_v4p5
 ```
 loads proper firmware for this setup into the FC7

 ```
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -r
```
Resets the FC7 and keeps the firmware loaded
```
ping fc7 -c 7
```
Checks the connectivity with the FC7
```
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -p
```

Pings the RD53B from the desktop and back. If works the hardware is running. If not something is wrong with the setup (-problem with power -problem with elink/optic link/SMA/display port connection
-problem with FC7).
 If successful, the output should look like this:

```
 Trying to shutdown Calibration DQM Server...
|02:59:26|I|Operation completed
|02:59:26|I|Trying to shutdown Monitor DQM Server...
|02:59:26|I|Operation completed
|02:59:26|I|>>> Interfaces  destroyed <<<
|02:59:26|I|@@@ End of CMSIT miniDAQ @@@
```
-Useful DAQ commands
```
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -c bertest
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -c pixelalive
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -c noise
CMSITminiDAQ -f CMSIT_RD53B_Optical.xml -c scurve
You are now ready to begin the TAP0 scans 
```

IMPORTANT NOTE: DigitalScan operates at a rapid pace and generates diverse plots. BERscanTest requires more time to complete. Employ DigitalScan for initiating communication with the RD53B chip. If you intend to conduct additional tests, refrain from interrupting BERscanTest midway. Halting BERscanTest results in the chip entering an abnormal state (possibly transmitting PRBS signals), rendering communication nonfunctional. To restore communication, a power cycle is necessary. DigitalScan effectively establishes communication with speed and efficiency.

7. It runs a bit error rate test (sending an amount of data for 10 seconds that give us the rate of errors per time) this bit error rate depeneds on mulitple parameters, one of thoese being the TAP0 setting. This setting sets the amplitude of the bits. 
The TAP0 scan is an expierment to determine how our bit error rate is realted to the TAP0 setting by looking at each TAP0 and the error rate that follows it to see at what TAP0 the bit error rate is zero.

The python files to run scans are located in this directory
```
 /home/kucms/TrackerDAQ/TrackerDAQ/python
 ```
 8. For a TAP0 scan, to modify the range(min,max) of the scan and the increments(steps) of the scan you must edit the  BERT_Scan.py file with vim. 
 ```
 v /home/kucms/TrackerDAQ/TrackerDAQ/python/BERT_Scan.py
 ```
 modify these lines to edit the TAP0 range an the TAP1
 ```
 11     tap0_min    = 100
 12     tap0_max    = 300
 13     tap0_step   = 10
 18     TAP1        = 200
 ```
 
9. In addition we need to modify the TAP1 setting in this xml file

 ```
v /home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v3/CMSIT_RD53B_Optical_BERT.xml
```

This is what needs to be modified
```
CML_CONFIG_SER_EN_TAP  =  "0b00"

CML_CONFIG_SER_INV_TAP =  "0b00"

DAC_CML_BIAS_0         =   "500"

DAC_CML_BIAS_1         =     "0"

DAC_CML_BIAS_2         =     "0"
```

- Don't change DAC_CML_BIAS_0 or DAC_CML_BIAS_2.

- DAC_CML_BIAS_1 should be changed to the desired TAP1 setting, for example "0" or "100".

- To use TAP1 = 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b00".

- To use TAP1 > 0, CML_CONFIG_SER_EN_TAP and CML_CONFIG_SER_INV_TAP should be set to "0b01".


10. Once ready to run TAP0 scan navigate too this directory:
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v3
```
inside here you can run the TAP0 scan with the following command:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
```

Analysis:

To recover the data in plot form we need to run these command 
```
# specific e-link
./TrackerDAQ/scripts/analyze_RD53B.sh 138
# all e-links
./TrackerDAQ/scripts/analyze_RD53B.sh
```
Here is an example on how to copy the plots to your computer 
```
cd /Users/priority/Documents/CMS

./getplots.sh
```
Heres how to show the plots 
```
show raw_plots_PortCard_RD53B/BERT_TAP0_Scans/Optical_FMC_PortCard_DP_SMA_Adapter/elink138_D0_SS0_TAP1_0/*.png
``` 
This shows all the plots in that files to show the directory we need to use this
```
ll raw_plots_PortCard_RD53B/BERT_TAP0_Scans/Optical_FMC_PortCard_DP_SMA_Adapter/
```
