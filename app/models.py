from app import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    favartist = db.relationship('FavArtist', backref='artist', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class FavArtist(db.Model):
    id = db.Column(db.Integer)
    name = db.Column(db.String(100),primary_key=True, nullable=False)
    genres = db.Column(db.String(100), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"FavArtist('{self.id}', '{self.name}','{self.genres}','{self.followers}','{self.popularity}')"
