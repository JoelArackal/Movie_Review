from flask import render_template, Blueprint, request, current_app, redirect, url_for
import os
from movie_reviews.models import Movie
from movie_reviews import db

main = Blueprint('main',__name__)
print('main')

data = [{'name': 'Leo', 'rating':8.5},{'name': 'Spiderman', 'rating':9.5}]

@main.route('/')
@main.route('/home')
def home():
    movies = Movie.query.order_by(Movie.rating.desc())
    return render_template('home.html', title='Home', movies=movies)

@main.route('/api')
def api():
    return data