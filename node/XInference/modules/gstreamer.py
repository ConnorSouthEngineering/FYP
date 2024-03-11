import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst
Gst.init(None)

import asyncio

camera_task = None

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


