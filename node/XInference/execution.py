import json
import configparser
import sys
from aiohttp import web
import asyncio
import getpass
from jtop import jtop
import datetime
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
Gst.init(None)

from modules.gstreamer import update_system_cameras, manage_pipelines, initialise_gstreamer, play_pipelines, add_new_sink
from modules.connection import configure_connection, connect_devices
from modules.inference import finalise_inference
from modules.deployments import retrieve_active_deployments, get_model, gather_model_information, extract_list_from_string
from modules.classes import PipelineStorage
from modules.monitoring import dump_logs, compile_performance_entry

cameras = []
pipelines = PipelineStorage()
deployment_count = 0
csv_log = []
global jetson

async def intercept_launch_inference(request):
    body = await request.json()
    deployment_model = body[0]['initialise_deployment']
    inference_task = loop.create_task(launch_inference(deployment_model))
    await inference_task
    return web.Response(text="Inference launched", content_type='application/json')

async def launch_inference(deployment_id, model_id, pipeline, name, tee):
    global deployment_count
    global jetson
    global csv_log
    abs_path = f'/home/{getpass.getuser()}/Desktop/FYP/node/XInference/node.conf'
    node_config = configparser.ConfigParser()
    node_config.read(abs_path)

    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Retrieving model"))
    model_information = await get_model(model_id, node_config)
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Model data retrieved"))

    num_frames = model_information['num_frames']
    triton_location_name = model_information['location_name']
    deployment_name = f"deployment_{deployment_id}"

    height, width, config_classes = await gather_model_information(triton_location_name)   
    class_list = await extract_list_from_string(config_classes)
    
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f"Attempting to add sink"))
    create_sink_task = loop.create_task(add_new_sink(pipeline, deployment_name, tee))
    while True:
        appsink = pipeline.get_by_name(f'sink_{deployment_name}')
        if not appsink:
            print("Appsink not found.")
        else:
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f"Sink successfully added"))
            break
        await asyncio.sleep(1)
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Finalising inference"))
    inference_task = loop.create_task(finalise_inference(pipeline, f'sink_{deployment_name}', int(height), int(width), class_list, num_frames, triton_location_name, deployment_count, jetson, csv_log, loop))
    await inference_task
    deployment_count = inference_task.result()
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Inference launched for {name}, Total Deployments: {deployment_count}'))
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
    global jetson
    global csv_log
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Retrieving Deployments for {name}'))
    node_deployments_task = loop.create_task(retrieve_active_deployments(name))
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f"Deployments retrieved"))
    await node_deployments_task                    
    deployments = node_deployments_task.result()
    if deployments:
        for deployment in deployments:
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Launching inference for {name}'))
            inference_task = loop.create_task(launch_inference(deployment['deployment_id'], deployment['model_id'], pipeline, name, tee))
            await inference_task
        return
    else:
        print(f"No active deployments for camera: {name}")
    return

async def server_up():
    global cameras
    global pipeline
    global jetson
    global csv_log

    file_path = f"/home/{getpass.getuser()}/Desktop/FYP/node/XInference/analytics/Logs/XInference_Deployment_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.csv"
    await compile_performance_entry(jetson, csv_log, "Initialising Logging")
    
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
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Server Initialised"))

    monitoring_task = loop.create_task(dump_logs(csv_log, file_path))
    camera_task = loop.create_task(update_system_cameras(cameras))
    
    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Configuring Connection"))
    connection_task =  loop.create_task(configure_connection())
    await connection_task 
    
    if connection_task.result() == 'isolated':
        print("The node cannot connect securely with the master server") 
        loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Failed to Establish Connection"))
        sys.exit(1)
    
    elif connection_task.result() == 'remote':
        loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Connection Established"))
        print("The node has connected securely with the master server")    

        node_devices = await get_cameras("manual")
        
        loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Connecting Devices To Master Server"))
        device_connection_task = loop.create_task(connect_devices(node_devices))
        await device_connection_task
        
        if device_connection_task.result() == 'Synced':
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Connection Established"))
            node_devices = await get_cameras("manual")
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Initialising Gstreamer"))
            gstreamer_task = loop.create_task(initialise_gstreamer())
            await gstreamer_task
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Gstreamer Initialised"))
            gloop = gstreamer_task.result()
            
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Creating Pipelines"))
            pipeline_task = loop.create_task(manage_pipelines(node_devices, gloop))
            await pipeline_task
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Pipelines Created"))

            pipelines = pipeline_task.result()
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Set Pipelines State"))
            display_task = loop.create_task(play_pipelines(pipelines))

            await display_task
            if display_task.result() == 'Displayed':
                loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Pipelines State set to Playing"))
            
                for name, info in pipelines.items():
                    print("Processing deployment pipeline: "+name)
                    loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Processing Pipeline {name}'))
                    
                    pipeline = info['pipeline'] 
                    tee = info['tee']
                    deployments_pipeline = loop.create_task(execute_deployment_pipeline(name, pipeline, tee))
                    await deployments_pipeline      
            else:
                loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Pipelines State failed to set"))
                for error in display_task.result():
                    print(error)
                sys.exit(1)
        else:
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, "Failed to Establish Connection"))
            print(f"Initial devices have failed to sync with the master service")
            sys.exit(1)
    else:
        print("Server could not be configured")
        sys.exit(1)
    
async def main():
    await server_up()


if __name__ == "__main__":
    with jtop() as jetson: 
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        loop.run_forever()