from threading import Thread
from time import sleep
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init()

from time import sleep

main_loop = GLib.MainLoop()

main_loop_thread = Thread(target=main_loop.run)
main_loop_thread.start()

pipeline= Gst.parse_launch("v4l2src device=/dev/video0 ! video/x-raw, format=(string)UYVY, width=(int)1280, height=(int)720, framerate=(fraction)45/1 ! videoconvert ! videoscale ! video/x-raw, width=1280, height=720 ! ximagesink sync=false")

pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()
main_loop_thread.join()