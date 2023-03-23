#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    Finds the optimum global threshold value for target threshold using binary search algorithm.
    Online analysis is used to calculate hit occupancy in order to speed up the tuning.
    Allows tuning of multiple RD53A flavours at the same time.
'''

import numpy as np
from tqdm import tqdm

from bdaq53.system.scan_base import ScanBase
from bdaq53.chips.shift_and_inject import shift_and_inject
from bdaq53.analysis import online as oa

np.warnings.filterwarnings('ignore')


scan_configuration = {
    # Run for only SYNC: columns from 0 to 128
    'start_column': 0,
    'stop_column': 128,
    'start_row': 0,
    'stop_row': 192,

    'n_injections': 100,

    # Target threshold
    'VCAL_MED': 500,
    'VCAL_HIGH': 723,

    # This setting does not have to be changed, it only allows (slightly) faster retuning
    # E.g.: gdac_value_bits = [3, 2, 1, 0] uses the 4th, 3rd, 2nd, and 1st GDAC value bit.
    # GDAC is not an existing DAC, its value is mapped to the respective FE registers.
    'gdac_value_bits': range(9, -1, -1)
}


class GDACTuning(ScanBase):
    scan_id = 'global_threshold_tuning'

    def _configure(self, start_column=0, stop_column=400, start_row=0, stop_row=192, VCAL_MED=1000, VCAL_HIGH=4000, **_):
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

        VCAL_MED : int
            VCAL_MED DAC value.
        VCAL_HIGH_start : int
            VCAL_HIGH DAC value.
        '''

        self.data.start_column, self.data.stop_column, self.data.start_row, self.data.stop_row = start_column, stop_column, start_row, stop_row
        self.data.flavors = []
        if self.chip.chip_type.lower() == 'rd53a':
            self.n_flavours = 3
            if start_column < 128:
                self.data.flavors.append('SYNC')
            if start_column < 264 and stop_column > 128:
                self.data.flavors.append('LIN')
            if stop_column > 264:
                self.data.flavors.append('DIFF')
                left_border = 264
        else:
            self.n_flavours = 1
            self.data.flavors.append('DIFF')
            left_border = 0

        self.chip.masks['enable'][start_column:stop_column, start_row:stop_row] = True
        self.chip.masks['injection'][start_column:stop_column, start_row:stop_row] = True

        self.chip.masks.apply_disable_mask()

        self.chip.masks.update(force=True)

        # Global threshold scan should always be done with centered TDAC
        if 'LIN' in self.data.flavors:
            mean_tdac_lin = np.mean(self.chip.masks['tdac'][max(128, start_column):min(264, stop_column), start_row:stop_row])
            if mean_tdac_lin < 6 or mean_tdac_lin > 8:
                self.log.warning('Mean TDAC for LIN is {0:1.1f}. Global threhsold tuning should always be run with centered TDAC!'.format(mean_tdac_lin))
        if 'DIFF' in self.data.flavors:
            mean_tdac_diff = np.mean(self.chip.masks['tdac'][max(left_border, start_column):min(400, stop_column), start_row:stop_row])
            if mean_tdac_diff < -3 or mean_tdac_diff > 3:
                self.log.warning('Mean TDAC for DIFF is {0:1.1f}. Global threhsold tuning should always be run with centered TDAC!'.format(mean_tdac_diff))

        self.chip.setup_analog_injection(vcal_high=VCAL_HIGH, vcal_med=VCAL_MED)

        hmap_is_compressed = False if (self.chip_conf.get('CoreColEncoderConf', 0) & 0b01000000000) else True  # compression of hitmap word (in case of ITkPixV1)
        self.data.hist_occ = oa.OccupancyHistogramming(chip_type=self.chip.chip_type.lower(), hmap_is_compressed=hmap_is_compressed, rx_id=int(self.chip.receiver[-1]))

    def _scan(self, n_injections=100, gdac_value_bits=range(9, -1, -1), **_):
        '''
        Global threshold tuning main loop

        Parameters
        ----------
        n_injections : int
            Number of injections.
        gdac_value_bits : iterable
            Bits to toggle during tuning. Should be monotone.
        '''

        def update_best_gdacs(mean_occ, best_gdacs, best_gdac_offsets):
            for i in range(self.n_flavours):  # loop flavors
                if np.abs(mean_occ[i] - n_injections / 2.) < best_gdac_offsets[i]:
                    best_gdac_offsets[i] = np.abs(mean_occ[i] - n_injections / 2.)
                    best_gdacs[i] = gdac_new[i]
            return best_gdacs, best_gdac_offsets

        def write_gdac_registers(gdacs):
            ''' Write new GDAC setting for enabled flavors '''
            if 'SYNC' in self.data.flavors:
                self.chip.registers['VTH_SYNC'].write(gdacs[0])
                self.chip.configuration['registers']['VTH_SYNC'] = int(gdacs[0])
            if 'LIN' in self.data.flavors:
                self.chip.registers['Vthreshold_LIN'].write(gdacs[1])
                self.chip.configuration['registers']['Vthreshold_LIN'] = int(gdacs[1])
            if 'DIFF' in self.data.flavors:
                if self.chip.chip_type.lower() == 'rd53a':
                    self.chip.registers['VTH1_DIFF'].write(gdacs[2])
                    self.chip.configuration['registers']['VTH1_DIFF'] = int(gdacs[2])
                else:
                    self.chip.registers['DAC_TH1_L_DIFF'].write(gdacs[0])
                    self.chip.registers['DAC_TH1_R_DIFF'].write(gdacs[0])
                    self.chip.registers['DAC_TH1_M_DIFF'].write(gdacs[0])
                    self.chip.configuration['registers']['DAC_TH1_L_DIFF'] = int(gdacs[0])
                    self.chip.configuration['registers']['DAC_TH1_R_DIFF'] = int(gdacs[0])
                    self.chip.configuration['registers']['DAC_TH1_M_DIFF'] = int(gdacs[0])

        # Set GDACs to start value
        start_value = 2 ** gdac_value_bits[0]
        # FIXME: keep track of chip config here, since it is not provided by bdaq53 yet?
        gdac_new = [start_value] * self.n_flavours  # sync/linear/differential
        best_gdacs = [start_value] * self.n_flavours

        # Only check pixel that can respond
        sel_pixel = self.chip.masks['enable'].copy()
        sel_pixel[self.data.start_column:self.data.stop_column, self.data.start_row:self.data.stop_row] = True

        self.log.info('Searching optimal global threshold setting for {0}.'.format(', '.join(self.data.flavors)))
        self.data.pbar = tqdm(total=len(gdac_value_bits) * self.chip.masks.get_mask_steps() * 2, unit=' Mask steps')
        for scan_param_id in range(len(gdac_value_bits)):
            # Set the GDAC bit in all flavours
            gdac_bit = gdac_value_bits[scan_param_id]
            for i in range(self.n_flavours):
                gdac_new[i] = np.bitwise_or(gdac_new[i], 1 << gdac_bit)
            write_gdac_registers(gdac_new)

            # Calculate new GDAC from hit occupancies: median pixel hits < n_injections / 2 --> decrease global threshold
            hist_occ = self.get_occupancy(scan_param_id, n_injections)
            if self.chip.chip_type.lower() == 'rd53a':
                mean_occ = [np.median(hist_occ[:128][sel_pixel[:128]]),         # SYNC
                            np.median(hist_occ[128:264][sel_pixel[128:264]]),   # LIN
                            np.median(hist_occ[264:][sel_pixel[264:]])]         # DIFF
            else:
                mean_occ = [np.median(hist_occ[sel_pixel])]

            self.log.info('Mean occ. is {0} at GDAC setting {1}'.format(mean_occ, gdac_new))

            # Binary search does not have to converge to best solution for not exact matches
            # Thus keep track of best solution and set at the end if needed
            if not scan_param_id:  # First iteration --> initialize best gdac settings
                if self.chip.chip_type.lower() == 'rd53a':
                    best_gdac_offsets = [np.abs(mean_occ[0] - n_injections / 2.), np.abs(mean_occ[1] - n_injections / 2.), np.abs(mean_occ[2] - n_injections / 2.)]
                else:
                    best_gdac_offsets = [np.abs(mean_occ[0] - n_injections / 2.)]
            else:  # Update better settings
                best_gdacs, best_gdac_offsets = update_best_gdacs(mean_occ, best_gdacs, best_gdac_offsets)

            # Seedup by skipping remaining iterations if result for all selected flavors is already found
            if np.all((mean_occ == np.array([n_injections / 2.] * 3)) | np.isnan(mean_occ)):
                self.log.info('Found best result, skip remaining iterations')
                break

            # Update GDACS from measured mean occupancy
            for i in range(self.n_flavours):  # SYNC / LIN / DIFF
                if not np.isnan(mean_occ[i]) and mean_occ[i] < n_injections / 2.:  # threshold too high
                    gdac_new[i] = np.bitwise_and(gdac_new[i], ~(1 << gdac_bit))  # decrease threshold
        else:  # Loop finished but last bit = 0 still has to be checked
            self.data.pbar.close()
            scan_param_id += 1
            for i in range(self.n_flavours):
                gdac_new[i] = np.bitwise_and(gdac_new[i], ~(1 << gdac_bit))
            # Check if setting was already used before, safe time of one iteration
            if best_gdacs != gdac_new:
                write_gdac_registers(gdac_new)
                hist_occ = self.get_occupancy(scan_param_id, n_injections)
                if self.chip.chip_type.lower() == 'rd53a':
                    mean_occ = [np.median(hist_occ[:128][sel_pixel[:128]]),         # SYNC
                                np.median(hist_occ[128:264][sel_pixel[128:264]]),   # LIN
                                np.median(hist_occ[264:][sel_pixel[264:]])]         # DIFF
                else:
                    mean_occ = [np.median(hist_occ[sel_pixel])]

                self.log.info('Mean occ. is {0} at GDAC setting {1}'.format(mean_occ, gdac_new))

                best_gdacs, best_gdac_offsets = update_best_gdacs(mean_occ, best_gdacs, best_gdac_offsets)
        self.data.pbar.close()

        if self.chip.chip_type.lower() == 'rd53a':
            if 'SYNC' in self.data.flavors:
                self.log.success('Optimal VTH_SYNC value is {0:1.0f}'.format(best_gdacs[0]))
            if 'LIN' in self.data.flavors:
                self.log.success('Optimal Vthreshold_LIN value is {0:1.0f}'.format(best_gdacs[1]))
            if 'DIFF' in self.data.flavors:
                self.log.success('Optimal VTH1_DIFF value is {0:1.0f}'.format(best_gdacs[2]))
        else:
            self.log.success('Optimal DAC_TH1_DIFF value is {0:1.0f}'.format(best_gdacs[0]))

        # Set final result
        self.data.best_gdacs = best_gdacs
        write_gdac_registers(best_gdacs)

        self.data.hist_occ.close()  # stop analysis process

    def get_occupancy(self, scan_param_id, n_injections):
        ''' Analog scan and stuck pixel scan '''

        if self.chip.chip_type.lower() == 'rd53a':  # FIXME: makes ITkPixV1 stuck
            self.chip.revive()

        # Inject target charge
        with self.readout(scan_param_id=scan_param_id, callback=self.analyze_data_online):
            shift_and_inject(scan=self, n_injections=n_injections, pbar=self.data.pbar, scan_param_id=scan_param_id)

        # Get hit occupancy using online analysis
        occupancy = self.data.hist_occ.get()

        # Revive chip
        if self.chip.chip_type.lower() == 'rd53a':  # FIXME: makes ITkPixV1 stuck
            self.chip.revive()

        # Scan stuck pixels. TODO: check if this makes sense for ITkPixV1
        if self.chip.chip_type.lower() == 'rd53a':
            with self.readout(scan_param_id=scan_param_id, callback=self.analyze_data_online_no_save):
                for fe, _ in self.chip.masks.shift(masks=['enable']):
                    if not fe == 'skipped':
                        self.chip.toggle_output_select(send_ecr=True if fe == 'SYNC' else False, repetitions=10)
                    self.data.pbar.update(1)
            stuck = self.data.hist_occ.get() > 0
        else:
            stuck = np.zeros_like(self.chip.masks['tdac'])
        occupancy[stuck] = n_injections

        return occupancy

    def analyze_data_online(self, data_tuple, receiver=None):
        raw_data = data_tuple[0]
        if self.chip.chip_type.lower() == 'itkpixv1':  # ITkPixv1 needs ptot table for analysis
            self.data.hist_occ.add(raw_data, self.ptot_table[:])
        else:
            self.data.hist_occ.add(raw_data)
        super(GDACTuning, self).handle_data(data_tuple, receiver)

    def analyze_data_online_no_save(self, data_tuple, receiver=None):
        raw_data = data_tuple[0]
        if self.chip.chip_type.lower() == 'itkpixv1':  # ITkPixv1 needs ptot table for analysis
            self.data.hist_occ.add(raw_data, self.ptot_table[:])
        else:
            self.data.hist_occ.add(raw_data)

    def _analyze(self):
        pass


if __name__ == '__main__':
    with GDACTuning(scan_config=scan_configuration) as tuning:
        tuning.start()
