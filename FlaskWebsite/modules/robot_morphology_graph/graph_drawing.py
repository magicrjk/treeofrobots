import graphviz
import os
import sqlite3
import numpy as np
from graphviz import Graph
from robot_graph_constructor import RobotGraphConstructor
from graph_variables import top_nodes_dict, m_nodes_dict, s_nodes_dict, a_nodes_dict, o_nodes_dict, c_nodes_dict, struct_dict
from parser_helpers import add_struct_nodes, add_nodes, add_edges, interpolate_color

def connect_to_database(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    print("Attempting to connect to the database...")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

top_dict = top_nodes_dict
c_dict = c_nodes_dict
m_dict = m_nodes_dict
s_dict = s_nodes_dict
a_dict = a_nodes_dict
o_dict = o_nodes_dict

g = Graph(engine="neato")

g.attr(format="svg")
g.attr('node', shape='box')
g.attr('node', style='rounded,filled')
g.attr('node', fillcolor='white')
g.attr('node', fontcolor='gray')
g.attr('node', color='gray')
g.attr('node', fontsize='16')
g.attr('graph', fontsize='16')
g.attr('graph', outputorder="edgesfirst")
g.attr('graph', bgcolor='transparent')
g.attr('node', bgcolor='transparent')
g.attr(size='15,12.40' )

# Add the basic structure of the graph
add_struct_nodes(g, struct_dict)     

with open("init_robots.txt") as file:
    numbers = [int(line) for line in file]


#Read from database
database = os.path.join("Database", "processes_database.db")
conn = connect_to_database(database)
cursor = conn.cursor()

# Execute the query to retrieve the desired columns
cursor.execute("SELECT motion_performance, tactility_performance FROM robots")

# Fetch all the results
results = np.array(cursor.fetchall())

# Separate the data into vectors
y = results[:, 0]  # First column
x = results[:, 1]  # Second column

# Execute the query to retrieve the desired columns
cursor.execute("SELECT centroid_motion_direction, centroid_tactility_direction FROM genus")




x_graphs = np.array([x[numbers[0]], x[numbers[1]], x[numbers[2]]])
# XML path and colors should be the same length
interpolate_color_v = np.vectorize(interpolate_color)
xml_paths = [os.path.join("07_Robot_Ext_URDFs", str(numbers[0])+"_ext_urdf",str(numbers[0])+"_ext_urdf.xml") , os.path.join("07_Robot_Ext_URDFs",str(numbers[1])+"_ext_urdf",str(numbers[1])+"_ext_urdf.xml"), os.path.join("07_Robot_Ext_URDFs",str(numbers[2])+"_ext_urdf", str(numbers[2])+"_ext_urdf.xml") ]
colors = interpolate_color_v(x_graphs/5)
#colors = [ interpolate_color(1), interpolate_color(1), interpolate_color(1)]
rgcs = []
# Graph edge generation loop
for xml in xml_paths:
    rgc = RobotGraphConstructor(xml)
    rgc.parseRobotXml(top_dict, c_dict, m_dict, s_dict, a_dict, o_dict)
    rgcs.append(rgc)

# Draw the processed nodes, which should have the active flags set
add_nodes(g, top_nodes_dict)
add_nodes(g, c_nodes_dict)
add_nodes(g, m_nodes_dict)
add_nodes(g, s_nodes_dict)
add_nodes(g, a_nodes_dict)
add_nodes(g, o_nodes_dict)

for idx, rgc in enumerate(rgcs):
    add_edges(g, rgc.c_edges, colors[idx])
    add_edges(g, rgc.m_edges, colors[idx])
    add_edges(g, rgc.s_edges, colors[idx])
    add_edges(g, rgc.a_edges, colors[idx])
    add_edges(g, rgc.cluster_edges, colors[idx])
    #ADD EDGE FOR top_node here?
# can add images as nodes, like
#g.node("image", image="robot_graph.png")
g.render("robot_graph", "svg")
g.view()