def add_struct_nodes(gr, struct_dict):
    for key in struct_dict:
        
        new_node = struct_dict[key]
        if("fixedsize" in new_node.keys() and "width" in new_node.keys() and "height" in new_node.keys()):
            gr.node(key, label=new_node['label'], style="rounded", fixedsize=new_node['fixedsize'], height=new_node['height'], width=new_node['width'], pos=new_node['pos'])
        else:
            gr.node(key, label=new_node['label'], style="rounded", shape=new_node['shape'], pos=new_node['pos'])



def add_nodes(gr, node_dict):
    for key in node_dict:
        new_node = node_dict[key]
        if new_node["active"]:
            gr.node(key, label=new_node['label'], fontcolor="black", color="black", fixedsize=new_node['fixedsize'], height=new_node['height'], width=new_node['width'], pos=new_node['pos'])
        else:
            gr.node(key, label=new_node['label'], style="rounded", fixedsize=new_node['fixedsize'], height=new_node['height'], width=new_node['width'], pos=new_node['pos'])

# robot_data and mapping have the same dimensions.
def activate_nodes(node_dict, robot_data, mapping):
    for idx, data in enumerate(robot_data):
        target_map = mapping[idx]
        if(data in target_map.keys()):
            target_node = target_map[data] # this yields the name of the node we want
        else:
            print(data, " is not part of the mapping.")
            continue
        if(target_node in node_dict.keys()):
            node_dict[target_node]["active"] = True
        else:
            print(target_node, " is not part of the nodes.")
            continue

def create_edges(nodes_dict, robot_data, mapping):
    edges = []
    for idx, data in enumerate(robot_data):
        if(idx + 1 == len(robot_data)):
            # special case for connecting two clusters together
            continue
        parent_data = data
        child_data = robot_data[idx+1]
        parent_map = mapping[idx]
        child_map = mapping[idx+1]
        if(parent_data in parent_map.keys()):
            parent_node = parent_map[parent_data]
        else:
            # need a special case for handling exceptions, either at the
            # xml parsing level or here
            print("parent data missing")
            continue
        if(child_data in child_map.keys()):
            child_node = child_map[child_data]
        else:
            # need a special case for handling exceptions, either at the
            # xml parsing level or here
            print("child data missing")
            continue
        tpl = (parent_node, child_node)
        edges.append(tpl)
    #tpl_node = (child_node,top_node)
    #edges.append(tpl_node)
    return edges
    
def create_intercluster_edge(c1_edges, c2_edges):
    parent_node = c1_edges[-1][1]
    child_node = c2_edges[0][0]
    return [parent_node, child_node]
    
def add_edges(gr, edges, col):
    for edge in edges:
        gr.edge(edge[0],edge[1], color=col,style='dashed')

def interpolate_color(t):
    """
    Linearly interpolate between green, blue, and red.

    :param t: A float between 0 and 1 representing the interpolation factor.
    :return: A string representing the interpolated color in hex format #RRGGBB.
    """
    # Ensure t is within the range [0, 1]
    t = max(0, min(1, t))
    
    if t < 0.5:
        # Interpolate between green and blue
        t = t * 2  # Scale t to the range [0, 1]
        r = 0
        g = int((1 - t) * 255)
        b = int(t * 255)
    else:
        # Interpolate between blue and red
        t = (t - 0.5) * 2  # Scale t to the range [0, 1]
        r = int(t * 255)
        g = 0
        b = int((1 - t) * 255)

    return f"#{r:02x}{g:02x}{b:02x}"