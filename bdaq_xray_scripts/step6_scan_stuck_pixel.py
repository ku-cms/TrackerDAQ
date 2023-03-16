#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    This scan identifies stuck pixels. Stuck pixels have such a low
    threshold or are so noisy that the output of the comparator is
    effectively always high.
    It is important to identify these pixels and count them as "noisy"
    during chip qualification and chip tuning.
    Identifying stuck pixels is not completely straight forward
    since they do not change the output of the comparator and thus show no
    hits; the same result that not noisy pixels have.
'''

from tqdm import tqdm

import numpy as np
import tables as tb

from bdaq53.system.scan_base import ScanBase
from bdaq53.analysis import analysis
from bdaq53.analysis import plotting

scan_configuration = {
    'start_column': 0,
    'stop_column': 400,
    'start_row': 0,
    'stop_row': 192,

    # Warning: injecting into all pixels at once leads to n_injections-1 hits in a few pixels
    # To catch all stuck pixels inject at least 2 times (n_injections=2)
    'n_injections': 10
}


class StuckPixelScan(ScanBase):
    scan_id = 'stuck_pixel_scan'

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

        if start_column < 128 and self.chip.chip_type.lower() == 'rd53a':
            self.log.warning('Stuck pixels in the SYNC FE cannot be identified by this algorithm and will be ignored!')

        self.chip.masks['enable'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks['injection'][:] = False
        self.chip.masks.apply_disable_mask()

        self.chip.masks.update(force=True)
        self.chip.write_cal(cal_edge_mode=0, cal_edge_width=1, cal_edge_dly=0)   # pixel CalEdge => 1

    def _scan(self, n_injections=10, **_):
        '''
        Stuck pixel scan main loop

        Parameters
        ----------
        n_injections : int
            Number of injections.
        '''
        pbar = tqdm(total=self.chip.masks.get_mask_steps(), unit=' Mask steps')
        with self.readout():
            for fe, _ in self.chip.masks.shift(masks=['enable']):
                if not fe == 'skipped' and not fe == 'SYNC':    # Ignore SYNC FE
                    self.chip.toggle_output_select(send_ecr=False, repetitions=n_injections)
                pbar.update(1)
        pbar.close()
        self.log.success('Scan finished')

    def _analyze(self):
        with analysis.Analysis(raw_data_file=self.output_filename + '.h5', **self.configuration['bench']['analysis']) as a:
            a.analyze_data()
        with tb.open_file(a.analyzed_data_file) as in_file:
            occupancy = in_file.root.HistOcc[:].sum(axis=2)
            not_stuck_pixel_mask = occupancy < 1
            # Disabled mask has an inverted logic, thus & is needed
            self.chip.masks.disable_mask &= not_stuck_pixel_mask
            self.chip.masks.apply_disable_mask()

        self.log.success('Found and disabled {0} stuck pixels.'.format(np.count_nonzero(~not_stuck_pixel_mask)))

        if self.configuration['bench']['analysis']['create_pdf']:
            with plotting.Plotting(analyzed_data_file=a.analyzed_data_file) as p:
                p.create_standard_plots()
                p._plot_occupancy(p.HistOcc[:, :, 0].T > 0, title='Stuck pixels', z_label='# of hits', z_min=0, z_max=1, show_sum=False)


if __name__ == '__main__':
    with StuckPixelScan(scan_config=scan_configuration) as scan:
        scan.start()
