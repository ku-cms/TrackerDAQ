# TrackerDAQ

Software for the Tracker DAQ setups used at the University of Kansas (KU)... Rock Chalk, Jayhawk!
There are instructions for using setups with Ph2_ACF, an FC7, CERN or KSU FMCs, a port card (optional),
RD53A or RD53B single chip cards (SCC), and an RD53A quad module.

# Using Ph2_ACF

The main Ph2_ACF software repository (with instructions) is [here](https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF).

## Installation:

First, follow the instructions in the "Setup on CentOs7" section here, including all required packages:
https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF

Commands to install Ph2_ACF:
```
cd <working_area>
git clone --recurse-submodules https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF.git
cd Ph2_ACF
source setup.sh
mkdir build
cd build
cmake3 ..
make -j8 
cd ..
```

Commands to checkout a new version (using a tag) and update the submodules (MessageUtils and NetworkUtils);
there can be compile errors if you do not update the submodules:
```
git checkout <tag_name>
git submodule sync
git submodule update --init --recursive --remote
```

Here are commands to compile Ph2_ACF (only needed when updating software).

Full recompile (from scratch):
```
source setup.sh
rm -rf build
mkdir build
cd build
cmake3 ..
make -j8
cd ..
```

Compile (only make):
```
source setup.sh
cd build
make -j8
cd ..
```

Setup a Ph2_ACF working area and copy the required files.
choose a directory name (using DAQSettings_v1 for this example):
```
mkdir -p DAQSettings_v1
cp settings/RD53Files/CMSIT*.txt DAQSettings_v1
cp settings/CMSIT*.xml DAQSettings_v1
cp settings/lpGBTFiles/CMSIT_LpGBT-v1.txt DAQSettings_v1
cd DAQSettings_v1
```

Edit the "connection" line in these files with your FC7 IP address (e.g. 192.168.1.100):
```
CMSIT_RD53A.xml
CMSIT_RD53B.xml
```

Example connection line for 192.168.1.100:
```
<connection id="nanocrate" uri="ipbusudp-2.0://192.168.1.100:50001" address_table="file://${PH2ACF_BASE_DIR}/settings/address_tables/CMSIT_address_table.xml" />
```

# Backup data

There is a script to backup Ph2_ACF working areas and e-link data to R drive.

These directories on kucms-01:
```
/home/kucms/TrackerDAQ
/data1/kucms/bump_bond
```
are backed up to this directory on the R drive:
```
/mnt/kucms/BEAN_GRP/e-links/kucms-01
```

Setup:

Initialize KU kerberos:
```
kinit <your-ku-id>
klist
```
Mount R drive:
```
mnt-bean
```

Run backup script:
```
time /home/kucms/TrackerDAQ/TrackerDAQ/scripts/backup.sh
```

Run backup script with nohup in the background; update the date and version:
```
nohup bash -c 'time /home/kucms/TrackerDAQ/TrackerDAQ/scripts/backup.sh' > /home/kucms/backup_logs/backup_1999_12_31_v1.log 2>&1 &
```

When you are done using the R drive:
```
umnt-bean
kdestroy -A
```

# Using FC7s

To setup the FC7, see instructions [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/pc_connection/) and [here](https://cms-tracker-daq.web.cern.ch/cms-tracker-daq/tutorials/setting_up_sd/).
There are also useful FC7 slides [here](https://indico.cern.ch/event/986962/sessions/388476/attachments/2200337/3726618/FC7_Setup.pdf).
The FC7 firmware of various flavors is [here](https://gitlab.cern.ch/cmstkph2-IT/d19c-firmware/-/releases).
You should use an FC7 firmware version that is compatible with the Ph2_ACF software version.
Also, use an FC7 version that matches your hardware setup: RD53A or RD53B, CERN or KSU FMC, electrical or optical readout, etc.

To use the FC7, first turn it on.

Check that FC7 communication is working:
```
ping fc7 -c 3
```

Here are useful commands for the FC7.
You will need run the Ph2_ACF setup script before using these commands (see RD53A/B setup below for details). 

Help menu:
```
fpgaconfig --help
```
Load FC7 firmware from SD card:
```
fpgaconfig -c <config_file.xml> -i <FW_File_SD>
```
Reset FC7 after loading firmware:
```
CMSITminiDAQ -f <config_file.xml> -r
```
List available FC7 firmware versions loaded on the SD card:
```
fpgaconfig -c CMSIT.xml -l
```
Load new FC7 firmware onto the SD card:
```
fpgaconfig -c <config_file.xml> -f <FW_File_PC> -i <FW_File_SD>
```
Delete FC7 firmware from SD card:
```
fpgaconfig  -c <config_file.xml> -d <FW_File_SD>
```

# Using RD53A chips 

## Documentation

The main Ph2_ACF software repository (with instructions) is [here](https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF).
Useful RD53A information can be found at these links:
- [4th Tracker Upgrade DAQ school](https://indico.cern.ch/event/986962/timetable/?view=standard)
- [Inner Tracker Excercise](https://indico.cern.ch/event/986962/sessions/388630/attachments/2202617/3726620/IT_Excercise.pdf)
- [RD53A Manual](https://cds.cern.ch/record/2287593/)
- [RD53A Twiki](https://twiki.cern.ch/twiki/bin/viewauth/RD53/RD53ATesting)

## Using RD53A chips 

First, turn on the FC7.
Check that FC7 communication is working:
```
ping fc7 -c 3
```

Before powering on the single chip card (SCC), set the DIP switches on the SCC for LDO power mode.
To power the Single Chip card (SCC), you need a power supply with two channels.
Before connecting the SCC, to use LDO power mode,
set both channels on the power supply to 1.8 V and 0.9 A as the current limit.

Here is the setup required every time to use the Ph2_ACF software and the FC7.
Note the different hardware and computers for each setup.

Latest setup (from 2023) for an RD53A SCC with electrical readout using a CERN FMC.
Commands should be run in a terminal on the linux computer kucms.
```
cd /home/kucms/TrackerDAQ/update/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT_RD53A.xml -i IT-L12-CERN-L8-DIO5_1G28_v4p6
CMSITminiDAQ -f CMSIT_RD53A.xml -r
ping fc7 -c 3
CMSITminiDAQ -f CMSIT_RD53A.xml -p
```

Setup for an RD53A quad module with electrical readout using a KSU FMC.
Commands should be run in a terminal on the linux computer kucms.
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF
source setup.sh
cd DAQSettings_v2
fpgaconfig -c CMSIT_RD53A_Electrical.xml -i IT-L12-KSU-RD53A_QUAD_v4p5
CMSITminiDAQ -f CMSIT_RD53A_Electrical.xml -r
ping fc7 -c 3
CMSITminiDAQ -f CMSIT_RD53A_Electrical.xml -p
```

To run the standard BERT program (use the correct xml file for your setup):
```
CMSITminiDAQ -f CMSIT_RD53A.xml -c bertest
```

To run the standard pixel alive program (use the correct xml file for your setup):
```
CMSITminiDAQ -f CMSIT_RD53A.xml -c pixelalive
```

### Running BERTs

First, run the standard BERT program (use the correct xml file for your setup):
```
CMSITminiDAQ -f CMSIT_RD53A.xml -c bertest
```
This is useful to check that the data link is working.
If the BERT runs successfully and there are 0 errors, then follow the procedure in the "Running BERT TAP0 Scans" section.

If if the link is not working or if there are more than 0 errors, make sure that all the FC7 setup commands were successful
and that all hardware connections are good (display port cables, e-link, and CERN FMC on the FC7).
Sometimes the CERN FMC sits on an angle and becomes disconnected from the FC7 due to torque from the display port cable.
In addition, turning the RD53 off and then on can fix link problems in some cases.

### Running BERT TAP0 Scans

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

To copy the data to your local computer, use this script:
```
./scripts/getData.sh
```

To copy the plots to your local computer, use this script:
```
./scripts/getPlots.sh
```

### Info about settings

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
For BERT TAP0 scans, the scripts handle the xml config file modifications automatically.

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

# Using RD53B chips 

## Documentation

The main Ph2_ACF software repository (with instructions) is [here](https://gitlab.cern.ch/cms_tk_ph2/Ph2_ACF).
Useful RD53B information can be found at these links:
- The instructions for setting up the RD53B chip (requires CERN account login) are at [CROC Testing User Guide](https://croc-testing-user-guide.docs.cern.ch).
- [RD53B Manual](http://cds.cern.ch/record/2665301)
- [RD53B Twiki](https://twiki.cern.ch/twiki/bin/viewauth/RD53/RD53BTesting)

## Using RD53B chips 

TODO: Finish updating port card instructions!

Latest setup (from 2023) for an RD53B SCC (CROCv1) with optical readout using an optical FMC and a port card.

Based on the port card slot (J2, J3, and J4) and the supported e-link types (1, 1K, 5, and 5K), you need to:
- Use the correct hardware connections: make sure that the VTRX+ and e-link are connected to the correct locations.
- Make sure that the e-link is connected with the correct orientation based on its type.
- Use the correct red adapter board or the correct SMA cable mapping with adapter boards.
- Use the correct xml configuration file for all commands.
- Change the softlink "CMSIT_RD53B_Optical_BERT.xml".
- Update "python/BERT_Scan.py" and "python/BERT_Simple_Analyze.py" for your setup; see below for more details.

Here is the syntax for changing the "CMSIT_RD53B_Optical_BERT.xml" softlink:
```
example
```
For example, if you want to set the softlink to point to the file X, the command would be:
```
example
```

After connecting the e-link, adapter boards, etc., you can power on the FC7, port card, and RD53B chip.

Check that communication is working between the linux computer kucms and the FC7:
```
ping fc7 -c 3
```

Then, these setup commands should be run in a terminal on kucms.
In this example, we are using port card slot 4 and a Type 5K e-link,
which is why we are using the xml configuration file "CMSIT_RD53B_Optical_Type5_J4.xml".
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF
source setup.sh
cd DAQSettings_v3
fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -r
ping fc7 -c 3
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
```

Useful CMSITminiDAQ programs:
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c bertest
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c pixelalive
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c noise
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c scurve
```

If you want to modify the TAP1 setting:
- 1
- 2
- 3

Before running the BERT TAP0 scan and analysis scripts, make sure to edit these files as needed for your configuration:
- python/BERT_Scan.py: set the default TAP0 range, the "output_dir", and the "bash_script" for your setup
- python/BERT_Simple_Analyze.py: set the "base_plot_dir", "base_data_dir", and "output_csv_name" for your setup

Here is the command to run BERT TAP0 scans:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
```

Use this script to analyze RD53B data for one e-link or all e-links.
```
# specific e-link
./TrackerDAQ/scripts/analyze_RD53B.sh 138
# all e-links
./TrackerDAQ/scripts/analyze_RD53B.sh
```

To copy the data to your local computer, use this script from this repository:
```
./scripts/getData.sh
```

To copy the plots to your local computer, use this script from this repository:
```
./scripts/getPlots.sh
```

