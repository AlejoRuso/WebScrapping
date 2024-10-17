#Импорт библиотек
    #pip install requests
    #pip install beautifulsoup4
    #pip install lxml
    

import requests
import bs4
import json
from pprint import pprint
import re

#Список слов для поиска в заголовках статей
keywords = ['дизайн', 'фото', 'web', 'python']

#Получаем страницу с которой будем работать
response = requests.get('https://habr.com/ru/articles/')
soup = bs4.BeautifulSoup(response.text, features='lxml')

articles_list = soup.findAll('div', class_='tm-article-snippet tm-article-snippet')
#print(len(articles_list))

#отбираем заголовки
parsed_data = []

#Отбираем ссылки на статьи
for article in articles_list:
    link = f"https://habr.com{article.find('a', class_='tm-title__link')['href']}"
    #print(link)

    #Отбираем заголовки и время статей
    response = requests.get(link)
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    title = soup.find('h1').text.strip()
    time = soup.find('time')['datetime']

    #Сохраняем в словари
    parsed_data.append({
        'date': time,
        'title': title,
        'link': link
    })

#pprint(parsed_data)

#Отбираем заголовки по ключевым словам

final_list = []
for word in keywords:
    for i in parsed_data:
        match=re.search(word, i.get('title'))
        if match:
            final_list.append(i)
        else:
            pass

if len(final_list) == 0:
    print('Подходячщие статьи не найдены, измените ключевые слова')
else:
    pprint(final_list)