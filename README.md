# TrackerDAQ

Software for Tracker DAQ seutp used at the University of Kansas (KU).
Rock Chalk, Jayhawk!
There are instructions for both RD53A and RD53B single chip cards (SCC). 

# RD53A

## Teststand Setup Information

The standard Ph2_ACF software (with instructions) is here: [standard](https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF).
The development Ph2_ACF software (with instructions) is here: [dev](https://gitlab.cern.ch/cmsinnertracker/Ph2_ACF).
In order to use the "SER_SEL_OUT_[0-3]" settings for the RD53 chip, install the development Ph2_ACF software,
as this is not yet supported in the standard Ph2_ACF software.
To setup the FC7, see instructions [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/pc_connection/) and [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/setting_up_sd/).

## Using the FC7

First turn on FC7.
Check for communication:
```
ping fc7 -c 3
```

Before powering on the single chip card (SCC), set the DIP switches on the SCC for LDO power mode.
To power the Single Chip card (SCC), you need a power supply with two channels.
Before connecting the SCC, to use LDO power mode,
set both channels on the power supply to 1.8 V and 0.9 A as the current limit.

Here is the setup required every time to use the Ph2_ACF software and the FC7.
The current FC7 firmware version that we use is 4.1.
```
cd /home/kucms/TrackerDAQ/update/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT.xml -i IT-L12-CERN-L8-DIO5_1G28_v4p1
CMSITminiDAQ -f CMSIT.xml -r
ping fc7 -c 3
CMSITminiDAQ -f CMSIT.xml -p
```
To run the standard BERT program:
```
CMSITminiDAQ -f CMSIT.xml -c bertest
```

Here are some additional fpgaconfig commands that are useful for the FC7.

Command to list available FC7 firmware versions loaded on the SD card:
```
fpgaconfig -c CMSIT.xml -l
```
Command to load new FC7 firmware onto the SD card:
```
fpgaconfig -c <your_chosen_hardware_description_file.xml> -f <firmware_file_name_on_the_PC> -i <firmware_file_name_on_the_microSD>
```

## Running BERTs

First, run the standard BERT program:
```
CMSITminiDAQ -f CMSIT.xml -c bertest
```
This is useful to check that the data link is working.
If the BERT runs successfully and there are 0 errors, then follow the procedure in the "New Method" section.

If if the link is not working or if there are more than 0 errors, make sure that all the FC7 setup commands were successful
and that all hardware connections are good (display port cables, e-link, and CERN FMC on the FC7).
Sometimes the CERN FMC sits on an angle and becomes disconnected from the FC7 due to torque from the display port cable.
In addition, turning the RD53 off and then on can fix link problems in some cases.

### New Method

The new method starts now. Get excited, y'all!

First, connect one e-link and two display port cables to the red adapter board,
and connect the display port cables to the FC7 and SCC.
If not already done, power on the FC7 and SCC and run the FC7 setup commands.
Once these are done, you are ready to take data!

First, if you are not already there, go to the "DAQSettings_v1" directory in a terminal (the same directory used for the FC7 setup).
Make sure you have already done the FC7 setup and run the required `source setup.sh` script to setup your working environment.
From the "DAQSettings_v1" directory, run this python script using python3:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
```
Then answer the prompts. In general, you can use the default inputs (enter 'y' when asked) and only provide the cable number
(this must be an integer).
If other inputs are required, you can enter 'n' and then specify each input.

Once the scan is finished, you can analyze the data.
To analyze the data for a specific cable, run this script from the "DAQSettings_v1" directory
and provide the cable number as the first argument (this must be an integer).
```
./TrackerDAQ/scripts/analyze.sh <cable number>
```
This script copies the data to the "data" directory (yes, it's a fancy name)
and then runs a python script to create plots of all scans for that cable.
The plots are stored in... yes, you guessed it... the "plots" directory.

NOTE: The script also prints out the result for one of the scans found in the directory,
but currently this is a random scan based on the order of matching files for that cable number.
This should be updated to be the latest scan (or min, max of all scans, etc.).

To analyze the data for all cables, run this script from the "DAQSettings_v1" directory without providing any arguments.
```
./TrackerDAQ/scripts/analyze.sh
```
In this mode, the script makes plots of all scans for all cables
and then saves the results in a table (csv file) in the "output" directory.

### Old Method

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
```
time python3 TrackerDAQ/python/BERT_Scan.py -a <min TAP0> -b <max TAP0> -c <step TAP0> -d <secondary signal type> -e <output directory>
```

For standard e-link testing, use a min TAP0 of 100, a max TAP0 of 200, and a TAP0 step size of 10.
For the secondary signal type, use 0 for clock.
For the output directory, follow this format (example for e-link 100, secondary signal 0): "BERT_TAP0_Scans/DoubleDP_DPAdapter/elink100_SS0".

To test different secondary signals (e.g. for cross talk studies), use decimal values 0-3, which correspond to binary values 0b00 to 0b11.
The python script handles the conversion from decimal to binary.
This script will output the results to a unique file name in the specified directory.

There is a simple script to rsync data to your local machine if needed:
```
./scripts/getData.sh
```

To plot the data from the log file, use BERT_Analyze.py. 
This can create plots of single BERT scans and multiple BERT scans in the same plot.
```
python3 python/BERT_Analyze.py 
```

# RD53B 

## Documentation

These links require a CERN login! 
Instructions for setting up the RD53B chip: [CROC Testing User Guide](https://croc-testing-user-guide.docs.cern.ch)
Main code repository (use RD53 branch): [Ph2_ACF for RD53B](https://gitlab.cern.ch/alpapado/Ph2_ACF)
Custom KU version of repository (use RD53B_KU_DEV branch): [Custom Ph2_ACF for RD53B](https://gitlab.cern.ch/caleb/Ph2_ACF/-/tree/RD53B_KU_DEV)

Check FC7 communication
```
ping fc7 -c 3
```

Setup commands for RD53B CROC
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CROC.xml -i IT-L12-KSU-L8-DIO5_CROC_v4p4
RD53BminiDAQ -f CROC.xml -r
ping fc7 -c 3
RD53BminiDAQ -f CROC.xml -t RD53BTools.toml DigitalScan
```

**Important note:**
DigitalScan runs quickly and creates various plots. BERscanTest takes longer.
Use DigitalScan to initialize communication with the RD53B chip.
For BERscanTest, do not stop in the middle of the test if you want to run more tests.
Stopping BERscanTest leaves the chip in a strange state (likely sending PRBS signals) where communication no longer works,
and a power cycle is required to restore communication.
DigitalScan works well for quickly establishing communication.

Digital Scan
```
RD53BminiDAQ -f CROC.xml -t RD53BTools.toml DigitalScan
```

Basic BERT TAP0 Scans
```
RD53BminiDAQ -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_50_250 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_200_400 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_350_550 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_500_700 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_650_850 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
RD53BminiDAQ_TAP0_800_1000 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest
```

BERT TAP0 Scan script examples:
```
# Single DP cable
./TrackerDAQ/scripts/RD53B_BERT_Scan.sh BERT_TAP0_Scans/SingleDP/no_elink_0 BERT_TAP0_Scans/SingleDP/no_elink_0/scan_001.log
# e-link with two DP cables and adapter board
./TrackerDAQ/scripts/RD53B_BERT_Scan.sh BERT_TAP0_Scans/DoubleDP_DPAdapter/elink_137 BERT_TAP0_Scans/DoubleDP_DPAdapter/elink_137/scan_001.log
```

Analyze data:
```
# specific e-link
./TrackerDAQ/scripts/analyze_RD53B.sh 137
# all e-links
./TrackerDAQ/scripts/analyze_RD53B.sh
```

Programs: see RD53BTools.toml for available programs (e.g. BERscanTest)

List FC7 firmware versions loaded on SD card
```
fpgaconfig -c CROC.xml -l
```

Load new FC7 firmware onto the SD card
```
fpgaconfig -c <your_chosen_hardware_description_file.xml> -f <firmware_file_name_on_the_PC> -i <firmware_file_name_on_the_microSD>
```

Example
```
fpgaconfig -c CROC.xml -f IT-uDTC_L12-KSU-4xSCC_L8-DIO5_ELECTRICAL_CROC.bit -i IT-L12-KSU-L8-DIO5_CROC_v4p4
```

File defining RD53B BERT scan program: tools/RD53B/RD53BBERTscan.h.

Compiling Ph2_ACF

Full recompile
```
rm -rf build
mkdir build
cd build
cmake ..
make -j8
cd ..
```

Compile (only make)
```
cd build
make -j8
cd ..
```

