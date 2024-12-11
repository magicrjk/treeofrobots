import pandas as pd
import numpy as np
import os

def St_Sq_evaluation(i, filepath):
    F_max_C = np.zeros(80)
    F_qs_C = np.zeros(80)

    for k in range(80):
        filename = os.path.join(filepath, f'MP{k}_0_ForceData.csv')
        try:
            data = pd.read_csv(filename, comment='#', sep=";",encoding="iso8859_15")  # utf-8 didn't work... use something else
            t = data.iloc[:, 0]
            F = data.iloc[:, 1]

            F_max_C[k] = F.max()
            F_qs_C[k] = F[1000:3997].mean()
        except FileNotFoundError:
            # Assign high dummy values if file is not found
            F_max_C[k] = 1000
            F_qs_C[k] = 1000

    dC_skull = F_max_C[0:8]
    dC_face = F_max_C[8:16]
    dC_lower_legs = F_max_C[16:24]
    dC_thighs = F_max_C[24:32]
    dC_neck = F_max_C[32:40]
    dC_lower_arms = F_max_C[40:48]
    dC_back = F_max_C[48:56]
    dC_upper_arms = F_max_C[56:64]
    dC_chest = F_max_C[64:72]
    dC_abdomen = F_max_C[72:80]

    data_C_max = np.array([dC_skull, dC_face, dC_lower_legs, dC_thighs,
                           dC_neck, dC_lower_arms, dC_back, dC_upper_arms,
                           dC_chest, dC_abdomen])

    # Define F_max values for different parts
    F_max_values = [130, 65, 260, 440, 300, 320, 420, 300, 280, 220]

    # Check for unsafe situations for data_C_max
    unsafe_t_C = 0
    for n in range(8):
        for m in range(10):
            F_max = F_max_values[m]
            if data_C_max[m, n] > F_max:
                unsafe_t_C += 1

    CCF_t_C = 100 * (1 - unsafe_t_C / 80)

    d2C_skull = F_qs_C[0:8]
    d2C_face = F_qs_C[8:16]
    d2C_lower_legs = F_qs_C[16:24]
    d2C_thighs = F_qs_C[24:32]
    d2C_neck = F_qs_C[32:40]
    d2C_lower_arms = F_qs_C[40:48]
    d2C_back = F_qs_C[48:56]
    d2C_upper_arms = F_qs_C[56:64]
    d2C_chest = F_qs_C[64:72]
    d2C_abdomen = F_qs_C[72:80]

    data2_C_qs = np.array([d2C_skull, d2C_face, d2C_lower_legs, d2C_thighs,
                           d2C_neck, d2C_lower_arms, d2C_back, d2C_upper_arms,
                           d2C_chest, d2C_abdomen])

    # Define F_max values for different parts for quasistatic forces
    F_max_values_qs = [130, 65, 130, 220, 150, 160, 210, 150, 140, 110]

    # Check for unsafe situations for data2_C_qs
    unsafe_qs_C = 0
    for n in range(8):
        for m in range(10):
            F_max = F_max_values_qs[m]
            if data2_C_qs[m, n] > F_max:
                unsafe_qs_C += 1

    CCF_qs_C = 100 * (1 - unsafe_qs_C / 80)

    return CCF_t_C, CCF_qs_C