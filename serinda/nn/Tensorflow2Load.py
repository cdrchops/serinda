import os

import tensorflow as tf
from tensorflow import keras

print(tf.version.VERSION)

class Tensorflow2Load:
    # Define a simple sequential model
    def create_model(self):
        model = tf.keras.models.Sequential([
            keras.layers.Dense(512, activation='relu', input_shape=(784,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(10)
        ])

        model.compile(optimizer='adam',
                      loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=[tf.metrics.SparseCategoricalAccuracy()])

        return model

    # https://github.com/tensorflow/docs/blob/master/site/en/tutorials/keras/save_and_load.ipynb
    def loadMNIST(self):
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()

        train_labels = train_labels[:1000]
        test_labels = test_labels[:1000]

        train_images = train_images[:1000].reshape(-1, 28 * 28) / 255.0
        test_images = test_images[:1000].reshape(-1, 28 * 28) / 255.0

        # Create a basic model instance
        model = self.create_model()

        # Display the model's architecture
        model.summary()