import pytrends
import pandas as pd
from pytrends.request import TrendReq

data = {}
# keyword index
# value details
# details   0 - title
#           1 - link 
#           2 - list of articles


pytrend = TrendReq()
trending_today = pytrend.today_searches(pn = 'IN')
df_trending_today = pd.DataFrame(trending_today)

links =[]
for i, path in enumerate(trending_today):
    url = "https://trends.google.com" + path
    title_uf = url[43:]
    title_uf_2 = title_uf.split("&")
    details = [title_uf_2[0], "https://trends.google.com" + path]
    data[i] = details
print("Sucessfully got the trends. [",len(data),"]")
# got the  trending for the day sucessfully

print("Working on ", data[0][0], " ...")

from googlesearch import search
from googlesearch import SearchResult
url_list = list(search(data[0][0]))
data[0].append(url_list)
