#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    This script scans over different amounts of injected charge
    to find the effective threshold of the enabled pixels.
'''

from tqdm import tqdm
import numpy as np

from bdaq53.system.scan_base import ScanBase
from bdaq53.chips.shift_and_inject import shift_and_inject, get_scan_loop_mask_steps
from bdaq53.analysis import analysis
from bdaq53.analysis import plotting


scan_configuration = {
    'start_column': 0,
    'stop_column': 400,
    'start_row': 0,
    'stop_row': 192,

    'VCAL_MED': 500,
    'VCAL_HIGH_start': 625,
    'VCAL_HIGH_stop': 820,
    'VCAL_HIGH_step': 5
}


class ThresholdScan(ScanBase):
    scan_id = 'threshold_scan'

    def _configure(self, start_column=0, stop_column=400, start_row=0, stop_row=192, TDAC=None, **_):
        '''
        Parameters
        ----------
        start_column : int [0:400]
            First column to scan
        stop_column : int [0:400]
            Column to stop the scan. This column is excluded from the scan.
        start_row : int [0:192]
            First row to scan
        stop_row : int [0:192]
            Row to stop the scan. This row is excluded from the scan.
        TDAC : int / np.ndarray
            If int: TDAC value to use for all enabled pixels, overwriting any existing mask.
            If np.ndarray: TDAC mask to use for enabled pixels. Has to have shape to match start_column:stop_column, start_row:stop_row
        '''
        self.chip.masks['enable'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks['injection'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks.apply_disable_mask()

        if TDAC is not None:
            if type(TDAC) == int:
                self.chip.masks['tdac'][start_column:stop_column, start_row:stop_row] = TDAC
            elif type(TDAC) == np.ndarray:
                self.chip.masks['tdac'][start_column:stop_column, start_row:stop_row] = TDAC[start_column:stop_column, start_row:stop_row]

        self.chip.masks.update(force=True)

    def _scan(self, n_injections=100, VCAL_MED=500, VCAL_HIGH_start=1000, VCAL_HIGH_stop=4000, VCAL_HIGH_step=100, **_):
        '''
        Threshold scan main loop

        Parameters
        ----------
        n_injections : int
            Number of injections.

        VCAL_MED : int
            VCAL_MED DAC value.
        VCAL_HIGH_start : int
            First VCAL_HIGH value to scan.
        VCAL_HIGH_stop : int
            VCAL_HIGH value to stop the scan. This value is excluded from the scan.
        VCAL_HIGH_step : int
            VCAL_HIGH interval.
        '''

        vcal_high_range = range(VCAL_HIGH_start, VCAL_HIGH_stop, VCAL_HIGH_step)

        pbar = tqdm(total=get_scan_loop_mask_steps(scan=self) * len(vcal_high_range), unit=' Mask steps')
        for scan_param_id, vcal_high in enumerate(vcal_high_range):
            self.chip.setup_analog_injection(vcal_high=vcal_high, vcal_med=VCAL_MED)
            with self.readout(scan_param_id=scan_param_id):
                shift_and_inject(scan=self, n_injections=n_injections, pbar=pbar, scan_param_id=scan_param_id)

        pbar.close()
        self.log.success('Scan finished')

    def _analyze(self):
        with analysis.Analysis(raw_data_file=self.output_filename + '.h5', **self.configuration['bench']['analysis']) as a:
            a.analyze_data()
            mean_thr = np.median(a.threshold_map[np.nonzero(a.threshold_map)])
            mean_noise = np.median(a.noise_map[np.nonzero(a.noise_map)])
            if np.isfinite(mean_thr):
                self.log.info('Mean threshold is %i [Delta VCAL]' % (int(mean_thr)))
            else:
                self.log.warning('Mean threshold could not be determined!')

        if self.configuration['bench']['analysis']['create_pdf']:
            with plotting.Plotting(analyzed_data_file=a.analyzed_data_file) as p:
                p.create_standard_plots()

        return mean_thr, mean_noise


if __name__ == '__main__':
    with ThresholdScan(scan_config=scan_configuration) as scan:
        scan.start()
