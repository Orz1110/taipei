import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, CuDNNLSTM, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
from keras.utils import to_categorical
def normalize(df):
   norm = df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
   return norm
def train_windows(df, ref_day, predict_day):
   X_train, Y_train = [], []
   for i in range(df.shape[0]-predict_day-ref_day):
       X_train.append(np.array(df.iloc[i:i+ref_day, :-1]))
       Y_train.append(np.array(df.iloc[i+ref_day:i+ref_day+predict_day]["y"]))
   return np.array(X_train), np.array(Y_train)
def lstm_stock_model(shape):
   model = Sequential()
   model.add(CuDNNLSTM(256, input_shape=(shape[1], shape[2]), return_sequences=True))
   model.add(Dropout(0.2))
   model.add(CuDNNLSTM(256, return_sequences=True))
   model.add(Flatten())
   model.add(Dense(5, activation='tanh'))
   model.add(Dropout(0.2))
   model.add(Dense(5, activation='tanh'))
   model.add(Dropout(0.2))
   model.add(Dense(1, activation='tanh'))
   model.compile(loss="mean_absolute_error", optimizer="adam", metrics=['mean_absolute_error'])
   model.summary()
   return model
data_VD = pd.read_csv("D:/耿嘉/20190101000000_20190102000000.csv")

data_VD = data_VD[data_VD["DEVICEID"]=="V0111C0"]
print(len(data_VD))
data_t = data_VD[["BIGVOLUME", "CARVOLUME", "MOTORVOLUME"]]
data_t["sum"] = data_t.sum(axis=1)
data_t['y'] = data_t['sum'].shift(-60)
# 正規化
data_t.iloc[:, 3:5] = normalize(data_t.iloc[:, 3:5])
train = data_t
test = train[-1000:]
train = train.reset_index()
test = test.reset_index()
train = train[['sum', "y"]]
test = test[['sum', "y"]]

train = train.dropna()

X_train, Y_train = train_windows(train, 100, 1)
X_test, Y_test = train_windows(test, 100, 1)
print(X_train.shape)

model = lstm_stock_model(X_train.shape)
callback = EarlyStopping(monitor="mean_absolute_error", patience=10, verbose=1, mode="auto")
# history = model.fit(X_train,Y_train,batch_size=20,epochs=12)
history = model.fit(X_train, Y_train, epochs=500, batch_size=10, validation_split=0.1, callbacks=[callback], shuffle=True)
# history_test = model.fit(X_test, Y_test, epochs=500, batch_size=50, validation_split=0.1, callbacks=[callback], shuffle=True)
# predict = model.predict(X_test)
# plt.plot(predict)
# plt.plot(Y_test)
# epochs=range(500)
# train_loss = history.history['loss']
# test_loss = history_test.history['loss']
# plt.plot(train_loss)
# plt.plot(test_loss)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
lable = ['loss', 'val_loss']
plt.legend(lable)
plt.show()

