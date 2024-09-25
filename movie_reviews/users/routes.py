from flask import render_template, Blueprint, request, current_app, redirect, url_for,flash
from movie_reviews.models import User
from movie_reviews import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users',__name__)
print('users')

def validate(request):
    valid = True
    user = User.query.filter_by(username=request.form['username']).first()
    if user is not None:
        valid=False
        flash('Username already exists. Registration failed', 'danger')
    user = User.query.filter_by(email=request.form['email']).first()
    if user is not None:
        valid=False
        flash('Email already exists. Registration failed', 'danger')
    password1 = request.form['password1']
    password2=request.form['password2']
    if password1!=password2:
        valid=False
        flash("Passwords don't match",'danger')
    return valid
    


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        if validate(request):
            password_hash = bcrypt.generate_password_hash(request.form['password1']).decode('utf-8')
            user = User(username=request.form['username'],password=password_hash,email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash('User registration successfull', 'success')
            login_user(user)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.home'))
        

    return render_template('register.html', title='Register')


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login')

    
@users.route('/logout')
def logout():
    logout_user()
    next = request.args.get('next')
    return redirect(next) if next else redirect(url_for('main.home'))
    # return redirect(url_for('main.home'))