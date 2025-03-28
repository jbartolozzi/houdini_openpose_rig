import hou
import json

# Load the JSON data
def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Create points and bones in Houdini
def create_rig_from_json(data):
    # Create a new geometry container node in Houdini
    geo = hou.node('/obj').createNode('geo', 'OpenPose_Rig')
    geo.removeAllPrimitives()

    # Dictionary to store the created points for bone connectivity
    point_store = {}

    # Create points for joints
    for joint, info in data['joints'].items():
        # Extract position and convert to Houdini's coordinate system
        pos = hou.Vector3(info['position'])
        point = geo.createPoint()
        point.setPosition(pos)
        point.setAttribValue('Cd', [int(x) for x in info['color'].strip('()').split(',')])
        point.setAttribValue('name', joint)
        point_store[joint] = point

    # Create curves for bones
    for bone, info in data['bones'].items():
        start_joint = info['connect'][0]
        end_joint = info['connect'][1]
        start_point = point_store[start_joint]
        end_point = point_store[end_joint]

        # Create a line (curve) between two joints
        line = geo.createNurbsCurve(2, [start_point, end_point], False)
        line.setAttribValue('Cd', [int(x) for x in info['color'].strip('()').split(',')])

    # Layout the geo node for better visibility in viewport
    geo.layoutChildren()

# Path to the JSON file
json_path = 'openpose_rig.json'
data = load_json(json_path)
create_rig_from_json(data)
