def create_classes(db):
    class movies_filtered_data(db.Model):
        __tablename__ = 'movies_filtered_data'

        id = db.Column(db.Integer, primary_key=True)
        movieId = db.Column(db.Integer)
        title = db.Column(db.String(64))
        genres = db.Column(db.String(64))
        posters = db.Column(db.String(64))
        trailers = db.Column(db.String(64))
        ratings = db.Column(db.String(64))
        synopsis = db.Column(db.String(64))
        
        def __repr__(self):
            return '<movies_filtered_data %r>' % (self.movieId)
    class ratings(db.Model):
        __tablename__ = 'ratings'

        id = db.Column(db.Integer, primary_key=True)
        userId = db.Column(db.Integer)
        movieId = db.Column(db.Integer)
        rating = db.Column(db.Float)
        #userId = db.Column(db.String(64))
        #movieId = db.Column(db.String(64))
        #ratings = db.Column(db.String(64))
        timestamp = db.Column(db.Integer)
        
        def __repr__(self):
            return '<ratings %r>' % (self.movieId)
    return (movies_filtered_data,ratings)
