#!/usr/bin/bash
# analyze_RD53B.sh

cable_number=$1

# copy data
rsync -az /home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v1/BERT_TAP0_Scans data

# analyze data

# check if cable number is provided
if [ -z "$cable_number" ]
then
    # if cable number is not provided, analyze all cables
    python3 TrackerDAQ/python/BERT_Simple_Analyze.py -b
else
    # if cable number is provided, analyze that specific cable
    python3 TrackerDAQ/python/BERT_Simple_Analyze.py -b -n $cable_number
fi


