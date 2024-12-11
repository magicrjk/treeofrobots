import os
import time
import sys
import sqlite3
import shutil

sys.path.append(os.path.join("FlaskWebsite","modules","classification"))



def folder_contains_files(directory_path):
    for root, dirs, files in os.walk(directory_path):
        if files:
            print("The directory contains files.")
            return 1
    print("The directory is empty.")
    return 0

def read_txt_data():
    folder_path = os.path.join("FlaskWebsite", "uploads")  # Replace with the actual path to your folder
    txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
    data_array = []  # Initialize an empty array
    for txt_file in txt_files:
        with open(os.path.join(folder_path, txt_file), 'r') as file:  # Use the full file path
            lines = file.readlines()
            for line in lines:
                try:
                    # Convert each line to a float
                    data_array.append(float(line.strip()))
                except ValueError:
                    # Handle cases where the line cannot be converted to a float
                    print(f"Warning: Unable to convert line '{line.strip()}' to a float.")
    return data_array


#write init for classification based on new dummy robot with features
def init_for_classification_w_dummy(values):
# Create or overwrite the init.txt file for matlab
    
    file_path = "init_dummy.txt"  
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"{file_path} being written.")
    with open('init_dummy.txt', 'w') as file:
        for value in values:
            file.write(f"{value}\n")
    time.sleep(2)
    print("init_dummy.txt file created successfully!")

def write_init_matlab(values):
# Create or overwrite the init.txt file for matlab
    
    file_path = "init.txt"  
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"{file_path} being written.")
    with open('init.txt', 'w') as file:
        for value in values:
            file.write(f"{value}\n")
    time.sleep(2)

    print("init.txt file created successfully!")
    

def classification():

# if selected_new_robot_data < 1:
    print('Calling Python script for Genus Classification, please wait 20 seconds...')
    cmd = "python classification.py"
    returned_value = os.system(cmd)  # returns the exit code in unix
    time.sleep(30)
# else:

def classification_w_new_robot():
     print('Assigning data to correct folders ...')
     if folder_contains_files(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'new_robot'))) ==0:
         ()
         print ("No files in folder "+str(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', 'new_robot')))+" continuing without adding new robot")
     else:
          import files_transfer
          files_transfer.main()
          num_robot = files_transfer.find_num_robot()+1 #finds the current number of robots, and computes the robot number of the newly added robot (+1)
          #print(num_robot)
#          files_transfer.main() # it transfers the files
     robot_data_num = num_robot-1
     write_init_matlab([0,1, robot_data_num])
     print('Calling Python script for Genus Classification, please wait 20 seconds...')
     cmd = "python classification.py"
     returned_value = os.system(cmd)  # returns the exit code in unix
     time.sleep(180)

def reset_classification():
# this shall rewrite the original status of the database
    conn = sqlite3.connect(os.path.join('Database','tor_database.db'))
    cursor = conn.cursor()
    tables = ['robot_tactility_metrics', 'motion_metric_results']
    for table in tables:
        cursor.execute(f"DELETE FROM {table} WHERE robot_id > 14")
    conn.commit()
    conn.close()
    write_init_matlab([0,0,0])
    print('Calling Python script for Genus Classification, please wait 20 seconds...')
    cmd = "python classification.py"
    returned_value = os.system(cmd)  # returns the exit code in unix
    time.sleep(10)

def reevaluate_all_robots():
# this shall rewrite the original status of the database and reevlaute all data
    write_init_matlab([0,1,5])
    print('Calling Python script for Genus Classification, please wait 20 seconds...')
    cmd = "python classification.py"
    returned_value = os.system(cmd)  # returns the exit code in unix
    time.sleep(180)

def delete_folders_starting_with(prefix):
    for root, dirs, files in os.walk(".",topdown= True):
        for folder in dirs[:]:
            if folder.startswith(prefix):
                try:
                    shutil.rmtree(os.path.join(root, folder))
                    print(f"Deleted folder: {os.path.join(root, folder)}")
                except OSError as e:
                    print(f"Error deleting folder {os.path.join(root, folder)}: {e}")
# # INSERT THIS TO FLASK
# if selected_process_query == 1:
#      from Database.user_query_database import main
#      selected_robots = main()
#      print(selected_robots)
#      # Create or overwrite the init_robots.txt file for plotting
#      file_path = "init_robots.txt"  
#      if os.path.exists(file_path):
#         os.remove(file_path)
#      else:
#         print(f"{file_path} being written.")
#      with open('init_robots.txt', 'w') as file:
#         file.write(f"{selected_robots[0]}\n")
#         file.write(f"{selected_robots[1]}\n")
#         file.write(f"{selected_robots[2]}\n")

#      print("init_robots.txt file created successfully!")

#      #user_query_database()
#      from Visualization.robot_morphology_graph_generator import graph_drawing
#      from Visualization import fitness_plotting
#      #from Visualization import merge_graphics - NOT YET WORKING
# else:
#      file_path = "init_robots.txt"  
#      if os.path.exists(file_path):
#         os.remove(file_path)
#      else:
#         print(f"{file_path} being written.")
#      with open('init_robots.txt', 'w') as file:
#         file.write("0\n")
#         file.write("3\n")
#         file.write("12\n")
#      from Visualization.robot_morphology_graph_generator import graph_drawing
#      from Visualization import fitness_plotting
#      #from Visualization import merge_graphics - NOT YET WORKING
     

