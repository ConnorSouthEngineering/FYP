from aiohttp import web
import asyncio
import json
import platform 
import sys

from modules.gstreamer import update_system_cameras
from modules.connection import configure_connection

cameras = []

async def get_cameras(request):
    global cameras
    if len(cameras) > 0:
        body =  {
            "get_cameras":{"node":platform.node(),
                        "cameras":cameras}
        }
        json_body = json.dumps(body)  
        return web.Response(body=json_body, content_type='application/json')
    else:
        return web.Response(text=f"No Cameras Found") 

async def launch_inference():
    print("Launch inference")

async def server_up():
    server = '0.0.0.0'
    port = 2500
    app = web.Application()
    app.add_routes([web.post('/triton/initialise_deployment', launch_inference)])
    app.add_routes([web.get('/node/cameras', get_cameras)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, server, port)
    await site.start()
    connection_task =  loop.create_task(configure_connection())
    await connection_task
    if connection_task.result() == 'isolated':
        print("The node cannot connect securely with the master server")    
        print(f"This server has been launched in isolated mode: http://0.0.0.0:2500")
    elif connection_task.result() == 'remote':
        print("The node has connected securely with the master server")    
        print(f"This server has been launched in remote mode: http://0.0.0.0:2500")
    else:
        print("Server could not be configured")
        sys.exit(1)
    camera_task = loop.create_task(update_system_cameras(cameras))
    
    

async def main():
    await server_up()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
