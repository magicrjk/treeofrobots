import pandas as pd
import os
import numpy as np

def accrepres(i, filepath):
    k = 0
    n = 0

    mass = 0.8  # load in kg
    F_des = mass * 9.81

    if i == 0:
        h_lines = 21
    elif i in [1, 2, 3, 4, 8, 9]:
        h_lines = 1
    elif i == 6 or i == 7:
        h_lines = 0
    elif i == 10:
        h_lines = 13
    elif i == 11:  # ONLY FOR TESTING REMOVE 
        i = 0
        h_lines = 21
    else:
        h_lines = 1

    avg_Fz = []
    std_Fz = []
    max_Fz = []
    min_Fz = []
    res_single = []
    acc_single = []
    
    for k in range(30):
        if i == 0:  # FE
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=";")
                Fz_data = data.iloc[:, 21:24]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 1:  # LBR
            filename = os.path.join(filepath, f'ForceData_{k}.log')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=r"\s+")
                Fz_data = data.iloc[:, [2, 4, 6]]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i in [2, 3]:  # UR10e and UR5e
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=" ")
                Fz_data = data.iloc[:, 67:70]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 4:  # Yuanda
            filename = os.path.join(filepath, f'DataLogger_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep = r",\{|,|\},",engine='python')
                Fz_data = data.iloc[:, [3, 3, 4]]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                # Additional processing for data_2 can be included here if needed
            else:
                print(filename + " is not available.")
                continue
        elif i == 6:  # Kinova
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=",")
                Fz_org_data = data.iloc[4:, [1, 2, 3]]
                Fz = np.sqrt(np.sum(Fz_org_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 7:  # FR3
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=";")
                Fz_data = data.iloc[:, 21:24]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 8:  # M0609
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=";")
                Fz_data = data.iloc[:, :3]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 10:  # HC10
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=";")
                Fx_converted = (data.iloc[:, 1] - 10000) * 0.1
                Fy_converted = (data.iloc[:, 2] - 10000) * 0.1
                Fz_converted = (data.iloc[:, 3] - 10000) * 0.1
                Fz_data = np.vstack([Fx_converted, Fy_converted, Fz_converted]).T
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i == 9:  # GoFa
            filename = os.path.join(filepath, f'ForceData_{k}.txt')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep="\t", comment='%')
                Fz_data = data.iloc[:750, 1:4]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            else:
                print(filename + " is not available.")
                continue
        elif i > 10:  # New robot entries
            filename = os.path.join(filepath, f'ForceData_{k}.csv')
            if os.path.exists(filename):
                data = pd.read_csv(filename, skiprows=h_lines, sep=",")
                Fz_data = data.iloc[:, 1:4]
                Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                print('Evaluates the new robot')
            else:
                print('Missing a dataset for sensing performance evaluation')
                continue

        avg_Fz.append(np.abs(np.mean(Fz)))
        std_Fz.append(np.std(Fz))
        max_Fz.append(np.max(np.abs(Fz)))
        min_Fz.append(np.min(np.abs(Fz)))

        res_single.append(max_Fz[-1] - min_Fz[-1])

        acc_with_max = np.abs((np.max(np.abs(Fz))) - F_des)
        acc_with_min = np.abs((np.min(np.abs(Fz))) - F_des)
        if acc_with_max > acc_with_min:
            acc_single.append(acc_with_max)
        else:
            acc_single.append(acc_with_min)

    avg_avg_Fz = np.mean(avg_Fz)
    avg_max_Fz = np.mean(max_Fz)
    l_i_new = [max_Fz[a] - avg_max_Fz for a in range(len(max_Fz)-1)]
    out_acc = round_up_if_needed(np.max(acc_single),2)
    out_std_acc = np.std(acc_single)
    out_rep = round_up_if_needed(np.mean(l_i_new) + 3 * np.std(l_i_new),2)
    out_res = np.mean(res_single)
    out_std_res = np.std(res_single)
    out_max_res = round_up_if_needed(np.max(res_single),)

    return out_acc, out_rep, out_max_res

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor


#out_acc, out_rep, out_max_res = accrepres(0, os.path.join("01_Force_Sensing", "0_accrepres", "C_files"))
#print(out_acc, out_rep, out_max_res)