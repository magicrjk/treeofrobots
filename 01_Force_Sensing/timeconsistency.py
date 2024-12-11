import pandas as pd
import numpy as np
import os
from datetime import timedelta
from datetime import datetime

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor


def timeconsistency(i, filepath):
    k = 0
    n = 0
    Fz = 0

    if i == 0:
        h_lines = 23 #24
    elif i in [1,3,2]:
        h_lines = 0
    elif i in [ 4, 8]: #[1, 2, 3, 4, 8]:
        h_lines = 1
    elif i == 9 or i == 10:
        h_lines = 13 #14
    elif i == 6 or i == 7:
        h_lines = 0
    elif i == 11:
        i = 0
    else:
        h_lines = 0#1

    if i == 0:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep=";")
        Fz_data = data.iloc[:, [2, 3, 4]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = data.iloc[:, 1] / 3600 - data.iloc[0, 0] / 3600
        
    elif i == 1:
        filename = f'{i}_ForceData.txt' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines,sep=r"\s+")
        
        Fz_data = data.iloc[:, [2, 4, 6]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = data.iloc[:, 0] / 3600 - data.iloc[0, 0] / 3600
        
    elif i == 2:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep=r"\s+")
        Fz_data = data.iloc[:, [1, 2, 3]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        
        t = data.iloc[:, 0] / 3600 - data.iloc[4, 0] / 3600 #t = data.iloc[:, 0] / 3600 - data.iloc[4, 0] / 3600
        #print(data.iloc[:, 0][18]/3600- data.iloc[4, 0] / 3600)
        
    elif i == 3:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep =r"\s+")
        
        Fz_data = data.iloc[:, [1, 2, 3]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = data.iloc[:, 0] / 3600 - data.iloc[0, 0] / 3600
        
    elif i == 4:
        filename = 'DataLogger.csv' 
        filename = os.path.join(filepath, filename)
        # data = pd.read_csv(filename, skiprows=h_lines, sep = r",\{|,|\},",engine='python')
        # #data.iloc[:,[2]] =  data.iloc[:, [2]].replace("{","",regex=True)
        # Fz_data = data.iloc[:, [3, 3, 4]]  # %replace first Var4 by Var3...
        # #  data[:,10] and data[:,11] are in isoformat = 2022-03-24T17:14:59.512Z
        # t = data.iloc[:, [10]].apply(lambda x: [(datetime.fromisoformat(y)-datetime.fromisoformat(x[0])).total_seconds()/3600 for y in x])

        # Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        list_data = []
        list_time = []
        list_time_2 = []
        with open(filename, 'r') as file:
            next(file)
            for line in file:
                values = line.split()
                float_values = [value for value in values]  # Convert each value to float
                float_values = [float_values[0].split(",")[0], float_values[0].split(",")[1],
                                float(float_values[0].split(",")[2].split("{")[1]), float(float_values[0].split(",")[3]),
                                float(float_values[0].split(",")[4]), float(float_values[0].split(",")[5]),
                                float(float_values[0].split(",")[6]), float(float_values[0].split(",")[7].split("}")[0]),
                                float_values[0].split(",")[8], float_values[0].split(",")[9],
                                float_values[0].split(",")[10]]
                date_obj=datetime.strptime(float_values[9], '%Y-%m-%dT%H:%M:%S.%fZ')
                #date_obj_2=datetime.strptime(float_values[10], '%Y-%m-%dT%H:%M:%S.%fZ')
                t_1 = date_obj.timestamp()
                #t_2 = date_obj_2.timestamp()
                list_time.append((t_1)/3600)
                list_data.append([float_values[3],float_values[3],float_values[4]])

        time=np.array(list_time)
        t = time-time[0]
        Fz = np.sqrt(np.sum(np.array(list_data)**2, axis=1))
        
    elif i == 6:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep = ",")
        
        Fz_org_data = data.iloc[:, [1, 2, 3]]
        Fz_org = np.sqrt(np.sum(Fz_org_data**2, axis=1))
        t_org = data.iloc[:, 0]
        Fz = np.abs(Fz_org[3::4])
        t = t_org[3::4] / 3600
        
    elif i == 7:
        list_values=[]
        list_time=[]
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep=";")
        
        with open(filename, 'r') as file:
            
            for line in file:
                values = line.split("\n")
                values_1 = [value for value in values]
                float_values =[float(values_1[0].split(";")[2]), float(values_1[0].split(";")[3]),
                                float(values_1[0].split(";")[4])]
                float_time=[float(values_1[0].split(";")[1])]
                list_values.append(float_values) 
                list_time.append(float_time) 
        Fz_data = np.array(list_values)
        t=np.array(list_time) /3600
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))

    elif i == 8:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep=";")
        
        Fz_data = data.iloc[:, [0, 1, 2]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = np.arange(0, 26214.35, 0.025) / 3600
    elif i == 10:
        filename = f'{i}_ForceData.csv' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep=";")
        
        data_short = data.iloc[::250, :]
        Fx_converted = (data_short.iloc[:, 1] - 10000) * 0.1
        Fy_converted = (data_short.iloc[:, 2] - 10000) * 0.1
        Fz_converted = (data_short.iloc[:, 3] - 10000) * 0.1
        Fz_data = np.column_stack((Fx_converted, Fy_converted, Fz_converted))
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = data_short.iloc[:, 0] / 3600000
    elif i == 9:
        filename = f'{i}_ForceData.txt' 
        filename = os.path.join(filepath, filename)
        data = pd.read_csv(filename, header=h_lines, sep="\t")
        
        data_short = data.iloc[::10, :]
        Fz_data = data_short.iloc[:, [1, 2, 3]]
        Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
        t = data_short.iloc[:, 0] / 3600
    elif i > 10:
        filename = f'ForceData_{k}.csv'
        filename = os.path.join(filepath, filename, sep=",")
        try:
            data = pd.read_csv(filename, header=h_lines)
            Fz_data = data.iloc[:, [1, 2, 3]]
            Fz = np.sqrt(np.sum(Fz_data**2, axis=1))
            t = data.iloc[:, 0] / 3600
        except FileNotFoundError:
            print('Missing a dataset for sensing performance evaluation - tc')
    
    t_1 = int(np.where(round_up_if_needed(t, 2) >= 0.01)[0][0])
    
    t_2 = int(np.where(round_up_if_needed(t, 2) >= 0.10)[0][0])
    
    t_3 = int(np.where(round_up_if_needed(t, 2) >= 1.50)[0][0])
    
    t_4 = int(np.where(round_up_if_needed(t, 2) >= 7.00)[0][0])

    # print(np.where(round_up_if_needed(t, 2) >= 0.01))
    # print(np.where(round_up_if_needed(t, 2) >= 0.1))
    # print(np.where(round_up_if_needed(t, 2) >= 1.5))
    # print(np.where(round_up_if_needed(t, 2) >= 7.0))
    #print(round_up_if_needed(t[t_1],2))
    Fz = np.array(Fz)
    range_t1 = range(t_1 - 5, t_1 + 6)
    avg_Fz_t1 = np.mean(Fz[range_t1])
    range_t2 = range(t_2 - 5, t_2 + 6)
    avg_Fz_t2 = np.mean(Fz[range_t2])
    range_t3 = range(t_3 - 5, t_3 + 6)
    avg_Fz_t3 = np.mean(Fz[range_t3])
    range_t4 = range(t_4 - 5, t_4 + 6)
    avg_Fz_t4 = np.mean(Fz[range_t4])

    
    out_dTC_1 = round_up_if_needed(abs(avg_Fz_t1 - Fz[0]),2)
    out_dTC_2 = round_up_if_needed(abs(avg_Fz_t2 - Fz[0]),2)
    out_dTC_3 = round_up_if_needed(abs(avg_Fz_t3 - Fz[0]),2)
    out_dTC_4 = round_up_if_needed(abs(avg_Fz_t4 - Fz[0]),2)


    return out_dTC_1, out_dTC_2, out_dTC_3, out_dTC_4

Timedrift = timeconsistency(7, os.path.join("01_Force_Sensing", "7_timeconsistency", "C_files"))
print(Timedrift)