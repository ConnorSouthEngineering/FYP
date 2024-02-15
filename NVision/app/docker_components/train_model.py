import tensorflow as tf
import pathlib
from keras import layers, utils, losses, optimizers, Model
from load_data import FrameGenerator
from model_creation import Conv2Plus1D, add_residual_block, ResizeVideo
from visualise_results import plot_history, get_actual_predicted_labels, plot_confusion_matrix
# Define the dimensions of one frame in the set of frames created
HEIGHT = 224
WIDTH = 224


folder_path = "./processing-2024-02-15-23-22-14"

output_signature = (tf.TensorSpec(shape = (None, None, None, 3), dtype = tf.float32),
                    tf.TensorSpec(shape = (), dtype = tf.int16))
train_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/train"), 30, training=True),
                                          output_signature = output_signature)
                                          
# Create the validation set
val_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/validation"), 10),
                                        output_signature = output_signature)

test_ds = tf.data.Dataset.from_generator(FrameGenerator(pathlib.Path(folder_path+"/test"), 10),
                                        output_signature = output_signature)

# Print the shapes of the data
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)
val_ds = val_ds.cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)
test_ds = test_ds.cache().shuffle(1000).prefetch(buffer_size = AUTOTUNE)

train_ds = train_ds.batch(2)
val_ds = val_ds.batch(2)
test_ds = test_ds.batch(2)

input_shape = (None, 10, HEIGHT, WIDTH, 3)
input = layers.Input(shape=(input_shape[1:]))
x = input

x = Conv2Plus1D(filters=16, kernel_size=(3, 7, 7), padding='same')(x)
x = layers.BatchNormalization()(x)
x = layers.ReLU()(x)
x = ResizeVideo(HEIGHT // 2, WIDTH // 2)(x)

# Block 1
x = add_residual_block(x, 16, (3, 3, 3))
x = ResizeVideo(HEIGHT // 4, WIDTH // 4)(x)

# Block 2
x = add_residual_block(x, 32, (3, 3, 3))
x = ResizeVideo(HEIGHT // 8, WIDTH // 8)(x)

# Block 3
x = add_residual_block(x, 64, (3, 3, 3))
x = ResizeVideo(HEIGHT // 16, WIDTH // 16)(x)

# Block 4
x = add_residual_block(x, 128, (3, 3, 3))

x = layers.GlobalAveragePooling3D()(x)
x = layers.Flatten()(x)
x = layers.Dense(10)(x)

model = Model(input, x)

utils.plot_model(model, expand_nested=True, dpi=60, show_shapes=True, to_file='model.png')

model.compile(loss = losses.SparseCategoricalCrossentropy(from_logits=True), 
              optimizer = optimizers.Adam(learning_rate = 0.0001), 
              metrics = ['accuracy'])

history = model.fit(x = train_ds,
                    epochs = 50, 
                    validation_data = val_ds)

plot_history(history)
model.evaluate(test_ds, return_dict=True)

fg = FrameGenerator(pathlib.Path(folder_path+"/train"), 10, training=True)
labels = list(fg.class_ids_for_name.keys())

actual, predicted = get_actual_predicted_labels(model, train_ds)
plot_confusion_matrix(actual, predicted, labels, 'training')

actual, predicted = get_actual_predicted_labels(model, test_ds)
plot_confusion_matrix(actual, predicted, labels, 'test')
