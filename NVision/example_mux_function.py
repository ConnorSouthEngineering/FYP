import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import signal

# Initialize GStreamer
Gst.init(None)

# Create the main loop
loop = GLib.MainLoop()

# Handle SIGINT to stop the loop
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Create elements
pipeline = Gst.Pipeline.new("dynamic-pipeline")    ## Here the pipeline is created
source = Gst.ElementFactory.make("videotestsrc", "source") ## Then each individual element of the pipeline is created 
tee = Gst.ElementFactory.make("tee", "tee")                ##(i.e each segment of the string in parse_launch)
queue1 = Gst.ElementFactory.make("queue", "queue1")
sink1 = Gst.ElementFactory.make("autovideosink", "sink1")

if not pipeline or not source or not tee or not queue1 or not sink1:
    print("Not all elements could be created.")
    exit(-1)

# The elements are then added to the pipeline in order
pipeline.add(source)
pipeline.add(tee)
pipeline.add(queue1)
pipeline.add(sink1)

# Link elements
source.link(tee)
tee.link(queue1)
queue1.link(sink1)

# Function to add a new sink dynamically
def add_new_sink():
    queue = Gst.ElementFactory.make("queue")   ## This is dynamically named by gstreamer so functionality would need to be added to make queue identifiable
    sink = Gst.ElementFactory.make("autovideosink") ## This is dynamically named by gstreamer so functionality would need to be added to make sink identifiable
    pipeline.add(queue) ## Queue is used to isolate the information passing between src and sink along tee, so it is not impacted by other processing
    pipeline.add(sink) ## linked in order of heirarchy, a sink must be linked to a queue (think of it like a branch or stream) 
    queue.link(sink) ## and that queue must belong to a specific tee
    tee.link(queue)  ## Link takes the "source pad" of the target element and links to the "sink pad" of the next element 
    queue.sync_state_with_parent() ##Link flow: v4l2src -> tee -> queue -> sink
    sink.sync_state_with_parent()

# Function to remove a sink dynamically
def remove_sink(queue, sink):
    tee.unlink(queue)
    queue.set_state(Gst.State.NULL)
    sink.set_state(Gst.State.NULL)
    pipeline.remove(queue)
    pipeline.remove(sink)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

try:
    # Run the main loop
    loop.run()
except:
    # Clean up
    pipeline.set_state(Gst.State.NULL)
    print("Pipeline stopped")
