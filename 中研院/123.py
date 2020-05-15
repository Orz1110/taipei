import pandas as pd
data = pd.read_csv("C:/Users/Orz/Desktop/RTI_Location - 複製.csv")
# print(data["事故地址"])
address = data["事故地址"].astype("str")
print(address)
print(type(address[0]))
# print(address[0][:-1])
# print(address[0][-1:])

# 1.分割括號 2.刪除位置最後一字:口 3.檢查

for i in range(len(address)):
    address[i] = address[i].split('(', 1)[0]
    # print(address[i])
    if address[i][-1:] == "口":
        # print(address[i])
        address[i] = address[i][:-1]
        # print(address[i])
for i in range(len(address)):
    if address[i][-1:] == "口":
        # print(address[i])
        address[i] = address[i][:-1]
        print(address[i])
print(address)
address.to_csv("C:/Users/Orz/Desktop/事故清洗後.csv", index=False)