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

def pad_added_handler(src,new_pad,data):
    print("Pad added;", new_pad.get_name())

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
    Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, f"pipeline_before_{deployment_name}")
    if get_pipeline_state(pipeline) == Gst.State.PAUSED:
        ret = pipeline.set_state(Gst.State.PLAYING)
        print(f"Setting queue to PLAYING returned: {ret}")
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
    if gloop_state:
        print("Setting individual elements to PAUSED state and printing return values:")
        ret = queue.set_state(Gst.State.PAUSED)
        print(f"Setting queue to PAUSED returned: {ret}")
        ret = videoconvert.set_state(Gst.State.PAUSED)
        print(f"Setting videoconvert to PAUSED returned: {ret}")
        ret = videoscale.set_state(Gst.State.PAUSED)
        print(f"Setting videoscale to PAUSED returned: {ret}")
        ret = sink.set_state(Gst.State.PAUSED)
        print(f"Setting sink to PAUSED returned: {ret}")
    # Sync state with parent after adding to pipeline and linking
    print("Syncing state with parent and printing return values:")
    ret = queue.sync_state_with_parent()
    print(f"Syncing queue state with parent returned: {ret}")
    ret = videoconvert.sync_state_with_parent()
    print(f"Syncing videoconvert state with parent returned: {ret}")
    ret = videoscale.sync_state_with_parent()
    print(f"Syncing videoscale state with parent returned: {ret}")
    ret = sink.sync_state_with_parent()
    print(f"Syncing sink state with parent returned: {ret}")
    Gst.debug_bin_to_dot_file(pipeline, Gst.DebugGraphDetails.ALL, f"pipeline_after_{deployment_name}")
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

def generate_pipeline(camera_path):
    pipeline = Gst.Pipeline.new("dynamic-pipeline")
    source = Gst.ElementFactory.make("nvv4l2camerasrc", "source")
    source.set_property("device", "/dev/video0")
    capsfilter = Gst.ElementFactory.make("capsfilter", "caps")
    caps = Gst.Caps.from_string("video/x-raw(memory:NVMM), format=(string)UYVY, width=(int)1920, height=(int)1080, framerate=(fraction)30/1")
    capsfilter.set_property("caps", caps)
    nvvidconv = Gst.ElementFactory.make("nvvidconv", "nvvidconv")
    videoconvert = Gst.ElementFactory.make("videoconvert", "videoconvert")
    rgb_capsfilter = Gst.ElementFactory.make("capsfilter", "rgb_caps")
    rgb_caps = Gst.Caps.from_string("video/x-raw, format=(string)RGB")
    rgb_capsfilter.set_property("caps", rgb_caps)
    tee = Gst.ElementFactory.make("tee", "tee")

    pipeline.add(source)
    pipeline.add(capsfilter)
    pipeline.add(nvvidconv)
    pipeline.add(videoconvert)
    pipeline.add(rgb_capsfilter)
    pipeline.add(tee)

    if not source.link(capsfilter):
        print("Failed to link source to capsfilter")
    elif not capsfilter.link(nvvidconv):
        print("Failed to link capsfilter to nvvidconv")
    elif not nvvidconv.link(videoconvert):
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

async def display_sinks(pipelines):
    initialisation_errors = []
    for pipeline_name, pipeline_info in pipelines.items():
        print(pipeline_name)
        try:
            gst_pipeline = pipeline_info['pipeline'] 
            get_pipeline_state(gst_pipeline)
            Gst.debug_bin_to_dot_file(gst_pipeline, Gst.DebugGraphDetails.ALL, f"pipeline_{pipeline_name}_before_state")
            gst_pipeline.set_state(Gst.State.PLAYING)
            Gst.debug_bin_to_dot_file(gst_pipeline, Gst.DebugGraphDetails.ALL, f"pipeline_{pipeline_name}_after_state")
            get_pipeline_state(gst_pipeline)
        except Exception as e:
            initialisation_errors.append(e)
    if initialisation_errors:
        return initialisation_errors
    return "Displayed"

