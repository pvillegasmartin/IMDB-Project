from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import timedelta


def main():
    base_url = 'https://www.imdb.com/'

    page = requests.get('https://www.imdb.com/list/ls009668711/')
    soup = BeautifulSoup(page.content, 'html.parser')

    film_titles = soup.find_all('h3', class_="lister-item-header")
    for film in film_titles:
        link_detail = film.find('a')
        getting_info(base_url+link_detail.get('href'))

def getting_info(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')


if __name__ == "__main__":
    main()

