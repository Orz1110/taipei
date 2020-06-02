import urllib.request as req
url = "https://tpc.googlesyndication.com/pagead/js/r20200519/r20110914/client/window_focus_fy2019.js"
request = req.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")
print(data)

# import bs4
# root = bs4.BeautifulSoup(data, "html.parser")
# print(root.title)