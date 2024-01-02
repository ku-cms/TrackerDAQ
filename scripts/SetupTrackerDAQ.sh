#!/usr/bin/bash
# SetupTrackerDAQ.sh

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


