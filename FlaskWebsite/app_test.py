from flask import Flask, jsonify, send_file, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import zipfile
import sqlite3
import sys
import os
import io
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.patches as patches
import matplotlib.image as mpimg
from concurrent.futures import ProcessPoolExecutor
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator
import plotly.io as pio
import subprocess

from scipy.linalg import sqrtm

sys.path.append(os.path.join("FlaskWebsite","modules","robot_fitness_graph"))
from fitness_functions import hex_to_rgb, interpolate_color, confidence_ellipse

sys.path.append(os.path.join("FlaskWebsite","modules","classification"))
from classification_functions_py import init_for_classification_w_dummy, classification, write_init_matlab, classification_w_new_robot, reset_classification, delete_folders_starting_with, read_txt_data, reevaluate_all_robots

sys.path.append(os.path.join("FlaskWebsite","modules","query"))
from query_functions import generate_init_robots


sys.path.append(os.path.join("FlaskWebsite","modules","robot_morphology_graph"))
from graphviz import Graph
from robot_graph_constructor import RobotGraphConstructor
from graph_variables import top_nodes_dict, c_nodes_dict, m_nodes_dict, s_nodes_dict, a_nodes_dict, o_nodes_dict, struct_dict
from parser_helpers import add_struct_nodes, add_nodes, add_edges, interpolate_color

sys.path.append(os.path.join("FlaskWebsite","modules","robot_radar_graph"))
from radar_graph import radar_factory

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024
app.debug = False
global_var = {}

class MyFlaskApp:
    g = None
    m_dict = None
    s_dict = None
    a_dict = None
    o_dict = None 


    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.app.config['UPLOAD_FOLDER'] = os.path.join('FlaskWebsite', 'uploads')
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Edit the path to the database if necessary
        #database = os.path.join("Database", "processes_database.db")
        #conn = self.connect_to_database(database)
        #self.cursor = conn.cursor()
        self.query_robot_data() # Keep a copy of the robot data query, so we don't fetch it every time 
        #conn.close()

    



    def setup_routes(self):
        @self.app.route('/')
        def index(): # For getting robot recommendations
           return render_template('index.html')
        

        @self.app.route('/tree')
        def tree(): # For getting robot recommendations
           return render_template('tree.html')
        
        @self.app.route('/process')
        def process(): # For getting robot recommendations
           return render_template('process.html')
        
        @self.app.route('/metrics')
        def metrics(): # For getting robot recommendations
           return render_template('metrics.html')
        
        @self.app.route('/imprint')
        def imprint(): # For getting robot recommendations
           return render_template('imprint.html')
        
        @self.app.route('/privacy')
        def privacy(): # For getting robot recommendations
           return render_template('privacy.html')
        
        @self.app.route('/robot')
        def robot(): # For getting robot recommendations
           
           global global_var
           global_var['selected_robots'] = request.args.getlist("robot_id", type=int)
           selected_robots=global_var.get('selected_robots','not set')
           generate_init_robots(selected_robots)
           robot_numbers = self.retrieve_robot_numbers() # Get the robots that correspond to the processes           
           database = os.path.join("Database", "tor_database.db")
           conn = self.connect_to_database(database) 

           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_name_tuple = self.cursor.fetchone()
           robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
           self.cursor.execute("SELECT serial_number FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_sn_tuple = self.cursor.fetchone()
           robot_sn = robot_sn_tuple[0] if robot_sn_tuple else "Unknown Robot"
           self.cursor.execute("SELECT motion_performance FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_mf_tuple = self.cursor.fetchone()
           robot_mf = robot_mf_tuple[0] if robot_mf_tuple else "Unknown Robot"
           self.cursor.execute("SELECT tactility_performance FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_tf_tuple = self.cursor.fetchone()
           robot_tf = robot_tf_tuple[0] if robot_tf_tuple else "Unknown Robot"
           self.cursor.execute("SELECT genus_ID FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_g_tuple = self.cursor.fetchone()
           robot_g = robot_g_tuple[0] if robot_g_tuple else "Unknown Robot"
           self.cursor.execute("SELECT system_version FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_sv_tuple = self.cursor.fetchone()
           robot_sv = robot_sv_tuple[0] if robot_sv_tuple else "Unknown Robot"
           self.cursor.execute("SELECT datasheet FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_ds_tuple = self.cursor.fetchone()
           robot_ds = robot_ds_tuple[0] if robot_ds_tuple else "Unknown Robot"
           self.cursor.close()
           conn.close()
           self.construct_morphology_graph() # Set up the morphology graph
           self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
           self.construct_fitness_graph(False, False) # Construct the fitness graph, and save it under ./static/fitness_graph.png
           return render_template('robot01.html', text_input=[robot_name,selected_robots, robot_sn, robot_mf, robot_tf, robot_g, robot_sv, robot_ds], images=["fitness_graph", "morphology_graph",robot_name, robot_name])
        
        @self.app.route('/robot2')
        def robot2(): # For getting robot recommendations
           
           selected_robots=global_var.get('selected_robots','not set')
           robot_numbers = self.retrieve_robot_numbers() # Get the robots that correspond to the processes           
           database = os.path.join("Database", "tor_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_name_tuple = self.cursor.fetchone()
           robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
           self.cursor.close()
           conn.close()
           self.construct_morphology_graph() # Set up the morphology graph
           self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
           self.construct_fitness_graph(False, False) # Construct the fitness graph, and save it under ./static/fitness_graph.png
           return render_template('robot01.html', text_input=[robot_name,selected_robots], images=["fitness_graph", "morphology_graph",robot_name, robot_name])
        
        @self.app.route('/robot_tac')
        def robot_tac(): # For getting robot recommendations
           
           selected_robots=global_var.get('selected_robots','not set')
           robot_numbers = self.retrieve_robot_numbers() # Get the robots that correspond to the processes           
           database = os.path.join("Database", "tor_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_name_tuple = self.cursor.fetchone()
           robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
           self.cursor.close()
           conn.close()
           self.construct_morphology_graph() # Set up the morphology graph
           self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
           self.construct_fitness_graph(False, False) # Construct the fitness graph, and save it under ./static/fitness_graph.png
           return render_template('robot_tac.html', text_input=robot_name, images=["fitness_graph", "morphology_graph",robot_name, robot_name])
        
        @self.app.route('/robot_loc')
        def robot_loc(): # For getting robot recommendations
           
           selected_robots=global_var.get('selected_robots','not set')
           robot_numbers = self.retrieve_robot_numbers() # Get the robots that correspond to the processes           
           database = os.path.join("Database", "tor_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(selected_robots[0]),))
           robot_name_tuple = self.cursor.fetchone()
           robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
           self.cursor.close()
           conn.close()
           self.construct_morphology_graph() # Set up the morphology graph
           self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
           self.construct_fitness_graph(False, False) # Construct the fitness graph, and save it under ./static/fitness_graph.png
           return render_template('robot_loc.html', text_input=robot_name, images=["fitness_graph", "morphology_graph",robot_name, robot_name])
        
        

        @app.route('/figure')
        def figure():
            return render_template('figure.html')

        @self.app.route('/process/example')
        def process_example(): # For getting robot recommendations
           global global_var
           global_var['selected_process'] = request.args.getlist("process_id", type=int)
           selected_process=global_var.get('selected_process','not set')
           database = os.path.join("Database", "processes_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           process_name_tuple = self.cursor.fetchone()
           process_name = process_name_tuple[0] if process_name_tuple else "Unknown Process"
           self.cursor.execute("SELECT description FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           des_tuple = self.cursor.fetchone()
           description = des_tuple[0] if des_tuple else "Unknown Process"

           self.cursor.execute("""
           SELECT basic_operation1_ID, basic_operation2_ID, basic_operation3_ID, 
           basic_operation4_ID, basic_operation5_ID, basic_operation6_ID, 
           basic_operation7_ID, basic_operation8_ID 
           FROM processes 
           WHERE process_id = ?
           """, (str(selected_process[0]),))
           bos = self.cursor.fetchone()  
           bos_ids = [id for id in bos if id is not None]
           bos_names = []
           bos_desc = []
           feat_names=[]
           feat_desc=[]
           feat_mdesc=[]
           feature_list = []
           for id in bos_ids:
                self.cursor.execute("SELECT name FROM basic_operations WHERE basic_operation_ID = ?", (id,))
                name = self.cursor.fetchone()
                self.cursor.execute("SELECT description FROM basic_operations WHERE basic_operation_ID = ?", (id,))
                desc = self.cursor.fetchone()
                if name:
                    bos_names.append(name[0])  
                    bos_desc.append(desc[0]) 
           global_var['basic_operation_names'] = bos_names
           global_var['basic_operation_desc'] = bos_desc
           
           for ids in bos_ids:
            self.cursor.execute("""
            SELECT feature1_ID, feature2_ID, feature3_ID, 
            feature4_ID
            FROM basic_operations
            WHERE basic_operation_id = ?
            """, (str(ids),))
            features = self.cursor.fetchone()  
            if features:
                for feature in features:
                 feature_list.append(feature)

           feat_ids = [id for id in feature_list if id is not None]
           feat_ids = list(set(feat_ids))
           print("this is feats_ids:")
           print(feat_ids)
           for id in feat_ids:
                self.cursor.execute("SELECT name FROM features WHERE feature_ID = ?", (id,))
                name = self.cursor.fetchone()
                self.cursor.execute("SELECT description FROM features WHERE feature_ID = ?", (id,))
                desc = self.cursor.fetchone()
                self.cursor.execute("SELECT math_description FROM features WHERE feature_ID = ?", (id,))
                math_desc = self.cursor.fetchone()
                if name:
                    feat_names.append(name[0])  
                    feat_desc.append(desc[0]) 
                    feat_mdesc.append(math_desc[0])
           global_var['feat_ids'] = feat_ids
           global_var['feat_names'] = feat_desc
           self.cursor.close()
           conn.close()
           return render_template('process-example.html', text_input=[process_name,description], images=[process_name])
        
        @self.app.route('/process/example2')
        def process_example2(): # For getting robot recommendations
           
           selected_process=global_var.get('selected_process','not set')
           database = os.path.join("Database", "processes_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           process_name_tuple = self.cursor.fetchone()
           process_name = process_name_tuple[0] if process_name_tuple else "Unknown Process"
           self.cursor.execute("SELECT description FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           des_tuple = self.cursor.fetchone()
           description = des_tuple[0] if des_tuple else "Unknown Process"
           self.cursor.close()
           conn.close()
           return render_template('process-example.html', text_input=[process_name,description], images=[process_name])
        
        @self.app.route('/process/bos')
        def bos_example(): # For getting robot recommendations
           
           selected_process=global_var.get('selected_process','not set')
           bos_names=global_var.get('basic_operation_names','not set')
           bos_desc=global_var.get('basic_operation_desc','not set')
           feat_desc=global_var.get('feat_names','not set')
           database = os.path.join("Database", "processes_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           process_name_tuple = self.cursor.fetchone()
           process_name = process_name_tuple[0] if process_name_tuple else "Unknown Process"
           self.cursor.close()
           conn.close()
           

           return render_template('process-bos.html', text_input=bos_names, text_input_2=bos_desc, text_input_3=feat_desc, images=[process_name])
        
        @self.app.route('/process/qms')
        def qms_example(): # For getting robot recommendations
           selected_process=global_var.get('selected_process','not set')
           database = os.path.join("Database", "processes_database.db")
           conn = self.connect_to_database(database) 
           self.cursor = conn.cursor()
           self.cursor.execute("SELECT name FROM processes WHERE process_id = ?", (str(selected_process[0]),))
           process_name_tuple = self.cursor.fetchone()
           process_name = process_name_tuple[0] if process_name_tuple else "Unknown Process"
           required_feats = global_var.get('feat_ids', 'not set')
           required_feats = list(set(required_feats))
           required_feat_names = global_var.get('feat_names', 'not set')
        
           met_names = []
           met_desc = []
           metrics_list =[]

           for ids in required_feats:
            # Use parameterized query to prevent SQL injection
            self.cursor.execute("""
            SELECT process_quality_metric_ID FROM process_quality_metrics
            WHERE feature1_ID IN (?) OR feature2_ID IN (?) OR feature3_ID IN (?) OR feature4_ID IN (?) OR feature5_ID IN (?)
            """, (ids, ids, ids, ids, ids))

            metrics = self.cursor.fetchall()  # Use fetchall to get all matching rows
            for metric in metrics:
                 metrics_list.append(metric)
           met_ids = [id[0] for id in metrics_list if id[0] is not None]
           met_ids = list(set(met_ids))

           for id in met_ids:
            # Fetch name and description in a single query
                self.cursor.execute("""
                SELECT name, description FROM process_quality_metrics WHERE process_quality_metric_ID = ?
                """, (id,))
                result = self.cursor.fetchone()
        
                if result:
                    name, desc = result
                    met_names.append(name)
                    met_desc.append(desc)
           self.cursor.close()
           conn.close()

           return render_template('process-qms.html',text_input=required_feat_names, text_input_2=met_names, text_input_3=met_desc, images=[process_name])

        @self.app.route('/dummy_choice/dummy')
        def dummy(): # For adding a dummy robot
            return render_template('dummy_new.html')
        
        
        @self.app.route('/dummy_choice/dummy/dummy_result', methods=['POST'])
        def dummy_result(): # For displaying the dummy robot results, as well as the new graph
            global global_var
            global_var['dummy_name'] = request.form.get('text_input')
            dummy_name=global_var.get('dummy_name','not set')
            qualities = [request.form.get('fs_dropdown'), request.form.get('fc_dropdown'), request.form.get('u_dropdown'), request.form.get('fr_dropdown'), request.form.get('s_dropdown'), request.form.get('m_dropdown')]
            values = [0] * len(qualities) 
            # Assign a random value within the normalized range for low, med, high
            for i, quality in enumerate(qualities):
                if(quality == "none"):
                    values[i] = 0 # Has to be changed to being a NULL in the end
                elif(quality == "low"):
                    values[i] = np.random.uniform(low=0.1, high=0.33)
                elif(quality == "medium"):
                    values[i] = np.random.uniform(low=0.33, high=0.66)
                elif(quality == "high"):
                    values[i] = np.random.uniform(low=0.66, high=1)
            ideal_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 100, 0, 100, 0, 0, 0, 0, 0, 100, 100, 100, 100])
            worst_values = np.array([5, 1, 5, 1, 1, 1, 1, 5, 1, 5, 0, 5, 5, 0, 20, 0, 15, 5, 5, 5, 5, 0, 0,  0, 0])
            value_range = ideal_values-worst_values
            dummy_fs = abs((1-values[0])*value_range[0:7])
            dummy_fc1 = abs((1-values[1])*value_range[7:10])
            dummy_fc2 = abs(values[1]*value_range[10:11])
            dummy_fc3 = abs((1-values[1])*value_range[11:13])
            dummy_fc4 = abs(values[1]*value_range[13:14])
            dummy_fc5 = abs((1-values[1])*value_range[14:15])
            dummy_fc6 = abs(values[1]*value_range[15:16])
            dummy_mm = abs((1-values[2])*value_range[16:21])
            dummy_fr = abs(values[3]*value_range[21:23])
            dummy_s = abs(values[4]*value_range[23:25])
            dummy_m = abs((1.05-values[5])/2)
            robot_data_1 = list(np.concatenate((dummy_fs, dummy_fc1, dummy_fc2, dummy_fc3, dummy_fc4, dummy_fc5, dummy_fc6, dummy_mm, dummy_fr, dummy_s)))
            robot_data_2 = list(np.concatenate((dummy_fs, dummy_fc1, dummy_fc2, dummy_fc3, dummy_fc4, dummy_fc5, dummy_fc6, dummy_mm, dummy_fr, dummy_s, [dummy_m])))
            radar_img = self.generate_radar_graph(dummy_name, robot_data_1)
            
            reset_classification()

            #Generate the graph before the new robot is pushed
            write_init_matlab([0,0,0])
            generate_init_robots([0])
            time.sleep(1)
            classification()
            time.sleep(5)
            self.construct_fitness_graph(True, False)
           
            # Generate the new graph after the new robot has been added
            write_init_matlab([1,0,0])
            generate_init_robots([15])
            time.sleep(1)
            init_for_classification_w_dummy(robot_data_2)
            time.sleep(2)
            classification()
            time.sleep(5)
            
            self.query_robot_data()
            
            self.construct_fitness_graph(True, True)

            reset_classification()
            # Return the results with the images
            return render_template('dummy_result_new.html', text_input=dummy_name, 
                                    images=[radar_img, "fitness_graph_old", "fitness_graph_new"])


        @self.app.route('/upload_result_new', methods=['POST'])
        def upload_result_new(): # For processing the uploaded zip file
            global global_var
            global_var['dummy_name'] = request.form.get('text_input')
            self.app.debug = False
            if 'zipfile' not in request.files:
                return redirect(request.url)
            file = request.files['zipfile']
            if file.filename == '':
                return redirect(request.url)
            if file and file.filename.endswith('.zip'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Extract and list filenames in the zip
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    try:
                        
                        zip_ref.extractall(self.app.config['UPLOAD_FOLDER'])
                        
                    except Exception as e:
                        print(f"Error extracting files: {e}")
                    file_names = zip_ref.namelist()
                    # Implement check of correct data structure?
                

                return render_template('upload_result_new.html', file_names=file_names)
            return redirect(request.url)
        
        @self.app.route('/upload_result/new_robot_results', methods=['POST'])
        def new_robot_results(): # For displaying the results
            robot_counter = 14  #REPLACE BY NUMBER FROM YAML-READING ONCE MORE ROBOTS CAN BE ADDED 
            delete_folders_starting_with(f"{robot_counter}_")
            reset_classification()
            generate_init_robots([0])
            self.construct_fitness_graph(True, False)
            radar_img =[None]
            classification_w_new_robot()
            for filename in os.listdir(self.app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print('Upload folder emptied successfully!')
            self.query_robot_data()
            database = os.path.join("Database", "tor_database.db")
            conn = self.connect_to_database(database)
            new_robot = robot_counter+1
            robot_id, robot_data_1 = self.get_robot_metrics_results(conn, new_robot)
            #robot_name = self.get_robot_name(conn, new_robot) REPAIR
            dummy_name=global_var.get('dummy_name','not set')
            robot_name=dummy_name
            radar_img = self.generate_radar_graph(robot_name, robot_data_1)
            generate_init_robots([new_robot])
            robot_numbers = self.retrieve_robot_numbers() 
            self.construct_morphology_graph() # Set up the morphology graph
            self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
            self.construct_fitness_graph(True, True)
            conn.close()
            delete_folders_starting_with(str(robot_counter)+"_")
            reevaluate_all_robots()
            reset_classification()
            self.query_robot_data()


            return render_template('new_robot_results_new.html', text_input=robot_name, 
                                    images=[radar_img, "fitness_graph_old", "fitness_graph_new", "morphology_graph"])
          
        @self.app.route('/upload')
        def upload(): # For uploading new data
            return render_template('upload_new.html')

        @self.app.route('/sorry')
        def sorry(): # Spaceholder
            return render_template('Sorry.html')
        
        @self.app.route('/struct_dummy')
        def struct_dummy(): #structure file for dummy robot
            return render_template('StructDummy.html')
        
        @self.app.route('/struct_new')
        def struct_new(): # structure description for new robot
            return render_template('StructNew.html')
        
        @self.app.route('/use_cases')
        def use_cases(): # structure description for new robot
            return render_template('use_case_collection.html')
        
        @self.app.route('/query')
        def query(): # For getting TOR output for specific robot
            return render_template('query_new.html')
        
        @self.app.route('/query_result', methods=['POST'])
        def query_result(): # For displaying the branch of fix manipulators
            write_init_matlab([0,0,0])
            classification()
            selected_robots = request.form.getlist('robot')
            generate_init_robots(selected_robots)
            robot_numbers = self.retrieve_robot_numbers() # Get the robots that correspond to the processes
            database = os.path.join("Database", "tor_database.db")
            conn = self.connect_to_database(database) 
            self.construct_morphology_graph() # Set up the morphology graph
            self.populate_morphology_graph() # Populate the graph with the retrieved robot numbers, and save it under ./static/morphology_graph.png
            self.construct_fitness_graph(False, False) # Construct the fitness graph, and save it under ./static/fitness_graph.png
            conn.close()
            return render_template('query_result_new.html', images=["fitness_graph", "morphology_graph"])  # Pass to template
        
        @self.app.route('/query_result/metric_result', methods=['POST'])
        def metric_result(): # For displaying recommendation results
            
            database = os.path.join("Database", "tor_database.db")
            conn = self.connect_to_database(database)
            selected_robots = self.retrieve_robot_numbers()#[1,2,3] #FIX
            radar_img =[None]*len(selected_robots)
            for n in range(len(selected_robots)):
                robot_id, robot_data_1 = self.get_robot_metrics_results(conn, selected_robots[n])
                print(robot_id)
                robot_name = self.get_robot_name(conn, robot_id)
                radar_img[n] = self.generate_radar_graph(robot_name, robot_data_1)
            conn.close()
            return render_template('metric_result_new.html', images=radar_img)  # Pass to template
        
        @self.app.route('/dummy_choice/dummy_upload')
        def dummy_upload(): # For uploading new data
            #set back previous changes
            robot_counter =14
            delete_folders_starting_with(str(robot_counter)+"_")
            reset_classification()
            return render_template('dummy_upload_new.html')

        @self.app.route('/dummy_choice/dummy_upload_result', methods=['POST'])
        def dummy_upload_result(): # For adding a dummy robot
            #ADD HERE TO UPLOAD A zip-file with the init-dummy-data NOT YET WORKING
            global global_var
            global_var['dummy_name'] = request.form.get('text_input')
            dummy_name=global_var.get('dummy_name','not set')
            
            self.app.debug = False
            if 'zipfile' not in request.files:
                return redirect(request.url)
            file = request.files['zipfile']
            if file.filename == '':
                return redirect(request.url)
            if file and file.filename.endswith('.zip'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Extract and list filenames in the zip
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    try:
                        zip_ref.extractall(self.app.config['UPLOAD_FOLDER'])
                    except Exception as e:
                        print(f"Error extracting files: {e}")
                    file_names = zip_ref.namelist()
          
                return render_template('dummy_upload_result_new.html', file_names=file_names)
            return redirect(request.url)

        @self.app.route('/dummy_choice/dummy/dummy_w_m_result', methods=['POST'])
        def dummy_w_m_result(): # For displaying the dummy robot results, as well as the new graph
           
            dummy_name=global_var.get('dummy_name','not set')
            robot_data_1 = read_txt_data()
            radar_img = self.generate_radar_graph(dummy_name, robot_data_1)
            
            # Generate the graph before the new robot is pushed
            write_init_matlab([0,0,0])
            generate_init_robots([0])
            classification()
            self.query_robot_data()
            self.construct_fitness_graph(True, False)
           
            # Generate the new graph after the new robot has been added
            write_init_matlab([1,0,0])
            generate_init_robots([15])
            init_for_classification_w_dummy(robot_data_1)
            classification()
            self.query_robot_data()
            self.construct_fitness_graph(True, True)

            reset_classification()
            # Return the results with the images
            return render_template('dummy_w_metrics_new.html', text_input=dummy_name, 
                                    images=[radar_img, "fitness_graph_old", "fitness_graph_new"])

        @self.app.route('/f_sens_metric_definitions')
        def f_sens_metric_definitions(): # For getting robot recommendations
            return render_template('F_sens_metric_definitions_new.html')
    
        @self.app.route('/f_cont_metric_definitions')
        def f_cont_metric_definitions(): # For getting robot recommendations
            return render_template('F_cont_metric_definitions_new.html')

        @self.app.route('/f_reac_metric_definitions')
        def f_reac_metric_definitions(): # For getting robot recommendations
            return render_template('F_reac_metric_definitions_new.html')

        @self.app.route('/mm_metric_definitions')
        def mm_metric_definitions(): # For getting robot recommendations
            return render_template('MM_metric_definitions_new.html')
    
        @self.app.route('/s_metric_definitions')
        def s_metric_definitions(): # For getting robot recommendations
            return render_template('S_metric_definitions_new.html')
        
        @self.app.route('/download_dummy', methods=['GET','POST']) 
        # NO YET WORKING
        def download_dummy():
            relative_path = "example_dummy_w_metrics.zip"  # Adjust this relative path
            full_path = os.path.join(os.getcwd(), relative_path)
            return send_file(full_path, as_attachment=True)
            
        
        @self.app.route('/download', methods=['GET','POST']) 
        # NO YET WORKING
        def download():
            relative_path = "new_robot.zip"  # Adjust this relative path
            full_path = os.path.join(os.getcwd(), relative_path)
            return send_file(full_path, as_attachment=True)




    def run(self, debug=True):
        self.app.run(debug=debug)

    def get_all_process_names(self, button_value): 
            """Query all process names from the processes table."""
            print("Fetching all process names...")
            database = os.path.join("Database", "processes_database.db")
            conn = self.connect_to_database(database)


            # CONTINUE HERE - Fetch Process Names from process numbers and make them clickable
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT process1_ID, process2_ID, process3_ID, process4_ID FROM process_group WHERE process_group_ID = ?", (button_value))
                rows = cursor.fetchall()
                process_names = [row[0] for row in rows]
                print(f"Found {len(process_names)} processes.")
                return process_names
            except sqlite3.Error as e:
                print(f"Error retrieving process names: {e}")
                return []
    
    def connect_to_database(self, db_file):
        """Create a database connection to the SQLite database specified by db_file."""
        print("Attempting to connect to the database...")
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return conn
    
    def retrieve_robot_numbers(self):
        """
        Function for retrieving the appropriate robots, based on the processes selected by the user.
        Currently, a dummy function that just reads the numbers from init_robots.txt.
        Logic needs to be added.
        """
        # Read the list of robots?
        with open("init_robots.txt") as file:
            self.numbers = [int(line) for line in file]
        return self.numbers
    
    def query_robot_name(self):
        """ 
        Grab the data from the DB, and run queries to organize the data into the correct format for
        constructing the visualizations
        """
        database = os.path.join("Database", "tor_database.db")
        conn = self.connect_to_database(database)
        self.cursor = conn.cursor()
        # Execute the query to retrieve the desired columns
        self.cursor.execute("SELECT name FROM robots ")

        # Fetch all the results
        results = np.array(self.cursor.fetchall())

        # Separate the data into vectors
        self.robot_name = results[:, 0]  # First column
        

        conn.close()


    def query_robot_data(self):
        """ 
        Grab the data from the DB, and run queries to organize the data into the correct format for
        constructing the visualizations
        """
        database = os.path.join("Database", "tor_database.db")
        conn = self.connect_to_database(database)
        self.cursor = conn.cursor()
        # Execute the query to retrieve the desired columns
        self.cursor.execute("SELECT motion_performance, tactility_performance FROM robots")

        # Fetch all the results
        results = np.array(self.cursor.fetchall())

        # Separate the data into vectors
        self.y = results[:, 0]  # First column
        self.x = results[:, 1]  # Second column

        # Execute the query to retrieve the desired columns
        self.cursor.execute("SELECT centroid_motion_direction, centroid_tactility_direction FROM genus")

        # Fetch all the results
        results_genus = np.array(self.cursor.fetchall())

        # Separate the data into vectors
        self.y_genus = results_genus[:, 0]  # First column
        self.x_genus = results_genus[:, 1]  # Second column

        # Execute the query to retrieve the desired columns
        self.cursor.execute("SELECT covariance_matrix_comp1_1, covariance_matrix_comp1_2, covariance_matrix_comp2_1, covariance_matrix_comp2_2 FROM genus")

        # Fetch all the results
        results_genus_cov = np.array(self.cursor.fetchall())

        # Separate the data into vectors
        self.cov_values_1_1 = results_genus_cov[:, 0]  # First column
        self.cov_values_1_2 = results_genus_cov[:, 1]  # Second column
        self.cov_values_2_1 = results_genus_cov[:, 2]  # Third column
        self.cov_values_2_2 = results_genus_cov[:, 3]  # Fourth column

        conn.close()


    def rotate_2x2(self, matrix):
        # Rotation matrix (e.g., 90 degrees around the y-axis)
        theta=0
        rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
        ])
        # Apply rotation to the covariance matrix
        matrix_new = rotation_matrix @ matrix @ rotation_matrix.T
        return(matrix_new)

    
    def construct_fitness_graph(self, summary, updated):

        
        interpolate_color_v = np.vectorize(interpolate_color)
        hex_to_rgb_v = np.vectorize(hex_to_rgb)
        colors = interpolate_color_v(self.x / 5)
        colors_genus = interpolate_color_v(self.x_genus / 5)
        area = (30 * np.random.rand(len(self.x)))**2  # 0 to 15 point radii
        p_values = np.arange(0.15, 1.0, 0.4)

        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_box_aspect([2, 1, 1])
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0)) 
        ax.scatter(self.x, self.y, zs=10, zdir='z', c=colors, alpha=0.5)

        for n in range(len(self.x_genus)):
            database = os.path.join("Database", "tor_database.db")
            conn = self.connect_to_database(database) 
            self.cursor = conn.cursor()
            self.cursor.execute("SELECT name FROM genus WHERE genus_id = ?", (str(n+1),))
            genus_name = self.cursor.fetchone()
            genus_name =genus_name [0]
            self.cursor.close()
            conn.close()
            ax.scatter(self.x_genus[n], self.y_genus[n], zs=5, zdir='z', c=colors_genus[n], alpha=0.5, marker='x')
            ax.text(self.x_genus[n]+0.5, self.y_genus[n], 5.5, genus_name, fontsize=20, color=colors_genus[n])

        circ_x = 1.85
        circ_y = 0.5
        circ_z = -5 
        for n in range(len(self.x)):
                try:
                    database = os.path.join("Database", "tor_database.db")
                    conn = self.connect_to_database(database) 
                    self.cursor = conn.cursor()
                    self.cursor.execute("SELECT genus_ID FROM robots WHERE robot_id = ?", (str(n+1),))
                    genus = self.cursor.fetchone()
                    #print('here is the troubling genus:')
                    #print(genus)
                    genus = int(genus[0])
                    self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(n+1),))
                    robot_name_tuple = self.cursor.fetchone()
                    robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
                    self.cursor.close()
                    conn.close()
                except sqlite3.Error as e:
                    print(f"Error connecting to database: {e}")
                ax.plot([self.x_genus[genus-1],self.x[n]], [self.y_genus[genus-1],self.y[n]], [5, 10], color='lightgrey', linewidth=1)
                ax.plot([self.x_genus[genus-1], circ_x], [self.y_genus[genus-1], circ_y], [5, circ_z], color='lightgrey', linewidth=1)
                #ax.text(self.x[n-1]-0.2, self.y[n-1], 11.5, f'{robot_name}', fontsize=10, color='lightgrey')
        

        if updated:
            ax.scatter(self.x[-1], self.y[-1], zs=10, zdir='z', c=colors[-1], alpha=1, marker='o', s=300)

        for n_gen in range(len(self.x_genus)):
            table_covariances = np.array([[self.cov_values_1_1[n_gen], self.cov_values_1_2[n_gen]],
                                  [self.cov_values_2_1[n_gen], self.cov_values_2_2[n_gen]]])
            for p in p_values:
                s = -2 * np.log(1 - p)
                t = np.linspace(0, 2 * np.pi, num=100)
                D_1, V_1 = np.linalg.eig(table_covariances * s)
                D_1 = np.diag(D_1).T
                a_1 = np.dot(V_1, np.sqrt(D_1)) @ np.array([np.cos(t), np.sin(t)])
                ax.plot(a_1[0] + self.x_genus[n_gen], a_1[1] + self.y_genus[n_gen], zs=5, zdir='z', linestyle=':', linewidth=2, color=colors_genus[n_gen])
        
        ax.set_xlabel("Tactility Fitness", fontsize=14, fontname='sans-serif',labelpad=20)
        ax.set_ylabel("Motion Fitness", fontsize=14, fontname='sans-serif',labelpad=20)
        ax.set_zlabel("", fontsize=14, fontname='sans-serif',labelpad=20)
        ax.set_xlim([-0.5, 5.2])
        ax.set_ylim([-0.5, 1.5])
        ax.set_zlim([0, 12])
        ax.set_zticks([5, 10])
        ax.set_zticklabels(['genus', 'species'])
        ax.tick_params(axis='x', pad=10)
        ax.tick_params(axis='y', pad=10)
        ax.tick_params(axis='z', pad=10)
        plt.xticks(np.arange(0, 5.1, 1), fontsize=12, fontname='sans-serif')
        plt.yticks(np.arange(-0.5, 1.5, 0.5), fontsize=12, fontname='sans-serif')
        ax.zaxis.set_tick_params(labelsize=12)
        ax.view_init(elev=10, azim=-70)

        with open("init_robots.txt") as file:
                numbers = [int(line) for line in file]
        if numbers and numbers[0] != 0:
         for n in numbers:
                database = os.path.join("Database", "tor_database.db")
                conn = self.connect_to_database(database) 
                self.cursor = conn.cursor()
                print(n)
                self.cursor.execute("SELECT genus_ID FROM robots WHERE robot_id = ?", (str(n),))
                genus = self.cursor.fetchone()
                print(genus)
                genus = int(genus[0])
                self.cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (str(n),))
                robot_name_tuple = self.cursor.fetchone()
                robot_name = robot_name_tuple[0] if robot_name_tuple else "Unknown Robot"
                self.cursor.close()
                conn.close()
                if n == 15:
                    dummy_name=global_var.get('dummy_name','not set')
                    robot_name = dummy_name
                ax.plot([self.x_genus[genus-1],self.x[n-1]], [self.y_genus[genus-1],self.y[n-1]], [5, 10], color=interpolate_color(self.x[n-1]/5), linewidth=1)
                ax.plot([self.x_genus[genus-1], circ_x], [self.y_genus[genus-1], circ_y], [5, circ_z], color=interpolate_color(self.x[n-1]/5), linewidth=1)
                d = 10.2+n*0.2
                ax.text(self.x[n-1]-0.2, self.y[n-1], d, f'{robot_name}', fontsize=10, color=interpolate_color(self.x[n-1]/5))
        ax.scatter([circ_x], [circ_y], [circ_z], s=200, c=["black"], alpha=0.0, zorder=0)

        if not summary:
            plt.savefig(os.path.join("FlaskWebsite","static","fitness_graph.png"), format='png')
        else:

            file_name = "fitness_graph_new.png" if updated else "fitness_graph_old.png"
            if os.path.exists(os.path.join("FlaskWebsite","static","summary_fitness", file_name)):
                os.remove(os.path.join("FlaskWebsite","static","summary_fitness", file_name))
            plt.savefig(os.path.join("FlaskWebsite","static","summary_fitness", file_name), format='png')

    def construct_morphology_graph(self):
        self.top_dict = top_nodes_dict
        self.c_dict = c_nodes_dict
        self.m_dict = m_nodes_dict
        self.s_dict = s_nodes_dict
        self.a_dict = a_nodes_dict
        self.o_dict = o_nodes_dict
        self.g = Graph(engine="neato")
        self.g.attr(format="svg")
        self.g.attr('node', shape='box')
        self.g.attr('node', style='rounded')
        self.g.attr('node', fontcolor='gray')
        self.g.attr('node', color='gray')
        self.g.attr('node', fontsize='16')
        self.g.attr('graph', fontsize='16')
        self.g.attr('graph', outputorder="edgesfirst")
        self.g.attr(size='15,12.40')
        self.g.attr('graph', bgcolor='transparent')
        self.g.attr('node', bgcolor='transparent')  # Ensure no background color
        # Add the basic structure of the graph
        add_struct_nodes(self.g, struct_dict)    
    
    def populate_morphology_graph(self):
        if len(self.numbers) == 3:
            x_graphs = np.array([self.x[self.numbers[0]-1], self.x[self.numbers[1]-1], self.x[self.numbers[2]-1]])
        elif len(self.numbers) == 2:
            x_graphs = np.array([self.x[self.numbers[0]-1], self.x[self.numbers[1]-1]])
        elif len(self.numbers) == 1:
            x_graphs = np.array([self.x[self.numbers[0]-1]])

        # XML path and colors should be the same length
        interpolate_color_v = np.vectorize(interpolate_color)
        # Loop through the self.numbers and make the paths to the xmls
        xml_paths = [os.path.join("07_Robot_Ext_URDFs", str(num-1)+"_ext_urdf","ext_urdf.xml") for num in self.numbers]
        colors = interpolate_color_v(x_graphs/5)
        #colors = [ interpolate_color(1), interpolate_color(1), interpolate_color(1)]
        rgcs = []
        # Graph edge generation loop
        for xml in xml_paths:
            rgc = RobotGraphConstructor(xml)
            rgc.parseRobotXml(self.top_dict, self.c_dict, self.m_dict, self.s_dict, self.a_dict, self.o_dict)
            rgcs.append(rgc)
        # Draw the processed nodes, which should have the active flags set
        add_nodes(self.g, self.top_dict)
        add_nodes(self.g, self.c_dict)
        add_nodes(self.g, self.m_dict)
        add_nodes(self.g, self.s_dict)
        add_nodes(self.g, self.a_dict)
        add_nodes(self.g, self.o_dict)
        for idx, rgc in enumerate(rgcs):
            add_edges(self.g, rgc.c_edges, colors[idx])
            add_edges(self.g, rgc.m_edges, colors[idx])
            add_edges(self.g, rgc.s_edges, colors[idx])
            add_edges(self.g, rgc.a_edges, colors[idx])
            add_edges(self.g, rgc.cluster_edges, colors[idx])
        # can add images as nodes, like
        #self.g.node("image", image="robot_graph.png")
        self.g.attr('graph', bgcolor='transparent')
        self.g.render("morphology_graph", os.path.join("FlaskWebsite","static"), format='png')
        
        
    def generate_radar_graph(self, robot_name, robot_org_data ):
        spoke_labels = ['FS1', 'FS2', 'FS3', 'FS4', 'FS5', 'FS6', 'FS7', 'FC1', 'FC2', 'FC3', 'FC4', 'FC5', 'FC6', 'FC7', 'FC8', 'FC9', 'U1', 'U2', 'U4', 'U5', 'U6', 'FR1', 'FR2', 'S1', 'S2']
        N = len(spoke_labels)
        metric_to_wc = np.zeros(len(robot_org_data))
        value_range = np.zeros(len(robot_org_data))
        robot_org_data_array = np.zeros(len(robot_org_data))
        robot_data = np.zeros(len(robot_org_data))
        theta = radar_factory(N, frame='circle')
        if(robot_org_data == None):
            robot_data = np.random.uniform(low=0, high=1, size=(len(spoke_labels),)).tolist()
        else:
            ideal_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 100, 0, 100, 0, 0, 0, 0, 0, 100, 100, 100, 100])
            worst_values = np.array([5, 1, 5, 1, 1, 1, 1, 5, 1, 5, 0, 5, 5, 0, 20, 0, 15, 5, 5, 5, 5, 0, 0,  0, 0])
            robot_org_data_array = np.array(robot_org_data)
            value_range = ideal_values-worst_values

            # check for NaNs
            for i in range(len(robot_org_data_array[0:25])):
                if robot_org_data_array[i] is None:
                    if value_range[i] < 0:
                        robot_org_data_array[i] = 10000
                    else:
                        robot_org_data_array[i] = -10

            metric_to_wc = worst_values - robot_org_data_array[0:25]
            
            # kick out too bad values
            # for i in range(len(metric_to_wc)):
            #     if value_range[i] < 0:
            #         if metric_to_wc[i] < 0:
            #             robot_org_data_array[i] = worst_values[i]
            #     else:
            #         if metric_to_wc[i] > 0:
            #             robot_org_data_array[i] = worst_values[i]

            #normalize
            robot_data = np.zeros(len(robot_org_data[0:25])) 
            for n in range(len(robot_org_data[0:25])):
                if value_range[n] <0: # counts for all metrics where smaller is better
                    robot_data[n] = (worst_values[n]-robot_org_data_array[n])/abs(value_range[n])
                    if robot_data[n] <0:
                        robot_data[n] = -0.2

                else:
                    robot_data[n] = (robot_org_data_array[n])/abs(value_range[n])
                    if robot_data[n] <0:
                        robot_data[n] = -0.2
        

        img = mpimg.imread(os.path.join("FlaskWebsite","static","radarbackground_2.png"))

        # Create figure
        #fig, ax_polar = plt.subplots(figsize=(12,12), subplot_kw=dict(projection='radar', position=[0.393, 0.326, 0.345, 0.345]), zorder=2.5)
        fig, ax_polar = plt.subplots(figsize=(12,12), subplot_kw=dict(projection='radar', position=[0.248, 0.286, 0.425, 0.425]), zorder=2.5)
        ax_polar.set_ylim([-0.25, 1.06])
        ax_polar.plot(theta, robot_data, color='#43cd80', zorder=2.5)
        ax_polar.fill(theta, robot_data, facecolor='#ecfaf2', alpha=0.25, label='_nolegend_')
        ax_polar.set_varlabels(spoke_labels)
        ax_polar.set_axis_off()
        # Add the image as a background
        axes_coords = [0, 0, 1, 1] # plotting full width and height
        ax_image = fig.add_axes(axes_coords, zorder=-1)
        ax_image.imshow(img, alpha=1, zorder=-1)
        ax_image.axis('off')
        graph_name = str(robot_name) #+ " Tactile Performance"
        plt.savefig("./FlaskWebsite/static/" + graph_name + ".png",transparent=True)
        return graph_name
    

    def get_robot_name(self, conn, robot_id):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM robots WHERE robot_id = ?", (robot_id,))
            data = cursor.fetchone()
            robot_name = data[0]
            return robot_name
        except sqlite3.Error as e:
            print(f"Error retrieving robot name: {e}")
            return []

    def get_robot_metrics_results(self, conn, selected_robot_id):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM robot_tactility_metrics WHERE robot_id = ?", (selected_robot_id,))
            row_data = cursor.fetchone()
            robot_data = row_data[1:]
            robot_id = row_data[0]
            cursor.close()
            
            return robot_id, robot_data
        except sqlite3.Error as e:
            print(f"Error retrieving robot data: {e}")
            return []
       
    


if __name__ == '__main__':
    my_app = MyFlaskApp()
    my_app.run(debug=False)
