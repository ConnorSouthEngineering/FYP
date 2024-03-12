import os
import getpass
import uuid
import requests
import json
import configparser
import platform 
from datetime import datetime

def check_uuid(key):
    try:
        uuid_obj = uuid.UUID(key, version=4)
        return True
    except ValueError:
        return False

def reconnect(node_config):
    body = {
        "node_key_value":node_config['CONNECTION']['key'],
        "node_id":node_config['NODE_INFO']['node_id']
    }
    json_body = json.dumps(body)
    headers = {'Content-Type':'application/json'}
    try:
        return requests.post(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/connect",data=json_body,headers=headers)
    except:
        return
    
def connect(node_config):
    body = {
        "node_key_value":node_config['CONNECTION']['key'],
        "node_name":platform.node(),
        "creation_date":datetime.now().isoformat()
    }
    json_body = json.dumps(body)
    headers = {'Content-Type':'application/json'}
    try:
        return requests.post(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/connect",data=json_body,headers=headers)
    except:
        return

async def connect_devices(json_body):
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    headers = {'Content-Type':'application/json'}
    response = requests.post(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/connect/devices",data=json_body,headers=headers)
    if response and response.json()['status']:
        return response.json()['status']
    else:
        return "Error"
    

async def configure_connection():
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    if os.path.isfile(abs_path) and check_uuid(node_config['CONNECTION']['key']):
        if node_config['NODE_INFO']['node_id']:
            connection_response = reconnect(node_config)
            if connection_response and connection_response.json()['status'] == "Connected":
                return "remote"
            else:
                return "isolated"
        else:
            connection_response = connect(node_config)
            if connection_response and connection_response.json()['status'] == "Connected":
                node_config['NODE_INFO']['node_id'] = connection_response.json()['node_id']
                node_config['NODE_INFO']['node_name'] = platform.node()
                with open(abs_path, 'w') as old_config:
                    node_config.write(old_config)
                return "remote"
            else:
                return "isolated"
    else:
        return "isolated"
