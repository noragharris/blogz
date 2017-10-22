from app import db

class Blog_Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    blogs = db.relationship('Blog_Post', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # TODO insert dunder repr here