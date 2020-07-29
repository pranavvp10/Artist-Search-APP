from flask import render_template, request, Blueprint,Flask
from datetime import date
import app.dta as sp
from app import cache

main = Blueprint('main', __name__)




@main.route("/")
@main.route("/home")
@cache.cached()
def home():
    dt=date.today()
    a=sp.nr()
    name=[i for i in a]
    return render_template('home.html',name=name,dt=dt)

@main.route("/about")
@cache.cached()
def about():
    return render_template('about.html', title='About')   