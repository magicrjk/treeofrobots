import importlib
accrepres = importlib.import_module("01_Force_Sensing.accrepres").accrepres
timeconsistency = importlib.import_module("01_Force_Sensing.timeconsistency").timeconsistency
c_accrepres = importlib.import_module("02_Force_Controller.AcF_PcF_REScF_OV_TS.c_accrepres").c_accrepres
c_ov_ts = importlib.import_module("02_Force_Controller.AcF_PcF_REScF_OV_TS.c_ov_ts").c_ov_ts
cB_results = importlib.import_module("02_Force_Controller.Bc.cB_results").cB_results
Minimum_applicable_force = importlib.import_module("02_Force_Controller.MAF.Minimum_applicable_force").Minimum_applicable_force
c_mat_vel_accrepres  = importlib.import_module("02_Force_Controller.MVC_IS.c_mat_vel_accrepres").c_mat_vel_accrepres
CS = importlib.import_module("03_Force_Reaction.CS").CS
tactile_CS = importlib.import_module("03_Force_Reaction.tactile_CS").tactile_CS
St_Sq_evaluation = importlib.import_module("04_Human_Safety.St_Sq_evaluation").St_Sq_evaluation
Teaching_metrics = importlib.import_module("05_Teaching.GF_GD_GE_ME.Teaching_metrics").Teaching_metrics #05_Teaching/GF_GD_GE_ME/Teaching_metrics.py
MF_evaluation = importlib.import_module("05_Teaching.MF.MF_evaluation").MF_evaluation
import numpy as np
import os
import sqlite3

def robot_tactility(new_robot_number):
    if new_robot_number == 5:
        range_ = list(range(14))
        robot_init = 14
    else:
        range_ = [new_robot_number]
        robot_init = 15

    print('Running tactile metrics evaluations, please wait...')
    
    sens_acc = np.full(robot_init, np.nan)
    sens_pres = np.full(robot_init, np.nan)
    sens_res = np.full(robot_init, np.nan)
    sens_tc1 = np.full(robot_init, np.nan)
    sens_tc2 = np.full(robot_init, np.nan)
    sens_tc3 = np.full(robot_init, np.nan)
    sens_tc4 = np.full(robot_init, np.nan)
    cont_acc = np.full(robot_init, np.nan)
    cont_pres = np.full(robot_init, np.nan)
    cont_res = np.full(robot_init, np.nan)
    cont_maf = np.full(robot_init, np.nan)
    cont_cB = np.full(robot_init, np.nan)
    cont_ts = np.full(robot_init, np.nan)
    cont_mvc = np.full(robot_init, np.nan)
    cont_ov = np.full(robot_init, np.nan)
    cont_is = np.full(robot_init, np.nan)
    freact_cs = np.full(robot_init, np.nan)
    freact_tcs = np.full(robot_init, np.nan)
    safe_St = np.full(robot_init, np.nan)
    safe_Sq = np.full(robot_init, np.nan)
    teach_GF = np.full(robot_init, np.nan)
    teach_GD = np.full(robot_init, np.nan)
    teach_GE = np.full(robot_init, np.nan)
    teach_ME = np.full(robot_init, np.nan)
    teach_MF = np.full(robot_init, np.nan)

    for metrics_set in range(5):
        if metrics_set == 0:
            n_evaluation_sets = 2
        elif metrics_set == 1:
            n_evaluation_sets = 6
        elif metrics_set == 2:
            n_evaluation_sets = 2
        elif metrics_set == 3:
            n_evaluation_sets = 1
        elif metrics_set == 4:
            n_evaluation_sets = 2

        for i in range_:
            no_info = False

            if metrics_set == 0:
                for evaluation in range(1, n_evaluation_sets + 1):
                    if evaluation == 1:
                        robot_series_name = os.path.join("01_Force_Sensing", f"{i}_accrepres")
                    elif evaluation == 2:
                        robot_series_name = os.path.join("01_Force_Sensing", f"{i}_timeconsistency")
                    else:
                        print('not existing metric evaluation')
                    
                    if not os.path.exists(robot_series_name):
                        print('no such robot dataset: ', robot_series_name)
                        no_info = True
                    
                    pos = "C"
                    position_series_name = os.path.join(robot_series_name, f"{pos}_files")
                    
                    if not os.path.exists(position_series_name):
                        print('no such position dataset: ', position_series_name)
                        no_info = True

                    if evaluation == 1:
                        if no_info:
                            sens_acc[i] = np.nan
                            sens_pres[i] = np.nan
                            sens_res[i] = np.nan
                        else:
                            sens_acc[i], sens_pres[i], sens_res[i] = accrepres(i,position_series_name)
                    elif evaluation == 2:
                        if no_info:
                            sens_tc1[i] = np.nan
                            sens_tc2[i] = np.nan
                            sens_tc3[i] = np.nan
                            sens_tc4[i] = np.nan
                        else:
                            sens_tc1[i], sens_tc2[i], sens_tc3[i], sens_tc4[i] = timeconsistency(i, position_series_name)

            elif metrics_set == 1:
                for evaluation in range(1, n_evaluation_sets + 1):
                    if evaluation == 1 or evaluation == 2:
                        robot_series_name = os.path.join("02_Force_Controller", "AcF_PcF_REScF_OV_TS", f"{i}_c_accrepres")
                    elif evaluation == 3 or evaluation == 4:
                        robot_series_name = os.path.join("02_Force_Controller", "Bc", f"{i}_cB")
                    elif evaluation == 5:
                        robot_series_name = os.path.join("02_Force_Controller", "MAF", f"{i}_minforce")
                    elif evaluation == 6:
                        robot_series_name = os.path.join("02_Force_Controller", "MVC_IS", f"{i}_c_accrepres")
                    else:
                        print('not existing metric evaluation')
                    
                    if not os.path.exists(robot_series_name):
                        print('no such robot dataset: ', robot_series_name)
                        no_info = True
                    
                    pos = "C"
                    position_series_name = os.path.join(robot_series_name, f"{pos}_files")
                    
                    if not os.path.exists(position_series_name):
                        print('no such position dataset:',  position_series_name)
                        no_info = True

                    if evaluation == 1:
                        if no_info:
                            cont_acc[i] = np.nan
                            cont_pres[i] = np.nan
                            cont_res[i] = np.nan
                            no_info = False
                        else:
                            cont_acc[i], cont_pres[i], cont_res[i] = c_accrepres(i, position_series_name)
                    elif evaluation == 2:
                        if no_info:
                            cont_ov[i] = np.nan
                            cont_ts[i] = np.nan
                            no_info = False
                        else:
                            cont_ov[i], cont_ts[i] = c_ov_ts(i,position_series_name)
                    elif evaluation == 3 or evaluation == 4:
                        if no_info:
                            cont_cB[i] = np.nan
                            no_info = False
                        else:
                            cont_cB[i] = cB_results(i,position_series_name)
                        no_info = False
                    elif evaluation == 5:
                        if no_info:
                            cont_maf[i] = np.nan
                            no_info = False
                        else:
                            cont_maf[i] = Minimum_applicable_force(i,position_series_name)
                    elif evaluation == 6:
                        if no_info:
                            cont_mvc[i] = np.nan
                            cont_is[i] = np.nan
                            no_info = False
                        else:
                            cont_mvc[i], cont_is[i] = c_mat_vel_accrepres(i)
                    else:
                        print('no such evaluation')

            elif metrics_set == 2:
                print(evaluation)
                for evaluation in range(1, n_evaluation_sets + 1):
                    if evaluation == 1 or evaluation == 2:
                        robot_series_name = os.path.join("03_Force_Reaction", f"{i}_contactsens")
                    else:
                        print('not existing metric evaluation')
                    
                    if not os.path.exists(robot_series_name):
                        print('no such robot dataset: ',robot_series_name)
                        no_info = True
                    
                    pos = "C"
                    position_series_name = os.path.join(robot_series_name, f"{pos}_files")
                    
                    if not os.path.exists(position_series_name):
                        print('no such position dataset: ',position_series_name)
                        no_info = True

                    if evaluation == 1:
                        if no_info:
                            freact_cs[i] = np.nan
                            no_info = False
                        else:
                            freact_cs[i] = CS(i, position_series_name)
                    elif evaluation == 2:
                        print("entered tactile if part")
                        if no_info:
                            print("no info stated")
                            freact_tcs[i] = np.nan
                            no_info = False
                        else:
                            print("tactile CS")
                            freact_tcs[i] = tactile_CS(i,position_series_name)

            elif metrics_set == 3:
                
                for evaluation in range(1, n_evaluation_sets + 1):
                    if evaluation == 1:
                        robot_series_name = os.path.join("04_Human_Safety", f"{i}_colltests")
                    else:
                        print('not existing metric evaluation')
                    
                    if not os.path.exists(robot_series_name):
                        print('no such robot dataset: ', robot_series_name)
                        no_info = True
                    
                    pos = "C"
                    position_series_name = os.path.join(robot_series_name, f"{pos}_files")
                    
                    if not os.path.exists(position_series_name):
                        print('no such position dataset: ',position_series_name)
                        no_info = True

                    if evaluation == 1:
                        if no_info:
                            safe_St[i] = np.nan
                            safe_Sq[i] = np.nan
                            no_info = False
                        else:
                            safe_St[i], safe_Sq[i] = St_Sq_evaluation(i,position_series_name)
            
            elif metrics_set == 4:
                for evaluation in range(1, n_evaluation_sets + 1):
                    if evaluation == 1:
                        robot_series_name = os.path.join("05_Teaching", "GF_GD_GE_ME",f"{i}_guidetests")
                    elif evaluation == 2:
                        robot_series_name = os.path.join("05_Teaching", "MF", f"{i}_guidingforce_slow")
                    else:
                        print('not existing metric evaluation')
                    
                    if not os.path.exists(robot_series_name):
                        print('no such robot dataset: ',robot_series_name)
                        no_info = True
                    
                    pos = "C"
                    position_series_name = os.path.join(robot_series_name, f"{pos}_files")
                    
                    if not os.path.exists(position_series_name):
                        print('no such position dataset: ',position_series_name)
                        no_info = True

                    if evaluation == 1:
                        if no_info:
                            teach_GF[i] = np.nan
                            teach_GD[i] = np.nan
                            teach_GE[i] = np.nan
                            teach_ME[i] = np.nan
                            no_info = False
                        else:
                            teach_GF[i], teach_GD[i], teach_GE[i], teach_ME[i] = Teaching_metrics(i, position_series_name)
                    elif evaluation == 2:
                        if no_info:
                            teach_MF[i] = np.nan
                            no_info = False
                        else:
                            teach_MF[i] = MF_evaluation(i, position_series_name)

    # Save results to SQLite database
    database_path = os.path.join("Database", "tor_database.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    

    if new_robot_number == 5:
        range_val = list(range(14))
    else:
        range_val = new_robot_number
    range_val_1 = [range_val] if isinstance(range_val, (int, np.integer)) else range_val

    if len(range_val_1) > 1:
        cursor.execute('''DROP TABLE IF EXISTS robot_tactility_metrics''')

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS robot_tactility_metrics (
            robot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sens_acc REAL, sens_pres REAL, sens_res REAL, sens_tc1 REAL, sens_tc2 REAL, sens_tc3 REAL, sens_tc4 REAL,
            cont_acc REAL, cont_pres REAL, cont_res REAL, cont_cB REAL, cont_ts REAL, cont_maf REAL, cont_mvc REAL, cont_ov REAL, cont_is REAL,
            teach_GF REAL, teach_GD REAL, teach_MF REAL, teach_GE REAL, teach_ME REAL,
            freact_tcs REAL, freact_cs REAL,
            safe_St REAL, safe_Sq REAL
        )
        '''
        cursor.execute(create_table_query)

        for i in range_val:
            cursor.execute('''
            INSERT OR REPLACE INTO robot_tactility_metrics (
                sens_acc, sens_pres, sens_res, sens_tc1, sens_tc2, sens_tc3, sens_tc4, 
                cont_acc, cont_pres, cont_res, cont_cB, cont_ts, cont_maf, cont_mvc, cont_ov, cont_is,
                teach_GF, teach_GD, teach_MF, teach_GE, teach_ME,
                freact_tcs, freact_cs,
                safe_St, safe_Sq
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sens_acc[i], sens_pres[i], sens_res[i], sens_tc1[i], sens_tc2[i], sens_tc3[i], sens_tc4[i], 
                cont_acc[i], cont_pres[i], cont_res[i], cont_cB[i], cont_ts[i], cont_maf[i], cont_mvc[i], cont_ov[i], cont_is[i],
                teach_GF[i], teach_GD[i], teach_MF[i], teach_GE[i], teach_ME[i],
                freact_tcs[i], freact_cs[i],
                safe_St[i], safe_Sq[i]
            ))
    else:
        i = range_val
        cursor.execute('''
        INSERT OR REPLACE INTO robot_tactility_metrics (
            sens_acc, sens_pres, sens_res, sens_tc1, sens_tc2, sens_tc3, sens_tc4, 
            cont_acc, cont_pres, cont_res, cont_cB, cont_ts, cont_maf, cont_mvc, cont_ov, cont_is,
            teach_GF, teach_GD, teach_MF, teach_GE, teach_ME,
            freact_tcs, freact_cs,
            safe_St, safe_Sq
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sens_acc[i], sens_pres[i], sens_res[i], sens_tc1[i], sens_tc2[i], sens_tc3[i], sens_tc4[i], 
            cont_acc[i], cont_pres[i], cont_res[i], cont_cB[i], cont_ts[i], cont_maf[i], cont_mvc[i], cont_ov[i], cont_is[i],
            teach_GF[i], teach_GD[i], teach_MF[i], teach_GE[i], teach_ME[i],
            freact_tcs[i], freact_cs[i],
            safe_St[i], safe_Sq[i]
        ))

    # for i in range_val:
    #     cursor.execute('''
    #     INSERT OR REPLACE INTO robot_tactility_metrics (
    #         sens_acc, sens_pres, sens_res, sens_tc1, sens_tc2, sens_tc3, sens_tc4, 
    #         cont_acc, cont_pres, cont_res, cont_cB, cont_ts, cont_maf, cont_mvc, cont_ov, cont_is,
    #         teach_GF, teach_GD, teach_MF, teach_GE, teach_ME,
    #         freact_tcs, freact_cs,
    #         safe_St, safe_Sq
    #     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     ''', (
    #         sens_acc[i], sens_pres[i], sens_res[i], sens_tc1[i], sens_tc2[i], sens_tc3[i], sens_tc4[i], 
    #         cont_acc[i], cont_pres[i], cont_res[i], cont_cB[i], cont_ts[i], cont_maf[i], cont_mvc[i], cont_ov[i], cont_is[i],
    #         teach_GF[i], teach_GD[i], teach_MF[i], teach_GE[i], teach_ME[i],
    #         freact_tcs[i], freact_cs[i],
    #         safe_St[i], safe_Sq[i]
    #     ))

    # cursor.execute('''CREATE TABLE IF NOT EXISTS robot_tactility_metrics (
    #                     robot_id INTEGER PRIMARY KEY,
    #                     sens_acc REAL, sens_pres REAL, sens_res REAL, sens_tc1 REAL, sens_tc2 REAL, sens_tc3 REAL, sens_tc4 REAL,
    #                     cont_acc REAL, cont_pres REAL, cont_res REAL, cont_cB REAL, cont_ts REAL, cont_maf REAL, cont_mvc REAL, cont_ov REAL, cont_is REAL,
    #                     teach_GF REAL, teach_GD REAL, teach_MF REAL, teach_GE REAL, teach_ME REAL,
    #                     freact_tcs REAL, freact_cs REAL,
    #                     safe_St REAL, safe_Sq REAL
                        
    #                   )''')

    # for i in range(1,15):
    #     cursor.execute('''INSERT OR REPLACE INTO robot_tactility_metrics VALUES ( ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    #                    (i, sens_acc[i], sens_pres[i], sens_res[i], sens_tc1[i], sens_tc2[i], sens_tc3[i], sens_tc4[i], 
    #                     cont_acc[i], cont_pres[i], cont_res[i], cont_cB[i], cont_ts[i], cont_maf[i], cont_mvc[i], cont_ov[i], cont_is[i],
    #                     teach_GF[i], teach_GD[i], teach_MF[i], teach_GE[i], teach_ME[i],
    #                     freact_tcs[i], freact_cs[i],
    #                     safe_St[i], safe_Sq[i],
    #                     ))
    
    conn.commit()
    conn.close()

    print("Completed tactile metrics evaluations and saved to 'robot_tactility.db'.")
