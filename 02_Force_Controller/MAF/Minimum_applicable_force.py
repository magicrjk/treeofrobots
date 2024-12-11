import numpy as np
import pandas as pd
import os
from nptdms import TdmsFile

def Minimum_applicable_force(i, filepath):
    min_app_F = []

    for n in range(3):
        filename = os.path.join(filepath, f'ForceData_{n}.tdms')
        try:
            tdms_file = TdmsFile.read(filename)
            data = tdms_file['Measuring values']
            
            if i == 8 or i == 0 or i == 7:
                Fz = np.sqrt(data['Chan. 4_3'].data**2 + data['Chan. 4_2'].data**2 + data['Chan. 4_1'].data**2)
                if i == 8:
                    Fz = Fz[4000:5000]

            elif i > 10:
                filename_csv = os.path.join(filepath, f'ForceData_{n}.csv')
                try:
                    data_csv = pd.read_csv(filename_csv) #, header=h_lines
                    Fz_data = data_csv.iloc[:, [1, 2, 3]]
                    Fz = np.sqrt((Fz_data**2).sum(axis=1))
                except FileNotFoundError:
                    try:
                        tdms_file = TdmsFile.read(filename)
                        data = tdms_file['Measuring values']
                        Fz = np.sqrt(data['Chan. 4_3'].data**2 + data['Chan. 4_2'].data**2 + data['Chan. 4_1'].data**2)
                    except FileNotFoundError:
                        print('Missing a dataset for controller performance evaluation - maf')
                        continue

            else:
                Fz = np.sqrt(data['Chan. 5_3'].data**2 + data['Chan. 5_2'].data**2 + data['Chan. 5_1'].data**2)
                if i == 9:
                    Fz = Fz[11900:12900]

            min_app_F.append(np.max(Fz))

        except FileNotFoundError:
            print(f'File {filename} not found.')

    out_F_C = round_up_if_needed(np.max(min_app_F),2)
    return out_F_C

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor
