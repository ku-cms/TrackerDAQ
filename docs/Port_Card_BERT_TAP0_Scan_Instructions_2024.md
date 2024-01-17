# Port Card BERT TAP0 Scan Instructions (2024)

## Login

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

## Port Card BERT TAP0 Scans for Type 5K e-links

For the port card BERT TAP0 scans, we use an RD53B SCC (CROCv1) with optical readout, an optical FMC, and a port card.
To test Type 5K e-links, there is a custom red adapter board (with jumpers) that is used to connect a display port (DP) cable on one side and the 15-pin paddle board of the e-link on the other side.

Check that communication is working between the linux computer kucms and the FC7:
```
ping fc7 -c 3
```

Then, these setup commands should be run in a terminal on kucms.
In this example, we are using port card slot 4 and a Type 5K e-link, which is why we are using the xml configuration file "CMSIT_RD53B_Optical_Type5_J4.xml".
Make sure that the FC7 is powered on before running these commands.
These setup commands only need to be run once after powering on the FC7.
```
cd /home/kucms/TrackerDAQ/elink_testing_v1/Ph2_ACF
source setup.sh
cd DAQSettings_v1
fpgaconfig -c CMSIT_RD53B_Optical_Type5_J4.xml -i IT-L8-OPTO_CROC_v4p5
CMSITminiDAQ -f CMSIT_RD53B_Optical_Type5_J4.xml -r
ping fc7 -c 3
```

Then, you should run these commands to establish communication with the RD53B chip.
These two commands should be run for every e-link after the RD53B is powered on and before running a BERT TAP0 scan.
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

Next, make sure to edit the necessary files for your configuration before running a BERT TAP0 scan.

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

## TODO
- Add pictures of Type 5K e-link setup.
- Document jumper settings.
- Document power settings.
- Add links to TrackerDAQ and Ph2_ACF repositories.
- Document terminals: two on kucms (login and edit), and one locally (copy)

## DONE
- Document setup commands.
