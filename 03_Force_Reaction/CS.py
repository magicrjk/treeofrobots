import pandas as pd
import numpy as np
import os
import re

def CS(i, filepath):
    a = 0
    n_stops = 0
    reliable_stop_data = np.zeros((7, 9))
    
    if i > 10:
        filename = os.path.join(filepath, '0_CS.csv')
    else:
        filename = os.path.join(filepath, f'{i}_CS.csv') 
    

    if i in [0,1,7,8,9]:
        data = pd.read_csv(filename, sep='\t', engine= 'python', quotechar='"')#delimiter=';')#'\t')
    else:
        data = pd.read_csv(filename, sep=';', engine= 'python', quotechar='"')#delimiter=';')#'\t')
    
    data = data.iloc[1:, 2:].values  # Convert dataframe to numpy array, skipping first row and first two columns

    # Check if 3 times stopped
    for k in range(7):
        a = 0
        for m in range(9):
            n = m * 3
            if np.sum(data[k, n:n+3]) == 3:
                reliable_stop_data[k, a] = 1
                n_stops += 1
            else:
                reliable_stop_data[k, a] = 0
            a += 1
    
    out_CS = round_up_if_needed((n_stops / 63) * 100,2)  # Calculate percentage of stops
    
    return out_CS

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor
#ContS = CS(0, os.path.join("03_Force_Reaction", f"{0}_contactsens", "C_files"))
#print(ContS)