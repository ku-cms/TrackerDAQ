# TrackerDAQ
Software for tracker DAQ seutp.

## Instructions
First turn on FC7.
Check for communication:
```
ping fc7
```

Turn on SCC power supply.
Use 1.8 V for LDO power mode with 0.9 A as the current limit.
Connect power to SCC.
The current FC7 firmware version that we use is 4.1.

Here is the required setup for the Ph2_ACF software and the FC7:
```
cd /home/kucms/TrackerDAQ/development/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT.xml -i IT-L12-CERN-L8-DIO5_1G28_v4p1
CMSITminiDAQ -f CMSIT.xml -r
ping fc7
CMSITminiDAQ -f CMSIT.xml -p
```

Command to list avaiable FC7 firmware versions loaded on the SD card:
```
fpgaconfig -c CMSIT.xml -l
```
Command to load new FC7 firmware onto the SD card:
```
fpgaconfig -c <your_chosen_hardware_description_file.xml> -f <firmware_file_name_on_the_PC> -i <firmware_file_name_on_the_microSD>
```

To run standard BERT:
```
CMSITminiDAQ -f CMSIT_BERT.xml -c bertest
```
You can modify the settings in CMSIT_BERT.xml with a text editor.
The TAP0 DAC setting is called CML_TAP0_BIAS, and it ranges from 0 to 1000.

The script BERT_Scan.sh handles the xml modification automatically.
Provide the TAP0 setting [0, 1000] as the first argument.
Note that communication fails for low values... e.g. TAP0 = 0.
Provide a directory as the second argument.
The optional third argument is the output file name (defaults to out.log in the specified directory).
```
./TrackerDAQ/scripts/BERT_Scan.sh 500 BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink200
```

To scan through TAP0 values, use BERT_Scan.py, which calls BERT_Scan.sh for different TAP0 values.
Provide the min TAP0 (-a), max TAP0 (-b), TAP0 step size (-c), and an output directory (-d).
```
time python3 TrackerDAQ/python/BERT_Scan.py -a 50 -b 600 -c 10 -d BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink200
```
This script will output the results to a unique file name in the specified directory (e.g. BERT_TAP0_Scans/DoubleDP_DoubleBonn_DoubleYellow/elink200/scan_001.log).

There is a simple script to rsync data to your local machine if needed.
```
./scripts/getData.sh
```

To plot the data from the log file, use BERT_Analyze.py. 
This can create plots of single BERT scans and multiple BERT scans in the same plot.
```
python3 python/BERT_Analyze.py 
```

