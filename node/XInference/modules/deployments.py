import requests
import json
import configparser
import getpass
import ast

async def extract_list_from_string(config_string):
    try:
        return ast.literal_eval(config_string)
    except ValueError:
        print("The string could not be converted to a list.")
        return []

async def get_device_id(camera, node_config):
    params = {"deviceName":camera}
    headers = {'Content-Type':'application/json'}
    try:
        return requests.get(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/device/name",params=params,headers=headers)
    except:
        return
    
async def get_deployment_models(camera_id, node_config):
    params = {"node_id":node_config['NODE_INFO']['node_id'], "device_id":camera_id}
    headers = {'Content-Type':'application/json'}
    try:
        return requests.get(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/deployments/active",params=params,headers=headers)
    except:
        return

async def get_model(model_id, node_config):
    headers = {'Content-Type':'application/json'}
    response = requests.get(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/models/id/{model_id}",headers=headers)
    body = response.json()
    print(body)
    return body[0]['get_model'][0]

async def retrieve_active_deployments(camera):
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    response = await get_device_id(camera, node_config)
    body = response.json()
    camera_id = body[0]['get_device_from_name']['device_id']
    response = await get_deployment_models(camera_id, node_config)
    body = response.json()
    return body[0]['get_nodes_deployment_models']['deployments']

async def gather_model_information(location_name):
    abs_path = f'/mnt/model_repo/{location_name}/1/model.savedmodel/assets/{location_name}.config'
    model_config = configparser.ConfigParser()
    model_config.read(abs_path)
    height = model_config['PREDICTION']['height']
    width = model_config['PREDICTION']['width']
    class_list = model_config['PREDICTION']['class_list']
    return height, width, class_list
