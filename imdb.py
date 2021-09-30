from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import timedelta
from lxml import etree

def scraping():
    base_url = 'https://www.imdb.com/'

    page = requests.get('https://www.imdb.com/list/ls009668711/')
    soup = BeautifulSoup(page.content, 'html.parser')

    df = pd.DataFrame(columns=["movie_name","description","director_name","rating","genre_list","stars_actors_list"\
        ,"user_reviews","critic_reviews","metascore","country_release_date","release_date","duration","filming_dates_initial","filming_dates_final"])

    film_titles = soup.find_all('h3', class_="lister-item-header")

    for film in film_titles:

        link_detail = film.find('a')
        id_film = link_detail.get('href')
        info_of_film = getting_info(base_url,id_film)
        df2 = pd.DataFrame.from_dict(info_of_film)
        df = df.append(df2, ignore_index=True)
        print(info_of_film['movie_name'])
    df.to_csv(path_or_buf='imdb_database.csv', sep=';',header=True)


def getting_info(base_url,link):

    #TODO: pay attention to null values

    # PRINCIPAL PAGE
    page = requests.get(base_url+link)
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))

    movie_name = dom.xpath('//h1')[0].text
    description = dom.xpath('//div/p/span[@data-testid="plot-xl"]')[0].text
    director_name = dom.xpath('//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt"]/li[1]//a')[0].text
    rating = dom.xpath('//span[@class="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"]')[0].text
    genre_list = []
    genre = dom.xpath('//div[@class="ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL"]//a/span')
    for i in genre:
        genre_list.append(i.text)

    stars_actors_list = []
    stars_actors = dom.xpath('//a[@data-testid="title-cast-item__actor"]')
    for j in stars_actors:
        stars_actors_list.append(j.text)

    user_reviews = dom.xpath('//span[@class="score"]')[0].text
    critic_reviews = dom.xpath('//span[@class="score"]')[1].text
    metascore = dom.xpath('//span[@class="score-meta"]')[0].text


    #RELEASE INFO
    releaseday_page = requests.get(base_url+link+'releaseinfo?ref_=tt_dt_rdat')
    releaseday_soup = BeautifulSoup(releaseday_page.content, 'html.parser')
    releaseday_dom = etree.HTML(str(releaseday_soup))
    country_release_date = releaseday_dom.xpath('//tr/td[@class="release-date-item__country-name"]/a')[0].text
    release_date = releaseday_dom.xpath('//tr/td[@class="release-date-item__date"]')[0].text

    #TECHNICAL INFO
    technical_page = requests.get(base_url + link + 'technical?ref_ = tt_spec_sm')
    technical_soup = BeautifulSoup(technical_page.content, 'html.parser')
    technical_dom = etree.HTML(str(technical_soup))
    duration = technical_dom.xpath('//tr[1]/td[2]')[0].text.split('(')[1].split(' ')[0]

    # FILMING_DATES
    try:
        filming_dates_page = requests.get(base_url + link + 'locations?ref_=tt_dt_loc')
        filming_dates_soup = BeautifulSoup(filming_dates_page.content, 'html.parser')
        filming_dates_dom = etree.HTML(str(filming_dates_soup))
        filming_dates = filming_dates_dom.xpath('//section[@id="filming_dates"]//li')[0].text.strip()
        filming_dates_initial = filming_dates.split(" - ")[0]
        filming_dates_final = filming_dates.split(" - ")[1]
    except:
        filming_dates_initial = None
        filming_dates_final = None

    to_append = {"movie_name":[movie_name],"description":[description],"director_name":[director_name],"rating":[rating],"genre_list":[genre_list],\
                 "stars_actors_list":[stars_actors_list],"user_reviews":[user_reviews],"critic_reviews":[critic_reviews],"metascore":[metascore],\
                 "country_release_date":[country_release_date],"release_date":[release_date],"duration":[duration],"filming_dates_initial":[filming_dates_initial]\
                ,"filming_dates_final":[filming_dates_final]}
    return to_append

def analysis(data):
    print('jakjai')

if __name__ == "__main__":
    try:
        data = pd.read_csv('imdb_database.csv')
    except:
        scraping()
        data = pd.read_csv('imdb_database.csv')
    analysis(data)
