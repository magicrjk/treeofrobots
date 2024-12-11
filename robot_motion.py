import pandas as pd
import os
import sqlite3

def robot_motion(new_robot_number):
    if new_robot_number == 5:
        range_ = list(range(14))
        robot_init = 14
    else:
        range_ = [new_robot_number]
        robot_init = 15

    print('Running motion metrics evaluations, please wait...')
    
    pos_acc = [None] * robot_init

    for i in range_:
        robot_series_name = os.path.join("06_Motion_Performance", f"{i}_motion_performance")
        os.makedirs(robot_series_name, exist_ok=True)

        filename = f'MotionData_{0}.csv'
        filepath = os.path.join(robot_series_name, filename)
        
        if not os.path.exists(filepath):
            print(f"Missing a dataset for motion performance evaluation. Filename: {filename}")
            print(f"Robot number {i}")
        else:
            data = pd.read_csv(filepath)
            pos_acc[i] = data.iloc[0, 0]

    fin = 1

    # Database operations
    database_path = os.path.join("Database", "tor_database.db")
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    if new_robot_number == 5:
        cursor.execute('DROP TABLE IF EXISTS motion_metric_results;')
        cursor.execute('''CREATE TABLE IF NOT EXISTS motion_metric_results (
                            mot_met_results_id INTEGER PRIMARY KEY,
                            robot_id INTEGER,
                            pos_rep NUMERIC
                          );''')

    for robot in range_:
        if pos_acc[robot] is not None:
            cursor.execute('''INSERT INTO motion_metric_results (robot_id, pos_rep)
                              VALUES (?, ?)''', (robot + 1, pos_acc[robot]))

    conn.commit()
    conn.close()

    print("Completed motion metrics evaluations and saved to the database.")
    return fin
