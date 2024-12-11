from robot_tactility import robot_tactility
from robot_motion import robot_motion
import xml.etree.ElementTree as ET
import os

import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
import copy

# Settings
debugging = 1

# General Variables
gray_color = [.5, .5, .5]

# Open the file for reading
with open('init.txt', 'r') as file:
    A = np.loadtxt(file, dtype=int)

#print(A)

# Add dummy robots?
n_dummy_robots = A[0]

# Determine the number of new robots added
if len(A) > 2:
    if A[2] == 5:
        n_new_robots = 0
    else:
        n_new_robots = A[1]
    new_robot_number = A[2]
else:
    n_new_robots = A[1]
    new_robot_number = 0

# Robot quantity (all robots including extended data)
n_industrial_robots = 3
n_robots_MIRMI_measured = 11
n_robots = n_robots_MIRMI_measured + n_industrial_robots + n_new_robots + n_dummy_robots
n_robots_result_table = n_robots_MIRMI_measured + n_industrial_robots + n_new_robots

"""
 Metrics evaluation
generates the tactile metrics results table, only needed if new robots 
are added.
"""

# ONLY FOR NEW ROBOT AND ADD ON TOP OF LIST
#print(new_robot_number)
if new_robot_number > 0:
    conn = sqlite3.connect(os.path.join('Database','tor_database.db'))
    data_check = pd.read_sql_query("SELECT * FROM robot_tactility_metrics", conn)
    conn.close()
    # Write the data to an Excel file
    
    if A[2] == 5: # means all robots are reevaluated if condition in robot_tactility and robot _motion ensures this
        fin = robot_tactility(new_robot_number)
        fin_2 = robot_motion(new_robot_number)
        n_robots = n_robots_MIRMI_measured + n_industrial_robots
    elif (len(data_check) - 1) < A[2]:
        fin = robot_tactility(new_robot_number)
        fin_2 = robot_motion(new_robot_number)
    else:
        n_robots = n_robots_result_table
        print("All robots already evaluated")

# Step One: Assemble Metric Scores
# a) collect all data
lowest = []
highest = []
metrics = [1, 2]
for metric in metrics:
    n = 1
    m = 1
    x_norm = [0, 0]
    # %% REPLACE BY READING FROM TABLE
    # % read data from table (generated by "robot_tactility")
    if metric == 1:
        conn = sqlite3.connect(os.path.join('Database','tor_database.db'))
        data = pd.read_sql_query("SELECT * FROM robot_tactility_metrics", conn)
        # conn = sqlite3.connect('Database/processes_database.db')
        # data = pd.read_sql_query("SELECT * FROM tactile_metric_results", conn)
        conn.close()
        try:
            data.to_excel(os.path.join("Results", "tactile_metrics_results.xlsx"), index=False,engine='openpyxl')
        except Exception as e:
            print(f"An error occurred: {e}")
        Tbl_all_data = data.iloc[:, 1:].to_numpy().T
        Tbl_all_data = Tbl_all_data[0:,:]

    elif metric == 2:
        # conn = sqlite3.connect('Database/processes_database.db')
        # data_2 = pd.read_sql_query("SELECT * FROM motion_metric_results", conn)
        conn = sqlite3.connect(os.path.join('Database','tor_database.db'))
        data_2 = pd.read_sql_query("SELECT * FROM motion_metric_results", conn)
        conn.close()
        Tbl_all_data = data_2['pos_rep'][:n_robots_result_table].to_numpy().T
    

    n1, n2 = np.atleast_2d(Tbl_all_data).shape
    Tbl_all = copy.deepcopy(Tbl_all_data)
    #print(Tbl_all)

    if n_dummy_robots > 0:
        dum_bot_met = []
        
        for n_dum in range(1, n_dummy_robots + 1):
            #print(metric)
            #print(n_dum)
            if metric == 1:
                # add one robot line modified at random

                # check for init_dummy file
                if not os.path.exists('init_dummy.txt'):
                    rand_bot = np.random.randint(0, Tbl_all.shape[1])
                    rand_change = np.random.rand() * 1.2
                    dum_bot_met = Tbl_all[:, rand_bot] * rand_change
                else:
                    with open('init_dummy.txt', 'r') as file:
                        A_1 = np.loadtxt(file)
                    dum_bot_met = A_1[:25]
                dum_bot_met = dum_bot_met.reshape(-1, 1)  # Ensure it's a column vector
                Tbl_all = np.column_stack((Tbl_all, dum_bot_met))
            else:
                if not os.path.exists('init_dummy.txt'):
                    dum_bot_met = np.full((Tbl_all.shape[0], 1), 0.07)
                else:
                    with open('init_dummy.txt', 'r') as file:
                        A_1 = np.loadtxt(file)
                    dum_bot_met = A_1[25]
                list_tblall = list(Tbl_all)
                list_tblall.append(dum_bot_met)
                #print(list_tblall)
                Tbl_all = np.array(list_tblall)
                    #print(A_1[25])
            #print(dum_bot_met)
            
            #print(type(dum_bot_met))
            #print(Tbl_all)
            #print(dum_bot_met)

    # if n_dummy_robots > 0:
    #     for n_dum in range(n_dummy_robots):
    #         if metric == 1:
    #             rand_bot = np.random.randint(0, np.atleast_2d(Tbl_all).shape[1])
    #             rand_change = np.random.random() * 1.2
    #             dum_bot_met = Tbl_all[:, rand_bot] * rand_change
    #         else:
    #             dum_bot_met = 0.07 * np.ones((n1, 1))
            
    #         Tbl_all = np.column_stack((Tbl_all, dum_bot_met))
    '''
    %% TODO: add error check - if both data sets are not same size!

    %% Augment by industrial robots

    % Augment data by additional info from industrial robots (Theoretically
    % here other augmentation methods could be added (not applied!))
    '''
    m, n = np.atleast_2d(Tbl_all).shape
    nan_count = np.ones(n)
    #print(type(Tbl_all))
    #print(metric)
    for count_table in range(n):
        n_NAN = 0
        for count_metrics in range(m):
            if np.isnan(np.atleast_2d(Tbl_all)[count_metrics, count_table]):
                n_NAN += 1
            #Tbl_all[m - 1, count_table] = (m - n_NAN) / m
            
            nan_count[count_table] =  ((m+1) - n_NAN) / (m+1)
    Tbl_all = np.vstack((Tbl_all,nan_count))


    Tbl = copy.deepcopy(Tbl_all)

    

    '''
        %% c) Create matrix of all feature vectors
        %idea: change metrics results to normalized version (1 = worst to inf = best) with 0 being replacer
        %for all NaNs

        % for the percentage metrics where the greater the better - turn data to be
        % the smaller the better

    '''
    highest = np.zeros(n1)
    lowest = np.zeros(n1)
    worst_case_data = np.zeros(n1)
    
    for i in range(n1):  # over lengthTbl_all
        n = 0
        highest[i] = 0#np.zeros(n1)
        lowest[i] = 1000#np.full(n1, 1000)
        
        for j in range(n_robots):
            if not np.isnan(Tbl[i, j]):
                if i in [21, 25, 24, 22, 10, 13, 15, 23]:  #for these metrics greater numbera are better
                    if Tbl[i,j]< lowest[i]:
                        lowest[i] = Tbl[i, j] #min(lowest[i], Tbl[i, j])
                        highest[i] = lowest[i]
                    else:
                        {}
                else:
                    if Tbl[i,j]> highest[i]:
                        highest[i] = Tbl[i, j] 
                    else:
                        {}
                    #highest[i] = max(highest[i], Tbl[i, j])
                
                n += 1

        #highest[highest == 0] = 1  # only in case of percentages in safety metrics
        if highest[i]==0:
            highest[i] = 1
        else:
            {}
        worst_case_data[i] = highest[i]

    for i in range(n1):
        for j in range(n_robots):
            if np.isnan(Tbl[i, j]):
                Tbl[i, j] = 0
            else:
                if i in [21, 25, 24, 22, 10, 13, 15, 23]:# 10 is cB
                    if Tbl[i, j] == 0:
                        Tbl[i, j] = 1
                    Tbl[i, j] = abs(Tbl[i, j] / worst_case_data[i])
                else:
                    if Tbl[i, j] == 0:
                        Tbl[i, j] = 1
                    Tbl[i, j] = abs(worst_case_data[i] / Tbl[i, j])
    
    #  d) augment data (optional - here not applied)
    aug_TBL = copy.deepcopy(Tbl)
    #  e) normalize parameterspace
    n_features, n_r = np.atleast_2d(aug_TBL).shape
    x_norm = np.zeros((n_features, n_r))

    for n in range(n_r):
        for m in range(n_features):
            x_max = np.max(aug_TBL[m, :])
            x_min = np.min(Tbl[m, :])
            x_norm[m, n] = (aug_TBL[m, n] - x_min) / (x_max - x_min) if x_max != x_min else 1

    if metric == 1:
        x_norm_t = x_norm
    else:
        x_norm_m = x_norm

#x = x_norm_t
#x_m = x_norm_m

# Step Two: Motivate Grouping
#  %% a) calculate overall metric for tactility/motion performance as 1-dimensional distances
#  %% TODO MAKE ADDABLE
total_dist = [abs(np.linalg.norm(x_norm_t[:, i])) for i in range(n_robots)]
dist = [np.linalg.norm(x_norm_t[:, i]) for i in range(n_robots)]
total_dist_m = [abs(np.linalg.norm(x_norm_m[:, i])) for i in range(n_robots)]
dist_m = [np.linalg.norm(x_norm_m[0, i]) for i in range(n_robots)]

motion_performance = dist_m[:n_robots]
x_i_2 = np.column_stack((dist[:n_robots], motion_performance[:n_robots]))

# Automated System Difference Evaluation
#  %% 3. Varianzanalyse:
#  % Verify existence of tactiliy groups
probs = np.zeros((n_robots, n_robots))
significant_pair = []
insignificant_pair = []

for metric in metrics:
    if metric == 1:
        x_norm_grouped = x_norm_t
    elif metric == 2:
        x_norm_grouped = x_norm_m

    if metric == 1:
        for xx in range(n_robots - 1):
            for yy in range(xx + 1, n_robots):
                stat, p = mannwhitneyu(x_norm_grouped[:, xx], x_norm_grouped[:, yy])
                probs[xx, yy] = p
                if p < 0.05:
                    significant_pair.append((xx, yy))
                else:
                    insignificant_pair.append((xx, yy))

                    
# 4. Distribution-based Clustering
        group = []
        count = 0
        
        for aa in range(len(insignificant_pair) - 1):
            if not any(insignificant_pair[aa][0] in g for g in group):
                group.append([insignificant_pair[aa][0]])
                nn = 0
                while insignificant_pair[aa + nn][0] == insignificant_pair[aa][0]:
                    if insignificant_pair[aa][0] != insignificant_pair[aa][1]:
                        group[count].append(insignificant_pair[aa][1])
                    nn += 1

                for rep in range(4):
                    l_group = len(group[count])
                    for mm in range(l_group):
                        x_in_group = group[count][mm]
                        rows, cols = np.where(np.atleast_2d(insignificant_pair) == x_in_group)
                        for n_rows in range(len(rows)):
                            if cols[n_rows] == 0:
                                if insignificant_pair[rows[n_rows]][1] not in group[count]:
                                    group[count].append(insignificant_pair[rows[n_rows]][1])
                            elif cols[n_rows] == 1:
                                if insignificant_pair[rows[n_rows]][0] not in group[count]:
                                    group[count].append(insignificant_pair[rows[n_rows]][0])
                count += 1

        n_groups = len(group)

    else:
        print('Clustering based on motion performance currently inactive as not enough motion metrics provided by manufacturers')

# Define Expected Centroids of Groups
a_mu_x_guess = [np.mean([dist[v] for v in group[i] if v != 0]) for i in range(n_groups)]
mu_x_guess = np.sort(a_mu_x_guess)

# 5. Expectation Maximization for Future Classification
max_dist_t = np.sqrt(26 * 1**2)
max_dist_m = np.sqrt(2 * 1**2)
n_rob = n_robots

motion_performance = dist_m[:n_robots]
x_i_2 = np.column_stack((dist[:n_robots], motion_performance[:n_robots]))
mu_y_guess = np.ones(n_groups) * np.mean(motion_performance)

table_means = [{'mu': [mu_x_guess[nn], mu_y_guess[nn]]} for nn in range(n_groups)]
cov = 0.1
table_covariances = [{'cov': [[cov, 0], [0, cov]]} for _ in range(n_groups)]

#Get Covariances


# table_means = [{'mu': np.array([mu_x_guess[nn], mu_y_guess[nn]])} for nn in range(n_groups)]
# cov = 0.1
# table_covariances = [{'cov': cov * np.ones((2, 2))} for nn in range(n_groups)]
P = np.ones(n_groups) / n_groups

threshold = 2
number_iterations = 1

while number_iterations < threshold:
    sum_P = 0
    P_x_in_g = np.zeros(n_groups)
    b = np.zeros((n_groups, n_rob))

    for robot_i in range(n_rob):
        for group_i in range(n_groups):
            diff = x_i_2[robot_i, :] - table_means[group_i]['mu']
            P_x_in_g[group_i] = (1 / np.sqrt(2 * np.pi * np.linalg.norm(table_covariances[group_i]['cov']))) * \
                                np.exp(-0.5 * diff @ np.linalg.inv(table_covariances[group_i]['cov']) @ diff.T)
            sum_P += P_x_in_g[group_i] * P[group_i]

        for group_i in range(n_groups):
            b[group_i, robot_i] = (P_x_in_g[group_i] * P[group_i]) / sum_P

    for group_i in range(n_groups):
        P[group_i] = np.sum(b[group_i, :]) / n_rob
        table_means[group_i]['mu'] = np.sum((b[group_i, :] / (n_rob * P[group_i]))[:, None] * x_i_2, axis=0)
        diff = x_i_2 - table_means[group_i]['mu']
        table_covariances[group_i]['cov'] = np.sum((b[group_i, :] / (n_rob * P[group_i]))[:, None, None] * 
                                                   (diff[:, :, None] @ diff[:, None, :]), axis=0)

    number_iterations += 1

# # Result prints:
# print(probs)
# print(table_means)
# print(table_covariances)

# # Boxplots
# x_bp = (x_norm_t.T[0:14]).T
# #print(probs)
# plt.figure(figsize=(10, 6))
# plt.boxplot(x_bp, patch_artist=True)  # Transpose to get boxplots for each row
# plt.title('Distribution of the Tactile Metric Scores Among the Tested Manipulators',fontsize=20, fontname='Times New Roman')
# plt.xlabel('Robot',fontsize=18, fontname='Times New Roman',labelpad=20)
# plt.ylabel('Tactility Metric Scores', fontsize=18, fontname='Times New Roman',labelpad=20)
# labels = ['FE', 'LBR', 'UR5e', 'UR10e', 'Yu+', 'Gen3', 'TM5', 'FR3', 'M0609', 'GoFa', 'HC10','','','']
# plt.xticks(ticks=np.arange(1, 15), labels=labels, rotation=45, fontsize=12, fontname='Times New Roman')
#  # Annotate significant differences
# for i in range(0,14):#x_bp.shape[0]):
#     i_n = 0
#     for j in range(0,14):#i + 1, x_bp.shape[0]):
#         if probs[i, j] > 0.05:  # Adjust the threshold as needed
#                 y = max(np.max(x_bp[i]), np.max(x_bp[j])) + i*0.1 +i_n*0.02+0.2  # Adjust the position as needed
#                 plt.plot([i + 1, j + 1], [y, y], color='red')  # Draw line between boxplots
#                 plt.plot([i + 1, i + 1], [y, y-0.01], color='red')  # Draw line between boxplots
#                 plt.plot([j + 1, j + 1], [y, y-0.01], color='red')  # Draw line between boxplots
#                 plt.text((i + j + 2) / 2, y, '*', ha='center', va='bottom', color='red')
#                 i_n = i_n+1

# plt.savefig(os.path.join("Results","significance_plot.pdf"), format='pdf')
# plt.show()


# # Plot
# p_values = np.arange(0.15, 1.2, 0.4)

# fig = plt.figure(figsize=(9, 9))

# plt.scatter(x_i_2[:,0], x_i_2[:,1], c='blue', alpha=0.5,marker='o', s=100)

# for n_gen in range(len(table_means)):
#     plt.scatter(table_means[n_gen]['mu'][0], table_means[n_gen]['mu'][1], c='green', alpha=0.5, marker='x')
#     for p in p_values:
#         s = -2 * np.log(1 - p)
#         t = np.linspace(0, 2 * np.pi, num=100)
#         D_1, V_1 = np.linalg.eig(table_covariances[n_gen]['cov'] * s)
#         D_1 = np.diag(D_1).T
#         a_1 = np.dot(V_1, np.sqrt(D_1)) @ np.array([np.cos(t), np.sin(t)])
#         plt.plot(a_1[0] + table_means[n_gen]['mu'][0], a_1[1] + table_means[n_gen]['mu'][1], linestyle=':', linewidth=2, color='green')

# plt.xlabel("Tactility Fitness", fontsize=20, fontname='Times New Roman',labelpad=20)
# plt.ylabel("Motion Fitness", fontsize=20, fontname='Times New Roman',labelpad=20)
# plt.xlim([-0.5, 5.2])
# plt.ylim([-0.5, 1.5])
# plt.tick_params(axis='x', pad=10)
# plt.tick_params(axis='y', pad=10)
# plt.yticks(np.arange(-0.5, 1.1, 0.5), fontsize=20, fontname='Times New Roman')
# plt.xticks(np.arange(-0.5, 5.1, 1), fontsize=20, fontname='Times New Roman')
# plt.savefig(os.path.join("Results","fitness_graph_2D.pdf"), format='pdf')

# plt.show()

# Plot grouped data
# plt.figure()
# plt.scatter(x_i_2[:, 0], x_i_2[:, 1], color=gray_color)
# plt.xlabel('Tactile metric')
# plt.ylabel('Motion metric')
# plt.xlim([0, max_dist_t])
# plt.ylim([0, max_dist_m])
# plt.show()

# print(x_i_2)
# print(n_groups)



# ROBOTS TO GENUS GROUPS

dist_cent = np.zeros((n_robots, n_groups))
closest_centroid = np.zeros(n_robots, dtype=int)
for iii in range(n_robots):
    dist_cent_min = 1000
    for n in range(n_groups):
        dist_cent[iii, n] = np.linalg.norm(table_means[n]['mu'] - x_i_2[iii, :])
        if dist_cent[iii, n] < dist_cent_min:
            dist_cent_min = dist_cent[iii, n]
            closest_centroid[iii] = int(n+1)

#print(int(closest_centroid[1]))

# Connect to the database
database_path = os.path.join("Database", "tor_database.db")
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# a) Create and fill in robot table

# Drop the table if it exists
cursor.execute('DROP TABLE IF EXISTS robots')

# Create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS robots (
    robot_id INTEGER PRIMARY KEY,
    name TEXT,
    serial_number TEXT,
    system_version TEXT,
    datasheet TEXT,
    motion_performance NUMERIC,
    tactility_performance NUMERIC,
    genus_ID INTEGER
)
'''
cursor.execute(create_table_query)
robot_id = 1  # Initialize robot_id to start from 1

for robot in range(n_robots):
    if robot > 13:
        if n_dummy_robots > 0:
            robotname = 'dummy_bot'
            serialnumber = 'dummy_number'
            system_version = 'dummy_version'
            datasheet = 'not_available'
        else:
            xml_path = os.path.join("07_Robot_Ext_URDFs", f"{robot}_ext_urdf", "ext_urdf.xml")
            tree = ET.parse(xml_path)
            root = tree.getroot()
            robotname = root.attrib['name']
            serialnumber = root.attrib['serial_number']
            system_version = root.attrib['system_version']
            datasheet = root.attrib['datasheet']
    else:
        xml_path = os.path.join("07_Robot_Ext_URDFs", f"{robot}_ext_urdf", "ext_urdf.xml")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        robotname = root.attrib['name']
        serialnumber = root.attrib['serial_number']
        system_version = root.attrib['system_version']
        datasheet = root.attrib['datasheet']

    cursor.execute('''
    INSERT INTO robots (name, serial_number, system_version, datasheet, motion_performance, tactility_performance, genus_ID)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (robotname, serialnumber, system_version, datasheet, x_i_2[robot,1], x_i_2[robot,0], int(closest_centroid[robot])))

# b) Create genus table

# Drop the table if it exists
cursor.execute('DROP TABLE IF EXISTS genus')

# Create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS genus (
    genus_id INTEGER PRIMARY KEY,
    name TEXT,
    centroid_motion_direction NUMERIC,
    centroid_tactility_direction NUMERIC,
    covariance_matrix_comp1_1 NUMERIC,
    covariance_matrix_comp1_2 NUMERIC,
    covariance_matrix_comp2_1 NUMERIC,
    covariance_matrix_comp2_2 NUMERIC
)
'''
cursor.execute(create_table_query)

# Add genus to the table
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for gr in range(n_groups):
    groupname = alphabet[gr]
    centroid_motion_direction = table_means[gr]['mu'][1]  
    centroid_tactility_direction = table_means[gr]['mu'][0]  
    covariance_matrix_comp1_1 = table_covariances[gr]['cov'][0][0]  
    covariance_matrix_comp1_2 = table_covariances[gr]['cov'][0][1]  
    covariance_matrix_comp2_1 = table_covariances[gr]['cov'][1][0]  
    covariance_matrix_comp2_2 = table_covariances[gr]['cov'][1][1]
    cursor.execute('''
    INSERT INTO genus (name, centroid_motion_direction, centroid_tactility_direction, covariance_matrix_comp1_1, covariance_matrix_comp1_2, covariance_matrix_comp2_1, covariance_matrix_comp2_2)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (groupname, centroid_motion_direction, centroid_tactility_direction, covariance_matrix_comp1_1, covariance_matrix_comp1_2, covariance_matrix_comp2_1, covariance_matrix_comp2_2))

# Commit changes and close the connection
conn.commit()
conn.close()
# %%