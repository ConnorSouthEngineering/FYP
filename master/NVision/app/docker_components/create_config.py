import tensorflow as tf
import os 
import configparser

def compile_number(current_number):
    number = ""
    for char in current_number:
        number += char
    return number

def get_dimensions(shape):
    dimensions = []
    current_number = []
    i = 0
    while i  < len(shape):
        char = shape[i]
        try:
            next_char = shape[i+1]
        except:
            return dimensions
        match char:
            case '(':
                pass
            case ')':
                pass
            case ',':
                pass
            case char if char.isdigit() and next_char.isdigit():
                current_number.append(char)
            case char if char.isdigit() and next_char == ',':
                current_number.append(char)
                full_number = compile_number(current_number)
                dimensions.append(int(full_number))
                current_number = []
            case char if char.isdigit() and next_char == ')':
                current_number.append(char)
                full_number = compile_number(current_number)
                dimensions.append(int(full_number))
                current_number = []
            case _:
                pass
        i += 1

def collect_model_configuration(model_path):
    loaded_model = tf.saved_model.load(model_path)
    serving_default = loaded_model.signatures['serving_default']

    for input_name, input_tensor in loaded_model.structured_input_signature[1].items():
        model_input_name = input_name
        model_input_shape = input_tensor.shape
        model_input_dtype = input_tensor.dtype

    for output_name, output_tensor in serving_default.structured_outputs.items():
        model_output_name = output_name
        model_output_shape = output_tensor.shape
        model_output_dtype = output_tensor.dtype
    return model_input_name, model_input_dtype, model_input_shape, model_output_name, model_output_dtype, model_output_shape

def write_config(config_lines, model_name, folder_path):
    with open(f"{folder_path}/{model_name}.pbtxt", "w") as file:
        for line in config_lines:
            file.write(line + "\n")
    print("Config file created")
    return

def create_triton_config(model_name, folder_path):
    model_path = os.path.join(folder_path,model_name)
    input_name,input_dtype,input_shape,output_name,output_dtype,output_shape = collect_model_configuration(model_path)

    type_mapping = {
        tf.bool: "TYPE_BOOL",
        tf.uint8: "TYPE_UINT8",
        tf.uint16: "TYPE_UINT16",
        tf.uint32: "TYPE_UINT32",
        tf.uint64: "TYPE_UINT64",
        tf.int8: "TYPE_INT8",
        tf.int16: "TYPE_INT16",
        tf.int32: "TYPE_INT32",
        tf.int64: "TYPE_INT64",
        tf.half: "TYPE_FP16",
        tf.float32: "TYPE_FP32",
        tf.float64: "TYPE_FP64",
        tf.string: "TYPE_STRING"
    }

    config_lines = [
        f"name: \"{model_name}\"",
        f"dynamic_batching {{ }}",
        "platform: \"tensorflow_savedmodel\"",
        "max_batch_size: 8",  
        "input [",
        f"  {{",
        f"    name: \"{input_name}\"",
        f"    data_type: {type_mapping[input_dtype]}",
        f"    dims: {get_dimensions(str(input_shape))}",
        f"  }}",
        "]",
        "output [",
        f"  {{",
        f"    name: \"{output_name}\"",
        f"    data_type: {type_mapping[output_dtype]}",
        f"    dims: {get_dimensions(str(output_shape))}",
        f"  }}",
        "]",
    ]
    write_config(config_lines, model_name, folder_path)
    return

def generate_training_config(labels, model_name, folder_path, epochs, num_frames, shuffle_size, batch_size, height, width):
    config = configparser.ConfigParser()
    config['PREDICTION'] = {
        'num_frames': num_frames,
        'class_list': labels,
        'height': height,
        'width': width
    }
    config['TRAINING'] = {
        'epochs': epochs,
        'shuffle_size': shuffle_size,
        'batch_size': batch_size
    }
    with open(f'{folder_path}/{model_name}.conf', 'w') as configfile:
        config.write(configfile)
    return