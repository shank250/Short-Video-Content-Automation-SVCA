import requests
from bs4 import BeautifulSoup

url = 'https://trends.google.com/home'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# trending_searches = soup.find_all('div', {'class': 'title'})
# for index, search in enumerate(trending_searches[:20]):
#     print(f"{index+1}. {search.text}")
print(soup.prettify())