from bs4 import BeautifulSoup
from core import *

import requests
import time
import urllib.request
import pathlib
import os
import py7zr

def download_data():
    print('''To download data, use:
  - https://archive.org/download/cablegate/cablegate_archive.torrent to download the torrent
  - https://archive.org/download/cablegate/cablegatepdf.zip to download the zip''')

def download_links():
    # get links
    url, files = get_links()
    local_path = str(pathlib.Path(__file__).parent.parent.absolute()).replace('\\', '/')
    data_path = local_path + '/data/cablegate/'
    print(data_path)
    # create folders if not exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    # save data
    index_progression = 0
    print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        urllib.request.urlretrieve(url + file, data_path + file)
        index_progression += 1
        print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)

    # un7z


def get_links():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    url = 'https://wlstorage.net/file/cablegate/'
    # request
    html_search = requests.get(url, headers=headers).text
    soup_search = BeautifulSoup(html_search, features='lxml')

    return url, [e['href'] for e in soup_search.find_all('a')][1:]

def un7z(data_path):
    files = os.listdir(data_path)
    index_progression = 0
    print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for file in files:
        print(file)
        py7zr.SevenZipFile(data_path + '/' + file, mode='r').extractall()
        index_progression += 1
        print_progress_bar(index_progression, len(files), prefix = 'Progress:', suffix = 'Complete', length = 50)
