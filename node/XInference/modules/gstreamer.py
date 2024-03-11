import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
Gst.init(None)

import asyncio
import json
import platform 
from aiohttp import web

camera_task = None
cameras = []

async def launch_inference():
    print("Launch inference")

async def update_system_cameras():
    while True:
        new_cameras = []
        global cameras
        monitor = Gst.DeviceMonitor()
        video_filter = Gst.Caps.from_string("video/x-raw")
        monitor.add_filter("Video/Source", video_filter)
        monitor.start()
        for device in monitor.get_devices():
            print(device.get)
            new_cameras.append(device.get_display_name())
        monitor.stop()

        if set(new_cameras) != set(cameras):
            cameras = new_cameras
        await asyncio.sleep(10)

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
