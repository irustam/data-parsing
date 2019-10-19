"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""
import requests
import os
import json

API_KEY = 'di6DIijcrJtPJH36BPf37BFRDi2ZYgQawLyuh3m3zU4P57RJycMQ6eox9VDFtNcA'

#Буду использовать АПИ сервиса поиска информации о музыкальных произведениях,
#альбомах и артистах с сайта https://apiseeds.com

#Пример запроса поиска информации о произведении по названию:
music_name = 'Innuendo'
limit = 5
url = f'https://orion.apiseeds.com/api/music/search/?apikey={API_KEY}&q={music_name}&limit={limit}'
data = requests.get(url)

if data.status_code == 200:
    j_data = data.json()
    if j_data.get('success') == True:
        for item in j_data.get('result'):
            print('title: ', item['title'])
            print('artist: ', item['artist'])
            print('album: ', item['album'])
            print('*'*30)

        with open(os.path.abspath('lesson1_2_songs.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(j_data.get('result')))

#Пример запроса списка альбомов автора по его id:
artist_id = '96be03d28450c29e7178ccb6c0c2e5dedd65f778'
url = f'https://orion.apiseeds.com/api/music/artist/{artist_id}/?apikey={API_KEY}'
data = requests.get(url)

if data.status_code == 200:
    j_data = data.json()
    if j_data.get('success') == True:
        albums = j_data.get('artist')['albums']
        #print(j_data)
        for item in albums:
            print('album title: ', item['title'])

        with open(os.path.abspath('lesson1_2_albums.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(albums))

#Пример запроса инфы альбома по его id:
album_id = '5cfcd0edba7d19ca6f362a91'
url = f'https://orion.apiseeds.com/api/music/album/{album_id}/?apikey={API_KEY}'
data = requests.get(url)

if data.status_code == 200:
    j_data = data.json()
    if j_data.get('success') == True:
        album_data = j_data.get('album')
        print(album_data)

        with open(os.path.abspath('lesson1_2_album_data.json'), 'a', encoding='utf-8') as f:
            f.write(json.dumps(album_data))