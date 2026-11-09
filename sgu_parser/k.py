import requests
from bs4 import BeautifulSoup

url = "https://www.sgu.ru/schedule/teacher/317"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.find_all('tr')

