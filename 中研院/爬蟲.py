from bs4 import BeautifulSoup
import requests
import pandas as pd

head_Html_lotto = 'https://api.tgos.tw/rec/count.aspx?AppID=n9MXVw+jpu4wefpZKWRinK3GsFdcC3IVojO1W2fh0uNmwMLppFqqLg==&APIID=A02&DataID=B01'
res = requests.get(head_Html_lotto, timeout=30)
# print(res)
df = pd.read_html('https://api.tgos.tw/rec/count.aspx?AppID=n9MXVw+jpu4wefpZKWRinK3GsFdcC3IVojO1W2fh0uNmwMLppFqqLg==&APIID=A02&DataID=B01')
print(df[0])
# total = df[0]
# for i in range(160, 162):
#     dfs = pd.read_html('https://opengovtw.com/gov?page='+str(i))
#     print(i)
#     total = pd.concat([total, dfs[0]])
# print(total)

