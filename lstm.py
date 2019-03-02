import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

import pandas as pd

# Data loading
data1 = pd.read_csv('training_data/0.csv')
data2 = pd.read_csv('training_data/1.csv')
data = data1.append(data2)
data = np.array(data, dtype=float)

target1 = pd.read_csv('labels/0.csv')
target2 = pd.read_csv('labels/1.csv')
target = target1.append(target2, sort=False)
pd.DataFrame(target)
target = np.array(target.columns.values)

# data = data.reshape(1, 1, 100)
# target = target.reshape((1, 1, 100))
# x_test=[i for i in range(100,200)]
# x_test=np.array(x_test).reshape((1,1,100));
# y_test=[i for i in range(101,201)]
# y_test=np.array(y_test).reshape(1,1,100)
#
#
# model = Sequential()
# model.add(LSTM(100, input_shape=(1, 100),return_sequences=True))
# model.add(Dense(100))
# model.compile(loss='mean_absolute_error', optimizer='adam',metrics=['accuracy'])
# model.fit(data, target, nb_epoch=10000, batch_size=1, verbose=2,validation_data=(x_test, y_test))
#
#
#
# predict = model.predict(data)
