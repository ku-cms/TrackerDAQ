#!/usr/bin/bash
# PortCard_BERT_Scan.sh

# Input arguments
XML_Config=$1
TAP0_Setting=$2
Signal_Setting=$3
Data_Dir=$4
Out_File=$5

# Check that required arguments have been provided

if [ -z "$XML_Config" ]
then
    echo " - Please provide an xml config file as the first argument."
    exit 1
fi

if [ -z "$TAP0_Setting" ]
then
    echo " - Please provide a TAP0 setting [0,1023] as the second argument."
    echo " - Note that communication fails for low values... e.g. TAP0 less than 50."
    exit 1
fi

if [ -z "$Signal_Setting" ]
then
    echo " - Please provide setting for the secondary signal type [0,3] as the third argument."
    exit 1
fi

if [ -z "$Data_Dir" ]
then
    echo " - Please provide a directory as the fourth argument."
    exit 1
fi

# Default output file if none is provided
if [ -z "$Out_File" ]
then
    Out_File="$Data_Dir/out.log"
    echo "Using default output file: $Out_File"
fi

# Create directory for data if it does not exist
mkdir -p "$Data_Dir"

# Assign the softlink for the xml config file.
ln -sf $XML_Config CMSIT_RD53B_Optical_BERT.xml

# Copy the xml file to a new file that we will edit.
cp CMSIT_RD53B_Optical_BERT.xml CMSIT_RD53B_Optical_BERT_Custom.xml

# Use sed to search and replace the TAP0 setting (DAC_CML_BIAS_0).

# Using sed with variables and quotes:
# https://askubuntu.com/questions/76808/how-do-i-use-variables-in-a-sed-command

# Updated sed command (credit: ChatGPT 3.5):
# - the -E option enables extended regular expressions to make the syntax simpler
# - the -i is for editing the file in place
# - should match zero or more whitespace characters (space, tab, or newline) around the equal sign
# - after replacement, it should maintain the same whitespace as the original line
sed -E -i "s/(DAC_CML_BIAS_0\s*=\s*)\"[0-9]+\"/\1\"$TAP0_Setting\"/" CMSIT_RD53B_Optical_BERT_Custom.xml

# Run BERT and send output to file
echo " - Running BERT with TAP0=$TAP0_Setting" | tee -a $Out_File
CMSITminiDAQ -f CMSIT_RD53B_Optical_BERT_Custom.xml -c bertest > "$Data_Dir/scan.log"

# Write values to output log file
grep DAC_CML_BIAS_0 CMSIT_RD53B_Optical_BERT_Custom.xml >> $Out_File
grep Final "$Data_Dir/scan.log" >> $Out_File

# Remove color codes from log file
# https://superuser.com/questions/380772/removing-ansi-color-codes-from-text-stream
sed -i -e 's/\x1b\[[0-9;]*m//g' $Out_File

# Run grep again to get exit code
# This exit code is used to determine if BERT ran successfully
grep Final "$Data_Dir/scan.log" > /dev/null
exit $?

