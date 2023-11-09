import requests
import random
import os
import math
import re
from pprint import pprint
import subprocess

dirpath = '/Users/jiyuan.zheng/Desktop/wallpapers'


def get_picture_list():
    endpoint = "https://wallhaven.cc/api/v1/search"
    random_page = round(random.random() * 100 + 1)
    rsp = requests.get(endpoint, params={
        "q": 'anime',
        "categories": '010',
        "purity": "100",
        "sorting": "relevance",
        "order": "desc",
        "ai_art_filter": "1",
        "page": random_page
    })
    data = rsp.json()['data']
    l = [x['path'] for x in data if x['file_size'] > 4650000]
    return l


def get_random_picture():
    picture_names = [x for x in os.listdir(dirpath)]
    picture_names = [x for x in picture_names if x.endswith(
        '.png') or x.endswith('.jpg')]
    paths = [os.path.join(dirpath, x) for x in picture_names]
    random_path = random.choice(paths)
    return random_path


def save_picture(picture_url):
    resp = requests.get(picture_url, stream=True)
    picture_name = os.path.basename(picture_url)
    picture_path = os.path.join(dirpath, picture_name)
    if resp.status_code == 200:
        with open(picture_path, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)


def execute_script(picture_path):
    script = f'''
    tell application "System Events"
        tell every desktop
            set picture to "{picture_path}"
        end tell
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True)
    return result.stdout


def main():
    # download random picture
    try:
        l = get_picture_list()
        picture_url = random.choice(l)
        save_picture(picture_url)
    except Exception:
        # no network
        print('Fail to download picture')
        pass

    random_picture_path = get_random_picture()
    execute_script(random_picture_path)


main()
