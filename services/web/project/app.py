from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS
from flask_session import Session
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config['SECRET KEY'] = 'My Secret Key'
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['SESSION_PERMANENT']= False 

Session(app)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db = SQLAlchemy(app)

from project.blog.models import User 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from project.blog.blog import blog
app.register_blueprint(blog)

from project.blog.auth import auth 
app.register_blueprint(auth, url_prefix='/auth')
