from flask_sqlalchemy import SQLAlchemy
from models import create_classes
import pandas as pd
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

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

#print(len(results))


ratings = pd.read_csv("resources/ratings.csv")
movies_full = pd.read_csv("resources/movies_filtered_data.csv")

print(ratings.head(3))
print('\n\n',ratings_n.head(3))

print(movies_full.head(3))
print('\n\n',movies_full_n.head(3))
