import pandas as pd
import requests
import time
import re
start = time.time()
# df = pd.read_csv("C:/Users/Orz/Desktop/跑正規化/0929跑正規化/711/超商資料集_狀態1.csv")
# df = df["分公司地址"]
#
# df = pd.read_excel("C:/Users/Orz/Desktop/中研院/藥局比對結果清洗前.xlsx")
# df = pd.read_csv("C:/Users/Orz/Desktop/test.csv")

# df = df["原始地址"]
# df = df["Address"]
df = pd.read_csv("C:/Users/Orz/Desktop/BGMOPEN1.csv", encoding="utf8")
df = df['營業地址']
c = ['、', '及', ';', '．', '/', '，', '‧', '；', '。', '.', '˙', '丶']
dd = ["〈", "(", "（"]
newtaipei = ["萬里區", "金山區", "板橋區", "汐止區", "深坑區", "石碇區", "瑞芳區", "平溪區", "雙溪區", "貢寮區", "新店區", "坪林區", "烏來區", "永和區", "中和區",
             "土城區", "三峽區", "樹林區", "鶯歌區", "三重區", "新莊區", "泰山區", "林口區", "蘆洲區", "五股區", "八里區", "淡水區", "三芝區", "石門區"]
a = ["縣", "市", "鄉", "鎮", "區", "里", "街", "路", "段", "村"]
num0, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10, num11, num12, num13, num14, num15 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
acc2num = 0
acc3num = 0
apinum = 0

# 規則1 同一單位多門牌
def cut_1(address):

    sentences = address
    sentences = re.split(r"[、及;．/，‧；。˙丶]", sentences)
    # print(sentences)
    str_ok = []
    for str in sentences:
        if "號" not in str and "樓" not in str and "地下室" not in str and "之" not in str:
            str = str + "號"
            # print(str)
        if "號" in str and "樓" not in str:
            if str[-1] != "號":
                str = str + "樓"
                # print(str)
        print(str)
        str_ok.append(str)
        # print("str1:", str)
    total = []
    total.append(str_ok[0])
    for i in range(1, len(str_ok)):
        sub_ok = str_ok[i]
        # print(sub_ok)
        if "號" not in str_ok[i] and "樓" in str_ok[i]:
            find_hao = str_ok[0].find("號")
            str_ok[i] = str_ok[0][0:find_hao+1] + str_ok[i]
            con = str_ok[i] in total
            # print("con", con)
            if con == True:
                str_ok[i] = str_ok[i-1][0:find_hao + 1]+sub_ok
            total.append(str_ok[i])

        elif "號" in str_ok[i] and "樓" not in str_ok[i]:
            for aa in range(len(a)):
                find_hao = str_ok[0].find("號")
                str_ok[i] = str_ok[0][0:find_hao + 1] + str_ok[i]
                # print("1:", str_ok[i])
                if str_ok[0][-1] == "號":
                    where = str_ok[0].find("號")
                    for j in range(len(a)):
                        if a[j] in str_ok[0]:
                            xx = where - str_ok[0].index(a[j])
                            if xx > 0:
                                # print("str_ok[i]",str_ok[i])
                                str_ok[i] = str_ok[0].split(a[j], 1)[0] + a[j] + sub_ok
            total.append(str_ok[i])

        elif "號" in str_ok[i] and "樓" in str_ok[i]:
            where = str_ok[0].find("號")
            for j in range(len(a)):
                if a[j] in str_ok[0]:
                    xx = where - str_ok[0].index(a[j])
                    if xx > 0:
                        # print("str_ok[i]",str_ok[i])
                        str_ok[i] = str_ok[0].split(a[j], 1)[0]+a[j]+sub_ok
            # print("2", str_ok[i])
            total.append(str_ok[i])
        else:
            continue

    return total, sentences
# ― _ ＿ － - – ╴
def check_1(address):
    # where1 = address.index("―")
    addr0 = address.split("―", 1)[0] + "-"
    addr1 = address.split("―", 1)[1]
    address = addr0 + addr1
    return address

def check_2(address):
    # where1 = address.index("_")
    addr0 = address.split("_", 1)[0] + "-"
    addr1 = address.split("_", 1)[1]
    address = addr0 + addr1
    return address

def check_3(address):
    # where1 = address.index("＿")
    addr0 = address.split("＿", 1)[0] + "-"
    addr1 = address.split("＿", 1)[1]
    address = addr0 + addr1
    return address

def check_4(address):
    # where1 = address.index("－")
    addr0 = address.split("－", 1)[0] + "-"
    addr1 = address.split("－", 1)[1]
    address = addr0 + addr1
    return address

def check_5(address):
    # where1 = address.index("-")
    addr0 = address.split("-", 1)[0] + "-"
    addr1 = address.split("-", 1)[1]
    address = addr0 + addr1
    return address

def check_6(address):
    # where1 = address.index("–")
    addr0 = address.split("–", 1)[0] + "-"
    addr1 = address.split("–", 1)[1]
    address = addr0 + addr1
    return address

def check_7(address):
    # where1 = address.index("╴")
    addr0 = address.split("╴", 1)[0] + "-"
    addr1 = address.split("╴", 1)[1]
    address = addr0 + addr1
    return address

def check_8(address):
    addr0 = address.split("村", 1)[0] + "里"
    addr1 = address.split("村", 1)[1]
    address = addr0 + addr1
    return address

def check_9(address):
    where = address.index("鄰")
    min123 = 99
    for e in range(len(a)):
        if a[e] in address:
            xx = where - address.index(a[e])

            # 找到鄰前面一個行政區域
            if min123 > xx and xx >= 0:
                min123 = xx
                minindex = e

    addr0 = address.split('鄰', 1)[0] + "鄰"
    addr1 = addr0.split(a[minindex], 1)[0] + a[minindex]
    addr2 = address.split('鄰', 1)[1]
    addr3 = addr1 + addr2

    return addr3
def check_10(address):
    where = address.index("里")
    for e in range(len(a)):
        if a[e] in address:
            xx = where - address.index(a[e])
            # 找到里前面一個行政區域
            if xx >= 0:
                minindex = e

    addr0 = address.split('里', 1)[0] + "里"
    # print(addr0)
    addr1 = addr0.split(a[minindex-1], 1)[0]+a[minindex-1]
    # print("addr1", addr1)
    addr2 = address.split('里', 1)[1]
    # print(addr2)
    addr3 = addr1 + addr2
    address = addr3
    return address


def check_11(address):
    where = address.index("村")
    for e in range(len(a)):
        if a[e] in address:
            xx = where - address.index(a[e])

            # 找到村前面一個行政區域
            if xx >= 0:
                minindex = e

    addr0 = address.split('村', 1)[0] + "村"
    addr1 = addr0.split(a[minindex-1], 1)[0] + a[minindex-1]
    addr2 = address.split('村', 1)[1]
    addr3 = addr1 + addr2
    address = addr3
    return address

################################################
for x in range(len(df)):  # len(acc23)
    # print(x)
    if x % 100 == 0:
        print(x)
    Address = []
    old = df[x]

    try:
        total, sentences = cut_1(df[x])
        if len(sentences) > 1:
            num0 += 1
    except:
        num1 += 1

    for ii in range(len(total)):
        Address.append(total[ii])
        # df.at[ii, "分割後"]
        # print("y", address)

    for jj in range(len(Address)):
        # df.at[len(Address), "分割後"] = old
        # df.at[jj, "分割後"] = old
        address = Address[jj]
        # 規則2 統一槓槓
        # print(jj, address)
        if "―" in address:
            address = check_1(address)
            num2 += 1
        if " _" in address:
            address = check_2(address)
            num2 += 1
        if "＿" in address:
            address = check_3(address)
            num2 += 1
        if "－" in address:
            address = check_4(address)
            num2 += 1
        if "-" in address:
            address = check_5(address)
            num2 += 1
        if "–" in address:
            address = check_6(address)
            num2 += 1
        if "╴" in address:
            address = check_7(address)
            num2 += 1

        # 規則3 去掉鄰
        if "鄰" in address:
            address = check_9(address)
            num4 += 1
            # print(address)
        # 規則4 舊縣市名稱(台北縣 臺北縣)
        if "台北縣" in address or "臺北縣" in address:
            a1 = address.split("縣", 1)[1]
            address = "新北市" + address
            num5 += 1
        # 規則5 行政區域錯誤
        for ii in range(len(newtaipei)):
            if newtaipei[ii] in address and "新北市" not in address:
                address = "新北市" + address.split('市', 1)[1]
                num6 += 1
        # 規則6 重複村
        if address.count("村") >= 2 and "新村" not in address and "大村村" not in address:
            a1 = address.split("村", 1)[0] + "村"
            a2 = address.split("村", 1)[1]
            a3 = a2.split("村", 1)[1]
            address = a1 + a3
            num7 += 1
        # 規則7 文字錯誤(裡改成里)
        if "裡" in address and "里" not in address:
            a1 = address.split("裡", 1)[0] + "里"
            a2 = address.split("裡", 1)[1]
            address = a1 + a2
            num8 += 1
        # 規則8 重複里
        if address.count(
                "里") >= 2 and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in \
                address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in \
                address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in \
                address and "埔里" not in address:
            a1 = address.split("里", 1)[0] + "里"
            a2 = address.split("里", 1)[1]
            a3 = a2.split("里", 1)[1]
            address = a1 + a3
            num9 += 1
        # 規則9 村里擇一排除(重複字串)
        if "村" in address and "里" in address and "新村" not in address and "里村" not in address and "村里" not in \
                address and "大村村" not in address and "大里" not in address and "后里" not in address and "里港" not in\
                address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in \
                address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in \
                address and "萬里" not in address and "埔里" not in address:
            # print("address:", address)
            a1 = address.split("里", 1)[0] + "里"
            a2 = address.split("村", 1)[1]
            address = a1 + a2
            num10 += 1
            # print(address)
            # df.a[aa[t],"原地址"] = old

        # 去除里
        if "里" in address:
            # print(address)
            address = check_10(address)
            num14 += 1

        # 去除村
        if "村" in address:
            address = check_11(address)
            num15 += 1


        # 規則10 地址不完整 (台東縣台東市)
        if "台東市" in address and "台東縣" not in address:
            address = "臺東縣" + address
            num11 += 1
        if "臺東市" in address and "臺東縣" not in address:
            address = "臺東縣" + address
            num11 += 1

        # if len(sentences) >= 2:
        print(x, sentences)
        # print(address)
        print("final:", address)
    ######################################################

    # df.at[x, "斷字後地址"] = address

# for i in range(len(address)):


# print(df["原始地址"])

    # if len(ok) != 0:
    #     for v in range(1, len(ok)):
    #         size = len(df)
    #         # print(size)
    #         df.at[size, "原地址"] = old
    #         df.at[size, "斷字後地址"] = ok[v]
    #         df.at[size, "備註1"] = "新增"
    # df.at[x, "原地址"] = old
    # df.at[x, "斷字後地址"] = address

#     try:
#         url = "http://geocoding.geohealth.tw/position.php?addr="+address
#         api = requests.get(url).json()
#         if api["accuracy"] == 1:
#             addr = api["fulladdr"]
#             twd97_x = api["TWD97_X"]
#             twd97_y = api["TWD97_Y"]
#             df.at[x,"twd97_x"] = twd97_x
#             df.at[x,"twd97_y"] = twd97_y
#             df.at[x,"GeoCoding地址_accuracy=1"] = addr
#             #print("addr:",addr)
#             if "樓" in address:
#                 floor = address.split('號',1)[1]
#                 for d in range(len(dd)):
#                     if dd[d] in floor:
#                         floor = floor.split(dd[d],1)[0]
#                 df.at[x,"比對地址"]=addr.split('號',1)[0]+"號" + floor
#                 df.at[x,"備註"] = "有變動_原地址有樓"
#             else:
#                 if "樓" in addr:
#                     df.at[x, "比對地址"]=addr.split('號', 1)[0]+"號"
#                     df.at[x, "備註"] = "有變動_原地址沒有樓但GEOCODING有"
#                 else:
#                     df.at[x,"比對地址"] = addr
#         elif api["accuracy"] == 2:
#             addr = api["fulladdr"]
#             addr = api["fulladdr"]
#             twd97_x = api["TWD97_X"]
#             twd97_y = api["TWD97_Y"]
#             df.at[x, "twd97_x"] = twd97_x
#             df.at[x, "twd97_y"] = twd97_y
#             df.at[x, "GeoCoding地址_accuracy=2"] = addr
#             df.at[x, "備註"] = "無法正規化_有退號"
#             acc2num += 1
#         else:
#             #print(address)
#             df.at[x,"備註"] = "無法正規化"
#             acc3num += 1
#     except:
#         apinum += 1
#         continue
#
# newappend = df[df['備註1'] == "新增"].index.tolist()
#
# for xx in range(len(newappend)):  # len(acc23)
#     address = df.at[newappend[xx], "斷字後地址"]
#     if "―" in address:
#         address = check_1(address)
#         num2 += 1
#     if " _" in address:
#         address = check_2(address)
#         num2 += 1
#     if "＿" in address:
#         address = check_3(address)
#         num2 += 1
#     if "－" in address:
#         address = check_4(address)
#         num2 += 1
#     if "-" in address:
#         address = check_5(address)
#         num2 += 1
#     if "–" in address:
#         address = check_6(address)
#         num2 += 1
#     if "╴" in address:
#         address = check_7(address)
#         num2 += 1
#
#     # 規則3 去掉鄰
#     if "鄰" in address:
#         address = check_9(address)
#         num4 += 1
#
#     # 規則4 舊縣市名稱(台北縣 臺北縣)
#     if "台北縣" in address or "臺北縣" in address:
#         a1 = address.split("縣", 1)[1]
#         address = "新北市" + address
#         num5 += 1
#     # 規則5 行政區域錯誤
#     for ii in range(len(newtaipei)):
#         if newtaipei[ii] in address and "新北市" not in address:
#             address = "新北市" + address.split('市', 1)[1]
#             num6 += 1
#
#     # 規則6 重複村
#     if address.count("村") >= 2 and "新村" not in address and "大村村" not in address:
#         a1 = address.split("村", 1)[0] + "村"
#         a2 = address.split("村", 1)[1]
#         a3 = a2.split("村", 1)[1]
#         address = a1 + a3
#         num7 += 1
#     # 規則7 文字錯誤(裡改成里)
#     if "裡" in address and "里" not in address:
#         a1 = address.split("裡", 1)[0] + "里"
#         a2 = address.split("裡", 1)[1]
#         address = a1 + a2
#         num8 += 1
#     # 規則8 重複里
#     if address.count(
#             "里") >= 2 and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         a1 = address.split("里", 1)[0] + "里"
#         a2 = address.split("里", 1)[1]
#         a3 = a2.split("里", 1)[1]
#         address = a1 + a3
#         num9 += 1
#     # 規則9 村里擇一排除(重複字串)
#     if "村" in address and "里" in address and "新村" not in address and "里村" not in address and "村里" not in address and "大村村" not in address and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         print(address)
#         a1 = address.split("里", 1)[0] + "里"
#         a2 = address.split("村", 1)[1]
#         address = a1 + a2
#         num10 += 1
#         print(address)
#         # df.loc[aa[t],"原地址"] = old
#     # 規則10 地址不完整 (台東縣台東市)
#     if "台東市" in address and "台東縣" not in address:
#         address = "臺東縣" + address
#         num11 += 1
#     if "臺東市" in address and "臺東縣" not in address:
#         address = "臺東縣" + address
#         num11 += 1
#
#     ######################################################
#     # 規則12 文字錯誤(行政區域名稱錯誤)
#     # 田沃村
#     if "連江縣" in address and "田澳村" in address:
#         a1 = address.split("澳", 1)[0] + "沃"
#         a2 = address.split("澳", 1)[1]
#         address = a1 + a2
#         num12 += 1
#     # 西林里
#     if "新北市" in address and "溪林里" in address:
#         a1 = address.split("溪", 1)[0] + "西"
#         a2 = address.split("溪", 1)[1]
#         address = a1 + a2
#         num13 += 1
#
#     # 規則13 區後面應為里
#     if "村" in address and "區" in address and "新村" not in address and "里" not in address:
#         address = check_8(address)
#         num3 += 1
#     df.at[newappend[xx], "斷字後地址"] = address
#     try:
#         url = "http://geocoding.geohealth.tw/position.php?addr="+address
#         api = requests.get(url).json()
#         if api["accuracy"] == 1:
#             addr = api["fulladdr"]
#             twd97_x = api["TWD97_X"]
#             twd97_y = api["TWD97_Y"]
#             df.at[newappend[xx],"twd97_x"] = twd97_x
#             df.at[newappend[xx],"twd97_y"] = twd97_y
#
#             df.at[newappend[xx],"GeoCoding地址"] = addr
#             #print("addr:",addr)
#             if "樓" in address:
#                 floor=address.split('號',1)[1]
#                 for d in range(len(dd)):
#                     if dd[d] in floor:
#                         floor = floor.split(dd[d],1)[0]
#                 df.at[newappend[xx],"比對地址"]=addr.split('號',1)[0]+"號" + floor
#                 df.at[newappend[xx],"備註"] = "有變動_原地址有樓"
#             else:
#                 if "樓" in addr:
#                     df.at[newappend[xx],"比對地址"]=addr.split('號',1)[0]+"號"
#                     df.at[newappend[xx],"備註"] = "有變動_原地址沒有樓但GEOCODING有"
#                 else:
#                     df.at[newappend[xx],"GeoCoding地址"] = addr
#                     df.at[newappend[xx],"比對地址"] = addr
#         elif api["accuracy"] == 2:
#             addr = api["fulladdr"]
#             twd97_x = api["TWD97_X"]
#             twd97_y = api["TWD97_Y"]
#             df.at[newappend[xx],"twd97_x"] = twd97_x
#             df.at[newappend[xx],"twd97_y"] = twd97_y
#             df.at[newappend[xx],"GeoCoding地址_accuracy=2"] = addr
#             df.at[newappend[xx],"備註"] = "無法正規化_有退號"
#             acc2num += 1
#         else:
#             df.at[newappend[xx],"備註"] = "無法正規化"
#             acc3num += 1
#     except:
#         apinum += 1
#         continue
#
# df_new = df[['原地址','斷字後地址','GeoCoding地址_accuracy=1','GeoCoding地址_accuracy=2','比對地址','備註','備註1','twd97_x','twd97_y','類型']]
# # df_new.to_csv('.csv',index=False,encoding="utf_8_sig")
end = time.time()
running_time = end-start
print("running_time:",running_time)
print("多個門牌:",num0)
print("多個門牌的錯誤:",num1)
print("槓槓:",num2)
print("區後面應為里:",num3)
print("去掉鄰:",num4)
print("舊縣市名稱(台北縣 臺北縣):",num5)
print("行政區域錯誤:",num6)
print("重複村:",num7)
print("文字錯誤(裡改成里):",num8)
print("重複里:",num9)
print("村里擇一排除(重複字串):",num10)
print("地址不完整 (台東縣台東市):",num11)
print("去除里", num14)
print("去除村", num15)
