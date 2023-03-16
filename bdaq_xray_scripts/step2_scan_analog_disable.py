#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    This basic scan injects a specified charge into
    enabled pixels to test the analog front-end.
    Pixel that do not exceed the minmal occupancy get masked.
'''

import tables as tb
import numpy as np

from bdaq53.analysis import analysis
from bdaq53.scans.scan_analog import AnalogScan
import bdaq53.analysis.analysis_utils as au


scan_configuration = {
    'start_column': 0,
    'stop_column': 400,
    'start_row': 0,
    'stop_row': 192,

    'VCAL_MED': 500,
    'VCAL_HIGH': 1450,

    'min_occupancy': 10
}


class AnalogDisableScan(AnalogScan):
    scan_id = 'analog_scan'

    def _analyze(self):
        super(AnalogDisableScan, self)._analyze()

        with analysis.Analysis(raw_data_file=self.output_filename + '.h5') as a:
            with tb.open_file(a.analyzed_data_file) as in_file:

                scan_config = au.ConfigDict(in_file.root.configuration_in.scan.scan_config[:])
                min_occupancy = scan_config.get('min_occupancy', 1)

                occupancy = in_file.root.HistOcc[:].sum(axis=2)
                disable_mask = np.logical_or(occupancy > min_occupancy, np.logical_not(self.chip.masks['enable']))
        n_disabled_pixels = np.count_nonzero(np.invert(disable_mask))

        self.chip.masks.disable_mask = disable_mask
        self.chip.masks.apply_disable_mask()
        self.log.success('Found and disabled {0} dead pixels.'.format(n_disabled_pixels))


if __name__ == '__main__':
    with AnalogDisableScan(scan_config=scan_configuration) as scan:
        scan.start()
