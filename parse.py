import requests
import bs4
from fake_headers import Headers
import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
host = 'https://habr.com'
headers = Headers(browser='chrome', os='win', headers=True).generate()
response = requests.get(host + '/ru/all/', headers=headers)
print(f'Ответ сервера {response.status_code}')
# print(*response.request.headers.items(), sep='\n')

soup = bs4.BeautifulSoup(response.text, features='lxml')
block_article = soup.find_all(name='div', class_='tm-article-snippet')

data = []
for word in KEYWORDS:
    for item in block_article:
        text = item.find(class_='article-formatted-body').text
        date = item.find(name='time')
        title = item.find(class_='tm-title__link')
        if word in text or word in title:
            data.append(
                {'дата': date.attrs['title'][:10], 'заголовок': title.text, 'ссылка': host + title.attrs['href']})
print()
if len(data):
    print('Итоговый список статей удовлетворяющих условиям поиска.')
    pprint.pprint(data)
else:
    print('Статей удовлетворяющих условиям поиска на Хабре нет')
