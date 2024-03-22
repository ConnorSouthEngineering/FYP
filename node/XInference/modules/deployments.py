import requests
import json
import configparser
import getpass

async def get_device_id(camera):
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    params = {"deviceName":camera}
    headers = {'Content-Type':'application/json'}
    try:
        return requests.post(f"http://{node_config['CONNECTION']['master_ip']}:{node_config['CONNECTION']['master_port']}/nodes/device/name",params=params,headers=headers)
    except:
        return
    
async def retrieve_active_deployments(camera):
    print(camera)
    camera_id = await get_device_id(camera)
    print(camera_id)
    return camera_id
