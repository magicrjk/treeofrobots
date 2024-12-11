import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from nptdms import TdmsFile

def c_accrepres(i, filepath):
    k = 0
    n = 0
    not_possible = False

    forces = {}

    Fz = 0
    F_des = 8

    avg_Fz = []
    std_Fz = []
    max_Fz = []
    min_Fz=[]
    acc_single = []
    res_single = []

    for k in range(30):
        filename = os.path.join(filepath, f'ForceData_{k}.tdms')
        
        try:
            tdms_file = TdmsFile.read(filename)
            data = tdms_file['Measuring values']
            

            if i == 8:
                Fz_data = np.array([data['Chan. 4_1'].data, data['Chan. 4_2'].data, data['Chan. 4_3'].data]).T
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                # plt.plot(Fz)
                                
                # plt.show()


            elif i > 10:
                filename_csv = os.path.join(filepath, f'ForceData_{k}.csv')
                try:
                    data_csv = pd.read_csv(filename_csv)  #header=h_lines
                    Fz_data = data_csv.iloc[:, [1, 2, 3]]
                    Fz = np.sqrt((Fz_data**2).sum(axis=1))
                except FileNotFoundError:
                    try:
                        tdms_file = TdmsFile.read(filename)
                        data = tdms_file['Measuring values']
                        Fz_data = np.array([data['Chan. 5_1'].data, data['Chan. 5_2'].data, data['Chan. 5_3'].data]).T
                        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                    except FileNotFoundError:
                        print('Missing a dataset for controller performance evaluation - acc rep res')
                        continue
            else:
                Fz_data = np.array([data['Chan. 5_1'].data, data['Chan. 5_2'].data, data['Chan. 5_3'].data]).T
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                #print(Fz[0:10])

            avg_Fz.append(np.abs(np.mean(Fz)))
            std_Fz.append(np.std(Fz))
            max_Fz.append(np.max(np.abs(Fz)))
            min_Fz.append(np.min(np.abs(Fz)))

            acc_with_max = np.abs(np.max(np.abs(Fz)) - F_des)
            acc_with_min = np.abs(np.min(np.abs(Fz)) - F_des)

            if acc_with_max > acc_with_min:
                acc_single.append(acc_with_max)
            else:
                acc_single.append(acc_with_min)

            res_single.append(np.abs(np.max(np.abs(Fz))-np.min(np.abs(Fz))))#2 * np.std(Fz))

        except FileNotFoundError:
            print(f'File {filename} not found.')

    avg_max_Fz = np.mean(max_Fz)
    #print(res_single)

    l_i_new = [max_fz - avg_max_Fz for max_fz in max_Fz]

    out_acc = round_up_if_needed(np.max(acc_single),2)
    out_std_acc = np.std(acc_single)
    out_rep = round_up_if_needed(np.mean(l_i_new) + 3 * np.std(l_i_new),2)
    out_std_res = np.std(res_single)
    out_max_res = round_up_if_needed(np.max(res_single),2)

    return out_acc, out_rep, out_max_res

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor


# out_acc, out_rep, out_max_res = c_accrepres(8, os.path.join("02_Force_Controller", "AcF_PcF_REScF_OV_TS", "8_c_accrepres", "C_files"))
# print(out_acc, out_rep, out_max_res)
