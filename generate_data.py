
movies_list = [
    {
        "title": 'Leo',
        "year": 2023,
        "image": 'leo.jpg'
    },
    {
        "title": 'MS Dhoni',
        "year": 2016,
        "image": 'ab376112181dcc2e.jpg'
    }
]

users_list = [
    {
        "username":'Joel',
        'email': 'abc@gmail.com',
        'password':'1234',
        'is_admin':True
    },
    {
        "username":'joel98',
        'email': 'abcd@gmail.com',
        'password':'1234',
        'is_admin':True
    },
    {
        "username":'test_user',
        'email': 'test@gmail.com',
        'password':'1234',
        'is_admin':False
    }
]

def generate():
    from movie_reviews import db,bcrypt,create_app
    from movie_reviews.models import User,Movie

    app = create_app()
    app.app_context().push()
    db.create_all()

    for user in users_list:
        pwd = bcrypt.generate_password_hash(user['password']).decode('utf-8')
        user_ = User(username=user['username'],email=user['email'],password=pwd,is_admin=user['is_admin'])
        db.session.add(user_)
    db.session.commit()

    for movie in movies_list:
        movie_ = Movie(**movie)
        db.session.add(movie_)

    db.session.commit()


if __name__=='__main__':
    generate()