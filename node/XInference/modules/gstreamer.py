import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst, GLib
import signal
Gst.init(None)

import asyncio
import json
import threading
from modules.classes import PipelineStorage

camera_task = None
pipelines = PipelineStorage()

async def initialise_gstreamer():
    Gst.init(None)
    loop = GLib.MainLoop()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    thread = threading.Thread(target=loop.run)
    thread.start()
    return loop

async def update_system_cameras(cameras):
    while True:
        new_cameras = []
        monitor = Gst.DeviceMonitor()
        video_filter = Gst.Caps.from_string("video/x-raw")
        monitor.add_filter("Video/Source", video_filter)
        monitor.start()
        for device in monitor.get_devices():
            new_cameras.append(device.get_display_name())
        monitor.stop()
        if set(new_cameras) != set(cameras):
            cameras.clear()
            cameras.extend(new_cameras) 

        await asyncio.sleep(10)

def get_pipeline_state(pipeline):
    state_change, current_state, pending_state = pipeline.get_state(Gst.CLOCK_TIME_NONE)
    return current_state

def add_sink(pipeline, deployment_name, tee):
    if get_pipeline_state(pipeline) == Gst.State.PLAYING:
        pipeline.set_state(Gst.State.NULL)
    queue = Gst.ElementFactory.make("queue", f"queue_{deployment_name}")
    queue.set_property("leaky", 2)
    queue.set_property("max-size-buffers", 0)

    videoconvert = Gst.ElementFactory.make("videoconvert", f"videoconvert_{deployment_name}")
    videoscale = Gst.ElementFactory.make("videoscale", f"videoscale_{deployment_name}")
    sink = Gst.ElementFactory.make("appsink", f"sink_{deployment_name}")
    sink = Gst.ElementFactory.make("appsink", None)
    sink.set_property("emit-signals", True)  
    sink.set_property("sync", False)
    sink.set_property("max-buffers", 10)  
    sink.set_property("drop", True)  
    sink.set_property("sync", False)

    if not all([queue, videoconvert, videoscale, sink]):
        print("Failed to create elements for new sink")
        return pipeline

    pipeline.add(queue)
    pipeline.add(videoconvert)
    pipeline.add(videoscale)
    pipeline.add(sink)

    pad_template = tee.get_pad_template("src_%u")
    src_pad = tee.request_pad(pad_template, None, None)
    sink_pad = queue.get_static_pad("sink")
    if not src_pad.link(sink_pad) == Gst.PadLinkReturn.OK:
        print("Failed to link tee to queue")

    queue.sync_state_with_parent()
    videoconvert.sync_state_with_parent()
    videoscale.sync_state_with_parent()
    sink.sync_state_with_parent()

    return pipeline

def get_camera_path(camera):
    monitor = Gst.DeviceMonitor()
    video_filter = Gst.Caps.from_string("video/x-raw")
    monitor.add_filter("Video/Source", video_filter)
    monitor.start()
    device_obj = None
    for device in monitor.get_devices():
        if device.get_display_name() == camera:
            device_obj = device
            break
    monitor.stop()
    props = device_obj.get_properties()
    camera_path = props.get_string("device.path")
    return camera_path

async def initialise_pipeline(camera, gloop):
    global pipelines
    camera_path = get_camera_path(camera)
    pipeline, tee = generate_pipeline(camera_path, gloop)
    pipeline = add_sink(pipeline,"initialisation", tee)
    pipelines.add_pipeline(camera, "initialisation", pipeline, tee)
    return

def generate_pipeline(camera_path):
    Gst.init(None)
    pipeline = Gst.Pipeline.new("dynamic-pipeline")
    source = Gst.ElementFactory.make("v4l2src", "source")
    source.set_property("device", camera_path)
    capsfilter = Gst.ElementFactory.make("capsfilter", "caps")
    caps = Gst.Caps.from_string("video/x-raw, format=(string)UYVY, width=(int)1280, height=(int)720, framerate=(fraction)45/1")
    capsfilter.set_property("caps", caps)
    nvvidconv = Gst.ElementFactory.make("nvvidconv", "nvvidconv")
    tee = Gst.ElementFactory.make("tee", "tee")
    
    pipeline.add(source)
    pipeline.add(capsfilter)
    pipeline.add(nvvidconv)
    pipeline.add(tee)

    return pipeline, tee

def generate_pipeline_CPU(camera_path):
    pipeline = Gst.Pipeline.new(f"dynamic-pipeline")
    source = Gst.ElementFactory.make("v4l2src", "source")
    source.set_property("device", camera_path)
    capsfilter = Gst.ElementFactory.make("capsfilter", "caps")
    caps = Gst.Caps.from_string("video/x-raw, format=(string)UYVY, width=(int)1920, height=(int)1080, framerate=(fraction)30/1")
    capsfilter.set_property("caps", caps)
    tee = Gst.ElementFactory.make("tee", "tee")
    
    if not all([pipeline, source, capsfilter, tee]):
        print("Not all elements could be created.")
        exit(-1)
    
    pipeline.add(source)
    pipeline.add(capsfilter)  
    pipeline.add(tee)
    
    if not source.link(capsfilter):
        print("Failed to link source to capsfilter")
    if not capsfilter.link(tee):  
        print("Failed to link capsfilter to tee")

    return pipeline, tee

async def manage_pipelines(node_devices, gloop):
    global pipelines
    cameras = json.loads(node_devices)["cameras"]
    for camera in cameras:
         if not pipelines.get_pipeline(camera):
            await initialise_pipeline(camera, gloop)
    return pipelines

async def display_sinks(pipelines):
    initialisation_errors = []
    for pipeline_name, pipeline_info in pipelines.items():
        print(pipeline_name)
        try:
            gst_pipeline = pipeline_info['pipeline'] 
            gst_pipeline.set_state(Gst.State.PLAYING)
        except Exception as e:
            initialisation_errors.append(e)
    if initialisation_errors:
        return initialisation_errors
    return "Displayed"