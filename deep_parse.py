import requests
import bs4
from fake_headers import Headers
import time
import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
host = 'https://habr.com'
headers = Headers(browser='chrome', os='win', headers=True).generate()

response = requests.get(host + '/ru/all/', headers=headers)
print(f'Ответ сервера {response.status_code}')

soup = bs4.BeautifulSoup(response.text, features='lxml')
block_article = soup.find_all(name='div', class_='tm-article-snippet')

links = []
for item in block_article:
    title = item.find(class_='tm-title__link')
    links.append(host + title.attrs['href'])
print(f'Общее количество ссылок {len(links)}')
time.sleep(3)

data = []
for i in range(len(links)):
    new_response = requests.get(links[i], headers=headers)
    print(f'Сейчас обрабатывается ссылка {i + 1}. Ответ сервера {new_response.status_code}')
    soup_deep = bs4.BeautifulSoup(new_response.text, features='lxml')
    text = soup_deep.find(class_='article-formatted-body').text
    date = soup_deep.find(name='time')
    title = soup_deep.find(name='title')
    link = links[i]
    words = []
    for word in KEYWORDS:
        if word in text:
            words.append(word)
            data.append({'дата': date.attrs['title'][:10], 'заголовок': title.text[:-7], 'ссылка': link})
    time.sleep(3)

print()
if len(data):
    print(f'Всего найдено статей {len(data)}')
    print('Итоговый список статей удовлетворяющих условиям поиска.')
    pprint.pprint(data)
else:
    print('Статей удовлетворяющих условиям поиска на Хабре нет')
