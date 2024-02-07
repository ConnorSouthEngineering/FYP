
Pipeline - take up whole screen
gst-launch-1.0 v4l2src device=/dev/video1 ! 'video/x-raw, format=UYVY, width=1920, height=1080' ! nvvidconv ! 'video/x-raw(memory:NVMM), format=I420, width=1920, height=1080' ! nvoverlaysink sync=false

Pipeline - show in smaller window:
gst-launch-1.0 v4l2src device=/dev/video1 ! 'video/x-raw, format=(string)UYVY, width=(int)1280, height=(int)720, framerate=(fraction)45/1' ! videoconvert ! videoscale ! 'video/x-raw, width=1280, height=720' ! ximagesink sync=false

If you want to feed one stream to multiple endpoints (i.e mux -- src to multiple sinks) you can do so via the tee element in the gstreamer pipeline. The tee element allows for the amount of sinks to be changed dynamically