#!/usr/bin/bash
# analyze.sh

cable_number=$1

# copy data
rsync -az /home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/BERT_TAP0_Scans data

# analyze data

# check if cable number is provided
if [ -z "$cable_number" ]
then
    # if cable number is not provided, analyze all cables
    python3 TrackerDAQ/python/BERT_Simple_Analyze.py
else
    # if cable number is provided, analyze that specific cable
    python3 TrackerDAQ/python/BERT_Simple_Analyze.py -a $cable_number
fi


