import xml.etree.ElementTree as ET
from graph_variables import top_mapping, c_mapping, m_mapping, s_mapping, a_mapping, o_mapping
from parser_helpers import activate_nodes, create_edges, create_intercluster_edge

'''
The class parses the given xml file and creates the node edges and activates the
relevant nodes, passed as the dict arguments for parseRobotXml.
'''
class RobotGraphConstructor:
    root = None

    # Edges
    c_edges = None
    m_edges = None
    s_edges = None
    a_edges = None
    o_edge = None
    cluster_edges = None

    # Internal vars for convenience
    jnt_name_set = set()
    link_name_set = set()

    def __init__(self, xml_path):
        tree = ET.parse(xml_path)
        self.root = tree.getroot()

    def parseRobotXml(self, top_nodes_dict, c_nodes_dict, m_nodes_dict, s_nodes_dict, a_nodes_dict, o_nodes_dict):
        self.parseControl(c_nodes_dict)
        self.parseMechanical(m_nodes_dict)
        self.parseSensor(s_nodes_dict)
        self.parseAcutation(a_nodes_dict)
        self.parseBase(o_nodes_dict)
        self.parseTop(top_nodes_dict)
        self.connectClusters()

    def parseControl(self, c_nodes_dict):
        ## CONTROL ARCHITECTURE
        _MOTION = None
        _HANDGUIDING = None
        _TACTILE = None
        # motion
        for con in self.root.iter("control"):
            if(con.attrib["class"] == "motion"):
                # consider only the first found sensor
                _MOTION = con.attrib["type"]
                break
            _MOTION = "none"


        # handguiding
        for con in self.root.iter("control"):
            if(con.attrib["class"] == "handguiding"):
                # consider only the first found sensor
                _HANDGUIDING = con.attrib["type"]
                break
            _HANDGUIDING = "none"
            
        # tactile
        for con in self.root.iter("control"):
            if(con.attrib["class"] == "tactile"):
                # consider only the first found sensor
                _TACTILE = con.attrib["type"]
                break
            _TACTILE = "none"

        c_robot_data = [_MOTION,_HANDGUIDING,_TACTILE]
        activate_nodes(c_nodes_dict, c_robot_data, c_mapping)
        self.c_edges = create_edges(c_nodes_dict, c_robot_data, c_mapping)

    def parseMechanical(self, m_nodes_dict):
        ## MECHANICAL STRUCTURE
        _DOF = None
        _TOPOLOGY = None
        _DESIGN = None
        # Sanity: Check that all parent and child links are in the list of links, else abort
        link_design_set = set()
        self.link_name_set = set()
        for link in self.root.iter("link"):    
            self.link_name_set.add(link.attrib['name'])
            link_design_set.add(link.attrib['type'])
        self.jnt_name_set = set()
        jnt_link_set = set()
        for joint in self.root.iter("joint"):
            self.jnt_name_set.add(joint.attrib['name'])
            jnt_link_set.add(joint.attrib['parent_link'])
            jnt_link_set.add(joint.attrib['child_link'])
        assert(self.link_name_set == jnt_link_set)

        # DOF: Check the number of links, and number of joints; n_link = n_jnt + 1, dof = n_jnt
        n_lnk = len(self.root.findall("link"))
        n_jnt = len(self.root.findall("joint"))
        if(n_jnt + 1 == n_lnk):
            _DOF = str(n_jnt)
            # If n_jnt + 1 = n_lnk, serial is the only option
            # No additional check done, so there will be outliers, but...
            _TOPOLOGY = "serial"

        # Design: Make sure that the links have identical types, else abort
        # From the design set, we want to make sure that there's only one type
        assert(len(link_design_set) == 1)
        _DESIGN = next(iter(link_design_set))

        # Node activation
        m_robot_data = [_DOF, _DESIGN, _TOPOLOGY]

        activate_nodes(m_nodes_dict, m_robot_data, m_mapping)
        self.m_edges = create_edges(m_nodes_dict, m_robot_data, m_mapping)

    def parseSensor(self, s_nodes_dict):
        ## SENSORY ARCHITECTURE
        _TOUCH = None
        _WRIST_WRENCH = None
        _JOINT_TORQUE = None
        _LINK_MOTION = None
        _JOINT_MOTION = None
        _CURRENT = None
        # Sanity check: Sensors should either be located in the joint or the link.
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["location"] not in self.link_name_set and sensor.attrib["location"] not in self.jnt_name_set):
                print("Sensor ", sensor.attrib["name"], " is not located in any of the joints or links! (Sensor location: ", sensor.attrib["location"], ")")

        # Touch: Partial, if any joint has touch, then include it 
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "touch"):
                # consider only the first found sensor
                _TOUCH = sensor.attrib["type"]
                break
            _TOUCH = "none"

        # Wrist wrench: Last joint only, else none
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "wrist_wrench"):
                # same as touch, since it is partial
                _WRIST_WRENCH = sensor.attrib["type"]
                break
            _WRIST_WRENCH = "none"

        # Joint Torque: AON, check that all joints have a corresponding sensor with this type, else none 
        s_jnt_trq_type_set = set()
        s_jnt_trq_loc_set = set()
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "joint_torque"):
                s_jnt_trq_type_set.add(sensor.attrib["type"])
                s_jnt_trq_loc_set.add(sensor.attrib["location"])
        if(len(s_jnt_trq_type_set) == 0):
            print("No joint torque sensors found.")
            _JOINT_TORQUE = "none"
        elif(len(s_jnt_trq_type_set) == 1):
            _JOINT_TORQUE = next(iter(s_jnt_trq_type_set))
            if(s_jnt_trq_loc_set != self.jnt_name_set):
                print("Not all joints are equipped with torque sensors! Setting it to none.")
                _JOINT_TORQUE = "none"
        else:
            print("Joint torque sensors have different types, which is not supported by the graph. Setting it to none.")
            _JOINT_TORQUE = "none"

                
        # Link motion: AON
        s_link_motion_type_set = set()
        s_link_motion_loc_set = set()
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "link_motion"):
                s_link_motion_type_set.add(sensor.attrib["type"])
                s_link_motion_loc_set.add(sensor.attrib["location"])
        if(len(s_link_motion_type_set) == 0):
            print("No link motion sensors found.")
            _LINK_MOTION = "none"
        elif(len(s_link_motion_type_set) == 1):
            _LINK_MOTION = next(iter(s_link_motion_type_set))
            if(s_link_motion_loc_set != self.link_name_set):
                print("Not all links are equipped with link motion sensors! Setting it to none.")
                _LINK_MOTION = "none"
        else:
            print("Link motion sensors have different types, which is not supported by the graph. Setting it to none.")
            _LINK_MOTION = "none"


        # Joint motion: AON
        s_jnt_motion_type_set = set()
        s_jnt_motion_loc_set = set()
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "joint_motion"):
                s_jnt_motion_type_set.add(sensor.attrib["type"])
                s_jnt_motion_loc_set.add(sensor.attrib["location"])
        if(len(s_jnt_motion_type_set) == 0):
            print("No link motion sensors found.")
            _JOINT_MOTION = "none"
        elif(len(s_jnt_motion_type_set) == 1):
            _JOINT_MOTION = next(iter(s_jnt_motion_type_set))
            if(s_jnt_motion_loc_set != self.jnt_name_set):
                print("Not all joints are equipped with joint motion sensors! Setting it to none.")
                _JOINT_MOTION = "none"
        else:
            print("Joint motion sensors have different types, which is not supported by the graph. Setting it to none.")
            _JOINT_MOTION = "none"


        # Current: AON
        s_current_type_set = set()
        s_current_loc_set = set()
        for sensor in self.root.iter("sensor"):
            if(sensor.attrib["class"] == "current"):
                s_current_type_set.add(sensor.attrib["type"])
                s_current_loc_set.add(sensor.attrib["location"])
        if(len(s_current_type_set) == 0):
            print("No link motion sensors found.")
            _CURRENT = "none"
        elif(len(s_current_type_set) == 1):
            _CURRENT = next(iter(s_current_type_set))
            if(s_current_loc_set != self.jnt_name_set):
                print("Not all joints are equipped with current sensors! Setting it to none.")
                _CURRENT = "none"
        else:
            print("Current sensors have different types, which is not supported by the graph. Setting it to none.")
            _CURRENT = "none"
        s_robot_data = [_TOUCH,_WRIST_WRENCH,_JOINT_TORQUE,_LINK_MOTION,_JOINT_MOTION,_CURRENT]
        activate_nodes(s_nodes_dict, s_robot_data, s_mapping)
        self.s_edges = create_edges(s_nodes_dict, s_robot_data, s_mapping)

    def parseAcutation(self, a_nodes_dict):
        ## ACTUATION ARCHITECTURE
        _ELECTRONICS = None
        _TRANSMISSION = None
        _DRIVE = None
        _TECHNOLOGY = None
        # electronics
        for act in self.root.iter("actuation"):
            if(act.attrib["class"] == "electronics"):
                # consider only the first found sensor
                _ELECTRONICS = act.attrib["type"]
                break
            _ELECTRONICS = "none"


        # transmission
        for act in self.root.iter("actuation"):
            if(act.attrib["class"] == "transmission"):
                # consider only the first found sensor
                _TRANSMISSION = act.attrib["type"]
                break
            _TRANSMISSION = "none"
            
        # drive
        for act in self.root.iter("actuation"):
            if(act.attrib["class"] == "drive"):
                # consider only the first found sensor
                _DRIVE = act.attrib["type"]
                break
            _DRIVE = "none"
            
        # technology
        for act in self.root.iter("actuation"):
            if(act.attrib["class"] == "technology"):
                # consider only the first found sensor
                _TECHNOLOGY = act.attrib["type"]
                break
            _TECHNOLOGY = "none"

        a_robot_data = [_ELECTRONICS,_TRANSMISSION,_DRIVE,_TECHNOLOGY]
        activate_nodes(a_nodes_dict, a_robot_data, a_mapping)
        self.a_edges = create_edges(a_nodes_dict, a_robot_data, a_mapping)

    def parseBase(self, o_nodes_dict):
        ## BASE
        _BASE = None
        for base in self.root.iter("base"):
            _BASE = base.attrib["type"]
            break
        o_robot_data = [_BASE]
        activate_nodes(o_nodes_dict, o_robot_data, o_mapping)
        self.o_edge = o_mapping[0][_BASE]

    def parseTop(self, top_nodes_dict):
        ## TOP
        _TOP = None
        for top in self.root.iter("top"):
            _TOP = top.attrib["type"]
            break
        top_robot_data = [_TOP]
        activate_nodes(top_nodes_dict, top_robot_data, top_mapping)
        self.top_edge = top_mapping[0][_TOP]

    def connectClusters(self):
        c_top_edge = [self.top_edge, self.c_edges[0][0]]
        c_m_edge = create_intercluster_edge(self.c_edges, self.m_edges)
        m_s_edge = create_intercluster_edge(self.m_edges, self.s_edges)
        s_a_edge = create_intercluster_edge(self.s_edges, self.a_edges)
        a_o_edge = [self.a_edges[-1][1], self.o_edge]
        self.cluster_edges = [c_top_edge, c_m_edge, m_s_edge, s_a_edge, a_o_edge]