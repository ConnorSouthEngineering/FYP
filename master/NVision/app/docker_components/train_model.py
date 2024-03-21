import tensorflow as tf
from keras import layers, utils, losses, optimizers, Sequential

import pathlib
import argparse
import os

from load_data import FrameGenerator
from visualise_results import plot_history, get_actual_predicted_labels, plot_confusion_matrix
from triton_packaging import create_triton_package

def extract_data(folder_path, num_frames):
        
    output_signature = (tf.TensorSpec(shape = (None, None, None, 3), dtype = tf.float32),
                        tf.TensorSpec(shape = (), dtype = tf.int16))
    
    train_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/train"), num_frames, training=True),
                                                output_signature = output_signature)                                       
    val_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/validation"), num_frames),
                                                output_signature = output_signature)
    test_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/test"), num_frames),
                                                output_signature = output_signature)
    
    return train_ds, val_ds, test_ds

def initialise_cache(train_ds, val_ds, test_ds):
    train_ds = train_ds.cache(filename="./cache/train_cache")
    val_ds = val_ds.cache(filename="./cache/val_cache")
    test_ds = test_ds.cache(filename="./cache/test_cache")
    
    return train_ds, val_ds, test_ds

def prefetch_data(train_ds, val_ds, test_ds, AUTOTUNE, shuffle_size=100):
    train_ds = train_ds.shuffle(shuffle_size).prefetch(buffer_size = AUTOTUNE)
    val_ds = val_ds.shuffle(shuffle_size).prefetch(buffer_size = AUTOTUNE)
    test_ds = test_ds.shuffle(shuffle_size).prefetch(buffer_size = AUTOTUNE)

    return train_ds, val_ds, test_ds

def initialise_batch(train_ds, val_ds, test_ds, batch_size):
    train_ds = train_ds.batch(batch_size)
    val_ds = val_ds.batch(batch_size)
    test_ds = test_ds.batch(batch_size)

    return train_ds, val_ds, test_ds

def create_model(num_frames, height, width, folder_path):
    input_shape = (num_frames, height, width, 3)

    model = Sequential()

    model.add(layers.ConvLSTM2D(filters = 4, kernel_size = (3, 3), activation = 'tanh',data_format = "channels_last",
                            recurrent_dropout=0.2, return_sequences=True, input_shape = input_shape))
        
    model.add(layers.MaxPooling3D(pool_size=(1, 2, 2), padding='same', data_format='channels_last'))
    model.add(layers.TimeDistributed(layers.Dropout(0.2)))
    
    model.add(layers.ConvLSTM2D(filters = 8, kernel_size = (3, 3), activation = 'tanh', data_format = "channels_last",
                            recurrent_dropout=0.2, return_sequences=True))
        
    model.add(layers.MaxPooling3D(pool_size=(1, 2, 2), padding='same', data_format='channels_last'))
    model.add(layers.TimeDistributed(layers.Dropout(0.2)))
        
    model.add(layers.ConvLSTM2D(filters = 14, kernel_size = (3, 3), activation = 'tanh', data_format = "channels_last",
                            recurrent_dropout=0.2, return_sequences=True))
        
    model.add(layers.MaxPooling3D(pool_size=(1, 2, 2), padding='same', data_format='channels_last'))
    model.add(layers.TimeDistributed(layers.Dropout(0.2)))
        
    model.add(layers.ConvLSTM2D(filters = 16, kernel_size = (3, 3), activation = 'tanh', data_format = "channels_last",
                            recurrent_dropout=0.2, return_sequences=True))
        
    model.add(layers.MaxPooling3D(pool_size=(1, 2, 2), padding='same', data_format='channels_last'))
        
    model.add(layers.Flatten()) 
    num_classes = sum(1 for _ in pathlib.Path(folder_path+"/train").iterdir() if _.is_dir())
    model.add(layers.Dense(num_classes, activation = "softmax"))
    #model.summary()
    return model

def get_class_maps(folder_path, num_frames):
    fg = FrameGenerator(pathlib.Path(folder_path+"/train"), num_frames, training=True)
    classes= fg.class_ids_for_name
    labels = list(classes.keys())
    return labels

def main():
    with tf.device('/GPU:0'):
        parser = argparse.ArgumentParser()
        parser.add_argument('--model_name', type=str, default="test1")
        parser.add_argument('--epochs', type=int, default=15)
        parser.add_argument('--num_frames', type=int, default=10)
        parser.add_argument('--shuffle_size', type=int, default=200)
        parser.add_argument('--batch_size', type=int, default=3)
        args = parser.parse_args()
        model_name = args.model_name
        epochs = args.epochs
        num_frames = args.num_frames
        shuffle_size = args.shuffle_size
        batch_size = args.batch_size 

        height = 224
        width = 224
        
        #folder_path = "/home/connor/Desktop/FYP/master/NVision/model_tasks/Test_2024-03-21-16-52"
        folder_path = "/mnt"
        repo_path = "/model_repo"

        train_ds, val_ds, test_ds = extract_data(folder_path, num_frames)

        AUTOTUNE = tf.data.AUTOTUNE

        train_ds, val_ds, test_ds = initialise_cache(train_ds, val_ds, test_ds)

        train_ds, val_ds, test_ds = prefetch_data(train_ds, val_ds, test_ds, AUTOTUNE, shuffle_size)

        train_ds, val_ds, test_ds = initialise_batch(train_ds, val_ds, test_ds, batch_size)

        model = create_model(num_frames, height, width, folder_path)
        
        callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)

        model.compile(loss = losses.SparseCategoricalCrossentropy(from_logits=False), 
                    optimizer = optimizers.Adam(learning_rate = 0.0001), 
                    metrics = ['accuracy'])

        history = model.fit(x = train_ds,
                            epochs = epochs, 
                            validation_data = val_ds,
                            batch_size=32,
                            callbacks=[callback])
        plot_history(history, model_name, folder_path)
            
        model.evaluate(test_ds, return_dict=True)
            
        labels = get_class_maps(folder_path, num_frames)

        actual, predicted = get_actual_predicted_labels(model, train_ds)
        plot_confusion_matrix(actual, predicted, labels, 'training', model_name, folder_path)

        actual, predicted = get_actual_predicted_labels(model, test_ds)
        plot_confusion_matrix(actual, predicted, labels, 'test', model_name, folder_path)

        model.save(os.path.join(folder_path, model_name), save_format='tf')
        
        create_triton_package(labels, model_name, folder_path, repo_path, epochs, num_frames, shuffle_size, batch_size, height, width)
        input()

if __name__ == "__main__":
    main()