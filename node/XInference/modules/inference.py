import cv2
import numpy as np
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException
from collections import deque
from PIL import Image

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst, GLib
Gst.init(None)

from .gstreamer import get_pipeline_state

def preprocess_frames(frame, WIDTH, HEIGHT):
    frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    return frame_rgb.astype('float32') / 255.0  

async def initialise_inference(pipeline, sink_name, height, width, class_list, sequence_length, model_name):
    print(get_pipeline_state(pipeline))
    triton_url = 'localhost:8000'
    triton_client = httpclient.InferenceServerClient(url=triton_url)
    if not isinstance(pipeline, Gst.Pipeline):
        print("The provided argument is not a Gst.Pipeline instance.")
        return

    appsink = pipeline.get_by_name(sink_name)
    if not appsink:
        print("Appsink not found.")
        return

    frames_queue = deque(maxlen=sequence_length)
    if get_pipeline_state(pipeline) != Gst.State.PLAYING:
        print("Pipeline in incorrect state restart the node")
        return

    print("Pipeline and sink were correctly retrieved")
    print(f"Inference for {sink_name} with model {model_name} is occuring")
    GLib.timeout_add_seconds(1, pull_frame, pipeline, appsink, sink_name, frames_queue, int(width), int(height), sequence_length, triton_client, model_name, class_list)
    return

def pull_frame(pipeline, appsink, sink_name, frames_queue, width, height, sequence_length, triton_client, model_name, class_list):
    
    sample = appsink.emit("pull-sample")
    if sample is None:
        print("No more frames or sink unavailable.")
        return True
    
    try:
        buffer = sample.get_buffer()
        caps_format = sample.get_caps().get_structure(0)
        input_width = caps_format.get_value("width")
        input_height = caps_format.get_value("height")
        success, map_info = buffer.map(Gst.MapFlags.READ)
        
        if not success:
            print("Failed to map buffer")
            return True
        img_data = np.frombuffer(map_info.data, dtype=np.uint8)
        img = Image.frombytes("RGB", (input_width, input_height), img_data)
        img.save(f"{sink_name}.jpg")
        frame = np.frombuffer(map_info.data, dtype=np.uint8).reshape((input_height, input_width, 3))
        processed_frame = preprocess_frames(frame, width, height)  
        frames_queue.append(processed_frame)
    finally:
        if 'map_info' in locals() and map_info:
            buffer.unmap(map_info)

    if len(frames_queue) == sequence_length:
        input_batch = np.stack(list(frames_queue), axis=0)
        input_batch = np.expand_dims(input_batch, axis=0)
            
        try:
            input_tensor = httpclient.InferInput('conv_lstm2d_input', input_batch.shape, "FP32")
            input_tensor.set_data_from_numpy(input_batch)
            response = triton_client.infer(model_name, inputs=[input_tensor])                
            output_data = response.as_numpy('dense')
            predicted_class = class_list[np.argmax(output_data)]
            print(f"Deployment_sink: {sink_name} Predicted class: {predicted_class}")
        except InferenceServerException as e:
            print(f"InferenceServerException: {str(e)}")
        frames_queue.clear() 
    return True  
