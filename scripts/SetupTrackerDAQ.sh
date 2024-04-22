#!/usr/bin/bash
# SetupTrackerDAQ.sh

#
# Run this script to setup the TrackerDAQ framework in your Ph2_ACF working area.
# - This script should be run from your DAQ settings directory (e.g. DAQSettings_v1).
# - This script will create softlinks in your working area to scripts in the TrackerDAQ repository.
# - This script will copy Ph2_ACF xml config files from the TrackerDAQ repository.
# - This script only needs to be run once to setup the working area.
#
# Command to run this script:
# ~/TrackerDAQ/TrackerDAQ/scripts/SetupTrackerDAQ.sh
#

INSTALL_DIR=/home/kucms/TrackerDAQ/TrackerDAQ
XML_DIR=settings/Ph2_ACF_v4_22
TARGET_DIR=TrackerDAQ

# Check if the install directory exists; if it does not, exit.
if [ ! -d "$INSTALL_DIR" ]
then
    echo " - The install directory '$INSTALL_DIR' does not exist"
    echo " - Please install TrackerDAQ and/or modify the installation path in this script."
    exit 1
fi

# Check if the target directory already exists; if it does, exit.
if [ -d "$TARGET_DIR" ]
then
    echo " - The target directory '$TARGET_DIR' already exists."
    echo " - If you want to rerun setup, please remove the directory '$TARGET_DIR' first."
    exit 1
fi

echo " - Creating the target directory '$TARGET_DIR' and subdirectories."

mkdir $TARGET_DIR
mkdir $TARGET_DIR/python
mkdir $TARGET_DIR/scripts
mkdir $TARGET_DIR/macros

# Create softlinks
echo " - Creating symbolic links in the target directory '$TARGET_DIR'"
echo "   that point to the install directory '$INSTALL_DIR'."

# Create softlinks for python scripts
cd $TARGET_DIR/python
ln -s $INSTALL_DIR/python/BERT_Run_Scan.py .
ln -s $INSTALL_DIR/python/BERT_Simple_Analyze.py .
ln -s $INSTALL_DIR/python/analyze_occupancy.py .
cd ../..

# Create softlinks for bash scripts
cd $TARGET_DIR/scripts
ln -s $INSTALL_DIR/scripts/PortCard_BERT_Scan.sh .
ln -s $INSTALL_DIR/scripts/analyze_RD53B.sh .
cd ../..

# Create softlinks for ROOT macros
cd $TARGET_DIR/macros
ln -s $INSTALL_DIR/macros/analyze_occupancy.C .
cd ../..

# Copy Ph2_ACF xml config files
echo " - Copying Ph2_ACF xml config files from '$INSTALL_DIR/$XML_DIR'."
cp $INSTALL_DIR/$XML_DIR/*.xml .

echo "TrackerDAQ setup is complete!"
