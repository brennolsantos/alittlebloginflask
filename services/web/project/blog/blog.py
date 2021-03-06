import json
from flask import request, jsonify, Blueprint, abort, session, make_response
from project.app import db
from project.blog.models import User, Post, Comment, Category
from flask_login import login_required, current_user

blog = Blueprint('blog', __name__)

# TODO
## Post and comment system 


@blog.route("/", methods=['GET'])
def last_posts():
    posts = Post.query.order_by(Post.id).all()
    
    response = {}
    
    if not posts:
        response = {
            'Empty': True
        }

        return make_response(jsonify(response), 204)

    for p in posts:
        r = {
            'user': p.user,
            'category': p.category,
            'title': p.title,
            'text': p.text
        }

        response[p.id] = r


    return make_response(jsonify(response), 200)



@blog.route('/addcategory', methods=['POST', 'GET'])
@login_required 
def add_category():
    if request.method == 'POST':
        name = request.form['name']

        if Category.query.filter_by(name = name).first():
            return make_response("Error", 400)

        cat = Category(name = name)
        db.session.add(cat)
        db.session.commit()

        res = {
            'id': cat.id,
            'name': cat.name
        }
       
        return make_response(jsonify(res), 201)

    elif request.method == 'GET':
        name = request.form['name']

        cat = Category.query.filter_by(name = name).first()

        if not cat:
            res = {
                'status': 'Category does not exist'
            }
            return make_response(jsonify(res), 400)

        res = {
            'id': cat.id,
            'name': cat.name
        }

        return make_response(jsonify(res), 200)


@blog.route('/pcategory', methods=['POST'])
@login_required 
def post_category():
    cat = request.form['category']

    posts = Post.query.filter_by(category = cat).all()
    response = {}

    if not posts:
        response = {
            'Empty': True
        }

        return make_response(jsonify(response), 204)

    for p in posts:
        r = {
            'user': p.user,
            'category': p.category,
            'title': p.title,
            'text': p.text
        }

        response[p.id] = r 

    return make_response(jsonify(response), 200)

@blog.route('/profile', methods=['POST'])
def profile():
    id = request.form['id']

    user = User.query.get(id)

    if not user:
        res = {
            'status': 'User does not exist'
        }

        return make_response(jsonify(res), 400)

    res = {
        'name': user.name,
        'email': user.email
    }

    return make_response(jsonify(res), 200)


@blog.route('/post', methods=['GET', 'POST'])
@login_required
def view_post():
    if request.method == 'POST':
        user = request.form['user']
        title =  request.form.get('title')
        text = request.form.get('text')
        category = request.form['category']

        post = Post(user = user, category = category, title = title, text = text)
        db.session.add(post)
        db.session.commit()

        res = {
            'status': 'Post created',
            'id': post.id
        }

        return make_response(jsonify(res), 201)

    elif request.method == 'GET':
        id = request.form['id']
        post = Post.query.get(id)

        if not post:
            res = {
                'status': 'Post doesn\'t exist'
            }

            return make_response(jsonify(res), 400)

        res = {
            'id': post.id,
            'user': post.user,
            'category': post.category,
            'title': post.title,
            'text': post.text
        }
        
        return make_response(jsonify(res), 200)



@blog.route('/comment', methods=['POST'])
@login_required
def make_comment():
    post_id = request.form['post']

    post = Post.query.get(post_id)

    if not post:
        res = {
            'status': 'Post doesn\'t exist'
        }

        return make_response(jsonify(res), 400)

    user = request.form['user']
    text = request.form.get('text')

    com = Comment(author=user, post = post.id, text = text)
    db.session.add(com)
    db.session.commit()

    res = {
        'id': com.id,
        'author': com.author,
        'post': com.post,
        'text': com.text
    }

    return make_response(jsonify(res), 201)



@blog.route('/getcomment', methods=['POST'])
@login_required
def get_comment():
    id = request.form['id']

    com = Comment.query.get(id)
    if not com:
        res = {
            'status': 'Comment does not exist'
        } 

        return make_response(jsonify(res), 400)

    res = {
        'id': com.id,
        'author': com.author,
        'post': com.post,
        'text': com.text
    }

    return make_response(jsonify(res), 200)





@blog.route('/postcomments', methods=['POST'])
@login_required
def post_comments():
    id = request.form['id']

    coms = Comment.query.filter_by(post = id).all()

    res = {}

    for c in coms:
        res[c.id] = {
            'author': c.author,
            'text': c.text
        }

    return make_response(jsonify(res), 200)


    

    

