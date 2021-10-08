#!/opt/homebrew/bin/bash
# getData.sh

# kucms
#rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/development/Ph2_ACF/DAQSettings_v1/BERT_TAP0_Scans data

# kucms-01
rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/development/Ph2_ACF/DAQSettings_v1/BERT_TAP0_Scans data
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/development/Ph2_ACF/DAQSettings_v1/BERT_Scan_Compare_SCC data

