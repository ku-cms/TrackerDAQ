#!/opt/homebrew/bin/bash
# getPlots.sh

# kucms-01
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53A
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/RD53A/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53A_v2
#rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53B

rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v3/plots/ raw_plots_PortCard_RD53B
rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53A

