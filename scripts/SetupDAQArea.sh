#!/usr/bin/bash
# SetupDAQArea.sh

# Run this script to set up a DAQ working area. 
# - This script should be run from a Ph2_ACF directory.
# - Provide the name of the new DAQ settings directory (e.g. DAQSettings_v1).
# - This script will create the new DAQ settings directory and copy the Ph2_ACF settings files.

# Example command:
# SetupDAQArea.sh DAQSettings_v1

DAQ_DIR=$1

# check if directory is not set
if [[ -z "${DAQ_DIR}" ]]
then
    echo "The variable DAQ_DIR is not set (empty)."
    echo "Please provide the name of a directory to create (e.g. DAQSettings_v1) as the first argument."
    exit 1
fi

echo "Creating ${DAQ_DIR}..."
mkdir -p ${DAQ_DIR}

echo "Copying Ph2_ACF settings files to ${DAQ_DIR}..."
cp settings/RD53Files/CMSIT*.txt ${DAQ_DIR}
cp settings/CMSIT*.xml ${DAQ_DIR}
cp settings/lpGBTFiles/CMSIT*.txt ${DAQ_DIR}

cd ${DAQ_DIR}

echo "Done!"

