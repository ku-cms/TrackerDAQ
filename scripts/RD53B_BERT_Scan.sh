#!/usr/bin/bash
# RD53B_BERT_Scan.sh

# input arguments
dataDir=$1
outFile=$2

# Check that required arguments have been provided

if [ -z "$dataDir" ]
then
    echo " - Please provide a directory as the first argument."
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

# TODO: make option to select executable
# TODO: make executables that write/read CML BIAS 0,1,2 settings for all TAP0 ranges

# Run BERT and send output to file
echo "Running RD53B BERT TAP0 Scan" 

#RD53BminiDAQ -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
#RD53BminiDAQ_TAP0_50_100 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
#RD53BminiDAQ_TAP0_50_250 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
#RD53BminiDAQ_TAP0_200_400 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
#RD53BminiDAQ_TAP0_350_550 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"

#RD53BminiDAQ_TAP0_20_100_TAP1_100 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
#RD53BminiDAQ_TAP0_50_200_TAP1_100 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"
RD53BminiDAQ_TAP0_50_250 -f CROC_BERT.xml -t RD53BTools.toml BERscanTest > "$dataDir/scan.log"

# Write values to output log file
#grep Final "$dataDir/scan.log" >> $outFile
grep 'DEBUG\|Final' "$dataDir/scan.log" >> $outFile

# Remove color codes from log file
# https://superuser.com/questions/380772/removing-ansi-color-codes-from-text-stream
sed -i -e 's/\x1b\[[0-9;]*m//g' $outFile

# Run grep again to get exit code
# This exit code is used to determine if BERT ran successfully
grep Final "$dataDir/scan.log" > /dev/null
exit $?

