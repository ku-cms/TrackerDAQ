#
# ------------------------------------------------------------
# Copyright (c) All rights reserved
# SiLab, Institute of Physics, University of Bonn
# ------------------------------------------------------------
#

'''
    Tune global and local threshold and disable noisy and stuck pixels.
    Run a threshold scan in the end to verify results.
'''

from bdaq53.scans.tune_global_threshold import GDACTuning
from bdaq53.scans.tune_local_threshold import TDACTuning
from bdaq53.scans.scan_noise_occupancy import NoiseOccScan
from bdaq53.scans.scan_stuck_pixel import StuckPixelScan
from bdaq53.scans.scan_threshold import ThresholdScan


scan_configuration = {
    # Run for only LIN and DIFF: columns from 128 to 400
    'start_column': 128,
    'stop_column': 400,
    'start_row': 0,
    'stop_row': 192,

    # Target threshold
    'VCAL_MED': 500,
    'VCAL_HIGH': 723,
}

noise_occ_scan_configuration = {
    # Start the scan with a fresh disable mask (resets pixels disabled by other scans)?
    'reset_disable_mask': True,

    # 'max_occupancy': 1e-6,  # Maximum noise occupancy per bunch crossing
    'n_triggers': 1e7,      # Total number of triggers which are send
    'min_occupancy': 10,    # All pixels with more hits than this threshold are masked as noisy
    'certainty': 2.0,       # Expected/tolerable number of wrongly classified pixels (noisy vs. quiet). Note that amount of noise changes with time on a real chip.
    'stop_timeout': 20,     # Scan stops if number of unclassified pixels did not change for stop_timeout seconds. Hard cut is applied to remaining pixels.
    'max_scan_time': 120    # Maximum scan time to prevent not terminating scan. Hard cut is applied to remaining pixels.
}


if __name__ == '__main__':
    noise_occ_scan_configuration['start_column'] = scan_configuration['start_column']
    noise_occ_scan_configuration['stop_column'] = scan_configuration['stop_column']
    noise_occ_scan_configuration['start_row'] = scan_configuration['start_row']
    noise_occ_scan_configuration['stop_row'] = scan_configuration['stop_row']

    with GDACTuning(scan_config=scan_configuration) as global_tuning:
        global_tuning.start()

    with TDACTuning(scan_config=scan_configuration) as local_tuning:
        local_tuning.start()

    # skip the rest!
    ## First noise occupancy scan
    #with NoiseOccScan(scan_config=noise_occ_scan_configuration) as noise_occ_scan:
    #    noise_occ_scan.start()

    #with StuckPixelScan(scan_config=scan_configuration) as stuck_pix_scan:
    #    stuck_pix_scan.start()

    ## Second noise occupancy scan, find more noisy pixels
    #noise_occ_scan_configuration['reset_disable_mask'] = False
    #with NoiseOccScan(scan_config=noise_occ_scan_configuration) as noise_occ_scan:
    #    noise_occ_scan.start()

    ## Calculate scan range for threshold scan
    #target_threshold = scan_configuration['VCAL_HIGH'] - scan_configuration['VCAL_MED']
    #scan_configuration['VCAL_HIGH_start'] = scan_configuration['VCAL_MED'] + target_threshold - 50
    #scan_configuration['VCAL_HIGH_stop'] = scan_configuration['VCAL_MED'] + target_threshold + 50
    #scan_configuration['VCAL_HIGH_step'] = 2
    #with ThresholdScan(scan_config=scan_configuration) as thr_scan:
    #    thr_scan.start()

