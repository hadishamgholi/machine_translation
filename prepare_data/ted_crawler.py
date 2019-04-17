from bs4 import BeautifulSoup
import requests
import time
import os
talk_path = os.getcwd() + '\\talks.txt'
failed_path = os.getcwd() + '\\fails.txt'


def get_talks(page_num):
    page = requests.get(f'https://www.ted.com/talks/quick-list?page={page_num}').text
    soup = BeautifulSoup(page, features="html.parser")
    title_list = soup.find_all("span", {'class':"l3"})
    return [title.find('a')['href'] + '\n' for title in title_list]

def write_talks_to_file():
    with open(talk_path, 'w') as talk_file:
        for page_num in range(1, 107):
            print(page_num)
            talks = get_talks(page_num)
            while len(talks) == 0:
                talks = get_talks(page_num)
            talk_file.write(f'page : {page_num}\n')
            talk_file.writelines(talks)
            time.sleep(1)

if not os.path.exists(talk_path):
    write_talks_to_file()
