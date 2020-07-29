from flask import render_template, url_for, flash,redirect, request, abort, Blueprint,Flask
from flask_login import current_user, login_required
from app import db
from app.models import User,FavArtist
from app.search.forms import SearchForm
import app.dta as sp
from app import  cache


searchs = Blueprint('search', __name__)



@searchs.route("/search", methods=['GET', 'POST'])
@cache.cached()
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        name = sp.search_artist(form.artist_name.data)['name']
        genres = sp.search_artist(form.artist_name.data)['genres']
        popularity = sp.search_artist(form.artist_name.data)['popularity']
        followers = sp.search_artist(form.artist_name.data)['followers']
        fav_art = FavArtist(name=name, genres=str(genres), followers=followers, popularity=popularity, artist=current_user)
        db.session.add(fav_art)
        db.session.commit()
        #db.drop_all()
        flash('added artist info', 'success')
        return redirect(url_for('search.searchresult', name=name, genres=genres, popularity=popularity, followers=followers))
    return render_template('search.html', form=form)


@searchs.route("/searchresult")
@cache.cached()
def searchresult():
    name = str(request.args.get('name'))
    genres = str(request.args.get('genres'))
    popularity = int(request.args.get('popularity'))
    followers = int(request.args.get('followers'))

    return render_template('searchresult.html', title='search result', **request.args)