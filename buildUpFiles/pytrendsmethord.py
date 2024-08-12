import pytrends
import pandas as pd
import json
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
i = 0
for path in trending_today:
    details = []
    url = "https://trends.google.com" + path
    title_uf = url[43:]
    title_uf_2 = title_uf.split("&")
    # adding details
    details.append(title_uf_2[0])
    details.append("https://trends.google.com" + path)
    data[i] = details

    print("Working on ", data[i][0], " ...")
    from googlesearch import search
    from googlesearch import SearchResult
    url_list = list(search(data[i][0]))
    data[i] = data[i] + url_list
    print(data[i])
    i += 1
print("Sucessfully got the trends. [",len(data),"]")
# got the  trending for the day sucessfully


with open("data.json", "w") as f:
    json.dump(data, f)
print("Succesfully dumped the  data. :)")
