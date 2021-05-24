import os
from models import create_classes
from sqlalchemy import create_engine, Table, Column, Float, Integer, String, MetaData

import pandas as pd

ratings = pd.read_csv("resources/ratings.csv")
movies_full = pd.read_csv("resources/movies_filtered_data.csv")


meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///movies_db.sqlite"

print("connection to databse")
engine = create_engine(connection)

#if not engine.has_table("movies_filtered_data"):
if True:
    print("Creating Table")

    table1 = Table(
        'movies_filtered_data', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('movieId', Integer),
        Column('title', String),
        Column('genres',String),
        Column('posters', String),
        Column('trailers', String),
        Column('ratings', String),
        Column('synopsis', String)
    )

    meta.create_all(engine)
    
    print("Table created")
    seed_data1 = []
    for row in movies_full.iterrows():
        seed_data1.append(dict(row[1].iloc[2:]))
    with engine.connect() as conn:
        conn.execute(table1.insert(), seed_data1)

    print("Movies Data Imported")
else:
    print("Table already exists")




#if not engine.has_table("ratings"):
if True:
    print("Creating Table")

    table2 = Table(
        'ratings', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('userId', Integer),
        Column('movieId', Integer),
        Column('rating', Float),
        Column('timestamp', Integer)
    )

    meta.create_all(engine)
    
    print("Table created")
    seed_data2 = []
    for row in ratings.iterrows():
        seed_data2.append(dict(row[1]))
    with engine.connect() as conn:
        conn.execute(table2.insert(), seed_data2)

    print("Ratings Data Imported")
else:
    print("Table already exists")
print("Database Generation complete")
