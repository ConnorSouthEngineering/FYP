from aiohttp import web
import asyncio
import json
import configparser
import sys
import getpass
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
Gst.init(None)

from modules.gstreamer import update_system_cameras, manage_pipelines, initialise_gstreamer, display_sinks, add_new_sink, get_pipeline_state
from modules.connection import configure_connection, connect_devices
from modules.inference import initialise_inference
from modules.deployments import retrieve_active_deployments, get_model, gather_model_information, extract_list_from_string
from modules.classes import PipelineStorage

cameras = []
pipelines = PipelineStorage()
active_infernce = {}

async def intercept_launch_inference(request):
    body = await request.json()
    deployment_model = body[0]['initialise_deployment']
    inference_task = loop.create_task(launch_inference(deployment_model))
    await inference_task
    return web.Response(text="Inference launched", content_type='application/json')

async def launch_inference(deployment_id, model_id, pipeline, name, tee):
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)
    model_information = await get_model(model_id, node_config)
    num_frames = model_information['num_frames']
    triton_location_name = model_information['location_name']
    deployment_name = f"deployment_{deployment_id}"
    height, width, config_classes = await gather_model_information(triton_location_name)   
    class_list = await extract_list_from_string(config_classes)
    if not get_pipeline_state(pipeline) == Gst.State.PLAYING:
        ret = pipeline.set_state(Gst.State.PLAYING)
        print(f"Setting queue to PLAYING returned: {ret}")
    create_sink_task = loop.create_task(add_new_sink(pipeline, deployment_name, tee))
    while True:
        appsink = pipeline.get_by_name(f'sink_{deployment_name}')
        if not appsink:
            print("Appsink not found.")
        else:
            break
        await asyncio.sleep(1)
    inference_task = loop.create_task(initialise_inference(pipeline, f'sink_{deployment_name}', int(height), int(width), class_list, num_frames, triton_location_name))
    await inference_task
    return

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

async def execute_deployment_pipeline(name, pipeline, tee):
    node_deployments_task = loop.create_task(retrieve_active_deployments(name))
    await node_deployments_task                    
    deployments = node_deployments_task.result()
    if deployments:
        for deployment in deployments:
            print(deployment)
            inference_task = loop.create_task(launch_inference(deployment['deployment_id'], deployment['model_id'], pipeline, name, tee))
            await inference_task
        return
    else:
        print(f"No active deployments for camera: {name}")
    return

async def server_up():
    server = '0.0.0.0'
    port = 2500
    app = web.Application()
    app.add_routes([web.post('/triton/initialise_deployment', intercept_launch_inference)])
    app.add_routes([web.get('/node/available', available_node)])
    app.add_routes([web.get('/node/cameras', get_cameras)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, server, port)
    await site.start()
    camera_task = loop.create_task(update_system_cameras(cameras))
    connection_task =  loop.create_task(configure_connection())
    await connection_task
    global pipelines
    if connection_task.result() == 'isolated':
        print("The node cannot connect securely with the master server")    
        sys.exit(1)
    elif connection_task.result() == 'remote':
        print("The node has connected securely with the master server")    
        print(f"This server has been launched in remote mode: http://0.0.0.0:2500")
        node_devices = await get_cameras("manual")
        device_connection_task = loop.create_task(connect_devices(node_devices))
        await device_connection_task
        if device_connection_task.result() == 'Synced':
            node_devices = await get_cameras("manual")
            gstreamer_task = loop.create_task(initialise_gstreamer())
            await gstreamer_task
            gloop = gstreamer_task.result()
            pipeline_task = loop.create_task(manage_pipelines(node_devices, gloop))
            await pipeline_task
            pipelines = pipeline_task.result()
            display_task = loop.create_task(display_sinks(pipelines))
            await display_task
            if display_task.result() == 'Displayed':
                print("Device pipelines initialised successfully")
                print(pipelines.display_all_pipelines())                
                for name, info in pipelines.items():
                    print("Processing deployment pipeline: "+name)
                    pipeline = info['pipeline'] 
                    tee = info['tee']
                    deployments_pipeline = loop.create_task(execute_deployment_pipeline(name, pipeline, tee))
                    await deployments_pipeline       
            else:
                print("Device pipeline(s) failed to initialise")
                for error in display_task.result():
                    print(error)
                sys.exit(1)
        else:
            print(f"Initial devices have failed to sync with the master service")
            sys.exit(1)
    else:
        print("Server could not be configured")
        sys.exit(1)
    
async def main():
    await server_up()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()


