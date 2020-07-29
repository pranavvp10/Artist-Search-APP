from app.models import User,FavArtist
from app import db,bcrypt
from flask import Flask, render_template, url_for, flash, redirect,request,Blueprint
from app.users.forms import RegistrationForm, LoginForm
import  app.dta as sp
import spotipy
from flask_login import login_user,current_user,logout_user,login_required
from app import cache

users = Blueprint('users', __name__)




@users.route("/register", methods=['GET', 'POST'])
@cache.cached()
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hash_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!,now login', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
@cache.cached()
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
@cache.cached()
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account")
@login_required
@cache.cached()
def account():
    return render_template('account.html', title='Account')

@users.route("/artist")
@cache.cached()
def fav_artist():
    usr = current_user
    fav = usr.favartist
    return render_template('artist.html', title='Artist',fav=fav)

@users.route("/artist/<a_name>")
@cache.cached()
def artist_info(a_name):
    artist=FavArtist.query.get_or_404(a_name)
    tt=sp.top_tracks(a_name)
    return render_template('ainfo.html',title=artist.name,artist=artist,tt=tt)

@users.route("/artist/<a_name>/delete",methods=['POST'])
@cache.cached()
def del_art(a_name):
    artist=FavArtist.query.get_or_404(a_name)
    db.session.delete(artist)
    db.session.commit()
    return redirect(url_for('main.home'))