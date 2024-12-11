import pandas as pd
import numpy as np
import os

def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor


def Teaching_metrics(i, filepath):
  
    k = 4
    vel = 250
    energy = {
        'E_1_C': np.zeros(30),
        'ME_C': np.zeros(30)
    }
    forces = {
        'F_x_mean_C': np.zeros(30),
        'F_x_stddev_C': np.zeros(30),
        'F_y_mean_C': np.zeros(30),
        'F_y_stddev_C': np.zeros(30),
        'F_z_mean_C': np.zeros(30),
        'F_z_stddev_C': np.zeros(30)
    }

    for n in range(30):
        
        if i == 9:
            filename = f'ForceData_{n}.txt'
            filename_posvel = f'ForceData_{n}_posvel.txt'
        else:
            filename = f'MP_{k}_{n}_ForceData.txt'
            filename_posvel = f'MP_{k}_{n}_ForceData_posvel.txt'
            
        try:
            data = pd.read_table(os.path.join(filepath, filename), skiprows=0, sep="\t")
            F = np.array([data.iloc[:, 1] * 2.5, data.iloc[:, 2] * 2.5, data.iloc[:, 3] * 10]).T
            t_F = data.iloc[:, 0]

             

            data_posvel = pd.read_table(os.path.join(filepath, filename_posvel), skiprows=0, sep="\t")
            pos = data_posvel.iloc[:, 1:4]
            velocity = data_posvel.iloc[:, 4:7]
            vel_y = np.sqrt(velocity.iloc[:, 1] ** 2)
            t_vel = data_posvel.iloc[:, 0]
        except FileNotFoundError:
            continue
        
        x_offset = np.mean(F[:2000, 0])
        y_offset = np.mean(F[:2000, 1])
        z_offset = np.mean(F[:2000, 2])

        Fx = F[:, 0] - x_offset
        Fy = F[:, 1] - y_offset
        Fz = F[:, 2] - z_offset

        start_f_motion = start_b_motion = stop_f_motion = stop_b_motion = 0
        bb = -1
        acceleration_start = 0
        mean_vel = []
        for aa in range(11, len(vel_y) - 10, 10):
            
            bb += 1

            if vel_y[aa] > 2 and acceleration_start == 0:
                acceleration_start = aa

            mean_vel.append(np.linalg.norm(np.mean(vel_y[aa-10:aa])))
            mean_vel.append(np.linalg.norm(np.mean(vel_y[aa:aa+10])))

            if mean_vel[bb] > (vel - 3):
                if mean_vel[bb-1] < (vel - 3):
                    if start_f_motion == 0:
                        start_f_motion = aa
                    elif start_f_motion > 0 and start_b_motion == 0:
                        start_b_motion = aa
                    else:
                        print("third motion start detected")
                if mean_vel[bb+1] < (vel - 3):
                    if stop_f_motion == 0:
                        stop_f_motion = aa
                    elif stop_f_motion > 0 and stop_b_motion == 0:
                        stop_b_motion = aa
                    else:
                        print("third motion stop detected")
            _ = mean_vel.pop(-1)

        
        time_motion_start_f = t_vel[start_f_motion ]
        time_motion_start_b = t_vel[start_b_motion ]
        time_motion_stop_f = t_vel[stop_f_motion ]
        time_motion_stop_b = t_vel[stop_b_motion ]

        force_f_start_point = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_start_f, 2))[0]
        force_b_start_point = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_start_b, 2))[0]
        force_f_stop_point = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_stop_f, 2))[0]
        force_b_stop_point = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_stop_b, 2))[0]
        #POTETIAL ERROR: always -1 to matlab

        Fx_cut = np.abs(Fx[force_f_start_point[0]:force_f_stop_point[0]+1])
        Fy_cut = np.abs(Fy[force_f_start_point[0]:force_f_stop_point[0]+1])
        Fz_cut = np.abs(Fz[force_f_start_point[0]:force_f_stop_point[0]+1])
        t_F_cut = t_F[force_f_start_point[0]:force_f_stop_point[0]+1]

        start_f_motion_w_a = start_f_motion - 50
        stop_f_motion_w_a = stop_f_motion + 50
        #print(stop_f_motion_w_a)

        x_0_2 = np.abs(pos.iloc[acceleration_start-1, 1])
        dx = 2 * np.abs(pos.iloc[stop_f_motion_w_a, 1]) # entire trajectory from -200 to +200 (on pos.iloc[:,1])
        dx2 = -np.abs(pos.iloc[start_f_motion-1, 1]) + x_0_2
        #print(pos.iloc[:,1])
        #print(dx2)

        time_motion_start_f_w_a = t_vel[start_f_motion_w_a]
        time_motion_stop_f_w_a = t_vel[stop_f_motion_w_a]
        time_acceleration_start = t_vel[acceleration_start-1]
        #print(time_acceleration_start)

        force_f_start_point_w_a = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_start_f_w_a, 2))[0]
        force_f_start_point_w_a =force_f_start_point_w_a -1
        force_f_stop_point_w_a = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_stop_f_w_a, 2))[0]
        force_f_stop_point_w_a =force_f_stop_point_w_a -1
        force_acc_start = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_acceleration_start, 2))[0]

        #print(force_f_start_point_w_a[0])
        #print(force_f_stop_point_w_a[0])

        n_samples = len(Fy[force_f_start_point_w_a[0]:force_f_stop_point_w_a[0]+1])
        n_samples_2 = len(Fy[force_acc_start[0]:force_f_start_point[0]+1])
        #print(n_samples_2)

        x_t = np.linspace(0.0, dx * 0.001, n_samples)
        x_t_2 = np.linspace(0.0, dx2 * 0.001, n_samples_2)
        #print(np.size(x_t))

        energy['E_1_C'][n] = np.trapz(np.abs(Fy[force_f_start_point_w_a[0]:force_f_stop_point_w_a[0]+1]),x_t) #* 1000 (for mJ)
        energy['ME_C'][n] = np.trapz( np.abs(Fy[force_acc_start[0]:force_f_start_point[0]+1]),x_t_2) #* 1000

        forces['F_x_mean_C'][n] = np.mean(Fx_cut)
        forces['F_x_stddev_C'][n] = np.std(Fx_cut)
        forces['F_y_mean_C'][n] = np.mean(Fy_cut)
        forces['F_y_stddev_C'][n] = np.std(Fy_cut)
        forces['F_z_mean_C'][n] = np.mean(Fz_cut)
        forces['F_z_stddev_C'][n] = np.std(Fz_cut)

    out_mean_E_1_C = round_up_if_needed(abs(np.mean(energy['E_1_C'])),2)
    out_std_E_1_C = abs(np.std(energy['E_1_C']))
    out_mean_sig_F_C = round_up_if_needed(np.mean(forces['F_y_stddev_C']),2)
    out_std_sig_F_C = np.std(forces['F_y_stddev_C'])
    out_mean_all_C = round_up_if_needed(np.mean(forces['F_y_mean_C']),2)
    out_std_all_C = np.std(forces['F_y_mean_C'])
    out_ME_C = round_up_if_needed(abs(np.mean(energy['ME_C'])),2)
    out_ME_C_std = abs(np.std(energy['ME_C']))
    

    l_i_C = np.zeros(10)
    for xx in range(10):
        l_i_C[xx] = np.linalg.norm(out_mean_all_C - forces['F_y_mean_C'][xx])

    std_li_C = np.std(l_i_C)
    RP_gf_C = np.mean(l_i_C) + 3 * std_li_C

    return out_mean_all_C, out_mean_sig_F_C, out_mean_E_1_C, out_ME_C

#out_mean_all_C, out_mean_sig_F_C, out_mean_E_1_C, out_ME_C = Teaching_metrics(1, os.path.join("05_Teaching", "GF_GD_GE_ME","1_guidetests","C_files"))
#print(out_mean_all_C, out_mean_sig_F_C, out_mean_E_1_C, out_ME_C)