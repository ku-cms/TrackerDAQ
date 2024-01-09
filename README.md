# TrackerDAQ

Software for the Tracker DAQ setups used at the University of Kansas (KU)... Rock Chalk, Jayhawk!
There are instructions for using setups with Ph2_ACF, an FC7, CERN, KSU, or optical FMCs, a port card (optional),
RD53A or RD53B single chip cards (SCC), an RD53A quad module, and an RD53B 1x2 CROC digital module.

TODO: Finish updating instructions for Type 5K e-links!
- Write down standard TAP0 scan ranges: [100, 1000, 100] and [50, 150]
- Improve instructions for adjusting TAP0 scan settings.
- Add instructions for changing TAP1 setting.

DONE:
- Update installation section, including soft link and xml setup. 
- Document adapter board jumper settings.
- Include port card and RD53B chip power settings.
- Move debugging errors to a new section.
- Add command to ssh to kucms.
- Add details on alias for ssh command.
- Add the Macbook terminal fix for LC_CTYPE and LC_ALL variables to the login section.

# Login

We are using Ph2_ACF and TrackerDAQ on the kucms linux machine in Malott 4078.
The hostname is "kucms.phsx.ku.edu", and we are using the user "kucms".
If you need to use the password and do not know it, please contact Caleb Smith (caleb.smith@ku.edu) or Alice Bean (abean@ku.edu).

You can either open a terminal on the kucms desktop, or you can login remotely with ssh.
If the kucms desktop is freezing when running the terminal and/or the file explorer, please restart the kucms linux machine and try again; this should (hopefully) fix these problems.
If you still encounter problems with the kucms desktop, please contact the KU Physics IT support with details about the problem (tsc_phsx@ku.edu).

Here is the ssh command to login to kucms:
```
ssh -Y kucms@kucms.phsx.ku.edu
```

For convenience, you can create an alias for this login command on your personal machine (if you are using Mac or Linux).
First, check which shell you are using by running these commands in a terminal on your personal machine.
```
echo $0
echo $SHELL
```
If you are using bash, you can add aliases to one of the bash startup configuration files (for example, ~/.bash_profile).
If you are using zsh, then you can add aliases to one of the zsh startup configuration files (for example, ~/.zprofile).

You can add this line to your shell configuration file:
```
alias kucms='ssh -Y kucms@kucms.phsx.ku.edu'
```

To apply changes to your current session, you need to source your configuration file.
This is not required for new terminal sessions, as those will load the new configuration on startup.

Example source command for bash:
```
source ~/.bash_profile
```
Example source command for zsh:
```
source ~/.zprofile
```
You can check that the new alias is available with these commands:
```
alias
alias kucms
```
Then, you can login using the new alias:
```
kucms
```
If you are using a Mac and encounter this error after logging into kucms with ssh:
```
Last failed login: Thu Jan  4 10:24:34 CST 2024 from 10.105.79.64 on ssh:notty
There was 1 failed login attempt since the last successful login.
Last login: Thu Jan  4 10:19:55 2024 from 10.105.79.64
perl: warning: Setting locale failed.
perl: warning: Please check that your locale settings:
	LANGUAGE = (unset),
	LC_ALL = (unset),
	LC_CTYPE = "UTF-8",
	LANG = "en_US.UTF-8"
    are supported and installed on your system.
perl: warning: Falling back to the standard locale ("C").
```
then you will need to fix this before using Ph2_ACF, as we discovered that the command to program the FC7 firmware will not work:
```
[kucms@kucms DAQSettings_v1]$ fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
04.01.2024 10:31:28: |140251851439552|I| Loading IT-L8-OPTO_CROC_v4p5 into the FPGA...
terminate called after throwing an instance of 'std::runtime_error'
  what():  Board with id 0 does not exist in file CMSIT_RD53B_Optical_Type5_J4.xml
Aborted (core dumped)
```

We found the solution here: https://stackoverflow.com/questions/2499794/how-to-fix-a-locale-setting-warning-from-perl

First, logout of kucms.

If you are using bash, add these lines to ~/.bash_profile on your machine:
```
# Setting for the new UTF-8 terminal support
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```
and then run this command on your machine:
```
source ~/.bash_profile
```

If you are using zsh, add these lines to ~/.zprofile on your machine:
```
# Setting for the new UTF-8 terminal support
LC_CTYPE=en_US.UTF-8
LC_ALL=en_US.UTF-8
```
and then run this command on your machine:
```
source ~/.zprofile
```

Check that these variables are now set to the values that you just specified:
```
echo $LC_CTYPE
echo $LC_ALL
```
Finally, login to kucms again and check that there are no errors.
```
kucms
```
You can then follow the setup instructions and confirm that the FC7 program and reset commands work.

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

Use this script to setup symbolic links for the TrackerDAQ framework;
this only needs to be run once to setup the working area.
The script will only create new soft links if there is no
TrackerDAQ directory in the current working area.
```
~/TrackerDAQ/TrackerDAQ/scripts/SetupTrackerDAQ.sh
```

Then, copy the xml config file that you need for this working area and create a soft link
that will be used by the TAP0 scan script.
For example, here are the commands to copy and create the soft link for the xml config file
for Type 5K e-links tested in port card slot J4.
```
cp ~/TrackerDAQ/TrackerDAQ/settings/CMSIT_RD53B_Optical_Type5_J4.xml .
ln -s CMSIT_RD53B_Optical_Type5_J4.xml CMSIT_RD53B_Optical_BERT.xml
```

If you are setting up new xml files from scratch,
edit the "connection" line in these files with your FC7 IP address (e.g. 192.168.1.100):
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

Check that FC7 communication is working (run on the kucms linux machine):
```
ping fc7 -c 3
```

Here are useful commands for the FC7; these should be run run on the kucms linux machine.
You will need run the Ph2_ACF setup script before using these commands (see RD53A/B setup below for details). 

Help menu:
```
fpgaconfig --help
```
Load FC7 firmware from SD card:
```
fpgaconfig -c <xml_config_file> -i <FW_File_SD>
```
Reset FC7 after loading firmware:
```
CMSITminiDAQ -f <xml_config_file> -r
```
List available FC7 firmware versions loaded on the SD card:
```
fpgaconfig -c <xml_config_file> -l
```
Load new FC7 firmware onto the SD card:
```
fpgaconfig -c <xml_config_file> -f <FW_File_PC> -i <FW_File_SD>
```
Delete FC7 firmware from SD card:
```
fpgaconfig  -c <xml_config_file> -d <FW_File_SD>
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

Commands should be run on the kucms linux machine.

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

A display port (DP) cable should be connected between the RD53B chip (use the DP1 port) and the red adapter board.
For Type 5K e-links tested with the port card, we are using the
"TBPIX 15 to Display Port Rev A" board that was developed in 2023.
This adapter board has two jumpers for every channel (ten jumpers in total).
We are using e-link channels CMD and D3.

Here are the standard jumper settings on the red adapter board used for Type 5K e-links:
- CMD: P -> N, N -> P
- D3:  P -> N, N -> P

Refer to the diagram on the red adapter board, and make sure that CMD and D3 both have two jumpers
matching these standard jumper settings.
Make sure that the jumpers are fully inserted.
The BERT TAP0 scans have shown problems (large error rates that do not converge to 0 errors)
when the jumpers have poor connection.

Finally, insert the Type 5K e-link that will be tested.
The 15-pin paddle board on the e-link should connect to the red adapter board
with the notch on the left (matching the white dot) and the leads facing up.
The 45-pin paddle board on the e-link should connect to the port card slot J4
with the notch on the left (towards the gray DC-DC converter) and the leads away from the black bail.
The VTRX+ on the bottom of the port card should be in slot Z3.

### Power Settings

After checking the jumper configuration/connection and the e-link connection/configuration, you can power on the FC7, port card, and RD53B chip.
There are also fans used to cool the port card and RD53B chip that should be used to prevent overheating.

We are powering the port card in constant voltage mode.
We put the power cables on one power suppy output channel (on the left side of the power supply),
with the white cable on positive and the black cable on negative.

For the port card, we are using constant voltage mode with these settings:
- Voltage limit: 10.16 V - should measure about 10.17 V when output is on.
- Current limit:  0.80 A - should measure about  0.16 A when output is on.

We are powering the RD53B chip in LDO mode with a constant voltage.
We put the power cables on two power supply output channels (two pairs of red and black cables)
with the red cables on positive ouputs and the black cables on negative outputs.

For the RD53B chip, we are using constant voltage mode with these settings on two output channels:
- Voltage limit: 1.60 V - should measure about 1.60 V when output is on.
- Current limit: 2.00 A - should measure about 0.76 A (left) and 0.40 A (right) when output is on and about 0.94 A (left) and 0.81 (right) after establishing communication.

### BERT TAP0 scans (with optical readout using the port card)

Commands should be run on the kucms linux machine.

Latest setup (from 2024) for an RD53B SCC (CROCv1) with optical readout using an optical FMC and a port card.

Based on the port card slot (J2, J3, and J4) and the supported e-link types (1, 1K, 5, and 5K), you need to:
- Use the correct hardware connections: make sure that the VTRX+ and e-link are connected to the correct locations.
- Make sure that the e-link is connected with the correct orientation based on its type.
- Use the correct red adapter board or the correct SMA cable mapping with adapter boards.
- Use the correct xml configuration file for all commands.
- Change the softlink "CMSIT_RD53B_Optical_BERT.xml".
- Update "BERT_Scan.py" and "BERT_Simple_Analyze.py" for your setup; see below for more details.

Check that communication is working between the linux computer kucms and the FC7:
```
ping fc7 -c 3
```

Then, these setup commands should be run in a terminal on kucms.
In this example, we are using port card slot 4 and a Type 5K e-link,
which is why we are using the xml configuration file "CMSIT_RD53B_Optical_Type5_J4.xml".
Make sure that the FC7 is powered on before running these commands.
```
cd /home/kucms/TrackerDAQ/elink_testing_v1/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -r
ping fc7 -c 3
```

Then, you should run these commands to establish communication with the RD53B chip.
The port card and RD53B chip need to be powered on before running these commands.
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c bertest
```

Here are other useful CMSITminiDAQ programs for reference:
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c bertest
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c pixelalive
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c noise
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -c scurve
```

Before running the BERT TAP0 scan and analysis scripts, make sure to edit these files as needed for your configuration:
- These files should be edited from the directory "/home/kucms/TrackerDAQ/TrackerDAQ/python", which is where this repository is installed.
- There are softlinks to these files in the working areas, for example in "/home/kucms/TrackerDAQ/elink_testing_v1/Ph2_ACF/DAQSettings_v1/TrackerDAQ/python".
- BERT_Scan.py: set the default TAP0 range, the "output_dir", and the "bash_script" for your setup.
- BERT_Simple_Analyze.py: set the "base_plot_dir", "base_data_dir", and "output_csv_name" for your setup.

Here is the command to run BERT TAP0 scans:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
```

Use this script to analyze RD53B data for one e-link (specify which e-link number) or all e-links.
```
# specific e-link (specify e-link number)
./TrackerDAQ/scripts/analyze_RD53B.sh <elink_number>
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

### Debugging Errors

If you see lpGBT errors like this for "CMSITminiDAQ" commands:
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
...
|11:22:00|I|Initializing communication to Low-power Gigabit Transceiver (LpGBT): 0
|11:22:00|I|    --> Configured up and down link mapping in firmware
|11:22:00|I|LpGBT version: LpGBT-v1
|11:22:01|E|LpGBT PUSM status: ARESET
|11:22:01|E|>>> LpGBT chip not configured, reached maximum number of attempts (10) <<<
```
then you should reprogram and reset the FC7 with these commands, which usually fixes the issue:
```
fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -r
```
If you still have communication problems, then you can turn off the RD53B and the port card,
reprogram and reset the FC7, and then turn the RD53B chip and port card on.
Then, you can repeat the "CMSITminiDAQ" command to re-establish communication:  
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
```

Similary, if you see lpGBT errors like this when running the BERT_Run_Scan.py python script:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
...
Running BERT with TAP0=200
Running BERT with TAP0=210
terminate called after throwing an instance of 'Exception'
  what():  [RD53lpGBTInterface::WriteReg] LpGBT register writing issue
  ./TrackerDAQ/scripts/PortCard_BERT_Scan.sh: line 54: 25469 Aborted                 (core dumped) CMSITminiDAQ -f CMSIT_RD53B_Optical_BERT_Custom.xml -c bertest > "$dataDir/scan.log"
```
then you should reprogram and reset the FC7 with these commands, which usually fixes the issue:
```
fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -r
```
Then, you should re-establish communication with these commands before continuing:
```
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -p
```

## Digital module (RD53B 1x2 CROC digital module)

### Power Settings

We are powering the port card in constant voltage mode.
We put the power cables on one power suppy output channel (on the left side of the power supply),
with the white cable on positive and the black cable on negative.

For the port card, we are using constant voltage mode with these settings:
- Voltage limit: 10.16 V - should measure about 10.17 V when output is on.
- Current limit:  0.80 A - should measure about  0.15 A when output is on.

We are powering the digital module in constant current mode.
We put both power cables on one power supply output channel (on the right side of the power supply),
with both red cables on positive and both black cables on negative.

For the digital module, we are using constant current mode with these settings:
- Current limit: 3.80 A - should measure about 3.80 A when output is on.
- Voltage limit: 1.70 V - should measure about 1.63 V when output is on.

### Electrical readout

For electrical readout of the RD53B 1x2 CROC digital module,
we are using the KSU FMC in slot L12 of the FC7 (the slot on the right).
The digital module should connect to the KSU FMC (in the upper left port) using a mini-DP cable.

We are using Ph2_ACF tag v4-13,
and we are using FC7 firmware v4.6 for KSU (L12) electrical readout for CROCv1 QUAD modules.

Setup:
```
cd /home/kucms/TrackerDAQ/croc/Ph2_ACF
source setup.sh
cd DAQSettings_v3
fpgaconfig -c CMSIT_RD53B_Digital_Module_Electrical.xml -i IT-L12-KSU-CROC_QUAD_v4p6
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Electrical.xml -r
ping fc7 -c 3
```

Run tests:
```
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Electrical.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Electrical.xml -c bertest
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Electrical.xml -c pixelalive
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Electrical.xml -c scurve
```

### Optical readout

For optical readout of the RD53B 1x2 CROC digital module,
we are using the optical FMC in slot L8 of the FC7 (the slot on the left).
The port card should connect to the optical FMC using an optical fiber;
the optical fiber channels 6 and 7 should be connected to the leftmost position of the bottom row of the optical FMC.
We are using a "TFPX H1x2 K" e-link (e-link 520),
with the 15-pin connector P1 installed on the digital module
and the 45-pin connector installed on port card slot J4.

Here are the software and firmware versions that we are using (as of December 14, 2023).
For Ph2_ACF, we are using the Ph2_ACF tag v4-18.
We are using FC7 firmware v4.8 for optical readout (L8), quad module, and CROCv1.   
Note that we are using a dedicated working area for modules in kucms at this path:
```
/home/kucms/TrackerDAQ/modules/Ph2_ACF
```

RD53B digital module optical readout:

Setup:
```
cd /home/kucms/TrackerDAQ/modules/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT_RD53B_Digital_Module_Optical_J4.xml -i IT-L8-OPTO-CROC_QUAD_v4p8
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -r
ping fc7 -c 3
```

Run tests:
```
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -p
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -c bertest
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -c pixelalive
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -c scurve
```

To resolve the "LpGBT PUSM status: ARESET" error, reprogram and reset the FC7 using these commands:
```
fpgaconfig -c CMSIT_RD53B_Digital_Module_Optical_J4.xml -i IT-L8-OPTO-CROC_QUAD_v4p8
CMSITminiDAQ -f CMSIT_RD53B_Digital_Module_Optical_J4.xml -r
```

Here is the command to run BERT TAP0 scans:
```
python3 TrackerDAQ/python/BERT_Run_Scan.py
```

Use this script to analyze RD53B data for one e-link or all e-links.
```
# specific e-link
./TrackerDAQ/scripts/analyze_RD53B.sh 520
# all e-links
./TrackerDAQ/scripts/analyze_RD53B.sh
```


