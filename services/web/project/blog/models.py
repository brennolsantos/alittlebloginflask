from project.app import db
from flask_login import UserMixin

# User model


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(100))
    active = db.Column(db.Boolean(), default=True, nullable=False)



#Post Category 
class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)


# Blog post model
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    text = db.Column(db.Text, nullable=True)



# Commentary in a post
class Comment(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)

