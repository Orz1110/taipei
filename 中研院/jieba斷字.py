# encoding=utf-8
import jieba
import pandas as pd
import sys
import numpy as np
import jieba.analyse

jieba.set_dictionary("dict.txt")
jieba.load_userdict("userdict.txt")

# data = pd.read_excel("C:/Users/Orz/Desktop/中研院/藥局比對結果清洗前.xlsx")
data = pd.read_csv("C:/Users/Orz/Desktop/test.csv")

data = data["Address"][0:30]
# print(data[0:20])
newtaipei = ["萬里區","金山區","板橋區","汐止區","深坑區","石碇區","瑞芳區","平溪區","雙溪區","貢寮區","新店區","坪林區","烏來區","永和區","中和區","土城區","三峽區","樹林區","鶯歌區","三重區","新莊區","泰山區","林口區","蘆洲區","五股區","八里區","淡水區","三芝區","石門區"]
# print(data)
# jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
strs = list(data)
print(type(strs))

"""把字串半形轉全形"""
def strB2Q(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 全形空格直接轉換
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):  # 全形字元（除空格）根據關係轉化
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)
"""把字串全形轉半形"""
def strQ2B(ustring):

    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全形空格直接轉換
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全形字元（除空格）根據關係轉化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)
"""國字轉數字"""
def _trans(s):
    digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, "一一": 11,
             "二二": 22, "三三": 33, "四四": 44, "五五": 55, "六六": 66, "七七": 77, "八八": 88, "九九": 99}
    num = 0
    if s:
        idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
        if idx_q != -1:
            num += digit[s[idx_q - 1:idx_q]] * 1000
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的处理
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]
    return num
def trans(chn):
    chn = chn.replace('零', '')
    idx_y, idx_w = chn.rfind('亿'), chn.rfind('万')
    if idx_w < idx_y:
        idx_w = -1
    num_y, num_w = 100000000, 10000
    if idx_y != -1 and idx_w != -1:
        return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:idx_w]) * num_w + _trans(chn[idx_w + 1:])
    elif idx_y != -1:
        return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:])
    elif idx_w != -1:
        return _trans(chn[:idx_w]) * num_w + _trans(chn[idx_w + 1:])
    return _trans(chn)
# 規則1 同一單位多門牌
def cut(address):
    c = ['、', '及', ';', '．', '/', '，', '‧', '；', '。', '.', '˙', '丶']
    dd = ["〈", "(", "（"]
    b = ["樓", "號", "弄", "巷", "段", "路", "大道", "街", "村", "里", "區", "鎮", "鄉", "市", "縣"]
    a = ["縣", "市", "鄉", "鎮", "區", "里", "村", "街", "大道", "路", "段", "巷", "弄", "號", "樓"]
    ok = []
    new1 = address
    All_ok = []
    while c[0] in new1 or c[1] in new1 or c[2] in new1 or c[3] in new1 or c[4] in new1 or c[5] in new1 or c[
        6] in new1 or c[7] in new1 or c[8] in new1 or c[9] in new1 or c[10] in new1 or c[11] in new1:
        where = []

        for n in range(len(c)):
            if c[n] in new1:
                where.append(new1.index(c[n]))
            else:
                where.append(999)
        minwhere = min(where)
        minindex = where.index(minwhere)

        new = new1.split(c[minindex], 1)[0]

        if "號" not in new and "樓" not in new:
            new = new + "號"
        if "號" in new and "樓" not in new:
            length = len(new)
            where = new.index("號")
            if length - 1 != where:
                new = new + "樓"
        ok.append(new)
        new1 = new1.split(c[minindex], 1)[1]
    ok.append(new1)
    # print("ok:", ok)
    for i in range(1, len(ok)):
        find = 0
        for ii in range(len(b)):
            if b[ii] in ok[i]:
                e = b[ii]
                find = 1
                # print(e)

        if find == 1:
            min123 = 99
            minindex = 99
            l = i - 1
            # print(e)
            if e not in ok[l] and e == "巷":
                e = "號"

            if e not in ok[l] and e == "街":
                e = "段"

            if e not in ok[l] and e == "段":
                e = "路"

            if e not in ok[l] and e == "路":
                e = "街"

            where = ok[l].index(e)

            for ii in range(0, len(a)):
                if a[ii] in ok[l]:
                    xx = where - ok[l].index(a[ii])
                    if min123 > xx and xx > 0:
                        min123 = xx
                        # print("min123:",min123)
                        minindex = ii
            if minindex == 99:
                minindex = a.index(e)
                # print("a[minindex]",a[minindex])
            addr0 = ok[l].split(a[minindex], 1)[0]
            if len(addr0) == 2:
                address = ok[i]
            else:
                address = addr0 + a[minindex] + ok[i]
            ok[i] = address
    return (ok)
def check_8(address):
    addr0 = address.split("村", 1)[0]+"里"
    addr1 = address.split("村", 1)[1]
    address_3 = addr0+addr1
    return address_3


# 1.同一單位多門牌
all_ok = []
for str in strs:
    # print("str:", str)
    ok = cut(str)
    # print(ok)
    for j in range(len(ok)):
        all_ok.append(ok[j])
for i in range(len(all_ok)):
    print("原始:", all_ok[i])
    address = all_ok[i]



    # 規則6 重複村
    if address.count("村") >= 2 and "新村" not in address and "大村村" not in address:
        a1 = address.split("村", 1)[0] + "村"
        a2 = address.split("村", 1)[1]
        a3 = a2.split("村", 1)[1]
        address = a1 + a3
    # 規則7 文字錯誤(裡改成里)
    if "裡" in address and "里" not in address:
        a1 = address.split("裡", 1)[0] + "里"
        a2 = address.split("裡", 1)[1]
        address = a1 + a2
        # 規則8 重複里
    if address.count(
            "里") >= 2 and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
        a1 = address.split("里", 1)[0] + "里"
        a2 = address.split("里", 1)[1]
        a3 = a2.split("里", 1)[1]
        address = a1 + a3
    # 規則9 村里擇一排除(重複字串)
    if "村" in address and "里" in address and "新村" not in address and "里村" not in address and "村里" not in address and "大村村" not in address and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
        a1 = address.split("里", 1)[0] + "里"
        a2 = address.split("村", 1)[1]
        address = a1 + a2
    # 規則10 地址不完整 (台東縣台東市)
    if "台東市" in address and "台東縣" not in address:
        address = "臺東縣" + address
    if "臺東市" in address and "臺東縣" not in address:
        address = "臺東縣" + address


    ######################################################
    # 規則12 文字錯誤(行政區域名稱錯誤)
    # 田沃村
    if "連江縣" in address and "田澳村" in address:
        a1 = address.split("澳", 1)[0] + "沃"
        a2 = address.split("澳", 1)[1]
        address = a1 + a2
    # 西林里
    if "新北市" in address and "溪林里" in address:
        a1 = address.split("溪", 1)[0] + "西"
        a2 = address.split("溪", 1)[1]
        address = a1 + a2
    # 蓮海路
    if "高雄市" in address and "連海路" in address:
        a1 = address.split("連", 1)[0] + "蓮"
        a2 = address.split("連", 1)[1]
        address = a1 + a2

    # 規則13
    if "村" in all_ok[i] and "區" in all_ok[i] and "新村" not in all_ok[i] and "里" not in all_ok[i]:
        address_3 = check_8(all_ok[i])
        all_ok[i] = address_3

    # 全形轉半形
    resu = strQ2B(all_ok[i])
    # print(resu)

    # 斷字
    seg_list = jieba.cut(resu, use_paddle=True)  # 使用paddle模式
    address = '/'.join(list(seg_list))
    address = address.split("/")
    print(address)

    # 2.刪除重複區域名稱
    address_1 = sorted(set(address), key=address.index)
#
#
#   # 規則4.新北市修改
    for j in range(len(address_1)):
        if "台北縣" in address_1[0] or "臺北縣" in address_1[0]:
            address_1[0] = "新北市"

    # 規則5.行政區域錯誤
    for ii in range(len(newtaipei)):
        if newtaipei[ii] in address_1 and "新北市" not in address_1[0]:
            address_1[0] = "新北市"
    print("fix", address_1)









        # del address_1[del_lol]






    # 合併list
    # space = ""
    # print(space.join(address))

    # print(address)
    # seg_list = jieba.cut(str, cut_all=False)
    # address_1 ="/ ".join(seg_list)
    # address_1 = address_1.split("/")
    # print(address_1)


# #規則5 行政區域錯誤
#     for ii in range(len(newtaipei)):
#         if newtaipei[ii] in address and "新北市" not in address :
#             address="新北市" + address.split('市',1)[1]
#             num6 +=1
# #規則6 重複村
#     if address.count("村") >= 2 and "新村" not in address and "大村村" not in address:
#         a1 =address.split("村",1)[0]+"村"
#         a2 =address.split("村",1)[1]
#         a3 =a2.split("村",1)[1]
#         address =a1+a3
#         num7 +=1
# #規則7 文字錯誤(裡改成里)
#     if "裡" in address and "里" not in address:
#         a1 =address.split("裡",1)[0]+"里"
#         a2 =address.split("裡",1)[1]
#         address =a1+a2
#         num8 +=1
# #規則8 重複里
#     if address.count("里") >= 2 and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         a1 =address.split("里",1)[0]+"里"
#         a2 =address.split("里",1)[1]
#         a3 =a2.split("里",1)[1]
#         address =a1+a3
#         num9 +=1
# #規則9 村里擇一排除(重複字串)
#     if "村" in address and "里" in address and "新村" not in address and  "里村" not in address and  "村里" not in address and "大村村" not in address and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         a1 =address.split("里",1)[0]+"里"
#         a2 =address.split("村",1)[1]
#         address =a1+a2
#         num10 +=1
#
#         #df.loc[aa[t],"原地址"] = old
# #規則10 地址不完整 (台東縣台東市)
#     if "台東市" in address and "台東縣" not in address :
#         address ="臺東縣"+address
#         num11 +=1
#     if "臺東市" in address and "臺東縣" not in address :
#         address ="臺東縣"+address
#         num11 +=1
# ######################################################
# #規則12 文字錯誤(行政區域名稱錯誤)
# #田沃村
#     if "連江縣" in address and "田澳村" in address :
#         a1 =address.split("澳",1)[0]+"沃"
#         a2 =address.split("澳",1)[1]
#         address =a1+a2
#         num12 +=1
# #西林里
#     if "新北市" in address and "溪林里" in address :
#         a1 =address.split("溪",1)[0]+"西"
#         a2 =address.split("溪",1)[1]
#         address =a1+a2
#         num13 +=1
#
# #規則13 區後面應為里
#     if "村" in address and "區" in address and "新村" not in address and "里" not in address:
#         address = check_8(address)
#         num3 += 1





    #
    # 精确模式
    # seg_list = jieba.cut(str)  # 默认是精确模式
    # print(", ".join(seg_list))

