import matplotlib.pyplot as plt
import tensorflow as tf
from keras import Model
import seaborn as sns
import numpy as np

def plot_history(history,model_name, folder_path):

  fig, (ax1, ax2) = plt.subplots(2)

  fig.set_size_inches(18.5, 10.5)

  ax1.set_title('Loss')
  ax1.plot(history.history['loss'], label = 'train')
  ax1.plot(history.history['val_loss'], label = 'test')
  ax1.set_ylabel('Loss')

  max_loss = max(history.history['loss'] + history.history['val_loss'])

  ax1.set_ylim([0, np.ceil(max_loss)])
  ax1.set_xlabel('Epoch')
  ax1.legend(['Train', 'Validation'])

  ax2.set_title('Accuracy')
  ax2.plot(history.history['accuracy'],  label = 'train')
  ax2.plot(history.history['val_accuracy'], label = 'test')
  ax2.set_ylabel('Accuracy')
  ax2.set_ylim([0, 1])
  ax2.set_xlabel('Epoch')
  ax2.legend(['Train', 'Validation'])
  plt.savefig(f"{folder_path}/{model_name}_history.png")
  plt.close(fig)


def get_actual_predicted_labels(model, dataset): 
  actual = [labels for _, labels in dataset.unbatch()]
  predicted = model.predict(dataset)

  actual = tf.stack(actual, axis=0)
  predicted = tf.concat(predicted, axis=0)
  predicted = tf.argmax(predicted, axis=1)

  return actual, predicted

def plot_confusion_matrix(actual, predicted, labels, ds_type, model_name, folder_path):
    # Set the size and font scale for the plots
    sns.set(rc={'figure.figsize':(len(labels)*5, len(labels)*5)})
    sns.set(font_scale=1.8)
    
    # Create the confusion matrix
    cm = tf.math.confusion_matrix(actual, predicted)
    
    # Create the plot
    figure_confusion, ax = plt.subplots()
    ax = sns.heatmap(cm, annot=True, fmt='g')
    
    # Set titles and labels
    ax.set_title('Confusion matrix of action recognition for ' + ds_type)
    ax.set_xlabel('Predicted Action')
    ax.set_ylabel('Actual Action')
    
    # Set the tick labels
    ax.set_xticklabels(labels, rotation=90)
    ax.set_yticklabels(labels, rotation=0)
    
    # Save the plot
    plt.savefig(f"{folder_path}/{model_name}_{ds_type}_confusion.png")
    
    # Close the plot to avoid displaying it in a Jupyter notebook or similar environment
    plt.close(figure_confusion)
