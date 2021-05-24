from flask_sqlalchemy import SQLAlchemy
from models import create_classes
from flask import Flask, render_template
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
import json
import os



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///movies_db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

movies_filtered_data, ratings_data = create_classes(db)

movies_full_n = db.session.query(movies_filtered_data.movieId,movies_filtered_data.title,movies_filtered_data.genres,
                                 movies_filtered_data.posters,movies_filtered_data.trailers,movies_filtered_data.ratings,
                                 movies_filtered_data.synopsis).all()
movies_full_n = pd.DataFrame(movies_full_n)
movies_full_n.columns = ['movieId','title', 'genres', 'posters', 'trailers', 'ratings','synopsis']

ratings_n = db.session.query(ratings_data.userId,ratings_data.movieId,ratings_data.rating,ratings_data.timestamp).all()
ratings_n = pd.DataFrame(ratings_n)
ratings_n.columns = ['userId', 'movieId', 'rating', 'timestamp']

#ratings = pd.read_csv("resources/ratings.csv")
#movies_full = pd.read_csv("resources/movies_filtered_data.csv")

ratings = ratings_n
movies_full = movies_full_n

#movies_full.replace(NaN,'NA')

final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')

final_dataset.fillna(0,inplace=True)

no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index,:]

final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > 50].index]


csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)



def recommendation_list(movie_idx):
    n_movies_to_reccomend = 5
    movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
    distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
    rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),\
                           key=lambda x: x[1])[:0:-1]
    recommend_frame = []
    for val in rec_movie_indices:
        movie_idx = final_dataset.iloc[val[0]]['movieId']
        idx = movies_full[movies_full['movieId'] == movie_idx].index
        recommend_frame.append({'Title':movies_full.iloc[idx]['title'].values[0],'Distance':val[1]})
    df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
    return df

@app.route("/")
def home():
    return render_template("index.html")#, vacation=restaurants_data)

@app.route("/movies")
def movies():

    return render_template("movies.html")

@app.route("/detail")
def detail():

    return render_template("detail.html")

@app.route("/objective")
def objective():

    return render_template("detail.html")

@app.route("/solution")
def solution():

    return render_template("detail.html")

@app.route("/output")
def output():

    return render_template("detail.html")


@app.route("/recommend_movies/<name>")
def recommend_movies(name):
    #name = name.title()
    print(name)
    data = []
    data_dict = {}
    movie_data = movies_full[movies_full['title'].str.contains(name)]
    if not len(movie_data):
        name = name.title()
        movie_data = movies_full[movies_full['title'].str.contains(name)]
    if len(movie_data):
        movie_data = movie_data.iloc[0]
        dt = {'name':movie_data['title'],'poster':movie_data['posters'],'trailer':movie_data['trailers'],
              'rating':movie_data['ratings'],'synopsis':movie_data['synopsis']}
        data.append({'name':movie_data['title'],'poster':movie_data['posters'],'trailer':movie_data['trailers'],
                     'rating':movie_data['ratings'],'synopsis':movie_data['synopsis']})
        
        recommended = recommendation_list(movie_data['movieId'])['Title']
        
        recommended_movies = {}
        recommended_movies = []
        for name in recommended:
            name = name.split('(')[0]
            rec_movie_data = movies_full[movies_full['title'].str.contains(name)]
            if len(rec_movie_data):
                rec_movie = rec_movie_data.iloc[0]
                #print(rec_movie['posters'])
                if rec_movie['posters'] is not np.nan:
                    #recommended_movies[name] = rec_movie['posters']
                    #dt[name] = rec_movie['posters']
                    recommended_movies.append({'name':name,'poster':rec_movie['posters']})
                    #recommended_movies[name]={'name':name,'poster':rec_movie['posters']}
                else:
                    recommended_movies.append({'name':name,'poster':None})
                    #recommended_movies[name]={'name':name,'poster':None}
            else:
                a=0
                #recommended_movies[name] = 'a'
        #data.append(recommended_movies)
        data.append(recommended_movies)
        #data.append(data_dict)
    else:
        a=0
        data.append(None)
    #data.append(dt)
    print(data)
    data = json.dumps(data)
    #data1 = json.dumps(recommended_movies)
    print(data)
    return data#,data1
if __name__ == "__main__":
    app.run(debug=True)
    
######## Output Format
###     output_fromat = [{'movie_data':{'movie_name':name,'poster':poster_url_img,'trailer':url_to_trailer_webpage,'ratings':floating_number_out_of_10,'synopsis':a_short_paragraph_with_endline_at_start_and_end},'recommended_movies':{'movie1':poster_url_img,'movie2':poster_url_img,'movie3':poster_url_img,'movie4':poster_url_img,'movie5':poster_url_img}}]
