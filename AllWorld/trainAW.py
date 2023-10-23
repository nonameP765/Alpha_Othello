import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.models import load_model

import os
import json


np.random.seed(3)

with open('./gameData_x.json') as fopen:
    fx = json.load(fopen)
print("x input load success")
with open('./gameData_y.json') as fopen:
    fy = json.load(fopen)
print("y input load success")

trainRate: int = 8

x_train = np.array(fx)
y_train = np.array(fy)
x_val = x_train[:500]
y_val = y_train[:500]

model = Sequential()

model.add(Conv2D(48, padding='same', input_shape=(2, 8, 8), kernel_size=(5, 5), activation='relu',
                 data_format='channels_first'))

for i in range(trainRate):
    model.add(Conv2D(96, padding='same', kernel_size=(3, 3), activation='relu', data_format='channels_first'))

model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8 * 8, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])

if os.path.isfile('./savingModel.h5'):
    model = load_model('./savingModel.h5')

while True:
    hist = model.fit(x_train, y_train, epochs=200, batch_size=128, validation_data=(x_val, y_val))

    weight_file = './weights.hd5'
    model.save_weights(weight_file, overwrite=True)

    model_file = './model.yml'
    with open(model_file, 'w') as yml:
        model_yaml = model.to_yaml()
        yml.write(model_yaml)

    model.save('./savingModel.h5')