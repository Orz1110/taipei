import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import imdb
(x_train,y_train),(x_test,y_test) = imdb.load_data(num_words=10000)
from tensorflow.keras.preprocessing import sequence
# 整理sequence長度
x_train = sequence.pad_sequences(x_train, maxlen=100)
# 看前100個字就好(怕太長)
x_test = sequence.pad_sequences(x_test, maxlen=100)
# x_train.shape
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Embedding
from tensorflow.keras.layers import LSTM
model = Sequential()
model.add(Embedding(10000,128))
# Embedding層把離散或整數的資料變得連續
model.add(LSTM(150))
model.add(Dense(1,activation="sigmoid"))
model.summary()
# 167400 = 3*(128+150+1)*150+(128+150+1)*150
model.compile(loss="binary_crossentropy",optimizer="adam",metrics=["accuracy"])
model.fit(x_train,y_train,batch_size=32,epochs=5)
score = model.evaluate(x_test, y_test)
print(score[0],score[1])

