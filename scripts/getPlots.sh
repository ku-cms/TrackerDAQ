#!/bin/bash
# getPlots.sh

# kucms
#rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/elink_testing_v1/Ph2_ACF/DAQSettings_v1/plots/ plots_elink_testing_v1
#rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/elink_testing_v2/Ph2_ACF/DAQSettings_v1/plots/ plots_elink_testing_v2
#rsync -az kucms@kucms.phsx.ku.edu:/home/kucms/TrackerDAQ/modules/Ph2_ACF/DAQSettings_v1/plots/ plots_modules

# kucms-02
rsync -az kucms@PHSX-kucms-02.phsx.ku.edu:/home/kucms/TrackerDAQ/elink_testing_v3/Ph2_ACF/DAQSettings_v1/plots/ plots_elink_testing_v3

