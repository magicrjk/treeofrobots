-- create all tables
-- CREATE TABLE
-- application(
--     application_ID INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT, 
--     description TEXT, 
--     location TEXT,
--     reference TEXT,
--     domain_ID INTEGER,
--     process_ID INTEGER,
--     user_ID INTEGER);

-- DROP TABLE motion_metric_results
-- CREATE TABLE 
-- domain(
--     domain_ID INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT, 
--     description TEXT,
--     user_ID INTEGER);

-- DROP TABLE process_group

-- CREATE TABLE 
-- process_group(
--     process_group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT, 
--     description TEXT, 
--     domain_ID INTEGER,
--     process1_ID INTEGER, 
--     process2_ID INTEGER, 
--     process3_ID INTEGER, 
--     process4_ID INTEGER,
--     process5_ID INTEGER,
--     process6_ID INTEGER,
--     process7_ID INTEGER,
--     process8_ID INTEGER,
--     process9_ID INTEGER,
--     process10_ID INTEGER,
--     process11_ID INTEGER,
--     process12_ID INTEGER,
--     process13_ID INTEGER,
--     process14_ID INTEGER,
--     process15_ID INTEGER,
--     process16_ID INTEGER,
--     user_ID INTEGER
-- );

-- DROP TABLE processes

-- CREATE TABLE processes (
--     process_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
--     name TEXT, 
--     description TEXT, 
--     process_group_ID INTEGER,
--     basic_operation1_ID INTEGER,
--     basic_operation2_ID INTEGER,
--     basic_operation3_ID INTEGER,
--     basic_operation4_ID INTEGER,
--     basic_operation5_ID INTEGER,
--     basic_operation6_ID INTEGER,
--     basic_operation7_ID INTEGER,
--     basic_operation8_ID INTEGER,
--     user_ID INTEGER

-- );

-- DROP TABLE basic_operations

-- CREATE TABLE basic_operations (
--     basic_operation_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
--     name TEXT, 
--     description TEXT, 
--     feature1_ID INTEGER,
--     feature2_ID INTEGER,
--     feature3_ID INTEGER,
--     feature4_ID INTEGER,
--     user_ID INTEGER

-- );

-- CREATE TABLE features (
--     feature_id INTEGER PRIMARY KEY AUTOINCREMENT ,
--     name TEXT, 
--     description TEXT, 
--     math_description TEXT,
--     user_ID INTEGER

-- );



CREATE TABLE robot_metric_groups (
    robot_metric_group_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

DROP TABLE robot_metrics

CREATE TABLE IF NOT EXISTS robot_metrics (
    robot_metric_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    short_name TEXT,
    math_description TEXT,
    robot_metric_group_ID INTEGER,
    user_ID INTEGER
);





DROP TABLE process_quality_metrics

CREATE TABLE process_quality_metrics (
    process_quality_metric_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
    name TEXT, 
    description TEXT,  
    feature1_ID INTEGER,
    feature2_ID INTEGER,
    feature3_ID INTEGER,
    feature4_ID INTEGER,
    feature5_ID INTEGER,
    feature6_ID INTEGER,
    feature7_ID INTEGER,
    feature8_ID INTEGER,
    feature9_ID INTEGER,
    user_ID INTEGER

);

-- CREATE TABLE user (
--     user_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
--     firstname TEXT, 
--     middlename TEXT,
--     lastname TEXT,
--     email_adress TEXT, 
--     affiliation INTEGER,
--     user_category_ID INTEGER

-- );

-- CREATE TABLE user_category (
--     user_category_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
--     name TEXT, 
--     description TEXT, 
--     allowances TEXT

-- );

DROP TABLE process_metric_categories

CREATE TABLE process_metric_categories (
    process_metric_category_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
    name TEXT, 
    description TEXT,
    process_metric1_ID INTEGER,
    process_metric2_ID INTEGER,
    process_metric3_ID INTEGER,
    process_metric4_ID INTEGER,
    process_metric5_ID INTEGER,
    user_ID INTEGER
);


-- CREATE TABLE robots (
--     robot_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
--     robot_data_ID INTEGER,
--     name TEXT, 
--     description TEXT,
--     serial_number TEXT
--     );

DROP TABLE basic_operation_to_feature

CREATE TABLE IF NOT EXISTS basic_operation_to_feature (
    basic_operation_ID INTEGER,
    feature_ID INTEGER,
    PRIMARY KEY (basic_operation_ID, feature_ID),
    FOREIGN KEY (basic_operation_ID) REFERENCES basic_operations(basic_operation_ID),
    FOREIGN KEY (feature_ID) REFERENCES features(feature_ID)
);


DROP TABLE robot_metric_categories

CREATE TABLE robot_metric_categories (
    robot_metric_category_ID INTEGER PRIMARY KEY AUTOINCREMENT ,
    name TEXT, 
    description TEXT,
    process_metric_categories1_ID INTEGER,
    process_metric_categories2_ID INTEGER,
    process_metric_categories3_ID INTEGER,
    process_metric_categories4_ID INTEGER,
    user_ID INTEGER
);

DROP TABLE robot_metric_category_to_group

CREATE TABLE IF NOT EXISTS robot_metric_category_to_group(
    robot_metric_category_ID INTEGER,
    robot_metric_group_ID INTEGER,
    FOREIGN KEY (robot_metric_category_ID) REFERENCES robot_metric_categories(robot_metric_category_ID),
    FOREIGN KEY (robot_metric_group_ID) REFERENCES robot_metric_groups(robot_metric_group_ID)
);


-- CREATE TABLE process_to_metric_category (
--     process_ID INTEGER,
--     process_metric_category_ID INTEGER,
--     FOREIGN KEY (process_ID) REFERENCES processes(process_ID),
--     FOREIGN KEY (process_metric_category_ID) REFERENCES process_metric_categories(process_metric_category_ID),
--     PRIMARY KEY (process_ID, process_metric_category_ID)
-- );

DROP TABLE metric_to_robot_category

CREATE TABLE metric_to_robot_category (
    process_metric_category_ID INTEGER,
    robot_metric_category_ID INTEGER,
    FOREIGN KEY (process_metric_category_ID) REFERENCES process_metric_categories(process_metric_category_ID),
    FOREIGN KEY (robot_metric_category_ID) REFERENCES robot_metric_categories(robot_metric_category_ID),
    PRIMARY KEY (process_metric_category_ID, robot_metric_category_ID)
);

DROP TABLE robot_category_to_genus

CREATE TABLE robot_category_to_genus (
    robot_category_genus_ID INTEGER PRIMARY KEY,
    robot_metric_category_ID INTEGER,
    genus_ID INTEGER,
    FOREIGN KEY (robot_metric_category_ID) REFERENCES robot_metric_categories(robot_metric_category_ID),
    FOREIGN KEY (genus_ID) REFERENCES genus(genus_ID)
);

DROP TABLE basic_operation_to_metrics
CREATE TABLE IF NOT EXISTS basic_operation_to_metrics (
    basic_operation_ID INTEGER NOT NULL,
    process_quality_metric_ID INTEGER NOT NULL,
    FOREIGN KEY (basic_operation_ID) REFERENCES basic_operations (basic_operation_ID),
    FOREIGN KEY (process_quality_metric_ID) REFERENCES process_quality_metrics (process_quality_metric_ID)
);


-- delete table

/*

INSERT INTO 
user_category (name, description, allowances)
VALUES
( "creator", "established this databse", "all"),
( "admin", "maintains the database can alter, create and drop tables and lines", "all"),
( "contributor", "can create new lines", "create"),
( "contributor_extended", "can create new lines and tables", "create"),
( "user", "can only see and query", "query")
*/

/*
INSERT INTO 
user (firstname, middlename, lastname, email_adress, affiliation, user_category_ID)
VALUES
( "Robin", "Jeanne", "Kirschner", "robin-jeanne.kirschner@tum.de", "TUM-MIRMI", 1),
( "Peter", "", "So", "peter.so@tum.de", "TUM-MIRMI", 1),
( "Kuebra", "", "Karacan", "kuebra.karacan@tum.de", "TUM-MIRMI", 1)

*/





INSERT INTO 
features (name, description, math_description, user_ID)
VALUES
( "F1", "goal pose", "x_d(t_final)", 1),
( "F2", "goal force", "f_d(t_final)", 1),
( "F3", "desired motion trajectory", "x_d(0:t_final)", 1),
( "F4", "desired force profile", "f_d(0:t_final)", 1),
( "F5", "induced velocity", "dx(0:t_final)", 1),
( "F6", "geometric constraint", "dx.(f_d/|f_d|)", 1),
( "F7", "initial desired force", "f(0)", 1),
( "F8", "constrained force profile in the nominal direction", "f=[0,0,f_z,0,0,0]", 1),
( "F9", "desired velocity profile", "dx_d(0:t_final)", 1)



-- INSERT INTO 
-- basic_operations (name, description, feature1_ID, feature2_ID, feature3_ID, feature4_ID, user_ID)
-- VALUES
-- ("Go to Pose", "Motion to a desired goal pose", 1, 5, 0, 0, 1),
-- ("Establish Contact", "Motion to a desired goal pose which is in contact with an object", 1, 2, 5, 6, 1),
-- ("Apply Force", "A defined force which is applied in contact to an object", 4, 6, 0, 0, 1),
-- ("Apply Material", "Generating a steady flow of material onto and object with geometric constraints", 6, 9, 3, 0, 1),
-- ("Follow Contour", "Generating a steady motion while being in contact with an object at desired force and adhering to geometric constraints", 3, 5, 6, 8, 1),
-- ("Follow Path", "Motion with certain desired constraints along the trajectory", 3, 5, 0, 0, 1),
-- ("Sense Force/Weigh", "sense a contact force or a weight induced force (weigh)", 7, 0, 0, 0, 1),
-- ("Manipulate", "Generating a steady motion profile with desired force profile adhering to geometric constraints", 3, 4, 5, 6, 1);



INSERT INTO
process_quality_metrics (name, description, feature1_ID, feature2_ID, feature3_ID, feature4_ID,feature5_ID, feature6_ID, feature7_ID, feature8_ID, feature9_ID, user_ID)
VALUES
("positioning accuracy tolerance", "how close to a desired pose does the initial pose have to be for successful task completion", 1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
("displacement tolerance", "how close to an geometric constraint does the initial pose or a path have to be for successful task completion", 1, 5, 0, 0, 0, 0, 0, 0, 0, 1),
("motion error tolerance", "how close to the desired motion profile does the actual one have to be for successful task completion", 3, 0, 0, 0, 0, 0, 0, 0, 0, 1),
("dispensing flow error tolerance", "how much can the dispensing flow and resulting dispensed material density deviate from the ideal scenario for successful task completion", 5, 9, 0, 0, 0, 0, 0, 0, 0, 1),
("disturbance force tolerance", "how much disturbance force can be compensated for successful task completion", 1, 2, 3, 4, 5, 6, 7, 8, 9, 1),
("fitting tolerance", "how restrictive are the geometric constraints that need to be considered for successful task execution", 6, 0, 0, 0, 0, 0, 0, 0, 0, 1),
("force profile error tolerance", "how much can the force deviate from a desired profile for successful task execution", 4, 8, 0, 0, 0, 0, 0, 0, 0, 1),
("force estimation error tolerance", "how exact has an external force/weight to be known to ensure successful task execution", 2, 4, 7, 0, 0, 0, 0, 0, 0, 1),
("force tolerance", "how accurate does the force have to be applied to ensure successful task execution", 2, 4, 5, 0, 0, 0, 0, 0, 0, 1),
("process cycle time", "how fast does the task have to be executed", 1, 2, 3, 4, 5, 6, 7, 8, 9, 1),
("fault reaction quality", "how efficient does a fault scenario have to be recovered for the task to be successfully completed", 1, 2, 3, 4, 5, 6, 7, 8, 9, 1),
("teaching", "how intuitive and efficient does the adaptation and task learning process have to be to be considered successful task execution (especially for future adaptive tasks)", 1, 2, 3, 4, 5, 6, 7, 8, 9, 1);




DROP TABLE process_metric_categories


INSERT INTO
process_metric_categories (name, description, process_metric1_ID, process_metric2_ID, process_metric3_ID, process_metric4_ID, process_metric5_ID, user_ID)
VALUES
("motion", "all process metrics describing motion constraints", 1, 2, 3, 4, 0, 1),
("motion and force", "all process metrics involving a combination of motion and force requirements", 5, 6, 0, 0, 0, 1),
("force", "all process metrics describing force constraints", 7, 8, 9, 0, 0, 1),
("general", "metrics describing requirements for successful task completion on safety and efficiency level", 10, 11, 12, 0, 0, 1);



-- INSERT INTO 
-- processes (
--     name,
--     description,
--     basic_operation1_ID,
--     basic_operation2_ID,
--     basic_operation3_ID,
--     basic_operation4_ID,
--     basic_operation5_ID,
--     basic_operation6_ID,
--     basic_operation7_ID,
--     basic_operation8_ID,
--     user_ID
-- )
-- VALUES
-- ('Coupling or Insertion', 'This process involves positioning components for assembly or disassembly, establishing contact, and applying necessary forces.', 1, 2, 3, NULL, NULL, NULL, NULL, NULL, 1),
-- ('Wiring', 'This process includes positioning wires or cables, establishing contact points, and ensuring accurate connections.', 1, 2, 3, NULL, NULL, NULL, NULL, NULL, 1),
-- ('Levering', 'In this process, components are manipulated using leverage to achieve desired positions or movements.', 1, 2, 8, 3, NULL, NULL, NULL, NULL, 1),
-- ('(Un)Screwdriving', 'This process involves driving or unscrewing fasteners, ensuring proper positioning and torque.', 1, 2, 8, 3, NULL, NULL, NULL, NULL, 1),
-- ('Applying Adhesive or Sealing Material', 'This process includes positioning components, establishing contact, following a contour, and applying adhesive or sealing materials.', 1, 2, 5, 4, NULL, NULL, NULL, NULL, 1),
-- ('Spraying', 'In this process, materials are sprayed onto surfaces following a predetermined path.', 1, 6, 4, NULL, NULL, NULL, NULL, NULL, 1),
-- ('Painting', 'This process involves positioning, establishing contact, following a contour, applying paint, and ensuring even coverage.', 1, 2, 6, 3, 4, 5, NULL, NULL, 1),
-- ('Soldering or Welding', 'Components are positioned, contact is established, solder or weld material is applied, and joints are fused.', 1, 2, 5, 6, 4, NULL, NULL, NULL, 1),
-- ('Arc or Laser Welding', 'This process involves positioning components, following a path, and applying welding using arc or laser technology.', 1, 6, 4, NULL, NULL, NULL, NULL, NULL, 1),
-- ('Machine Tending', 'In this process, machines are tended to by positioning tools, establishing contact, and manipulating workpieces as needed.', 1, 2, 8, 7, NULL, NULL, NULL, NULL, 1),
-- ('Machine Steering', 'Components are positioned, contact is established, and steering actions are performed to guide machines.', 1, 2, 3, NULL, NULL, NULL, NULL, NULL, 1),
-- ('Tool Exchange', 'This process involves positioning tools, establishing contact, exchanging tools, and manipulating components.', 1, 2, 8, 7, 3, NULL, NULL, NULL, 1),
-- ('Drilling or Riveting', 'Components are positioned, contact is established, and drilling or riveting actions are performed.', 1, 2, 5, 3, NULL, NULL, NULL, NULL, 1),
-- ('Polishing', 'Surfaces are positioned, contact is established, a contour is followed, force is applied, and polishing is performed.', 1, 2, 5, 3, 6, NULL, NULL, NULL, 1),
-- ('Grinding', 'Components are positioned, contact is established, and grinding actions are performed to shape or smooth surfaces.', 1, 2, 5, 3, 6, NULL, NULL, NULL, 1),
-- ('Filing', 'In this process, components are positioned, contact is established, and filing actions are performed to refine edges or surfaces.', 1, 2, 5, 3, 6, NULL, NULL, NULL, 1),
-- ('Pick and Place', 'In this process, objects are manipulated in their position for a defined pose A to another defined pose B', 1, 2, 3, 7, 8, NULL, NULL, NULL, 1);


-- INSERT INTO
-- process_group (
--     name, 
--     description, 
--     domain_ID, 
--     process1_ID, 
--     process2_ID,
--     process3_ID,
--     process4_ID,
--     process5_ID,
--     process6_ID,
--     process7_ID,
--     process8_ID,
--     process9_ID,
--     process10_ID,
--     process11_ID,
--     process12_ID,
--     process13_ID,
--     process14_ID,
--     process15_ID,
--     process16_ID,
--     user_ID)
-- VALUES
-- ('Assembly/Disassembly', 'Processes related to assembling or disassembling components.',1, 1,2,3,4,NULL, NULL,NULL,NULL, NULL, NULL,NULL,NULL,NULL, NULL,NULL,NULL, 1),
-- ('Dispensing', 'Processes related to applying materials or coatings.', 1, 5, 6, 7, NULL, NULL, NULL,NULL,NULL, NULL, NULL,NULL,NULL,NULL, NULL,NULL,NULL, 1),
-- ('Welding/Soldering', 'Processes related to welding or soldering components.', 1, 8, 9, NULL, NULL,NULL, NULL,NULL,NULL, NULL, NULL,NULL,NULL,NULL, NULL,NULL,NULL, 1),
-- ('Handling', 'Processes related to changing components.', 1, 10, 11, 12, NULL,NULL, NULL,NULL,NULL, NULL, NULL,NULL,NULL,NULL, NULL,NULL,NULL, 1),
-- ('Processing', 'Processes related to finishing or refining surfaces.', 1, 13, 14, 15, 16, NULL, NULL,NULL,NULL, NULL, NULL,NULL,NULL,NULL, NULL,NULL,NULL,1);

-- INSERT  INTO
-- domain (
--     name, 
--     description, 
--     user_ID)
-- VALUES
-- ('Industrial', 'Processes related to manufacturing and production.', 3);

-- INSERT INTO
-- process_metric_categories (
--     name, 
--     description, 
--     process_metric1_ID, 
--     process_metric2_ID, 
--     process_metric3_ID, 
--     process_metric4_ID, 
--     process_metric5_ID, 
--     user_ID)
-- VALUES
-- ('Motion', 'Metrics related to motion constraints.', 1, 2, 3, 4, NULL, 3),
-- ('Force', 'Metrics related to force constraints.', 7, 8, 9, NULL, NULL, 3),
-- ('Motion and force', 'Metrics related to motion and force constraints.', 5, 6, NULL, NULL, NULL, 3),
-- ('General', 'General metrics for task completion.', 11, 12, 13, NULL, NULL, 3);

INSERT INTO
robot_metric_categories (
    name, 
    description, 
    process_metric_categories1_ID, 
    process_metric_categories2_ID, 
    process_metric_categories3_ID, 
    process_metric_categories4_ID, 
    user_ID)
VALUES
('Motion', 'Metrics related to motion constraints.', 1, NULL, NULL, NULL, 3),
('Tactility', 'Metrics related to force constraints.', 3, NULL, NULL, NULL, 3),
('Motion and tactility', 'Metrics related to motion and force constraints.', 1, 2, 3, 4, 3);

-- Example data for process_to_metric_category
INSERT INTO process_to_metric_category (process_ID, process_metric_category_ID)
VALUES
(1, 3),  -- Assuming process with ID 1 is linked to process metric category ID 1
(2, 3),
(3, 3),
(4, 3),
(5, 3),
(6, 3),
(7, 3),
(8, 3),
(9, 3),
(10, 3),
(11, 3),
(12, 3),
(13, 3),
(14, 3),
(15, 3),
(16, 3);

-- Example data for metric_to_robot_category
INSERT INTO metric_to_robot_category (process_metric_category_ID, robot_metric_category_ID)
VALUES
(1, 1),  -- Assuming process metric category ID 1 is linked to robot metric category ID 1
(3, 2),
(3, 3),
(1, 3),
(2, 2),
(2, 3),
(4, 1),
(4, 2),
(4, 3);


INSERT INTO robot_category_to_genus (robot_metric_category_ID, genus_ID)
VALUES
(1, 1),  -- Example: Mapping robot metric category 1 to genus cat 1 , position controlled
(2, 2),  -- Example: Mapping robot metric category 2 
(2, 3),  -- Example: Mapping robot metric category 2 to genus 3, cobots
(3, 4);  -- Example: Mapping robot metric category 3 to genus 4, tactile robots

INSERT INTO basic_operation_to_feature (basic_operation_ID, feature_ID)
VALUES
(1, 1),  -- Example: Mapping basic operation 1 to feature 1, goal pose
(1, 5),
(2, 1),
(2, 2),
(2, 5),
(2, 6),
(3, 4),
(3, 6),
(4, 6),
(4, 9),
(5, 3),
(5, 5),
(5, 6),
(5, 8),
(6, 3),
(6, 5),
(7, 7),
(8, 3),
(8, 4),
(8, 5),
(8, 6);


INSERT INTO basic_operation_to_metrics (basic_operation_ID, process_quality_metric_ID)
VALUES
(1, 1),
(1, 2),
(1, 5),
(2, 1),
(2, 2),
(2, 5),
(2, 9),
(3, 5),
(3, 6),
(3, 7),
(3, 8),
(3, 9),
(4, 4),
(4, 5),
(5, 1),
(5, 3),
(5, 5),
(5, 7),
(5, 9),
(6, 3),
(6, 5),
(7, 5),
(7, 8),
(8, 1),
(8, 2),
(8, 3),
(8, 5),
(8, 6),
(8, 7),
(8, 8),
(8, 9);

INSERT INTO robot_metric_groups (name) VALUES
    ('Force Sensing Metrics'),
    ('Force Control Metrics'),
    ('Force Reaction Metrics'),
    ('Human Safety Metrics'),
    ('Teaching Metrics'),
    ('Motion Fitness Metrics');


INSERT INTO robot_metrics (name, description, short_name, math_description, robot_metric_group_ID, user_ID)
VALUES
    -- Force Sensing Metrics
    ('Force Sensing Accuracy', 'Measure the system capability to sense forces accurately.', 'sens_acc', 'Defined according to Eq. [Ak_f].', 1, 3),
    ('Force Sensing Precision', 'Measure the system capability to sense forces precisely.', 'sens_pres', 'Defined according to Eq. [Precision].', 1, 3),
    ('Force Sensing Resolution', 'Measure the system capability to sense forces with fine granularity.', 'sens_res', 'Defined according to Eq. [Resolution].', 1, 3),
    ('Force Sensing Drift 1min', 'Measure the force sensing drift after 1 minute.', 'sens_tc1', 'Defined according to Eq. [SD_1].', 1, 3),
    ('Force Sensing Drift 10min', 'Measure the force sensing drift after 10 minutes.', 'sens_tc2', 'Defined according to Eq. [SD_2].', 1, 3),
    ('Force Sensing Drift 1hr', 'Measure the force sensing drift after 1 hour.', 'sens_tc3', 'Defined according to Eq. [SD_3].', 1, 3),
    ('Force Sensing Drift 8hrs', 'Measure the force sensing drift after 8 hours.', 'sens_tc4', 'Defined according to Eq. [SD_4].', 1, 3),

    -- Force Control Metrics
    ('Force Control Accuracy', 'Measure the accuracy of the applied forces in comparison to a desired force.', 'cont_acc', 'Defined according to Eq. [Ak_fc].', 2, 3),
    ('Force Control Precision', 'Measure the precision of the applied forces.', 'cont_pres', 'Defined according to Eq. [Precision_fc].', 2, 3),
    ('Force Control Resolution', 'Measure the resolution of the applied forces.', 'cont_res', 'Defined according to Eq. [Resolution_fc].', 2, 3),
    ('Force Control Settling Time', 'Measure the time taken to settle at the desired force.', 'cont_ts', 'Defined according to Eq. [ST].', 2, 3),
    ('Force Control Overshoot', 'Measure the overshoot forces during force control.', 'cont_ov', 'Defined according to Eq. [Overshoot].', 2, 3),
    ('Force Control Minimum Force', 'Measure the minimal force that the system can apply.', 'cont_maf', 'Defined according to Eq. [MinForce].', 2, 3),
    ('Force Control Stability', 'Measure the stability under changing environmental conditions.', 'cont_is', 'Defined according to Eq. [Stability].', 2, 3),
    ('Force Control Bandwidth', 'Measure the bandwidth of force control.', 'cont_cB', 'Defined according to Eq. [Cont_cB].', 2, 3),
    ('Internal Reading Material Variation Stability', 'Measure the stability in internal reading material variation.', 'cont_mvc', 'Defined according to Eq. [Cont_mvc].', 2, 3),

    -- Force Reaction Metrics
    ('Contact Sensitivity', 'Measure the sensitivity to detect contacts.', 'freact_cs', 'Defined according to Eq. [CS].', 3, 3),
    ('Tactile Contact Sensitivity', 'Measure the sensitivity to detect tactile contacts.', 'freact_tcs', 'Defined according to Eq. [tCS].', 3, 3),

    -- Human Safety Metrics
    ('Transient Contact Force', 'Measure the conformance to transient contact force thresholds.', 'safe_St', 'Defined according to Eq. [transient_iso_conf].', 4, 3),
    ('Quasi-Static Contact Force', 'Measure the conformance to quasi-static contact force thresholds.', 'safe_Sq', 'Defined according to Eq. [qs_iso_conf].', 4, 3),

    -- Teaching Metrics
    ('Minimum Motion Force', 'Measure the minimum force required for hand-guiding.', 'teach_MF', 'Defined according to Eq. [MF].', 5, 3),
    ('Guiding Force', 'Measure the force required for guiding.', 'teach_GF', 'Defined according to Eq. [GF].', 5, 3),
    ('Guiding Force Deviation', 'Measure the deviation in guiding force.', 'teach_GD', 'Defined according to Eq. [GFD].', 5, 3),
    ('Guiding Energy', 'Measure the required guiding energy.', 'teach_GE', 'Defined according to Eq. [GE].', 5, 3),
    ('Maneuver Effort', 'Measure the effort required for maneuvering.', 'teach_ME', 'Defined according to Eq. [ME].', 5, 3),

    -- Motion Fitness Metrics
    ('Pose/Path Accuracy', 'Measure the accuracy of the robot pose and path.', 'pose_acc', 'Defined according to Eq. [PoseAccuracy].', 6, 3),
    ('Pose Drift', 'Measure the drift in the robot pose over time.', 'pose_drift', 'Defined according to Eq. [PoseDrift].', 6, 3),
    ('Position Overshoot', 'Measure the overshoot in the robot position during motion.', 'pos_ov', 'Defined according to Eq. [PositionOvershoot].', 6, 3),
    ('Stabilization Time', 'Measure the time taken for the robot to stabilize at the target position.', 'stab_time', 'Defined according to Eq. [StabilizationTime].', 6, 3),
    ('Path Velocity Characteristics', 'Measure the velocity characteristics of the robot along its path.', 'path_vel', 'Defined according to Eq. [PathVelocity].', 6, 3);


INSERT INTO robot_metric_category_to_group(robot_metric_category_ID, robot_metric_group_ID)
VALUES
    -- Motion category mappings
    (1, 6),  -- Motion Fitness Metrics
    -- Tactility category mappings
    (2, 1),  -- Force Sensing Metrics
    (2, 2),  -- Force Control Metrics
    (2, 3),  -- Force Reaction Metrics
    (2 ,4),  -- Human Safety Metrics
    (2, 5), -- Teaching Metrics
   --Motion and tactility category mappings
    (3, 1),  -- Force Sensing Metrics
    (3, 2),  -- Force Control Metrics
    (3, 3),  -- Force Reaction Metrics
    (3, 4),  -- Human Safety Metrics
    (3, 5), -- Teaching Metrics
    (3, 6); -- Motion Fitness Metrics