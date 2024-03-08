# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

# stdlib
import os
from datetime import datetime

# local
from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.model import MovieClient

# don't change the name
app = Flask(__name__)

# TODO: you should fill out these with the appropriate values
app.config['MONGO_URI'] = 'mongodb+srv://aakashpatel0377:mongoDBAakashMM@cluster0.tuubvqi.mongodb.net/cmsc388j_db?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = 'secretkey3333'
OMDB_API_KEY = 'def9a8ce' 

# DO NOT REMOVE OR MODIFY THESE 4 LINES (required for autograder to work)
if os.getenv('MONGO_URI'):
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
if os.getenv('OMDB_API_KEY'):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# don't change the name
mongo = PyMongo(app)
# don't change the name 
movie_client = MovieClient(OMDB_API_KEY)

# --- Do not modify this function ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))

    return render_template('index.html', form=form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    movie_list = []
    error_msg = None
    try:
        movie_list = movie_client.search(query) # This is the list of movie object pertaining to the movie we searched
    except ValueError as e:      
        error_msg = e
    return render_template('query_results.html', results = movie_list, error_msg = error_msg)

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = None
    form = None
    reviews = []
    error_msg = None
    review = {}
    try:
        movie = movie_client.retrieve_movie_by_id(movie_id)
        form = MovieReviewForm()
        if request.method == 'POST' and form.validate_on_submit():
            review = {
                'imdb_id': movie_id,
                'commenter': form.name.data,
                'content': form.text.data,
                'date': current_time()
            }
        mongo.db.reviews.insert_one(review)
        reviews = list(mongo.db.reviews.find({'imdb_id': movie_id}))
    except ValueError as e:
        error_msg = e

    return render_template('movie_detail.html', reviews=reviews, error_msg = error_msg, form=form, movie = movie)

# Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

