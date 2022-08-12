#!/opt/homebrew/bin/bash
# getPlots.sh

# kucms-01
rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/update/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53A
rsync -az kucms@kucms-01.phsx.ku.edu:/home/kucms/TrackerDAQ/croc/Ph2_ACF/DAQSettings_v1/plots/ raw_plots_RD53B

