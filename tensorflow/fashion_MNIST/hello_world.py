# TensorFlow and tf.keras
import os

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

(train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

class_chinese_names = ['T恤/上衣', '裤子', '套头衫', '连衣裙', '外套', '凉鞋', '衬衫', '运动鞋', '包', '短靴']

print(train_images.shape)  # (60000, 28, 28)  60,000 个图像，每个图像由 28 x 28 的像素

train_images = train_images / 255.0  # 归一化,像素是1-255,除以255得到0-1之前的值
test_images = test_images / 255.0

model_file = 'hello_model'
checkpoint_path = "training_1/cp.ckpt"
batch_size = 32
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1,
                                                 save_freq=5 * batch_size)


def get_model():
    if os.path.exists(model_file):
        model = tf.keras.models.load_model(model_file)
    else:
        model = keras.Sequential()
        model.add(keras.layers.Flatten(input_shape=(28, 28)))
        model.add(keras.layers.Dense(128, activation='relu'))
        model.add(keras.layers.Dense(256, activation='relu'))
        model.add(keras.layers.Dense(10, activation='softmax'))

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
    model.summary()
    return model


def fit(model):
    if os.path.exists(checkpoint_path):
        model.load_weights(checkpoint_path)
    model.fit(train_images, train_labels, epochs=10, batch_size=batch_size,
              validation_data=(test_images, test_labels),
              callbacks=[cp_callback])
    model.save(model_file)
    return model


if __name__ == '__main__':
    model = get_model()
    # test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    # print('\nTest accuracy:', test_acc)
    # 附加一个 softmax 层，将 logits 转换成更容易理解的概率。 实际是网络结构的一部分,这行相当于模型上再加层
    # probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(test_images)
    # print(class_chinese_names[np.argmax(predictions[0])])

    timage = cv2.imread('t2.jpeg', 0)
    timage = cv2.resize(timage, dsize=(28, 28)) / 256
    cv2.imshow('image', timage)
    cv2.waitKey(5000)
    img = (np.expand_dims(timage, 0))
    predictions = model.predict(img)
    print(predictions)
    print(class_chinese_names[np.argmax(predictions[0])])
