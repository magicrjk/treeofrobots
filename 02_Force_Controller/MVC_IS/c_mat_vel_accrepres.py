import os
import pandas as pd
import numpy as np
from nptdms import TdmsFile

def c_mat_vel_accrepres(i):
    margin = 0.1

    kk = 0
    jj = 0
    settled = np.zeros((5, 2))
    trial_settled = np.zeros(3)
    F_des = 8

    if i == 9:
        setup = 0
    else:
        setup = 1

    if setup == 0:
        factor = 800
        factor_2 = 200
        threshold = 6500
        if i == 8:
            factor = 700
            factor_2 = 200
    else:
        factor = 30
        factor_2 = 30
        threshold = 80
        if i == 1:
            factor = 1000
            factor_2 = 3000
            threshold = 3500

    for kk in range(2):
        velocity = 'Static' if kk == 0 else 'Dynamic'
        velocity_series_name = f"{velocity}_contact"

        for jj in range(5):
            na = 0
            materials = ['alu', 'PE', 'blue', 'yellow', 'foam']
            mat = materials[jj]

            material_series_name = os.path.join("02_Force_Controller", "MVC_IS", f"{i}_c_accrepres", "C_files", velocity_series_name, mat)
            if not os.path.exists(material_series_name):
                os.makedirs(material_series_name)
            
            k_end = 2

            for k in range(k_end + 1):
                if setup == 0:
                    filename = f'ForceData_{k}.tdms'
                    if not os.path.exists(os.path.join(material_series_name, filename)):
                        na = 1
                    else:
                        # Assuming a function to read TDMS files
                        data = TdmsFile.read(os.path.join(material_series_name, filename))
                        Fz_1 = np.abs(data['Measuring values']['Chan. 5_3'].data)
                else:
                    if i == 0 or i == 7:
                        filename = f'ForceData_{k}.txt'
                        if not os.path.exists(os.path.join(material_series_name, filename)):
                            na = 1
                        else:
                            data = pd.read_table(os.path.join(material_series_name, filename), sep=",")
                            Fz_1 = np.abs(data.iloc[:, 3])
                    elif i == 1: # LBR
                        filename = f'ForceData_{k}.log'
                        if not os.path.exists(os.path.join(material_series_name, filename)):
                            na = 1
                        else:
                            data = pd.read_table(os.path.join(material_series_name, filename), skiprows=1, sep=r"\s+")
                            Fz_1 = np.abs(data.iloc[:, 20])
                    elif i == 8: # M0609
                        filename = f'ForceData_{k}.csv'
                        if not os.path.exists(os.path.join(material_series_name, filename)):
                            na = 1
                        else:
                            data = pd.read_csv(os.path.join(material_series_name, filename), skiprows=1, sep=";")
                            Fz_1 = np.abs(data.iloc[:, 2])
                            factor_2 = 500
                    elif i > 10:
                        # filename = f'ForceData_{k}.csv'
                        # if not os.path.exists(os.path.join(material_series_name, filename)):
                        #     filename = f'ForceData_{k}.txt'
                        #     if not os.path.exists(os.path.join(material_series_name, filename)):
                        #         na = 1
                        #     else:
                        #         data = pd.read_table(os.path.join(material_series_name, filename))
                        #         Fz_1 = np.abs(data.iloc[:, 3])
                        # else:
                        #     data = pd.read_csv(os.path.join(material_series_name, filename), skiprows=1)
                        #     Fz_data = data.iloc[:, 1:4]
                        #     Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
                        filename = f'ForceData_{k}.csv'
                        ex = os.path.exists(os.path.join(material_series_name, filename))
                        print(filename)
                        print(jj)
                        print(kk)

                        if not ex:
                            print('missing a dataset for controller performance evaluation - mvc is')
                            filename = f'ForceData_{k}.txt'
                            ex_1 = os.path.exists(os.path.join(material_series_name, filename))
                            if not ex_1:
                                print('missing a dataset for controller performance evaluation - mvc is')
                            else:
                                data = pd.read_csv(os.path.join(material_series_name, filename))
                                Fz_1 = abs(data.iloc[:, 3])
                        else:
                            data = pd.read_csv(filename, skiprows=1)
                            Fz_data = data.iloc[:, [1, 2, 3]].values
                            Fz_1 = np.sqrt(np.sum(Fz_data**2, axis=1))
                            print('evaluates the new robot')
                    else:
                        na = 1

                if na == 1:
                    trial_settled[k] = 0
                    Fz_1 = 0
                else:
                    Fz_start = np.argmax(Fz_1) + factor
                    if Fz_start > threshold:
                        Fz_start = threshold
                    Fz = Fz_1[Fz_start:Fz_start+factor_2]
                    F_threshold_settle = np.mean(Fz) + margin * np.mean(Fz)
                    Fz_std = np.std(Fz)

                    if np.max(Fz) < F_threshold_settle:
                        trial_settled[k] = 1
                    else:
                        trial_settled[k] = 0

            if np.sum(trial_settled) == (k_end + 1) and np.mean(Fz) > 0 and (0.8 * 8) < np.mean(Fz) < (1.2 * 8):
                settled[jj, kk] = 1
            else:
                settled[jj, kk] = 0

    out_MVC = 100 * np.sum(settled[:, 0]) / 5
    out_IS = 100 * np.sum(settled[:, 1]) / 5

    return out_MVC, out_IS