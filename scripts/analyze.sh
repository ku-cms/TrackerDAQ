#!/usr/bin/bash
# analyze.sh

# copy data
rsync -az /home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/BERT_TAP0_Scans data

# analyze data
python3 TrackerDAQ/python/BERT_Simple_Analyze.py

