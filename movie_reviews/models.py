from datetime import datetime
from movie_reviews import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review',backref='author', lazy=True,cascade="all, delete-orphan")

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(30), nullable=False, default='default.jpg')
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True, default='')
    reviews = db.relationship('Review',backref='movie', lazy=True,cascade="all, delete-orphan")
    review_count = db.Column(db.Integer,nullable=True,default=0)
    positive_count = db.Column(db.Integer,nullable=True,default=0)
    rating = db.Column(db.Float,nullable=True,default=0)


    def __repr__(self):
        return str(self.title)
    
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False, default='')
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    label = db.Column(db.String(100), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    review_score = db.Column(db.Float, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"{self.content[:20]}"
    
    

'''
app.app_context().push()
db.create_all()
'''



'''
Spider-Man: Across the Spider-Verse is a remarkable cinematic masterpiece that pushes the boundaries of animation and storytelling.
 With its breathtaking art style and profound ability to depict emotions, this film weaves a web of brilliance that captivates audiences from start to finish. One of the most striking aspects of this movie is its unparalleled artistry.
 The visual style combines vibrant colors, dynamic animation techniques, and a diverse range of art
 '''

'''
Personally I felt this movie was a major step down from everything the first one did well while desperately trying to to rehit the same story beats to make you remember the actual complete film that you like, but I'm getting ahead of my self. The first problem I want 
to address is the real lack of character work for anyone not named Gwen; Miles, Peter, Miguel
'''

'''
Spider-Man: Across the Spider-Verse is an absolute game-changer in the world of animation and superhero storytelling. 
From start to finish, it takes audiences on an electrifying, emotionally charged journey that redefines what we thought was possible in the realm of comic book adaptations. This film is a masterpiece that effortlessly weaves together innovation, nostalgia, and heart. 
One of the standout elements of the film is its animation style.
'''