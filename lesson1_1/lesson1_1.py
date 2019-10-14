"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import requests
import os

nickname = 'irustam'
repos = 1000
page = 1
while True:
    url = f'https://api.github.com/users/{nickname}/repos?per_page={repos}&page={page}'

    data = requests.get(url)
    count = 0
    if data.status_code == 200:
        j_data = data.json()
        for item in j_data:
            print(item['id'], item['full_name'])
            count += 1
        with open(os.path.abspath('lesson1_1.json'), 'a', encoding='utf-8') as f:
            f.write(data.text)

    if count < repos:
        break
    else:
        page += 1