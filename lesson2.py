"""
Источник https://geekbrains.ru/posts
Задача:
Необходимо обойти все записи блога и получить следующую структуру информации:

{
"title": заголовок статьи,
"image": Заглавное изображение статьи (ссылка),
"text": Текст статьи,
"pub_date": time_stamp даты публикации,
"autor": {"name": Имя автора,
               "url": ссылка на профиль автора,
               },
}
по окончании сбора, полученые данные должны быть сохранены в json файл.
В структуре должны присутсвовать все статьи на дату парсинга
"""
from bs4 import BeautifulSoup
import requests
import random
import time
import json
import os
import datetime

def get_soup(url):
    """
    Принимает урл и возвращает суп по урлу
    """
    data = requests.get(url)
    if data.status_code == 200:
        return BeautifulSoup(data.text, 'lxml')
    else:
        return None

def get_url_list(soup_data):
    """
    Получает суп страницы и возвращает список ссылок на посты со страницы
    """
    posts_links_soup = soup_data.find_all('a', class_='post-item__title')
    url_lst = []
    for post_link in posts_links_soup:
        url_lst.append(website + post_link['href'])

    return url_lst

def get_post_urls(url):
    """
    Принимает урл на блог и возвращает список урлов на посты со всех страниц блога
    """
    posts_links_lst = []

    while True:
        soup_data = get_soup(url)

        if soup_data:
            posts_links_lst.extend(get_url_list(soup_data))

            next_link_soup = soup_data.find('a', attrs = {'rel': 'next'}, text = '›')
            print(next_link_soup)

        if not next_link_soup:
            break
        url = website + next_link_soup['href']
        #time.sleep(random.randint(1, 5))

    return posts_links_lst

def get_image(body):
    """
    Принимает содержимое страницы и возвращает ссылку на первую попавшуюся картинку или None
    """
    body = body.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
    soup_data = BeautifulSoup(body, 'lxml')
    next_link_soup = soup_data.find('img')
    if next_link_soup:
        return next_link_soup['src']
    else:
        return None

def get_post_info(url_lst):
    """
    Принимает список урлов на посты и возвращает данные постов в словаре, где у каждого поста указанные выше данные
    """
    post_info = {}
    for url in url_lst:
        soup_data = get_soup(url)

        if soup_data:
            post_data = soup_data.find('script', attrs={'type': 'application/ld+json'})
            post_dict_data = json.loads(post_data.get_text())
            print(url)

            post_info[url] = {
                            'title': post_dict_data['headline'],
                            'image': get_image(post_dict_data['articleBody']),
                            'text': post_dict_data['articleBody'],
                            'pub_date': datetime.datetime.fromisoformat(post_dict_data['datePublished']).timestamp(),
                            'author': {'name': post_dict_data['author']['name'],
                                       'url': post_dict_data['author']['url'],
                                       },
                            }
        else:
            post_info[url] = {'error': True}
        #time.sleep(random.randint(1, 5))
    return post_info

def save_data(post_info):
    """
    Принимает словарь с данными постов и сохраняет в формате json в файле
    """
    with open(os.path.abspath('lesson2.json'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(post_info))


url = 'https://geekbrains.ru/posts'
website = url.split("//")[0] + '//' + url.split("//")[-1].split("/")[0]

posts_links_lst = get_post_urls(url)

post_info_dict = get_post_info(posts_links_lst)
save_data(post_info_dict)

print(len(posts_links_lst))