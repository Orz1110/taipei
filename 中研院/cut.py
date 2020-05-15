# encoding=utf-8
import jieba
import pandas as pd
import sys
import numpy as np
import jieba.analyse
import re
# jieba.set_dictionary("dict.txt")
# jieba.load_userdict("userdict.txt")

# data = pd.read_excel("C:/Users/Orz/Desktop/中研院/藥局比對結果清洗前.xlsx")
data = pd.read_csv("C:/Users/Orz/Desktop/test.csv")

# data = data["原始地址"]
data = data["Address"]
#
newtaipei = ["萬里區","金山區","板橋區","汐止區","深坑區","石碇區","瑞芳區","平溪區","雙溪區","貢寮區","新店區","坪林區","烏來區","永和區","中和區","土城區","三峽區","樹林區","鶯歌區","三重區","新莊區","泰山區","林口區","蘆洲區","五股區","八里區","淡水區","三芝區","石門區"]

b = ["樓", "號", "弄", "巷", "段", "路", "大道", "街", "村", "里", "區", "鎮", "鄉", "市", "縣"]
a = ["縣", "市", "鄉", "鎮", "區", "里", "村", "街", "大道", "路", "段", "巷", "弄", "號", "樓"]

dd = ["〈", "（", "("]
all_df = []
c = ['、', '及', ';', '．', '/', '，', '‧', '；', '。', '.', '˙', '丶']
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
    digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    num = 0
    if s:
        # s = "一百五十三"
        idx_b, idx_s = s.find('百'), s.find('十')
        print(idx_s)
        if idx_b != -1:
            num += digit[s[idx_b - 1:idx_b]] * 100
        if idx_s != -1:
            # 十前忽略一的处理
            num += digit.get(s[idx_s - 1:idx_s], 1) * 10
        if s[-1] in digit:
            num += digit[s[-1]]
        # print(num)
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


def cut_1(address):

    sentences = address
    sentences = re.split(r"[、及;．/，‧；。˙丶]", sentences)
    print(sentences)
    str_ok = []
    for str in sentences:
        if "號" not in str and "樓" not in str:
            str = str + "號"
            # print(str)
        if "號" in str and "樓" not in str:
            if str[-1] != "號":
                str = str + "樓"
                # print(str)
        # print(str)
        str_ok.append(str)
        # print("str1:", str)
    total = []
    total.append(str_ok[0])
    for i in range(1, len(str_ok)):
        sub_ok = str_ok[i]

        if "號" not in str_ok[i] and "樓" in str_ok[i] and i == 1:
            find_hao = str_ok[0].find("號")
            str_ok[i] = str_ok[0][0:find_hao + 1] + str_ok[i]
            # print("1:", str_ok[i])
            total.append(str_ok[i])

        elif "號" in str_ok[i] and "樓" in str_ok[i]:
            where = str_ok[0].find("號")
            for j in range(len(a)):
                if a[j] in str_ok[0]:
                    xx = where - str_ok[0].index(a[j])
                    if xx > 0:
                        # print("str_ok[i]",str_ok[i])
                        str_ok[i] = str_ok[0].split(a[j], 1)[0]+a[j]+sub_ok
            # print("2",str_ok[i])
            total.append(str_ok[i])

        elif "號" not in str_ok[i] and "樓" in str_ok[i] and i!= 1:
            find_hao = str_ok[i-1].find("號")
            str_ok[i] = str_ok[i-1][0:find_hao + 1] + str_ok[i]
            # print("3:", str_ok[i])
            total.append(str_ok[i])
    return total

        # find_list = []
        # for j in range(len(a)):
        #     find_list.append(str.find(a[j]))
        # print(max(find_list))
        # print(str[0:max(find_list)+1])


    # ok = sentences
    # return ok



# 統一-符號
def check_1(address):
    #where1 = address.index("―")
    addr0=address.split("―",1)[0]+"-"
    addr1=address.split("―",1)[1]
    address = addr0+addr1
    return address
def check_2(address):
    #where1 = address.index("_")
    addr0=address.split("_",1)[0]+"-"
    addr1=address.split("_",1)[1]
    address = addr0+addr1
    return address
def check_3(address):
    #where1 = address.index("＿")
    addr0=address.split("＿",1)[0]+"-"
    addr1=address.split("＿",1)[1]
    address = addr0+addr1
    return address
def check_4(address):
    #where1 = address.index("－")
    addr0=address.split("－",1)[0]+"-"
    addr1=address.split("－",1)[1]
    address = addr0+addr1
    return address
def check_5(address):
    #where1 = address.index("-")
    addr0=address.split(" -",1)[0]+"-"
    addr1=address.split(" -",1)[1]
    address = addr0+addr1
    return address
def check_6(address):
    #where1 = address.index("–")
    addr0=address.split("–",1)[0]+"-"
    addr1=address.split("–",1)[1]
    address = addr0+addr1
    return address
def check_7(address):
    #where1 = address.index("╴")
    addr0=address.split("╴",1)[0]+"-"
    addr1=address.split("╴",1)[1]
    address = addr0+addr1
    return address

# 行政區域錯誤 村改里
def check_8(address):
    addr0 = address.split("村", 1)[0]+"里"
    addr1 = address.split("村", 1)[1]
    address = addr0+addr1
    return address
def check_9(address):
    where = address.index("鄰")
    min123 = 99
    for e in range(len(a)):
        if a[e] in address:
            xx = where - address.index(a[e])
            if min123 > xx and xx >= 0:
                min123 = xx
                minindex = e

    addr0 = address.split('鄰', 1)[0] + "鄰"
    addr1 = addr0.split(a[minindex], 1)[0] + a[minindex]
    addr2 = address.split('鄰', 1)[1]
    addr3 = addr1 + addr2

    return addr3

ccc = ['、', '及', ';', '．', '/', '，', '‧', '；', '。', '.', '˙', '丶']

# 1.同一單位多門牌
all_ok = []
for str in strs:
    print("str:", str)
    # if (ccc[0] in str or ccc[1] in str or ccc[2] in str or ccc[3] in str or ccc[4] in str or ccc[5] in str
    #     or ccc[6] in str or ccc[7] in str or ccc[8] in str or ccc[9] in str or ccc[10] in str or ccc[11] in str) :
    total = cut_1(str)
    # print(total)
    for j in range(len(total)):
        # all_ok.append(ok[j])
        print("total:", total[j])

# for i in range(len(all_ok)):
#     # print(all_ok[i])
#     address = all_ok[i]
#     # 規則2 統一槓槓
#     if "―" in address:
#         address = check_1(address)
#     if " _" in address:
#         address = check_2(address)
#     if "＿" in address:
#         address = check_3(address)
#     if "－" in address:
#         address = check_4(address)
#     if " -" in address:
#         address = check_5(address)
#     if "–" in address:
#         address = check_6(address)
#     if "╴" in address:
#         address = check_7(address)
#
#     # 規則3 去掉鄰
#     if "鄰" in address:
#         address = check_9(address)
#
#     # 規則4 舊縣市名稱(台北縣 臺北縣)
#     if "台北縣" in address or "臺北縣" in address:
#         a1 = address.split("縣", 1)[1]
#         address = "新北市" + address
#
#     # 規則5 行政區域錯誤
#     for ii in range(len(newtaipei)):
#         if newtaipei[ii] in address and "新北市" not in address:
#             address = "新北市" + address.split('市', 1)[1]
#
#     # 規則6 重複村
#     if address.count("村") >= 2 and "新村" not in address and "大村村" not in address:
#         a1 = address.split("村", 1)[0] + "村"
#         a2 = address.split("村", 1)[1]
#         a3 = a2.split("村", 1)[1]
#         address = a1 + a3
#
#     # 規則7 文字錯誤(裡改成里)
#     if "裡" in address and "里" not in address:
#         a1 = address.split("裡", 1)[0] + "里"
#         a2 = address.split("裡", 1)[1]
#         address = a1 + a2
#
#     # 規則8 重複里
#     if address.count(
#             "里") >= 2 and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         a1 = address.split("里", 1)[0] + "里"
#         a2 = address.split("里", 1)[1]
#         a3 = a2.split("里", 1)[1]
#         address = a1 + a3
#
#     # 規則9 村里擇一排除(重複字串)
#     if "村" in address and "里" in address and "新村" not in address and "里村" not in address and "村里" not in address and "大村村" not in address and "大里" not in address and "后里" not in address and "里港" not in address and "苑里" not in address and "五里路" not in address and "太麻里" not in address and "阿里山" not in address and "佳里" not in address and "仁里" not in address and "富里" not in address and "玉里" not in address and "萬里" not in address and "埔里" not in address:
#         a1 = address.split("里", 1)[0] + "里"
#         a2 = address.split("村", 1)[1]
#         address = a1 + a2
#
#     # 規則10 地址不完整 (台東縣台東市)
#     if "台東市" in address and "台東縣" not in address:
#         address = "臺東縣" + address
#     if "臺東市" in address and "臺東縣" not in address:
#         address = "臺東縣" + address
#
#     # 規則12 文字錯誤(行政區域名稱錯誤)
#
#         # 田沃村
#     if "連江縣" in address and "田澳村" in address:
#         a1 = address.split("澳", 1)[0] + "沃"
#         a2 = address.split("澳", 1)[1]
#         address = a1 + a2
#         # 西林里
#     if "新北市" in address and "溪林里" in address:
#         a1 = address.split("溪", 1)[0] + "西"
#         a2 = address.split("溪", 1)[1]
#         address = a1 + a2
#         # 蓮海路
#     if "高雄市" in address and "連海路" in address:
#         a1 = address.split("連", 1)[0] + "蓮"
#         a2 = address.split("連", 1)[1]
#         address = a1 + a2
#
#     # 規則13 區後面應為里
#     if "村" in address and "區" in address and "新村" not in address and "里" not in address:
#         address = check_8(address)
#     # print("1:", address)
#
#
#     # # 全形轉半形
#     # resu = strQ2B(address)
#     # # print(resu)
#     #
#     # # ------------------------------斷字-----------------------------------------
#     # seg_list = jieba.cut(resu, use_paddle=True)  # 使用paddle模式
#     # # tags = jieba.analyse.extract_tags(resu, 10)
#     # # print(tags)
#     # address = '/'.join(list(seg_list))
#     # address = address.split("/")
#     # # print(address)
#     # stop = len(address)
#     # for j in range(len(address)):
#     #     # address[j] = trans(address[j])
#     #     # address[j] = str(ad)
#     #     if dd[0] in address[j] or dd[1] in address[j] or dd[2] in address[j]:
#     #         stop = j
#     #     # address[j] = trans(address[j])
#     # # print(address[0:stop])
#     # address = address[0:stop]
#     # print(address)
#
#     # 合併list
#     space = ""
#     final_address = space.join(address)
#     all_df.append(final_address)
# for p in range(len(all_df)):
#     ok = cut(all_df[p])
#     print("ok",ok)
# # all_df = pd.DataFrame(all_df)
# # print(all_df)
# # all_df.to_csv("C:/Users/daveyap/Desktop/藥局測試_output.csv",index=False,encoding="utf_8_sig")
#
#     # print(address)
#     # seg_list = jieba.cut(str, cut_all=False)
#     # address ="/ ".join(seg_list)
#     # address = address.split("/")
#     # print(address)
#
#
