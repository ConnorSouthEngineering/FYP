from aiohttp import web
import asyncio
import json
import configparser
import sys
import getpass
import os
import ast
import builtins
from datetime import datetime
import pdb
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst, GLib
Gst.init(None)
# Save the original print function
import builtins
import time

# Record the start time
start_time = time.time()

# Ensure we save the original print function before it gets overridden
# to prevent any recursion with our custom print function.
_original_print = builtins.print

def timestamped_print(*args, **kwargs):
    elapsed_time = time.time() - start_time
    # Format the elapsed time. The formatting here is to match your requested output as closely as possible.
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Now using _original_print to ensure we call the true original print function.
    _original_print(f"{int(hours)}:{int(minutes):02d}:{seconds:09.6f}", *args, **kwargs)

# Override the built-in print with our custom function
builtins.print = timestamped_print

# Example usage
print("This is a test message with a timestamp.")
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "./"

# Now every print call will include a timestamp
print("Hello, world!")
from modules.gstreamer import update_system_cameras, manage_pipelines, initialise_gstreamer, display_sinks, add_new_sink
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
    create_sink_task = loop.create_task(add_new_sink(pipeline, deployment_name, tee))
    while True:
        appsink = pipeline.get_by_name(f'sink_{deployment_name}')
        queue = pipeline.get_by_name(f'queue_{deployment_name}')
        videoconvert = pipeline.get_by_name(f'videoconvert_{deployment_name}')
        videoscale = pipeline.get_by_name(f'videoscale_{deployment_name}')
        if not appsink:
            print("Appsink not found.")
        else:
            print("Pre set state")
            current_state = appsink.get_state(2)
            print(current_state)
            current_state = queue.get_state(2)
            print(current_state)
            current_state = videoconvert.get_state(2)
            print(current_state)
            current_state = videoscale.get_state(2)
            print(current_state)
            queue.set_state(Gst.State.PLAYING)
            videoconvert.set_state(Gst.State.PLAYING)
            videoscale.set_state(Gst.State.PLAYING)
            appsink.set_state(Gst.State.PLAYING)
            print("Post set state")
            current_state = appsink.get_state(2)
            print(current_state)
            current_state = queue.get_state(2)
            print(current_state)
            current_state = videoconvert.get_state(2)
            print(current_state)
            current_state = videoscale.get_state(2)
            print(current_state)
            appsink.set_state(Gst.State.PLAYING)
            await asyncio.sleep(10)
            print("Post sleep state")
            current_state = appsink.get_state(2)
            print(current_state)
            current_state = queue.get_state(2)
            print(current_state)
            current_state = videoconvert.get_state(2)
            print(current_state)
            current_state = videoscale.get_state(2)
            print(current_state)
            Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, f"DEBUG_{deployment_name}")
            break
        await asyncio.sleep(1)
    loop.create_task(initialise_inference(pipeline, f'sink_{deployment_name}', int(height), int(width), class_list, num_frames, triton_location_name))
    print("test")  
    inference_task = loop.create_task(initialise_inference(pipeline, f'sink_{deployment_name}', int(height), int(width), class_list, num_frames, triton_location_name))
    await inference_task
    return

async def a_launch_inference(deployment_id, model_id, pipeline):
    global pipelines
    pipeline_info = pipelines.get_pipeline("vi-output, ar0230 30-0043")
    sink_name = "sink_initialisation"
    inference_task = loop.create_task(initialise_inference(pipeline_info["pipeline"], sink_name))
    return web.Response(text="Inference launched", content_type='application/json')

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
    os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "/tmp"
    os.putenv('GST_DEBUG_DUMP_DIR_DIR', '/tmp')
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
        print(f"This server has been launched in isolated mode: http://0.0.0.0:2500")

        ### Please not the below is only for debugging and development purposes when the master server is off and should be removed when in a fit state
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
        else:
            print("Device pipeline(s) failed to initialise")
            for error in display_task.result():
                print(error)
            sys.exit(1)

    elif connection_task.result() == 'remote':
        print("The node has connected securely with the master server")    
        print(f"This server has been launched in remote mode: http://0.0.0.0:2500")
        node_devices = await get_cameras("manual")
        device_connection_task = loop.create_task(connect_devices(node_devices))
        await device_connection_task
        if device_connection_task.result() == 'Synced':
            ### Please not the below is only for debugging and development purposes when the master server is off and should be removed when in a fit state
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

""" loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever() """

