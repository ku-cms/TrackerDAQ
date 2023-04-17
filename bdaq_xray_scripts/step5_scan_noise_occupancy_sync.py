#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    This basic scan sends triggers without injection
    into enabled pixels to identify noisy pixels.
'''

import numpy as np
import tables as tb

from tqdm import tqdm

from bdaq53.system.scan_base import ScanBase
from bdaq53.analysis import analysis
from bdaq53.analysis import plotting

scan_configuration = {
    'start_column': 0,
    'stop_column': 128,
    'start_row': 0,
    'stop_row': 192,

    # Noise occupancy = min_occupancy / n_triggers
    
    # standard masking settings:
    #'n_triggers': 1e7,   # Total number of triggers which are send
    #'min_occupancy': 10  # All pixels with more hits than this threshold are masked as noisy
    
    # masking settings from Massimiliano:
    'n_triggers': 1e7,     # Total number of triggers which are send
    'min_occupancy': 1000  # All pixels with more hits than this threshold are masked as noisy
    
    # x-ray settings from Massimiliano:
    #'n_triggers': 5e7,     # Total number of triggers which are send
    #'min_occupancy': 1e19  # All pixels with more hits than this threshold are masked as noisy
}


class NoiseOccScan(ScanBase):
    scan_id = 'noise_occupancy_scan'

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
        self.chip.masks['injection'][:] = False
        self.chip.masks.apply_disable_mask()

        self.chip.masks.update(force=True)

        # Disable injection
        self.chip.enable_macro_col_cal(macro_cols=None)

        # Do not abort on expecte RX errors
        self.configuration['bench']['general']['abort_on_rx_error'] = False

    def _scan(self, start_column=0, stop_column=400, start_row=0, stop_row=192, n_triggers=1e6, min_occupancy=1, wait_cycles=400, **_):
        '''
        Noise occupancy scan main loop

        Parameters
        ----------
        n_triggers : int
            Number of triggers to send.
        wait_cycles : int
            Time to wait in between trigger packages in units of sync commands.
        '''

        self.data.n_pixels = (stop_column - start_column) * (stop_row - start_row)
        self.data.min_occupancy = min_occupancy
        n = int(n_triggers / 32)  # Trigger command will always send 32 triggers
        steps = []
        while n > 0:
            if n >= 50000:
                steps.append(50000)
                n -= 50000
            else:
                steps.append(n)
                n -= n

        # TODO: longterm solution may be to use inject_analog_single for all FE
        # TODO: make CONF_LATENCY less
        trigger_data = self.chip.write_sync(write=False)
        trigger_data += self.chip.generate_trigger_command(0xffffffff)  # effectively we send x32 triggers
        trigger_data += self.chip.write_sync(write=False) * wait_cycles

        if start_column < 128 and self.chip.chip_type.lower() == 'rd53a':  # If SYNC enabled
            self.log.info('SYNC enabled: Using analog injection based commnad.')
            trigger_data = self.chip.inject_analog_single(send_ecr=True, wait_cycles=wait_cycles, write=False)

        pbar = tqdm(total=n_triggers, unit=' Triggers', unit_scale=True)
        with self.readout():
            for stepsize in steps:
                self.chip.write_command(trigger_data, repetitions=stepsize)
                pbar.update(stepsize * 32)

        pbar.close()
        self.log.success('Scan finished')

    def _analyze(self):
        self.configuration['bench']['analysis']['store_hits'] = True
        with analysis.Analysis(raw_data_file=self.output_filename + '.h5', **self.configuration['bench']['analysis']) as a:
            a.analyze_data()
            with tb.open_file(a.analyzed_data_file) as in_file:
                occupancy = in_file.root.HistOcc[:].sum(axis=2)
                disable_mask = ~(occupancy > self.data.min_occupancy)  # Mask everything larger than min. occupancy
            n_disabled_pixels = np.count_nonzero(np.concatenate(np.invert(disable_mask)))
            self.chip.masks.disable_mask &= disable_mask
            self.chip.masks.apply_disable_mask()

        self.log.success('Found and disabled {0} noisy pixels.'.format(n_disabled_pixels))

        if self.configuration['bench']['analysis']['create_pdf']:
            with plotting.Plotting(analyzed_data_file=a.analyzed_data_file) as p:
                p.create_standard_plots()

        return n_disabled_pixels, round(float(n_disabled_pixels) / float(self.data.n_pixels) * 100., 2), occupancy.sum(), disable_mask


if __name__ == '__main__':
    with NoiseOccScan(scan_config=scan_configuration) as scan:
        scan.start()
