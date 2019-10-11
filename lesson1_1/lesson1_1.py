"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import requests
import os

nickname = 'irustam'
url = f'https://api.github.com/users/{nickname}/repos'

data = requests.get(url)

if data.status_code == 200:
    j_data = data.json()
    for item in j_data:
        print(item['id'], item['full_name'])

    with open(os.path.abspath('lesson1_1.json'), 'w', encoding='utf-8') as f:
        f.write(data.text)