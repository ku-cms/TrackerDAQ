#!/usr/bin/bash
# BERT_Scan.sh

TAP0_Setting=$1
dataDir=$2

# Check that required arguments have been provided

if [ -z "$TAP0_Setting" ]
then
    echo " - Please provide a TAP0 setting [0,1000] as the first argument."
    echo " - Note that communication fails for low values... e.g. TAP0 less than 50."
    exit 1
fi

if [ -z "$dataDir" ]
then
    echo " - Please provide a directory as the second argument."
    exit 1
fi

mkdir -p "$dataDir"

# Set CML_TAP0_BIAS in config file:

# using sed with variables and quotes:
# https://askubuntu.com/questions/76808/how-do-i-use-variables-in-a-sed-command
sed -e "s|CML_TAP0_BIAS           =   \"500\"|CML_TAP0_BIAS           =   \""${TAP0_Setting}"\"|g" CMSIT_BERT_Scan.xml > CMSIT_BERT_Scan_Custom.xml

# Run BERT

echo "Running BERT with TAP0=$TAP0_Setting"

grep CML_TAP0_BIAS CMSIT_BERT_Scan_Custom.xml

CMSITminiDAQ -f CMSIT_BERT_Scan_Custom.xml -c bertest > "$dataDir/scan.log"

grep Final "$dataDir/scan.log"

