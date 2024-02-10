import numpy as np
from keras.preprocessing import image
import tensorflow as tf
from keras_cv.models import ImageClassifier  # Verify the correct import path
from keras_cv.models import EfficientNetV2Backbone  # Adjust based on actual location

custom_objects = {
    'ImageClassifier': ImageClassifier,
    'EfficientNetV2Backbone': EfficientNetV2Backbone
}

with tf.keras.utils.custom_object_scope(custom_objects):
    loaded_model = tf.keras.models.load_model('./test.h5')
    print("model loaded")
    # Example for loading and preprocessing an image
    img_path = './rock.jpg'
    print("image defined")
    img = image.load_img(img_path, target_size=(224, 224))  # Adjust target_size to your model's expected input shape
    print("image loaded")
    img_array = image.img_to_array(img)
    print("image converted")
    img_array = np.expand_dims(img_array, axis=0)  # Model expects a batch of images, so create a batch of one
    print("image expaned")

    img_array /= 255.0

    predictions = loaded_model.predict(img_array)
    print("predictions loaded")
    predicted_class = np.argmax(predictions, axis=1)
    print("predictions formatted")
    print(predicted_class)
