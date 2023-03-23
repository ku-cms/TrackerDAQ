#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    This basic scan injects a digital pulse into
    enabled pixels to test the digital part of the chip.
'''

from tqdm import tqdm

from bdaq53.system.scan_base import ScanBase
from bdaq53.chips.shift_and_inject import shift_and_inject_digital, get_scan_loop_mask_steps
from bdaq53.analysis import analysis
from bdaq53.analysis import plotting


scan_configuration = {
    'start_column': 0,
    'stop_column': 400,
    'start_row': 0,
    'stop_row': 192
}


class DigitalScan(ScanBase):
    scan_id = 'digital_scan'

    def _configure(self, start_column=0, stop_column=400, start_row=0, stop_row=192, **_):
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
        '''

        self.chip.masks['enable'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks['injection'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks.apply_disable_mask()

#         self.chip.masks.load_logo_mask(['injection'])

        self.chip.masks.update(force=True)

        self.chip.setup_digital_injection()

    def _scan(self, n_injections=100, **_):
        '''
        Digital scan main loop

        Parameters
        ----------
        n_injections : int
            Number of injections.
        '''

        pbar = tqdm(total=get_scan_loop_mask_steps(scan=self), unit=' Mask steps')
        with self.readout(scan_param_id=0):
            shift_and_inject_digital(scan=self, n_injections=n_injections, pbar=pbar, scan_param_id=0)
        pbar.close()
        self.log.success('Scan finished')

    def _analyze(self):
        with analysis.Analysis(raw_data_file=self.output_filename + '.h5', **self.configuration['bench']['analysis']) as a:
            a.analyze_data()

        if self.configuration['bench']['analysis']['create_pdf']:
            with plotting.Plotting(analyzed_data_file=a.analyzed_data_file) as p:
                p.create_standard_plots()


if __name__ == '__main__':
    with DigitalScan(scan_config=scan_configuration) as scan:
        scan.start()
