#!/opt/homebrew/bin/bash
# getData.sh

# kucms-01

# data files
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/data/BERT_TAP0_Scans/ raw_data_RD53A
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/RD53A/Ph2_ACF/DAQSettings_v1/data/BERT_TAP0_Scans/ raw_data_RD53A_v2
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v1/data/BERT_TAP0_Scans/ raw_data_RD53B

rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v3/data/ raw_data_PortCard_RD53B

# output tables
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/output/ raw_output_RD53A
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/RD53A/Ph2_ACF/DAQSettings_v1/output/ raw_output_RD53A_v2
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v1/output/ raw_output_RD53B

