from flask import render_template, Blueprint, request, current_app, redirect, url_for,flash
import os
from movie_reviews.models import Movie, Review
from movie_reviews import db
from flask_login import current_user, login_required
from functools import wraps
import tensorflow as tf
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences

print('movies')

KAFKA_PUBLISH = False

if KAFKA_PUBLISH:
    from movie_reviews.movies.kafka_publish import get_producer,publish
    producer = get_producer()

f = open('./movie_reviews/aimodel/tokenizer.json')
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(json.load(f))
f.close()

vocab_size = 10000
max_length = 120
embedding_dim = 16
trunc_type='post'
oov_tok = "<OOV>"

# Build the model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Setup the training parameters
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.load_weights('./movie_reviews/aimodel/modelcheckpoint/my_checkpoint')

movies = Blueprint('movies',__name__)


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def check_(*a,**k):
            if current_user is not None and current_user.is_admin:
                return fn(*a,**k)

            else:
                print("No Admin privileges")
                return redirect(url_for('main.home'))
    
        return check_
    return wrapper


@movies.route('/movie/new', methods=['GET','POST'])
@login_required
@admin_required()
def add_movie():
    if request.method=='POST':
        print('POST')
        print(request.form['title'])
        movie = Movie(title=request.form['title'], year=request.form['year'], description=request.form['description'])
        if request.files['poster']:
            poster = request.files['poster']
            poster.save(os.path.join(current_app.root_path,'static/posters/', poster.filename))
            movie.image = poster.filename
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('add_movie.html', title='Add movie', legend='Add Movie')

@movies.route('/movie/<int:movie_id>/', methods=['GET','POST'])
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method=='POST':
        if current_user is not None:
            review = request.form['comment']
            test_seq = [review]
            test_seq = tokenizer.texts_to_sequences(test_seq)
            test_padded = pad_sequences(test_seq,maxlen=max_length, truncating=trunc_type)
            result = model.predict(test_padded)
            label= 'positive' if result[0][0]>=0.5 else 'negative'
            review = Review(content=review,label=label,movie=movie,review_score=result[0][0],author=current_user)
            movie.review_count+=1
            if review.review_score>=0.5:
                movie.positive_count+=1
            movie.rating = round(movie.positive_count/movie.review_count,2)
            db.session.add(review)
            db.session.add(movie)
            db.session.commit()
            if KAFKA_PUBLISH:
                publish(producer,movie,review,result[0][0])
            print(result)
        else:
            flash('User needs to login to add review', 'danger')
    reviews = Review.query.filter_by(movie=movie).order_by(Review.added_date.desc())
    return render_template('movie.html',movie=movie,title=movie.title,reviews=reviews)

@movies.route('/review/<int:review_id>/delete')
@login_required
def delete_review(review_id):
    print(review_id)
    review = Review.query.get_or_404(review_id)
    if review.author!=current_user:
        flash("User doesn't have permission to delete the review!", 'danger')
        return redirect(url_for('main.home'))
    
    movie = review.movie
    if review.label=='positive':
        movie.positive_count-=1
    movie.review_count-=1
    if movie.review_count!=0:
        movie.rating = round(movie.positive_count/movie.review_count,2)
    else:
        movie.rating = 0
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('movies.movie', movie_id=movie.id))

