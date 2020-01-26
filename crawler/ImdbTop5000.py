from urllib.request import urlopen as uReq

import re
from bs4 import BeautifulSoup as soup
import time
import json

movies = {'movies': []}

for i in range(1, 101, 1):
    # https://www.imdb.com/search/title?num_votes=10000,&sort=user_rating,desc&title_type=feature&page=1&ref_=adv_nxt
    #http://www.imdb.com/search/title?year='+str(year)+'&title_type=feature&page=11&ref_=adv_nxt
    #'http://www.imdb.com/search/title?year='+str(year)+'&title_type=feature&page='+str(i)+'&ref_=adv_nxt'
    currentUrl = 'https://www.imdb.com/search/title?num_votes=10000,&sort=user_rating,desc&title_type=feature&page='+str(i)+'&ref_=adv_nxt'
    print('Page Number: '+str(i)+'\n')

    currentClient = uReq(currentUrl)
    curent_raw_html = currentClient.read()
    currentClient.close()

    current_soup = soup(curent_raw_html, "html.parser")
    current_item_container = current_soup.find_all("div", {"class":"lister-item mode-advanced"})

    for current_movie_item in current_item_container:

        movie_model = {'movie': {'title': None, 'year': None, 'genres': []}}

        title = current_movie_item.find("div", {"class":"lister-item-content"}).h3.a
        year = current_movie_item.find("div", {"class":"lister-item-content"}).h3.find("span", {"class":"lister-item-year text-muted unbold"})
        genres = current_movie_item.find("div", {"class":"lister-item-content"}).p.find("span", {"class":"genre"})

        movie_model['movie']['title'] = title.string
        year_string = year.string.strip()
        year_int = re.findall('[1-3][0-9]{3}', year_string)
        movie_model['movie']['year'] = year_int[0]

        if genres is not None:
            genre_list = [x.strip() for x in genres.string.strip().split(',')]
            movie_model['movie']['genres'] = genre_list

        movies['movies'].append(movie_model)

    time.sleep(1)
print(len(movies['movies']))
with open('movie_list_5000.json', 'w') as file:
    # indented_data=json.dumps(movies, indent=2)
    json.dump(movies, file)
print('***********END***********')
