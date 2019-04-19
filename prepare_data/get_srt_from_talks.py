import requests
from bs4 import BeautifulSoup
import os
import shutil

folder = 'data'


def create_folder(path):
    path = os.path.join(path)
    if not os.path.exists(path):
        os.mkdir(path)

def write_paragraphs_to_file(paragraphs, path):
    with open(path, 'w', encoding="utf-8") as f:
        for p in paragraphs:
            # p_encoded = p.encode("utf-8")
            pp = p.replace('\t', '')
            f.write(f'{pp}\n')
        
def get_subtitle_from_talk(talk, lang):
    talk_url = f'https://www.ted.com/talks/{talk}/transcript?language={lang}'
    while True:
        page = requests.get(talk_url).text
        soup = BeautifulSoup(page, features="html.parser")

        if soup.find('div', {'class': 'Notice'}):
            return False

        paragraphs = [h.find('p').text for h in soup.find_all('div', {'class':'Grid__cell flx-s:1 p-r:4'})]
        if len(paragraphs) != 0:
            create_folder(os.path.join(folder, talk))
            write_paragraphs_to_file(paragraphs, os.path.join(folder, talk, lang))
            return True

def check_if_all_subs_available(talk):
    path = os.path.join(folder, talk)
    if os.path.exists(path) and len(os.listdir(path)) < len(langs):
        shutil.rmtree(path)


langs = ['fa', 'en']
collected = os.listdir(folder)
start_from_line = 3233
with open('talks.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[start_from_line:]):
        if not line.startswith('/talks/'):
            continue
        talk = line[7:].strip()
        if talk in collected:
            print(talk)
            continue        
        print(f'line : {i}')
        for lang in langs:
            success = get_subtitle_from_talk(talk, lang)
            if not success:
                check_if_all_subs_available(talk)
                break