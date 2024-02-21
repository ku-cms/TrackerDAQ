#!/usr/bin/bash
# SetupTrackerDAQ.sh

INSTALL_DIR=/home/kucms/TrackerDAQ/TrackerDAQ
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

echo " - Creating symbolic links in the target directory '$TARGET_DIR'"
echo "   that point to the install directory '$INSTALL_DIR'."

cd $TARGET_DIR/python
ln -s $INSTALL_DIR/python/BERT_Run_Scan.py .
ln -s $INSTALL_DIR/python/BERT_Simple_Analyze.py .
ln -s $INSTALL_DIR/python/analyze_occupancy.py .
cd ../..

cd $TARGET_DIR/scripts
ln -s $INSTALL_DIR/scripts/PortCard_BERT_Scan.sh .
ln -s $INSTALL_DIR/scripts/analyze_RD53B.sh .
cd ../..

cd $TARGET_DIR/macros
ln -s $INSTALL_DIR/macros/analyze_occupancy.C .
cd ../..
