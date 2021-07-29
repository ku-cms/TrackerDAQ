#!/usr/bin/bash
# BERT_Scan.sh

echo "Running BERT scan."

TAP0_Setting=$1
#dataDir="BERT_Scan_SingleDP_Data"
#dataDir="BERT_Scan_DoubleDP_DoubleBonn_Data"
#dataDir="BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink101_Data"
#dataDir="BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink102_Data"
#dataDir="BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink104_Data"
#dataDir="BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink106_Data"
dataDir="BERT_Scan_DoubleDP_DoubleBonn_DoubleYellow_elink111_Data"

if [ -z "$TAP0_Setting" ]
then
    echo " - Please provide a TAP0 setting [0,1000] as the first argument."
    echo " - Note that communication fails for low values... e.g. TAP0 less than 10."
    exit 1
fi

mkdir -p "$dataDir"


# Set CML_TAP0_BIAS in config file:

# using sed with variables and quotes:
# https://askubuntu.com/questions/76808/how-do-i-use-variables-in-a-sed-command
sed -e "s|CML_TAP0_BIAS           =   \"500\"|CML_TAP0_BIAS           =   \""${TAP0_Setting}"\"|g" CMSIT_BERT_Scan.xml > CMSIT_BERT_Scan_Custom.xml

grep CML_TAP0_BIAS CMSIT_BERT_Scan_Custom.xml

CMSITminiDAQ -f CMSIT_BERT_Scan_Custom.xml -c bertest > "$dataDir/scan.log"

grep Final "$dataDir/scan.log"

