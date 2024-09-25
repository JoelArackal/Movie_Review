from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from movie_reviews.config import Config 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from movie_reviews.main.routes import main
    from movie_reviews.users.routes import users
    from movie_reviews.movies.routes import movies

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(movies)

    return app