from aiohttp import web
import asyncio
import json
import configparser
import sys
import getpass

from modules.gstreamer import update_system_cameras
from modules.connection import configure_connection, connect_devices

cameras = []

async def available_node(request):
    return web.Response(text="Available")

async def get_cameras(request):
    global cameras
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    if not request == "manual":
        body =  {
            "get_cameras":{"node_id":node_config['NODE_INFO']['node_id'],
                        "cameras":cameras}
        }
        json_body = json.dumps(body)  
        return web.Response(body=json_body, content_type='application/json')
    else:
        body =  {"node_id":node_config['NODE_INFO']['node_id'],
                    "cameras":cameras
                    }
        json_body = json.dumps(body)  
        return json_body
    
async def launch_inference():
    print("Launch inference")

async def server_up():
    server = '0.0.0.0'
    port = 2500
    app = web.Application()
    app.add_routes([web.post('/triton/initialise_deployment', launch_inference)])
    app.add_routes([web.get('/node/available', available_node)])
    app.add_routes([web.get('/node/cameras', get_cameras)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, server, port)
    await site.start()
    camera_task = loop.create_task(update_system_cameras(cameras))
    connection_task =  loop.create_task(configure_connection())
    await connection_task
    if connection_task.result() == 'isolated':
        print("The node cannot connect securely with the master server")    
        print(f"This server has been launched in isolated mode: http://0.0.0.0:2500")
    elif connection_task.result() == 'remote':
        print("The node has connected securely with the master server")    
        print(f"This server has been launched in remote mode: http://0.0.0.0:2500")
        node_devices = await get_cameras("manual")
        device_connection_task = loop.create_task(connect_devices(node_devices))
        await device_connection_task
        if device_connection_task.result() == 'Synced':
            print(f"Initial devices have been synced with the master service")
        else:
            print(f"Initial devices have failed to sync with the master service")
            sys.exit(1)
    else:
        print("Server could not be configured")
        sys.exit(1)
    
async def main():
    await server_up()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
