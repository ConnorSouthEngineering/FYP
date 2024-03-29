import os
os.environ["GST_DEBUG_DUMP_DOT_DIR"] = "./"
os.environ["GST_DEBUG"] = "GST_STATE_DUMP:2"
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

def add_sink(pipeline, deployment_name, tee, gloop_state):
    queue = Gst.ElementFactory.make("queue", f"queue_{deployment_name}")
    queue.set_property("leaky", 2)
    queue.set_property("max-size-buffers", 5)
    queue.set_property("max-size-time", 16000000)

    videoconvert = Gst.ElementFactory.make("videoconvert", f"videoconvert_{deployment_name}")
    videoscale = Gst.ElementFactory.make("videoscale", f"videoscale_{deployment_name}")
    sink = Gst.ElementFactory.make("appsink", f"sink_{deployment_name}")
    sink.set_property("emit-signals", True)  
    sink.set_property("sync", False)
    sink.set_property("max-buffers", 5)  
    sink.set_property("drop", True)  

    if not all([queue, videoconvert, videoscale, sink]):
        print("Failed to create elements for new sink")
        return

    pipeline.add(queue)
    pipeline.add(videoconvert)
    pipeline.add(videoscale)
    pipeline.add(sink)

    if not queue.link(videoconvert):
        print("Failed to link queue to videoconvert")
    if not videoconvert.link(videoscale):
        print("Failed to link videoconvert to videoscale")
    if not videoscale.link(sink):
        print("Failed to link videoscale to sink")

    pad_template = tee.get_pad_template("src_%u")
    src_pad = tee.request_pad(pad_template, None, None)
    sink_pad = queue.get_static_pad("sink")
    if src_pad.link(sink_pad) != Gst.PadLinkReturn.OK:
        print("Failed to link tee to queue")
    
    ret = queue.sync_state_with_parent()
    print(f"Syncing queue state with parent returned: {ret}")
    ret = videoconvert.sync_state_with_parent()
    print(f"Syncing videoconvert state with parent returned: {ret}")
    ret = videoscale.sync_state_with_parent()
    print(f"Syncing videoscale state with parent returned: {ret}")
    ret = sink.sync_state_with_parent()
    print(f"Syncing sink state with parent returned: {ret}")
    if gloop_state:
        return False
    else:
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
    print(camera_path)
    return camera_path

async def add_new_sink(pipeline, deployment_name, tee):
    GLib.timeout_add_seconds(1, add_sink, pipeline, deployment_name, tee, True)

async def initialise_pipeline(camera, gloop):
    global pipelines
    camera_path = get_camera_path(camera)
    pipeline, tee = generate_pipeline(camera_path)
    pipeline = add_sink(pipeline,"initialisation", tee, False)
    pipelines.add_pipeline(camera, "initialisation", pipeline, tee)
    return

##Pipeline involving GPU optimised transition between UVYV to RGBA
def generate_pipeline(camera_path):
    pipeline = Gst.Pipeline.new(f"dynamic-pipeline-{camera_path}")
    source = Gst.ElementFactory.make("nvv4l2camerasrc", "source")
    source.set_property("device", camera_path)

    nvvidconv_UYVY = Gst.ElementFactory.make("nvvidconv", "nvvidconv_UYVY")

    capsfilter_UYVY = Gst.ElementFactory.make("capsfilter", "caps")
    caps = Gst.Caps.from_string("video/x-raw(memory:NVMM), format=(string)UYVY, width=(int)1920, height=(int)1080, framerate=(fraction)30/1")
    capsfilter_UYVY.set_property("caps", caps)

    nvvidconv_RGBA = Gst.ElementFactory.make("nvvidconv", "nvvidconv_RGBA")
    capsfilter_RGBA = Gst.ElementFactory.make("capsfilter", "RGBA_caps")
    caps_RGBA = Gst.Caps.from_string("video/x-raw, format=(string)RGBA")
    capsfilter_RGBA.set_property("caps", caps_RGBA)

    tee = Gst.ElementFactory.make("tee", "tee")

    pipeline.add(source)
    pipeline.add(nvvidconv_UYVY)
    pipeline.add(capsfilter_UYVY)
    pipeline.add(nvvidconv_RGBA)
    pipeline.add(capsfilter_RGBA)
    pipeline.add(tee)

    if not source.link(nvvidconv_UYVY):
        print("Failed to link source to nvvidconv_UYVY")
    elif not nvvidconv_UYVY.link(capsfilter_UYVY):
        print("Failed to link nvvidconv_UYVY to capsfilter_UYVY")
    elif not capsfilter_UYVY.link(nvvidconv_RGBA):
        print("Failed to link capsfilter_UYVY to nvvidconv_RGBA")
    elif not nvvidconv_RGBA.link(capsfilter_RGBA):
        print("Failed to link nvvidconv_RGBA to capsfilter_RGBA")
    elif not capsfilter_RGBA.link(tee):
        print("Failed to link capsfilter_RGBA to tee")
    else:
        print("Elements linked successfully")
    return pipeline, tee


##Pipeline involving CPU optimised transition between UVYV to RGB
def generate_pipeline_CPU(camera_path):
    pipeline = Gst.Pipeline.new(f"dynamic-pipeline-{camera_path}")
    source = Gst.ElementFactory.make("v4l2src", "source")
    source.set_property("device", camera_path)
    videoconvert_initialise = Gst.ElementFactory.make("videoconvert", "videoconvert")
    capsfilter = Gst.ElementFactory.make("capsfilter", "caps")
    caps = Gst.Caps.from_string("video/x-raw, format=(string)UYVY, width=(int)1920, height=(int)1080, framerate=(fraction)30/1")
    capsfilter.set_property("caps", caps)
    videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert2")
    rgb_capsfilter = Gst.ElementFactory.make("capsfilter", "rgb_caps")
    rgb_caps = Gst.Caps.from_string("video/x-raw, format=(string)RGB")
    rgb_capsfilter.set_property("caps", rgb_caps)
    tee = Gst.ElementFactory.make("tee", "tee")

    pipeline.add(source)
    pipeline.add(videoconvert_initialise)
    pipeline.add(capsfilter)
    pipeline.add(videoconvert)
    pipeline.add(rgb_capsfilter)
    pipeline.add(tee)

    if not source.link(videoconvert_initialise):
        print("Failed to link source to capsfilter")
    elif not videoconvert_initialise.link(capsfilter):
        print("Failed to link capsfilter to nvvidconv")
    elif not capsfilter.link(videoconvert):
        print("Failed to link nvvidconv to videoconvert")
    elif not videoconvert.link(rgb_capsfilter):
        print("Failed to link videoconvert to rgb_capsfilter")
    elif not rgb_capsfilter.link(tee):
        print("Failed to link rgb_capsfilter to tee")
    else:
        print("Elements linked successfully")
    return pipeline, tee

async def manage_pipelines(node_devices, gloop):
    global pipelines
    cameras = json.loads(node_devices)["cameras"]
    for camera in cameras:
         if not pipelines.get_pipeline(camera):
            await initialise_pipeline(camera, gloop)
    return pipelines

async def play_pipelines(pipelines):
    initialisation_errors = []
    for pipeline_name, pipeline_info in pipelines.items():
        try:
            gst_pipeline = pipeline_info['pipeline'] 
            gst_pipeline.set_state(Gst.State.PLAYING)
        except Exception as e:
            initialisation_errors.append(e)
    if initialisation_errors:
        return initialisation_errors
    return "Displayed"

