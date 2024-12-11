import os
import pandas as pd
import numpy as np

def MF_evaluation(i, filepath):
    if i in [0, 3, 5, 7, 8, 9]:
        direction = 'C2N2'
    else:
        direction = 'C1N1'

    vel_str = '02'
    #direction_series_name = os.path.join('05_Teaching', 'MF', f'{i}_guidingforce_slow', 'C_files', direction)
    #if not os.path.exists(direction_series_name):
    #    raise FileNotFoundError(f"Directory {direction_series_name} does not exist")

    MF_j = np.zeros(10)
    for n in range(10):
        
        if i in [8, 9]:
            filename = os.path.join(f'{direction}',f'ForceData_{n}.txt')
            filename_wotxt = os.path.join(f'{direction}',f'ForceData_{n}')
        else:
            filename = f'MP_{vel_str}_{n}_ForceData_{direction}.txt'
            filename_wotxt = f'MP_{vel_str}_{n}_ForceData_{direction}'

        filename = os.path.join(filepath, filename)
        filename_posvel = os.path.join(filepath, f'{filename_wotxt}_posvel.txt')

        if not os.path.exists(filename):
            out_mean_MF_Cx = 0
            out_std_MF_Cx = 0
        else:
            if i == 9:
                data = pd.read_csv(filename, delimiter='\t', skiprows=0, decimal=',')
                data_posvel = pd.read_csv(filename_posvel, delimiter='\t', skiprows=0, decimal=',')
            else:
                data = pd.read_csv(filename, delimiter='\t', skiprows=0)
                data_posvel = pd.read_csv(filename_posvel, delimiter='\t', skiprows=0)

            # list_data = []
            # with open(filename, 'r') as file:
            #     next(file)
            #     for line in file:
            #         values = line.split()
            #         float_values = [float(value) for value in values]  # Convert each value to float
            #         list_data.append(float_values)

            # data_2 = np.array(list_data)
            # # Define the factors for each column
            # factors = np.array([1, 2.5, 2.5, 10])  
            # data_2 = data_2 * factors
            # data_2_subset = data_2[:, 1:4]

            # list_data_p = []
            # with open(filename_posvel, 'r') as file:
            #     next(file)
            #     for line in file:
            #         values = line.split()
            #         float_values = [float(value) for value in values]  # Convert each value to float
            #         list_data_p.append(float_values)

            # data_2_p = np.array(list_data_p)
            # # Define the factors for each column
            # data_2_subset_p = data_2_p[:, 1]

            

            
            F = np.array([data.iloc[:, 1] * 2.5, data.iloc[:, 2] * 2.5, data.iloc[:, 3] * 10]).T
            # for i in range(0,len(data_2_subset)):
            #     for m in range(0,3):
            #         if data_2_subset[i][m]!=F[i][m]:
            #             print('ERROR_F')

            t_F = data.iloc[:, 0]

            position = data_posvel.iloc[:, 1:4]
            pos_x = np.abs(position.iloc[:, 0])


            # for i in range(0,len(data_2_subset_p)):
            #     print(data_2_subset_p[i],pos_x[i])
            #     if data_2_subset_p[i]!=pos_x[i]:
            #         print('ERROR_P')
            t_vel = data_posvel.iloc[:, 0]
            

            x_offset = np.mean(F[:2000, 0])
            Fx = F[:, 0] - x_offset

            disp = pos_x
            F_1 = Fx
            mean_disp_start = np.mean(disp[:500])
            boarder = mean_disp_start + 0.1

           # print(F_1[3710:3720])

            start_f_motion = 0
            finish = 0
            turned_data = False

            for aa in range(50, len(disp)):
                
                if turned_data:
                    if disp[aa] < boarder:
                        if finish == 0 and disp[aa+5] < boarder:
                            finish = 1
                            start_f_motion = aa
                else:
                    if disp[aa] > boarder:
                        if finish == 0 and disp[aa+5] > boarder:
                            finish = 1
                            start_f_motion = aa

            time_motion_start_f = t_vel[start_f_motion+1]
            #print(type(time_motion_start_f))
            #print(type(t_F))
            #print(len(t_F))
            #test_list = np.where(np.round(t_F, 2) == np.round(time_motion_start_f, 2))
            # print(test_list[0])
            # for i in [test_list[0][0]]:
            #     print(i)
            #     print(np.round(t_F, 3)[i])
            # test = [ np.round(t_F, 2)[i] for i in np.where(np.round(t_F, 2) == np.round(time_motion_start_f, 2))]
            # print(test)
            # print(np.round(t_F, 2)[0])
            #print(type(test))

            # print(time_motion_start_f)
            # print(round_up_if_needed(time_motion_start_f, 2))
            force_f_start_point = np.where(round_up_if_needed(t_F, 2) == round_up_if_needed(time_motion_start_f, 2))[0]
            # print(round_up_if_needed(t_F[force_f_start_point[0]], 2))
            #force_f_start_point is one less but should not play a role...
            # print(F_1[force_f_start_point[0]])
            # print(force_f_start_point[0])
            # print(t_F[force_f_start_point[0]-1])
            # print(round_up_if_needed(t_F[force_f_start_point[0]-1],2))
     

            MF_j[n] = np.abs(F_1[force_f_start_point[0]])
            # print(MF_j)
            

    if not os.path.exists(filepath):
        out_mean_MF_Cx = 0
        out_std_MF_Cx = 0
    else:
        out_mean_MF_Cx = round_up_if_needed(np.abs(np.mean(MF_j)),2)
        out_std_MF_Cx = np.abs(np.std(MF_j))

    return out_mean_MF_Cx


def round_up_if_needed(x, decimals=0):
    factor = 10 ** decimals
    x_scaled = x * factor
    x_rounded = np.where(np.round(x_scaled % 1,2) >= 0.5, np.ceil(x_scaled), np.round(x_scaled))
    return x_rounded / factor

# out_mean_MF_C = MF_evaluation(7, os.path.join("05_Teaching", "MF","7_guidingforce_slow","C_files"))
# print(out_mean_MF_C)