import cv2
import numpy as np
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException
from collections import deque
from PIL import Image
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import gi
gi.require_version('Gst','1.0')
from gi.repository import Gst, GLib
Gst.init(None)

from .gstreamer import get_pipeline_state
from .monitoring import compile_performance_entry

def preprocess_frames_RGBA(frame, WIDTH, HEIGHT):
    frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_RGBA2RGB)
    return frame_rgb.astype('float32') / 255.0  

def preprocess_frames_RGB(frame, WIDTH, HEIGHT):
    frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    return frame_rgb.astype('float32') / 255.0  

def load_data_RGB(mapped_data, input_height, input_width, width, height, sink_name, OUTPUT):
    buffered_data = np.frombuffer(mapped_data, dtype=np.uint8)
    if OUTPUT:
        img = Image.frombytes("RGB", (input_width, input_height), buffered_data)
        img.save(f"{sink_name}.png")
    frame = buffered_data.reshape((input_height, input_width, 3))
    return preprocess_frames_RGBA(frame, width, height)  

def load_data_RGBA(mapped_data, input_height, input_width, width, height, sink_name, OUTPUT):
    buffered_data = np.frombuffer(mapped_data, dtype=np.uint8)
    if OUTPUT:
        img = Image.frombytes("RGBA", (input_width, input_height), buffered_data)
        img_rgb = img.convert("RGB")
        img_rgb.save(f"{sink_name}.jpg")
    frame = buffered_data.reshape((input_height, input_width, 4))
    return preprocess_frames_RGBA(frame, width, height)  

async def finalise_inference(pipeline, sink_name, height, width, class_list, sequence_length, model_name, deployment_count, jetson, csv_log, loop):
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
    if sequence_length > 100:
        GLib.timeout_add_seconds(1, pull_frame_parallel, pipeline, appsink, sink_name, frames_queue, int(width), int(height), sequence_length, triton_client, model_name, class_list)
    else:
        GLib.timeout_add_seconds(1, pull_frame_linear, pipeline, appsink, sink_name, frames_queue, int(width), int(height), sequence_length, triton_client, model_name, class_list, jetson, csv_log, loop)
    deployment_count = deployment_count+1
    return deployment_count

def pull_frame_linear(pipeline, appsink, sink_name, frames_queue, width, height, sequence_length, triton_client, model_name, class_list, jetson, csv_log, loop):
    sample = appsink.emit("pull-sample")
    if sample is None:
        print("No more frames or sink unavailable.")
        return True
    try:
        buffer = sample.get_buffer()
        input_width = 1920
        input_height = 1080
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if not success:
            print("Failed to map buffer")
            return True

        ###Uncomment for use with GPU
        processed_frame = load_data_RGBA(map_info.data, input_height, input_width, width, height, sink_name, False)
        
        ##Uncomment for use with CPU
        #processed_frame = load_data_RGB(map_info.data, input_height, input_width, width, height, sink_name, False)
        frames_queue.append(processed_frame)
    finally:
        if 'map_info' in locals() and map_info:
            buffer.unmap(map_info)

    if len(frames_queue) == sequence_length:
        input_batch = np.stack(list(frames_queue), axis=0)
        input_batch = np.expand_dims(input_batch, axis=0)
        loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Batch of {sequence_length} Gathered for sink: {sink_name}'))
        try:
            input_tensor = httpclient.InferInput('conv_lstm2d_input', input_batch.shape, "FP32")
            input_tensor.set_data_from_numpy(input_batch)
            response = triton_client.infer(model_name, inputs=[input_tensor])                
            output_data = response.as_numpy('dense')
            predicted_class = class_list[np.argmax(output_data)]
            loggingtask = loop.create_task(compile_performance_entry(jetson, csv_log, f'Inference for sinK: {sink_name}'))
            print(f"{str(datetime.now().strftime('%H:%M:%S'))} - Deployment_sink: {sink_name} Predicted class: {predicted_class}")
        except InferenceServerException as e:
            print(f"InferenceServerException: {str(e)}")
        frames_queue.clear() 
    return True  

def pull_frame_parallel(pipeline, appsink, sink_name, frames_queue, width, height, sequence_length, triton_client, model_name, class_list):
    frames = gather_frames(appsink, sequence_length)
    process_frames_and_append(frames_queue, frames, width, height, sink_name)
    if len(frames_queue) == sequence_length:
        input_batch = np.stack(list(frames_queue), axis=0)
        input_batch = np.expand_dims(input_batch, axis=0)
            
        try:
            input_tensor = httpclient.InferInput('conv_lstm2d_input', input_batch.shape, "FP32")
            input_tensor.set_data_from_numpy(input_batch)
            response = triton_client.infer(model_name, inputs=[input_tensor])                
            output_data = response.as_numpy('dense')
            predicted_class = class_list[np.argmax(output_data)]
            print(f"{str(datetime.now().strftime('%H:%M:%S'))} - Deployment_sink: {sink_name} Predicted class: {predicted_class}")
        except InferenceServerException as e:
            print(f"InferenceServerException: {str(e)}")
        frames_queue.clear() 
    return True

def process_frame(sample, index, width, height, sink_name):
    try:
        buffer = sample.get_buffer()
        caps_format = sample.get_caps().get_structure(0)
        input_width = 1920
        input_height = 1080
        success, map_info = buffer.map(Gst.MapFlags.READ)
        if success:
            pass
        else:
            print("Failed to map buffer")
    finally:
        if 'map_info' in locals() and map_info:
            buffer.unmap(map_info)
    return (index, load_data_RGBA(map_info.data, input_height, input_width, width, height, sink_name, False))

def gather_frames(appsink, num_frames):
    frames = []
    while len(frames) < num_frames:
        sample = appsink.emit("pull-sample")
        if sample is None:
            print("No more frames or sink unavailable.")
            break  
        frames.append(sample)
    return frames

def process_frames_and_append(frames_queue, frames, width, height, sink_name):
    with ThreadPoolExecutor() as executor:
        future_to_frame = {executor.submit(process_frame, sample, i, width, height, sink_name): i for i, sample in enumerate(frames)}
        results_in_order = sorted([future.result() for future in future_to_frame], key=lambda x: x[0])
        for _, processed_frame in results_in_order:
            frames_queue.append(processed_frame)
        return frames_queue
    
            
