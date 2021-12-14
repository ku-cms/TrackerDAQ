# TrackerDAQ

Software for Tracker DAQ seutp used at the University of Kansas (KU).
Rock Chalk, Jayhawk!

## Setup

The standard Ph2_ACF software (with instructions) is here: [standard](https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF).
The development Ph2_ACF software (with instructions) is here: [dev](https://gitlab.cern.ch/cmsinnertracker/Ph2_ACF).
In order to use the "SER_SEL_OUT_[0-3]" settings for the RD53 chip, install the development Ph2_ACF software,
as this is not yet supported in the standard Ph2_ACF software.
To setup the FC7, see instructions [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/pc_connection/) and [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/setting_up_sd/).

## Usage

First turn on FC7.
Check for communication:
```
ping fc7 -c 3
```

Before powering on the SCC, set the DIP switches on the SCC for LDO power mode.
To power the Single Chip card (SCC), you need a power supply with two channels.
Before connecting the SCC, to use LDO power mode,
set both channels on the power supply to 1.8 V and 0.9 A as the current limit.

Here is the setup required every time to use the Ph2_ACF software and the FC7.
The current FC7 firmware version that we use is 4.1.
```
cd /home/kucms/TrackerDAQ/development/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT.xml -i IT-L12-CERN-L8-DIO5_1G28_v4p1
CMSITminiDAQ -f CMSIT.xml -r
ping fc7 -c 3
CMSITminiDAQ -f CMSIT.xml -p
```

Here are some additional fpgaconfig commands that are useful for the FC7.

Command to list avaiable FC7 firmware versions loaded on the SD card:
```
fpgaconfig -c CMSIT.xml -l
```
Command to load new FC7 firmware onto the SD card:
```
fpgaconfig -c <your_chosen_hardware_description_file.xml> -f <firmware_file_name_on_the_PC> -i <firmware_file_name_on_the_microSD>
```

To run the standard BERT program:
```
CMSITminiDAQ -f CMSIT.xml -c bertest
```

You can modify the settings in CMSIT.xml with a text editor.
The TAP0 DAC setting is called CML_TAP0_BIAS, and it ranges from 0 to 1023 as it is a 10 bit value.
Small/large TAP0 values correspond to low/high signal amplitudes.

All four output channels can each be set to different types of signals.
This is done using a 2 bit setting for SER_SEL_OUT_[0-3]:
```
0b00 = clock
0b01 = Aurora data
0b10 = PRBS 7
0b11 = grounded
```

Always set the "primary" channel SER_SEL_OUT_0 to Aurora data for read/write communication with the RD53 chip.
Otherwise, the initial communication with the RD53 chip for sending commands and settings will not work.
```
SER_SEL_OUT_0 = "0b01"
```
The "secondary" channels SER_SEL_OUT_[1-3] are not used for communication with the RD53 chip,
and they can be set to any of the four 2 bit settings (0b00 to 0b11).

The script BERT_Scan.sh handles the xml config file modification automatically.
To scan through TAP0 values, use BERT_Scan.py, which calls BERT_Scan.sh for different TAP0 values.
Provide the min TAP0 (-a), max TAP0 (-b), TAP0 step size (-c), secondary signal type (-d), and an output directory (-e).
For the secondary signal type, use decimal values 0-3, which correspond to binary values 0b00 to 0b11.
The python script handles the conversion from decimal to binary.
```
time python3 TrackerDAQ/python/BERT_Scan.py -a <min TAP0> -b <max TAP0> -c <step TAP0> -d <secondary signal type> -e <output directory>
```
This script will output the results to a unique file name in the specified directory.

There is a simple script to rsync data to your local machine if needed.
```
./scripts/getData.sh
```

To plot the data from the log file, use BERT_Analyze.py. 
This can create plots of single BERT scans and multiple BERT scans in the same plot.
```
python3 python/BERT_Analyze.py 
```

