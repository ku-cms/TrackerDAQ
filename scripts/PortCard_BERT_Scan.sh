#!/usr/bin/bash
# PortCard_BERT_Scan.sh

# input arguments
TAP0_Setting=$1
Signal_Setting=$2
dataDir=$3
outFile=$4

# Check that required arguments have been provided

if [ -z "$TAP0_Setting" ]
then
    echo " - Please provide a TAP0 setting [0,1023] as the first argument."
    echo " - Note that communication fails for low values... e.g. TAP0 less than 50."
    exit 1
fi

if [ -z "$Signal_Setting" ]
then
    echo " - Please provide setting for the secondary signal type [0,3] as the second argument."
    exit 1
fi

if [ -z "$dataDir" ]
then
    echo " - Please provide a directory as the third argument."
    exit 1
fi

# Default output file if none is provided
if [ -z "$outFile" ]
then
    outFile="$dataDir/out.log"
    echo "Using default output file: $outFile"
fi

# Create directory for data if it does not exist
mkdir -p "$dataDir"

# Set settings in config file.
# Note that having the exact number of spaces as the original file matter for search and replace.
# This is not ideal... it would be good to improve this.

# Using sed with variables and quotes:
# https://askubuntu.com/questions/76808/how-do-i-use-variables-in-a-sed-command


cp CMSIT_RD53B_Optical_BERT.xml CMSIT_RD53B_Optical_BERT_Custom.xml

# FIXME: We should find a better way to do this that does not break based on the number of spaces!!

# Be careful about the number of spaces!
#sed -i -e "s|DAC_CML_BIAS_0         =   \"500\"|DAC_CML_BIAS_0         =   \""${TAP0_Setting}"\"|g" CMSIT_RD53B_Optical_BERT_Custom.xml
sed -i -e "s|DAC_CML_BIAS_0         =    \"500\"|DAC_CML_BIAS_0         =    \""${TAP0_Setting}"\"|g" CMSIT_RD53B_Optical_BERT_Custom.xml

# Run BERT and send output to file
echo "Running BERT with TAP0=$TAP0_Setting" | tee -a $outFile
CMSITminiDAQ -f CMSIT_RD53B_Optical_BERT_Custom.xml -c bertest > "$dataDir/scan.log"

# Write values to output log file
grep DAC_CML_BIAS_0 CMSIT_RD53B_Optical_BERT_Custom.xml >> $outFile
grep Final "$dataDir/scan.log" >> $outFile

# Remove color codes from log file
# https://superuser.com/questions/380772/removing-ansi-color-codes-from-text-stream
sed -i -e 's/\x1b\[[0-9;]*m//g' $outFile

# Run grep again to get exit code
# This exit code is used to determine if BERT ran successfully
grep Final "$dataDir/scan.log" > /dev/null
exit $?

