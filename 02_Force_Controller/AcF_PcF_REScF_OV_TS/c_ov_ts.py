import numpy as np
import pandas as pd
import os
from nptdms import TdmsFile

def c_ov_ts(i, filepath):
    k = 0
    n = 0

    forces = {}

    Fz = 0
    F_des = 8
    Ov = 0
    time = 0

    start_k = 0
    end_k = 2

    avg_Fz = []
    Ov_list = []
    time_list = []

    for k in range(start_k, end_k + 1):
        filename = os.path.join(filepath, f'ForceData_OV_{k}.tdms')
        file_exists = False

        if i == 8:
            try:
                tdms_file = TdmsFile.read(filename)
                data = tdms_file['Measuring values']
                Fz1 = np.sqrt(data['Chan. 4_3'].data**2 + data['Chan. 4_2'].data**2 + data['Chan. 4_1'].data**2)
                file_exists = True
            except FileNotFoundError:
                pass
        elif i > 10:
            filename_csv = os.path.join(filepath, f'ForceData_OV_{k}.csv')
            try:
                data_csv = pd.read_csv(filename_csv)  #header=h_lines
                Fz_data = data_csv.iloc[:, [1, 2, 3]]
                Fz1 = np.sqrt((Fz_data**2).sum(axis=1))
                file_exists = True
            except FileNotFoundError:
                try:
                    tdms_file = TdmsFile.read(filename)
                    data = tdms_file['Measuring values']
                    Fz1 = np.sqrt(data['Chan. 5_3'].data**2 + data['Chan. 5_2'].data**2 + data['Chan. 5_1'].data**2)
                    file_exists = True
                except FileNotFoundError:
                    print('Missing a dataset for controller performance evaluation - ov ts')
                    continue
        else:
            try:
                tdms_file = TdmsFile.read(filename)
                data = tdms_file['Measuring values']
                Fz1 = np.sqrt(data['Chan. 5_3'].data**2 + data['Chan. 5_2'].data**2 + data['Chan. 5_1'].data**2)
                file_exists = True
            except FileNotFoundError:
                pass
        
        if not file_exists:
            continue

        begin_search = 501
        check_point = 500

        act = 0
        init = 0
        init_avg = 0
        fin = 0

        for jj in range(begin_search, len(Fz1)):
            if abs(Fz1[jj] - Fz1[jj - check_point]) < 0.5 and abs(Fz1[jj]) > 2 and act == 0:
                act = 1
                init = jj
                init_avg = jj + 500

            if ((abs(Fz1[jj] - Fz1[jj + check_point]) > 0.2 and jj - init_avg > 1800) or jj - init_avg > 2000) and act == 1:
                fin = jj
                break

        Fz = Fz1[init:fin]
        Fz_avg = Fz1[init_avg:fin]
        avg_Fz_value = abs(np.mean(Fz_avg))
        avg_Fz.append(avg_Fz_value)

        first_margin = avg_Fz_value - 0.03 * avg_Fz_value
        second_margin = avg_Fz_value + 0.03 * avg_Fz_value

        t = np.zeros(len(Fz1) + 1)
        active = 0
        t1 = 0
        t2 = 0

        for ii in range(fin):
            if abs(Fz1[ii]) >= first_margin and active == 0:
                active = 1
                t1 = t[ii]  # set start value if force is greater "zero"
            if abs(Fz1[ii]) <= first_margin or abs(Fz1[ii]) >= second_margin:
                t2 = t[ii]
            t[ii + 1] = t[ii] + 0.0033

        time_list.append(t2 - t1)
        Ov_list.append(max(abs(Fz1)) - avg_Fz_value)

    out_ov_max = round_up_if_needed(max(Ov_list),2)
    out_ts_max = round_up_if_needed(max(time_list),2)

    return out_ov_max, out_ts_max

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor
