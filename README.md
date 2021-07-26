# TrackerDAQ
Software for tracker DAQ seutp.

## Instructions
First turn on FC7.
Check for communication:
```
ping fc7
```

Turn on SCC power supply.
Use 1.8 V for LDO power mode.
Connect power to SCC.

```
cd /home/kucms/TrackerDAQ/development/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT.xml -l
fpgaconfig -c CMSIT.xml -i IT-L12-CERN-L8-DIO5_1G28_v4p1
CMSITminiDAQ -f CMSIT.xml -r
ping fc7
```

To run standard BERT:
```
CMSITminiDAQ -f CMSIT_BERT.xml -c bertest
```
You can modify the settings in CMSIT_BERT.xml.

To run BERT scan, use BERT_Scan.sh and provide the TAP0 setting [0, 1000] as the first argument.
Note that communication fails for low values... e.g. TAP0 less than 10.
```
./TrackerDAQ/scripts/BERT_Scan.sh 100
```

