# Functions
def xy_pos(x, y):
    return str(x) + ',' + str(y) + '!'

# Fixed node visual parameters
left_x = 1.5
mid_x = 3.75
right_x = 6
label_x = 8
cluster_label_x = 7.5

row_diff = 0.5
cluster_diff = 0.7
label_diff = 0.4
top_y = 13.6
top_y2 = 13.6

c0_y = 13
c1_y = c0_y-label_diff
c2_y = c1_y-row_diff
c3_y = c2_y-row_diff

m0_y = c3_y-cluster_diff
m1_y = m0_y-label_diff
m2_y = m1_y-row_diff
m3_y = m2_y-row_diff

s0_y = m3_y-cluster_diff
s1_y = s0_y-label_diff
s2_y = s1_y-row_diff
s3_y = s2_y-row_diff
s4_y = s3_y-row_diff
s5_y = s4_y-row_diff
s6_y = s5_y-row_diff

a0_y = s6_y-cluster_diff
a1_y = a0_y-label_diff
a2_y = a1_y-row_diff
a3_y = a2_y-row_diff
a4_y = a3_y-row_diff

o0_y = a4_y-cluster_diff

box_h = str(0.3)
num_w = str(0.5)
label_w = '10'#'2'
none_w = str(0.7)
small_w = '1.2'
med_w = '1.5'
large_w = '1.8'
no_w = '0.1'
no_h = '0.1'    

# Graph label-to-node mappings
# control
c_motion_map = {"position":"c1_left", "torque":"c1_center", "velocity":"c1_right","?":"c1_right_max"}
c_interaction_map = {"impedance":"c2_right","admittance":"c2_center", "none":"c2_left","?":"c2_right_max" }
c_tactility_map = {"impedance":"c3_right", "none":"c3_left","force":"c3_center","?":"c3_right_max"}
c_mapping = [c_motion_map, c_interaction_map, c_tactility_map]

# Mechanical
m_dof_map = {"6":"m1_left", "7":"m1_right","?":"m1_right_max"}
m_design_map = {"solid":"m2_left", "rods":"m2_mleft", "exo-tube":"m2_mright", "exo-shell":"m2_right","?":"m2_right_max"}
m_topology_map = {"parallel":"m3_left","serial":"m3_middle", "tree":"m3_right","?":"m3_right_max"}
m_mapping = [m_dof_map, m_design_map, m_topology_map]

# Sensor
s_touch_map = {"resistive":"s1_left", "none":"s1_middle","capacitive":"s1_right","?":"s1_right_max"}
s_wrist_wrench_map = {"piezo":"s2_left", "none":"s2_middle","strain_gauge":"s2_right","?":"s2_right_max"}
s_joint_torque_map = {"optical":"s3_left", "none":"s3_middle","strain_gauge":"s3_right","?":"s3_right_max"}
s_link_motion_map = {"hall_sensors":"s4_left", "none":"s4_middle","imu":"s4_right","?":"s4_right_max"}
s_joint_motion_map = {"hall_sensors":"s5_left", "none":"s5_middle","motor_encoders":"s5_right","?":"s5_right_max"}
s_current_map = {"amplifiers":"s6_left", "none":"s6_middle","hall_sensors":"s6_right","?":"s6_right_max"}
s_mapping = [s_touch_map,s_wrist_wrench_map,s_joint_torque_map,s_link_motion_map,s_joint_motion_map,s_current_map]

# Actuation
a_electronics_mapping = {"integrated":"a1_left", "remote":"a1_right","?":"a1_right_max"}
a_transmission_mapping = {"tendon_driven":"a2_left", "gear":"a2_right","?":"a2_right_max"}
a_drive_mapping = {"valve/piston":"a3_left", "bldc_motor":"a3_right","?":"a3_right_max"}
a_technology_mapping = {"electromechanical":"a4_left", "pneumatics":"a4_right","?":"a4_right_max"}
a_mapping = [a_electronics_mapping,a_transmission_mapping,a_drive_mapping,a_technology_mapping]

# Base
o_base_mapping = {"fixed":"o0_mleft","ground-vehicle":"o0_mright"}
o_mapping = [o_base_mapping]

# Top
o_top_mapping = {"fixed":"top_center", "else":"top_center2"}
top_mapping = [o_top_mapping]

# Graph node data
struct_dict = {
    
    'mechanical_bg': {
        "label": '',
        "fixedsize": 'True',
        "width": '8',
        "height": '1.85',
        "pos": xy_pos(4.7, 10.15)
    },
    'cluster_mech': {
        "label": '< <B>mechanical structure</B> >',
        "shape": 'plain',
        "pos": xy_pos(cluster_label_x, m0_y)
    },
    'm1_label': {
        "label": 'degrees of\nfreedom',
        "shape": 'plain',
        "pos": xy_pos(label_x, m1_y)
    },
    
    'm2_label': {
        "label": 'link design',
        "shape": 'plain',
        "pos": xy_pos(label_x, m2_y)
    },
    
    'm3_label': {
        "label": 'topology',
        "shape": 'plain',
        "pos": xy_pos(label_x, m3_y)
    },

    'control_bg': {
        "label": '',
        "fixedsize": 'True',
        "width": '8',
        "height": '1.85',
        "pos": xy_pos(4.7, 12.25)
    },
    'cluster_con': {
        "label": '< <B>controller type</B> >',
        "shape": 'plain',
        "pos": xy_pos(cluster_label_x, c0_y)
    },

    'c1_label': {
        "label": 'motion',
        "shape": 'plain',
        "pos": xy_pos(label_x, c1_y)
    },
    
    'c2_label': {
        "label": 'handguiding',
        "shape": 'plain',
        "pos": xy_pos(label_x, c2_y)
    },
    
    'c3_label': {
        "label": 'tactile',
        "shape": 'plain',
        "pos": xy_pos(label_x, c3_y)
    },
    
    'sensor_bg': {
        "label": '',
        "fixedsize": 'True',
        "width": '8',
        "height": '3.3',
        "pos": xy_pos(4.7, 7.3)
    },
    'cluster_sensory': {
        "label": '< <B>sensory architecture</B> >',
        "shape": 'plain',
        "pos": xy_pos(cluster_label_x, s0_y)
    },
    's1_label': {
        "label": 'touch',
        "shape": 'plain',
        "pos": xy_pos(label_x, s1_y)
    },
    
    's2_label': {
        "label": 'wrist wrench',
        "shape": 'plain',
        "pos": xy_pos(label_x, s2_y)
    },
    
    's3_label': {
        "label": 'joint torque',
        "shape": 'plain',
        "pos": xy_pos(label_x, s3_y)
    },
    
    's4_label': {
        "label": 'link motion',
        "shape": 'plain',
        "pos": xy_pos(label_x, s4_y)
    },
    
    's5_label': {
        "label": 'joint motion',
        "shape": 'plain',
        "pos": xy_pos(label_x, s5_y)
    },
    
    's6_label': {
        "label": 'current',
        "shape": 'plain',
        "pos": xy_pos(label_x, s6_y)
    },

    'actuation_bg': {
        "label": '',
        "fixedsize": 'True',
        "width": '8',
        "height": '2.4',
        "pos": xy_pos(4.7, 4.2)
    },
    'cluster_actuation': {
        "label": '< <B>actuation architecture</B> >',
        "shape": 'plain',
        "pos": xy_pos(cluster_label_x, a0_y)
    },
    'a1_label': {
        "label": 'electronics',
        "shape": 'plain',
        "pos": xy_pos(label_x, a1_y)
    },
    
    'a2_label': {
        "label": 'transmission',
        "shape": 'plain',
        "pos": xy_pos(label_x, a2_y)
    },
    
    'a3_label': {
        "label": 'drive',
        "shape": 'plain',
        "pos": xy_pos(label_x, a3_y)
    },
    
    'a4_label': {
        "label": 'technology',
        "shape": 'plain',
        "pos": xy_pos(label_x, a4_y)
    },
}

c_nodes_dict = {
    'c1_left': {
        "label": 'position',
        "shape": 'box',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, c1_y),
        "active": False
    },
    'c1_left': {
        "label": 'torque',
        "shape": 'box',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(mid_x, c1_y),
        "active": False
    },
    'c1_right': {
        "label": 'velocity',
        "shape": 'box',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, c1_y),
        "active": False
    },
    'c1_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, c1_y),
        "active": False
    },
    'c2_left': {
        "label": 'none',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, c2_y),
        "active": False
    },
    'c2_center': {
        "label": 'admittance',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(mid_x, c2_y),
        "active": False
    },
    'c2_right': {
        "label": 'impedance',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, c2_y),
        "active": False
    },
    'c2_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, c2_y),
        "active": False
    },
    'c3_left': {
        "label": 'none',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, c3_y),
        "active": False
    },
    'c3_center': {
        "label": 'force',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(mid_x, c3_y),
        "active": False
    },
    'c3_right': {
        "label": 'impedance',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, c3_y),
        "active": False
    },
    'c3_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, c3_y),
        "active": False
    }
}


m_nodes_dict = {
    'm1_left': {
        "label": '6',
        "shape": 'box',
        "fixedsize": 'True',
        "width": num_w,
        "height": '0.25',
        "pos": xy_pos(3, m1_y),
        "active": False
    },
    'm1_right': {
        "label": '7',
        "shape": 'box',
        "fixedsize": 'True',
        "width": num_w,
        "height": '0.25',
        "pos": xy_pos(4.5, m1_y),
        "active": False
    },
    'm1_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, m1_y),
        "active": False
    },
    'm2_left': {
        "label": 'solid',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, m2_y),
        "active": False
    },
    'm2_mleft': {
        "label": 'rods',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(3, m2_y),
        "active": False
    },
    'm2_mright': {
        "label": 'exo-tube',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(4.5, m2_y),
        "active": False
    },
    'm2_right': {
        "label": 'exo-shell',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, m2_y),
        "active": False
    },
    'm2_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, m2_y),
        "active": False
    },
    'm3_left': {
        "label": 'parallel',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, m3_y),
        "active": False
    },
    'm3_middle': {
        "label": 'serial',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(mid_x, m3_y),
        "active": False
    },
    'm3_right': {
        "label": 'tree',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, m3_y),
        "active": False
    },
    'm3_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, m3_y),
        "active": False
    }
}

s_nodes_dict = {
    's1_left': {
        "label": 'resistive',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s1_y),
        "active": False
    },
    's1_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s1_y),
        "active": False
    },
    's1_right': {
        "label": 'capacitive',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s1_y),
        "active": False
    },
    's1_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s1_y),
        "active": False
    },
    's2_left': {
        "label": 'piezo',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s2_y),
        "active": False
    },
    's2_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s2_y),
        "active": False
    },
    's2_right': {
        "label": 'strain gauge',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s2_y),
        "active": False
    },
    's2_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s2_y),
        "active": False
    },
    's3_left': {
        "label": 'optical',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s3_y),
        "active": False
    },
    's3_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s3_y),
        "active": False
    },
    's3_right': {
        "label": 'strain gauge',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s3_y),
        "active": False
    },
    's3_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s3_y),
        "active": False
    },
    's4_left': {
        "label": 'hall sensors',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s4_y),
        "active": False
    },
    's4_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s4_y),
        "active": False
    },
    's4_right': {
        "label": 'IMU',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s4_y),
        "active": False
    },
    's4_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s4_y),
        "active": False
    },
    's5_left': {
        "label": 'hall sensors',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s5_y),
        "active": False
    },
    's5_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s5_y),
        "active": False
    },
    's5_right': {
        "label": 'motor encoders',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s5_y),
        "active": False
    },
    's5_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s5_y),
        "active": False
    },
    's6_left': {
        "label": 'amplifiers',
        "fixedsize": 'True',
        "width": small_w,
        "height": box_h,
        "pos": xy_pos(left_x, s6_y),
        "active": False
    },
    's6_middle': {
        "label": 'none',
        "fixedsize": 'True',
        "width": none_w,
        "height": box_h,
        "pos": xy_pos(mid_x, s6_y),
        "active": False
    },
    's6_right': {
        "label": 'hall sensors',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, s6_y),
        "active": False
    },
    's6_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, s6_y),
        "active": False
    }
}


a_nodes_dict = {
    'a1_left': {
        "label": 'integrated',
        "fixedsize": 'True',
        "width": large_w,
        "height": box_h,
        "pos": xy_pos(left_x + 0.3, a1_y),
        "active": False
    },
    'a1_right': {
        "label": 'remote',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, a1_y),
        "active": False
    },
    'a1_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, a1_y),
        "active": False
    },
    'a2_left': {
        "label": 'tendon driven',
        "fixedsize": 'True',
        "width": large_w,
        "height": box_h,
        "pos": xy_pos(left_x + 0.3, a2_y),
        "active": False
    },
    'a2_right': {
        "label": 'gear',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, a2_y),
        "active": False
    },
    'a2_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, a2_y),
        "active": False
    },
    'a3_left': {
        "label": 'valve/piston',
        "fixedsize": 'True',
        "width": large_w,
        "height": box_h,
        "pos": xy_pos(left_x + 0.3, a3_y),
        "active": False
    },
    'a3_right': {
        "label": 'bldc motor',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, a3_y),
        "active": False
    },
    'a3_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, a3_y),
        "active": False
    },
    'a4_left': {
        "label": 'electromechanical',
        "fixedsize": 'True',
        "width": large_w,
        "height": box_h,
        "pos": xy_pos(left_x + 0.3, a4_y),
        "active": False
    },
    'a4_right': {
        "label": 'pneumatics',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(right_x, a4_y),
        "active": False
    },
    'a4_right_max': {
        "label": '?',
        "fixedsize": 'True',
        "width": num_w,
        "height": box_h,
        "pos": xy_pos(right_x+1.1, a4_y),
        "active": False
    }
}

o_nodes_dict = {
    'o0_mleft': {
        "label": 'fixed base',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(2.5, o0_y),
        "active": False
    },
    'o0_mright': {
        "label": 'ground-vehicle',
        "fixedsize": 'True',
        "width": med_w,
        "height": box_h,
        "pos": xy_pos(5, o0_y),
        "active": False
    }
}

top_nodes_dict = {
    'top_center': {
        "label": '',
        "fixedsize": 'True',
        "width": no_w,
        "height": no_h,
        "pos": xy_pos(mid_x, top_y),
        "active": False
    },
    'top_center2': {
        "label": '',
        "fixedsize": 'True',
        "width": no_w,
        "height": no_h,
        "pos": xy_pos(mid_x, top_y),
        "active": False
    },
}