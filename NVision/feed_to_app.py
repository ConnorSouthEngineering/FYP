from threading import Thread
from time import sleep
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
from gi.repository import Gst, GstApp, GLib

_ = GstApp

Gst.init()

from time import sleep

main_loop = GLib.MainLoop()

main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

pipeline= Gst.parse_launch("v4l2src device=/dev/video0 ! video/x-raw, format=(string)UYVY, width=(int)1280, height=(int)720, framerate=(fraction)45/1 ! videoconvert ! appsink name=sink")
appsink = pipeline.get_by_name('sink')

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sample = appsink.try_pull_sample(Gst.SECOND)
        if sample is not None:
            print("Sample received")
        else:
            continue
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()