# The function cB_results processes TDMS and CSV data files based on the input i and returns the bandwidth of the robot controller. 

# -For each dataset k (0 to 9), TDMS files are loaded to extract force data from three channels.
# -The desired force profile is generated based on sinusoidal variations.
# -The measured force is derived from the TDMS data.
# -The cross-spectral density (CSD) and power spectral density (PSD) are computed using the csd and welch functions from SciPy.
# -The transfer function is then calculated as the ratio of CSD to PSD.
# -If valid data is present, the maximum frequency where the transfer function exceeds a threshold is determined and averaged.
# -The bandwidth is determined as the frequency where the transfer function exceeds certain thresholds.
# -The function returns the bandwidth as out_BW, which is the averaged value across datasets. If no valid data is found, out_BW is NaN.


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import csd, welch
import warnings
from nptdms import TdmsFile

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor

def cB_results(i, filepath):
    pos = ['C']  # Assuming position series isn't used directly here
    BW = []
    BW_min = []
    # Initialize out_BW to handle cases where it's not assigned in conditional blocks
    out_BW = np.nan
    if i == 0:
        for k in range(10):
            filename = os.path.join(filepath, f'BW_{k}.tdms')   
            tdms_file = TdmsFile.read(filename)
            measured_data = tdms_file['Measuring values']
            chan_4_3 = measured_data['Chan. 4_3'].data
            chan_4_2 = measured_data['Chan. 4_2'].data
            chan_4_1 = measured_data['Chan. 4_1'].data
            amp = 8
            sf = 100  # Sampling Frequency
            max_frequency = []  # Initialize as empty list
            desired_force = []  # Initialize as empty list
            measured_force = []  # Initialize as empty list
            filename_12 = os.path.join(filepath, f'{k}.csv')
            if os.path.exists(filename_12):
                # print(f'Loading desired force data from: {filename_12}')  # Debugging: Print file name
                desired_data = pd.read_csv(filename_12, header=0)
                F = desired_data['desired_force'].values
                time = np.arange(0, len(F)) * 0.001  # Assuming a 1ms time step
            else:
                continue
            # Generate desired force profile
            time2 = [0]
            freq = 1 / 2 / np.pi / 0.25
            Fd = np.zeros_like(time)
            for j in range(len(time)):
                Fd[j] = np.abs(amp * np.sin(2 * np.pi * freq * time2[j]))
                if time2[j] >= 0.000:
                    freq += 2 * np.pi * 0.0025
                time2.append(time2[j] + 0.001)
                if time2[j + 1] > time[-1]:
                    time_vector = time2[:j + 1]
                    break
            idx = np.where(np.array(time_vector) >= 0.000)[0]
            if len(idx) > 0:
                sampling_time = np.array(time_vector)[idx[0]:]
                desired_force = Fd[idx[0]:]
            else:
                continue
            force = np.sqrt(chan_4_3**2 + chan_4_2**2 + chan_4_1**2)
            fm = force - np.mean(force[:50])
            
            # Detect significant changes in force
            io = next((i for i in range(10, len(fm)) if abs(fm[i] - fm[i - 10]) > 0.2), 0)
            measured_force = fm[io:io + len(sampling_time)]

            # Find transfer function
            if len(desired_force) > 0 and len(measured_force) > 0:
                desired_force_1 = np.array(desired_force)
                measured_force_1 = np.array(measured_force)
                # Match lengths
                min_length = min(len(time_vector), len(desired_force_1), len(measured_force_1))
                min_length = 2100
                desired_force_1 = desired_force_1[:min_length]
                measured_force_1 = measured_force_1[:min_length]
                time_vector = time_vector[:min_length]  # Ensure time_vector matches the lengths

                nperseg = min(1024, len(desired_force_1), len(measured_force_1))

                # Compute cross-spectral density and power spectral density
                f, Pxy = csd(desired_force_1, measured_force_1, nperseg=nperseg, fs=sf)
                f, Pxx = welch(desired_force_1, nperseg=nperseg, fs=sf)

                # Calculate the transfer function
                tsensor = Pxy / Pxx

                # Filter out nan values
                valid_indices = ~np.isnan(tsensor)
                tsensor = tsensor[valid_indices]
                f = f[valid_indices]

                if len(tsensor) > 0:
                    threshold_exceeded = np.where(np.logical_and(np.abs(tsensor) > 0, 20 * np.log10(np.abs(tsensor)) > 3))
                    if threshold_exceeded[0].size > 0:
                        for idx in threshold_exceeded[0]:  # Access only the first dimension
                            if f[idx] > 3:
                                max_frequency.append(f[idx])
                                break
                    else:
                        warnings.warn(f'Warning: No frequencies exceeded the threshold for dataset {k}.')
                else:
                    warnings.warn(f'Warning: Transfer function is empty or invalid for dataset {k}.')
            else:
                warnings.warn(f'Warning: Data is empty or invalid for dataset {k}.')
            if max_frequency:
                out_BW = round_up_if_needed(np.mean(max_frequency),0)

            else:
                    out_BW = np.nan

    elif i==7:
        for k in range(10):
            time = []
            time_vector = []
            time_offset = 0
            desired_force = []
            measured_force = []
            # Load desired force data
            filename_1 = os.path.join(filepath, f'{k}.csv')
            if os.path.exists(filename_1):
                print(f'Loading desired force data from: {filename_1}')  # Debugging: Print file name
                desired_data = pd.read_csv(filename_1, header=0)
                F = desired_data['desired_force'].values
                time = np.arange(0, len(F)) * 0.001  # Assuming a 1ms time step
            else:
                print(f'File not found: {filename_1}')
                continue
            # Generate desired force profile
            amp = -4
            freq = 0.5
            time2 = [0]
            Fd = np.zeros_like(time)
            for j in range(len(time)):
                Fd[j] = amp * np.sin(freq * time2[j]) - 4
                if time2[j] > 5.000:
                    freq += 0.0033
                time2.append(time2[j] + 0.0033)
                if time2[j + 1] > time[-1]:
                    time_vector = time2[:j + 1]
                    break
            # Select the portion of the data after 5 seconds
            idx = np.where(np.array(time_vector) > 5.0000)[0]
            if len(idx) > 0:
                sampling_time = np.array(time_vector)[idx[0]:]
                desired_force = Fd[idx[0]:]
            else:
                continue
            # Load measured force data
            filename_2 = os.path.join(filepath, f'BW_{k}.tdms')
            if os.path.exists(filename_2):
                tdms_file = TdmsFile.read(filename_2)
                measured_data = tdms_file['Measuring values']
                channels = ['Chan. 5_3', 'Chan. 5_2', 'Chan. 5_1']
                force_components = []
                for channel in channels:
                    if channel in measured_data:
                        force_components.append(measured_data[channel].data**2)
                    else:
                        print(f'Channel {channel} not found in TDMS file. Skipping.')
                if force_components:
                    force = np.sqrt(np.sum(force_components, axis=0))
                    Fm = force.flatten()
                else:
                    continue
            else:
                print(f'File not found: {filename_2}')
                continue
            io = 0
            for ii in range(len(Fm) - 1000):
                count = np.sum((1 < np.abs(Fm[ii] - Fm[ii:ii + 1000])) &
                            (np.abs((Fm[ii] - Fm[ii + 1000]) / (1000 * 0.0033)) > 2))
                if count > 900:
                    io = ii
                    break
            # Adjust for time offset and ensure data lengths match
            time_offset = abs(len(sampling_time) - len(time_vector))
            if io + time_offset + len(sampling_time) - 1 > len(Fm):
                print('Time offset issue, skipping this dataset')
                continue
            measured_force = Fm[io + time_offset:io + time_offset + len(sampling_time)]
            # Ensure both signals have the same length
            len_min = min(len(desired_force), len(measured_force))
            desired_force = desired_force[:len_min]
            measured_force = measured_force[:len_min]
            # Find Transfer Function
            sf = 303.03  # Sampling frequency
            win = 1024   # Number of segments for Welch's method
            # Calculate the cross-spectral density
            f, Pxy = csd(desired_force, measured_force, fs=sf, nperseg=win)
            # Calculate the power spectral density
            f, Pxx = welch(desired_force, fs=sf, nperseg=win)
            # Transfer function
            tsensor = Pxy / Pxx  # H1(f) = Pyx(f) / Pxx(f)
            x = 2 * np.pi * f
            y = 20 * np.log10(np.abs(tsensor))  # Convert magnitude to decibels
            # Calculate Bandwidth
            # Find the bandwidth and minimum bandwidth
            BW_val = np.nan
            BW_min_val = np.nan
            # Find where y > 3 for bandwidth (BW)
            idx_bw = np.where(y > 3)[0]
            if len(idx_bw) > 0:
                BW_val = x[idx_bw[0]] / (2 * np.pi)
            # Find where y < -3 for minimum bandwidth (BW_min)
            idx_bw_min = np.where(y < -3)[0]
            if len(idx_bw_min) > 0:
                BW_min_val = x[idx_bw_min[0]] / (2 * np.pi)
            # Store bandwidth results
            BW.append(BW_val)
            BW_min.append(BW_min_val)
            # Output the mean bandwidth
            if BW:
                out_BW = round_up_if_needed(np.nanmean(BW),0)
            else:
                out_BW = np.nan
    else: 
        out_BW = np.nan
    
    return out_BW
