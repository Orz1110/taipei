import pandas as pd
data_check = pd.read_csv("C:/Users/Orz/Desktop/中研院/check - 複製.csv")
# print(data_check)
data_final = pd.read_csv("C:/Users/Orz/Desktop/中研院/final手動尋找 - 複製.csv")
for i in data_check["Serial"]:
    # print(data_final[data_final["Serial"] == i].Time)
    # data_final[data_final["Serial"] == i]["Time"] = data_check[data_check["Serial"] == i]["Time"]
    # print(data_final[data_final["Serial"] == i]["Time"])
    # print(data_check[data_check["Serial"] == i].Time.tolist()[0])
    time = str(data_check[data_check["Serial"] == i].Time.tolist()[0])
    time = time.split(".")[0]
    data_final["Time"][data_final["Serial"] == i] = time

    Distance = str(data_check[data_check["Serial"] == i].Distance.tolist()[0])
    Distance = Distance.split(".")[0]
    data_final["Distance"][data_final["Serial"] == i] = Distance

    data_final["lon"][data_final["Serial"] == i] = data_check[data_check["Serial"] == i].lon.tolist()[0]
    data_final["lat"][data_final["Serial"] == i] = data_check[data_check["Serial"] == i].lat.tolist()[0]

    print(data_final[["lon","lat"]][data_final["Serial"] == i])
data_final.to_csv("C:/Users/Orz/Desktop/中研院/checkOutput.csv",index=False)