from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import InputRequired, Length

class SearchForm(FlaskForm):
    search_query = StringField('movie_name', validators=[InputRequired(), Length(min=1, max=30)])
    submit = SubmitField('Submit')

class MovieReviewForm(FlaskForm):
    name = StringField('Name/Alias', validators=[InputRequired(), Length(min=1, max=50)])
    text = TextAreaField('Content of Review', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')