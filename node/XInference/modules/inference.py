import cv2
import numpy as np
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException
from collections import deque
from gi.repository import Gst, GLib
from PIL import Image

Gst.init(None)

def preprocess_frames(frame, WIDTH, HEIGHT):
    frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    return frame_rgb.astype('float32') / 255.0

async def initialise_inference(pipeline, sink_name):
    HEIGHT, WIDTH = 224, 224
    MODEL_NAME = "Toyota_Model_Full_10"
    SEQUENCE_LENGTH = 10
    CLASS_LIST = ['cooking', 'drinking', 'eating', 'pouring']
    triton_url = 'localhost:8000'
    triton_client = httpclient.InferenceServerClient(url=triton_url)
    appsink = pipeline.get_by_name(sink_name)
    if not appsink:
        print("Appsink not found.")
        return
    frames_queue = deque(maxlen=SEQUENCE_LENGTH)
    state = get_pipeline_state(pipeline)
    if state != Gst.State.PLAYING:
        pipeline.set_state(Gst.State.PLAYING)
        print("Pipeline set to playing state")
    print("Inference Occuring")
    GLib.timeout_add_seconds(1, pull_frame, pipeline, appsink, frames_queue, WIDTH, HEIGHT, SEQUENCE_LENGTH, triton_client, MODEL_NAME, CLASS_LIST)

def get_pipeline_state(pipeline):
    state_change, current_state, pending_state = pipeline.get_state(Gst.CLOCK_TIME_NONE)
    return current_state

def pull_frame(pipeline, appsink, frames_queue, WIDTH, HEIGHT, SEQUENCE_LENGTH, triton_client, MODEL_NAME, CLASS_LIST):
    print("Inference Occurring")
    sample = appsink.emit("pull-sample")
    if sample is None:
        print("No more frames or sink unavailable.")
        return False  
    print("Buffers captured")
    try:
        print("Buffer mapping")
        buffer = sample.get_buffer()
        caps_format = sample.get_caps().get_structure(0)
        width = caps_format.get_value("width")
        height = caps_format.get_value("height")
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if not success:
            print("Failed to map buffer")
            return True
        img_data = np.frombuffer(map_info.data, dtype=np.uint8)
        img = Image.frombytes("RGB", (width, height), img_data)
        img.save("output_image.jpg")
        frame = np.frombuffer(map_info.data, dtype=np.uint8).reshape((height, width, 3))
        print("Created numpy frame")
        processed_frame = preprocess_frames(frame, WIDTH, HEIGHT)  
        frames_queue.append(processed_frame)
        print("Frame preprocessed")
    finally:
        if 'map_info' in locals() and map_info:
            buffer.unmap(map_info)
    if len(frames_queue) == SEQUENCE_LENGTH:
        print("Frame queue length acceptable initialising inference")
        input_batch = np.stack(list(frames_queue), axis=0)
        input_batch = np.expand_dims(input_batch, axis=0)
        try:
            input_tensor = httpclient.InferInput('conv_lstm2d_input', input_batch.shape, "FP32")
            input_tensor.set_data_from_numpy(input_batch)
            response = triton_client.infer(MODEL_NAME, inputs=[input_tensor])                
            output_data = response.as_numpy('dense')
            predicted_class = CLASS_LIST[np.argmax(output_data)]
            predicted_class = CLASS_LIST[np.argmax(output_data)]
            print(f"Predicted Class: {predicted_class}")
            print(f"Predicted Class: {predicted_class}")
        except InferenceServerException as e:
            print(f"InferenceServerException: {str(e)}")
        frames_queue.clear() 
    return True 
