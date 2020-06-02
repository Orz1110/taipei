import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, CuDNNLSTM, Dropout, TimeDistributed
import warnings
from sklearn.metrics import mean_squared_error
import os
import time
tStart = time.time()#計時開始
print(tStart)

warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# np.set_printoptions(threshold=np.inf)

def normalize(df):
    norm = df.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    max_x = df.apply(lambda x: max(x))
    min_x = df.apply(lambda x: min(x))
    return norm, max_x, min_x

def train_windows(df, ref_day, predict_day):
    X_train, Y_train = [], []
    for i in range(df.shape[0]-predict_day-ref_day+1):
        X_train.append(np.array(df.iloc[i:i+ref_day, :1]))
        Y_train.append(np.array(df.iloc[i+ref_day:i+ref_day+predict_day]["y"]))
    return np.array(X_train), np.array(Y_train)
#
def lstm_model(shape):
    model = Sequential()
    model.add(CuDNNLSTM(256, input_shape=(shape[1], shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(CuDNNLSTM(256, return_sequences=True))
    model.add(Dropout(0.2))
    # model.add(CuDNNLSTM(32, return_sequences=True))
    # model.add(Dropout(0.2))
    # model.add(TimeDistributed(Dense(1, activation='linear')))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    # model.add(Dense(32, activation='linear'))
    # model.add(Dropout(0.2))
    model.add(Dense(30, activation='relu'))
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=['mean_absolute_error'])
    model.summary()
    return model

# VD資料集

filepath = "D:/耿嘉/VD/"
filename = os.listdir(filepath)
# print(filename)
# pd.set_option('display.max_columns', None)
data_VD_all = pd.DataFrame([])

for i in range(len(filename)):
    data = pd.read_csv(filepath+filename[0])
    try:

        print(filename[i])
        data_VD = pd.read_csv(filepath + filename[i])
        data_VD = data_VD[data_VD["DEVICEID"] == "V4010A0"]
        # print(data_VD)
        data_VD_all = pd.concat([data_VD, data_VD_all])
        print(data_VD_all)

    except:
        pass
data_VD = data_VD_all
data = data_VD_all[['BIGVOLUME', 'CARVOLUME', 'MOTORVOLUME']]
# data_VD = pd.read_csv("D:/耿嘉/20190101000000_20190102000000.csv")

# point = "V6121A0"
point = "V4010A0"

# # data_VD = data_VD[data_VD["DEVICEID"] == point]
# data_VD = data_VD[data_VD["DEVICEID"] == point]
# print(data_VD)

#  不同車道加總
data_VD = data_VD.groupby("DATETIME2").sum()
print(data_VD)
# 資料異常處理(還沒做)
data_t = data_VD[["BIGVOLUME", "CARVOLUME", "MOTORVOLUME"]]
data_t["sum"] = data_t.sum(axis=1)
data_t['y'] = data_t['sum']
data_t = data_t[["sum", "y"]]
# plt.plot(data_t["sum"].values)
# plt.ylabel("volumns")
# plt.xlabel("min")
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.show()
print(data_t)



# 資料正規化
# print(data_t)
data_tt, max_norm_data, min_norm_data = normalize(data_t)
# print(max_norm_data)
# print(min_norm_data)
# print(data_tt)

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data_t = scaler.fit_transform(data_t)
# print(data_t)
data_t = pd.DataFrame(data_t, columns=["sum", "y"])
# data_t = scaler.inverse_transform(pd.DataFrame(data_t))
# print(data_t)

# train_test_split

from sklearn.model_selection import train_test_split
train, test = train_test_split(data_t, test_size=0.1, shuffle=False)
# # print(train)

# 資料整理

X_train, Y_train = train_windows(train, 120, 30)
X_test, Y_test = train_windows(test, 120, 30)
# Y_train = pd.DataFrame(Y_train, columns=["real"])
print(X_test)
print(Y_test)

def inverse_normalize(inv_data):
    inverse_norm_data = []
    for i in range(len(inv_data)):
        inverse_norm_data.append(np.array((max_norm_data[0] - min_norm_data[0]) * inv_data[i] + min_norm_data[0]))
    # inverse_norm_2 = inv_data.apply(lambda x: (max_norm_data[1] - min_norm_data[1]) * x + min_norm_data[1])
    return np.array(inverse_norm_data)

def draw(title,x_label,y_label,lable):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(lable)
    # plt.show()

inverse_norm_train = inverse_normalize(Y_train)

inverse_norm_test = inverse_normalize(Y_test)
# print(inverse_norm_train)
# plt.plot(inverse_norm_1)
# plt.show()


# ---- model TRAIN----

model = lstm_model(X_train.shape)
history = model.fit(X_train, Y_train, epochs=20, batch_size=1000, validation_split=0.1)

plt.figure(1)
plt.subplot(221)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
lable = ['loss', 'val_loss']
draw(point+"_train", "epoch", "mse", lable)
plt.legend(lable)

# ---- model TEST----

# history_test = model.fit(X_test, Y_test, epochs=100, batch_size=50, validation_split=0.1, shuffle=True)
# plt.plot(history_test.history['loss'])
# plt.plot(history_test.history['val_loss'])
# lable = ['loss', 'val_loss']
# draw("test", "epoch", "mse", lable)
# plt.legend(lable)

# predict = model.predict(X_train)
# inverse_norm_train_predict = inverse_normalize(predict)
# print(np.around(inverse_norm_train_predict))
# mse_train = np.sum((np.around(inverse_norm_train_predict) - inverse_norm_train)**2, axis=1)/len(inverse_norm_train)
# print(mse_train)
#
# lable = ["time"]
# plt.plot(mse_test)
# draw("V0111C0_train_mse", lable[0], "mse", lable)

predict_tr = model.predict(X_train)
predict_tr = inverse_normalize(predict_tr).T
real_tr = inverse_norm_train.T

predict = model.predict(X_test)
predict = inverse_normalize(predict).T
real = inverse_norm_test.T
tEnd = time.time()#計時結束
#列印結果
print("It cost %f sec" % (tEnd - tStart))#會自動做近位
print("預測-------\n", predict)
# print("預測-------\n", predict.T)
print("答案---------\n", real)
rmse_test = np.sqrt(np.sum((predict - real)**2, axis=1)/len(real))
print("誤差------\n\n", rmse_test)



mse_test = np.sum((predict - real)**2, axis=1)/len(real)
print("誤差------\n\n", mse_test)
# rmse = mean_squared_error(inverse_norm_test, np.around(inverse_norm_train_predict), squared=False)
# print("誤差------\n", rmse)
# mse = mean_squared_error(inverse_norm_test, np.around(inverse_norm_train_predict))
# print("誤差------\n", mse)


lable = ["time"]
plt.subplot(222)
plt.plot(rmse_test)
draw(point+"_test_rmse", lable[0], "rmse", lable)

plt.subplot(223)
lable = ["predict", "real"]
print(predict_tr[0])
print(real_tr[0])
plt.plot(predict_tr[0])
plt.plot(real_tr[0])
draw("train_predict&real", "min", "volumns", lable)


plt.subplot(224)
lable = ["predict", "real"]
print(predict[0])
print(real[0])
plt.plot(predict[0])
plt.plot(real[0])
draw("test_predict&real", "min", "volumns", lable)

plt.show()






'''

# 反正規化-train
final_train = pd.DataFrame([])
Y_train = pd.DataFrame(Y_train, columns=["real"])
final_train["real"] = Y_train["real"]
predict = pd.DataFrame(predict, columns=["predict"])
final_train["predict"] = predict["predict"]
final_train = scaler.inverse_transform(final_train)
# print(final_train)
#
# lable_1 = ["real", "predict"]
# plt.plot(final_train[:, 0])
# plt.plot(final_train[:, 1])
# plt.legend(lable_1)
# plt.title("train")
# plt.xlabel("time")
# plt.ylabel("volumn")
# plt.show()

# 反正規化-test

predict = model.predict(X_test)
final_test = pd.DataFrame([])
Y_test = pd.DataFrame(Y_test, columns=["real"])
final_test["real"] = Y_test["real"]
predict = pd.DataFrame(predict, columns=["predict"])
final_test["predict"] = predict["predict"]
final_test = scaler.inverse_transform(final_test)
print(final_test)


# 畫圖

plt.figure(1)
plt.subplot(211)
lable_1 = ["real", "predict"]
plt.plot(final_train[:, 0])
plt.plot(final_train[:, 1])
plt.legend(lable_1)
plt.title("train")
plt.xlabel("time")
plt.ylabel("volumn")

plt.subplot(212)
lable_1 = ["real", "predict"]
plt.plot(final_test[:, 0])
plt.plot(final_test[:, 1])
plt.legend(lable_1)
plt.title("test")
plt.xlabel("time")
plt.ylabel("volumn")

plt.show()
'''