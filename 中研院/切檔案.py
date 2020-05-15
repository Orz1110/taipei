import pandas as pd
data = pd.read_csv("C:/Users/Orz/Desktop/中研院/四大超商.csv")
print(data)
total_len = len(data)
#　C:\Users\Orz\Desktop\中研院\切檔案
for i in range(len(data)//500):
    data_1 = data[0:500]
    data = data.drop(data.index[:500])
    data_1['id'] = data_1.index
    print(data_1)
    # data_1.to_csv('C:/Users/Orz/Desktop/中研院/切檔案/' + str(i) + '.csv', index=False)

data_last = data
# data_last.to_csv('C:/Users/Orz/Desktop/中研院/切檔案/' + str((total_len//500)) + '.csv', index=False)
# 更改文件编码
# 文件统一改为utf-8无BOM
# -*- coding: UTF-8 -*-
import os
import pandas as pd

#需要把文件改成编码的格式（可以自己随时修改）
coding = 'utf-8_sig'
# 文件夹目录（可以更改文件编码的文件夹~）
file_dir = 'C:/Users/Orz/Desktop/中研院/切檔案/'

def run_coding():
    for root, dirs, files in os.walk(file_dir, topdown=False):
        for i in files:
            files_name = os.path.join(root, i)
            try:
                df1 = pd.read_csv(files_name, encoding='utf-8')
            except:
                df1 = pd.read_csv(files_name, encoding='gbk')
            df1.to_csv(files_name, encoding=coding, index=None)

if __name__ == '__main__':
    run_coding()
    print("It's done")