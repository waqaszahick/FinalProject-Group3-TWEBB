from bs4 import BeautifulSoup
import requests

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import sys

movies = pd.read_csv("resources/movies_filtered.csv")
ratings = pd.read_csv("resources/ratings.csv")


base = 'https://www.imdb.com'
movie_base_url = 'https://www.imdb.com/find?q={}&ref_=nv_sr_sm'

movies_lst = movies['title']
#movies_lst.shape

posters = []
trailers = []
ratings = []
synopsis = []

for name in movies_lst:
    try:
        url_name = name.replace(' ','+')
        url1 = movie_base_url.format(url_name)
        page1 = requests.get(url1)
        soup1 = BeautifulSoup(page1.text, 'html.parser')
        target_movies = soup1.findAll('tr',attrs={'class':'findResult odd'})
        if len(target_movies):
            movie_url = target_movies[0].findAll('td',attrs={'class':'result_text'})[0].findAll('a')[0]['href']
            url2 = base+movie_url
            page2 = requests.get(url2)
            soup2 = BeautifulSoup(page2.text, 'html.parser')
            try:
                movie_poster = soup2.findAll('div',attrs={'class':'poster'})[0].img['src']
                posters.append(movie_poster)
            except:
                posters.append(None)
            try:
                movie_rating = soup2.findAll('div',attrs={'class':'ratingValue'})[0].span.text
                ratings.append(movie_rating)
            except:
                ratings.append(None)
            try:
                movie_synopsis = soup2.findAll('div',attrs={'class':'plot_summary'})[0].findAll('div',attrs = {'class':'summary_text'})[0].text
                synopsis.append(movie_synopsis)
            except:
                synopsis.append(None)
            try:
                movie_trailer = base+soup2.findAll('div',attrs={'class':'videoPreview__videoContainer'})[0].a['href']
                trailers.append(movie_trailer)
            except:
                trailers.append(None)
            #print(movie_poster,movie_rating,movie_synopsis,movie_trailer)
            print('Done: {}'.format(name))
        else:
            print('Movie {} not found!!'.format(name))
            posters.append(None)
            ratings.append(None)
            synopsis.append(None)
            trailers.append(None)
    except:
        print('A problem occure at movie: {}'.format(name))
        posters.append(None)
        ratings.append(None)
        synopsis.append(None)
        trailers.append(None)
    #break

movies['posters'] = posters
movies['trailers'] = trailers
movies['ratings'] = ratings
movies['synopsis'] = synopsis

movies.to_csv('resources/movies_filtered_data.csv')
