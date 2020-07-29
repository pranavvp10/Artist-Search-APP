from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    artist_name=StringField('artist',validators=[DataRequired()])
    search = SubmitField('search')

class AddFav(FlaskForm):
    add=SubmitField('Add')