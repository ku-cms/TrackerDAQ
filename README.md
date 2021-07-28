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

The script BERT_Scan.sh handles the xml modification automatically.
Provide the TAP0 setting [0, 1000] as the first argument.
Note that communication fails for low values... e.g. TAP0 = 0.
```
./TrackerDAQ/scripts/BERT_Scan.sh 100
```

To scan through TAP0 values, use BERT_Scan.py, which calls BERT_Scan.sh for different TAP0 values.
```
python3 TrackerDAQ/python/BERT_Scan.py
```

