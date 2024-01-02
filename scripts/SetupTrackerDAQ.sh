#!/usr/bin/bash
# SetupTrackerDAQ.sh

INSTALL_DIR=/home/kucms/TrackerDAQ/TrackerDAQ
TARGET_DIR=TrackerDAQ

# Check if the directory already exists; if it does, exit.

if [ -d $TARGET_DIR ]
then
    echo "The directory '$TARGET_DIR' already exists."
    echo "If you want to rerun setup, please remove the directory '$TARGET_DIR' first."
    exit 1
fi

echo "Creating the directory '$TARGET_DIR' and subdirectories."

mkdir $TARGET_DIR
mkdir $TARGET_DIR/python
mkdir $TARGET_DIR/scripts

echo "Creating symbolic links."

cd $TARGET_DIR/python
ln -s $INSTALL_DIR/python/BERT_Run_Scan.py .
ln -s $INSTALL_DIR/python/BERT_Simple_Analyze.py .
cd ../..

cd $TARGET_DIR/scripts
ln -s $INSTALL_DIR/scripts/PortCard_BERT_Scan.sh .
ln -s $INSTALL_DIR/scripts/analyze_RD53B.sh .
cd ../..


