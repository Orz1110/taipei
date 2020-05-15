import geocoder
import pandas as pd
import requests
g = geocoder.google('Mountain View, CA')
# g.latlng
data = pd.read_csv("C:/Users/Orz/Desktop/all - 複製.csv")
con = data["事故位置GPS_X"].isna()
# print(con)
for i in range(len(data)):
    if con[i] == True:
        # print(data["location"][i])
        data["location"][i] = data["location"][i].split("往")[0]
        # print(data["location"][i])
address = data

for i in range(len(address)):
    if address["location"][i][-1:] == "口":
        # print(address[i])
        address["location"][i] = address["location"][i][:-1]

for i in range(len(address)):
    if address["location"][i][-1:] == "之":
        # print(address[i])
        address["location"][i] = address["location"][i][:-1]
        # print(address["location"][i])

for i in range(len(address)):
    if con[i] == True:
        try:
            print(address[i])
            url = "http://geocoding.geohealth.tw/position.php?addr=" + address['location'][i]
            api = requests.get(url).json()
            print(api)
            # data["事故位置GPS_X"].loc[i] = api["lat"]
            # data["事故位置GPS_Y"].loc[i] = api["lng"]
            # data["acc"].loc[i] = api["accuracy"]
            # print(data[i])
        except:
            print("Q")
# print(data)
# url = "http://geocoding.geohealth.tw/position.php?addr=" + address['location'][0]
# api = requests.get(url).json()
# print(api)