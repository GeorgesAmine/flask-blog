'''
This file binds the app together and create the packaging
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from mailjet_rest import Client

# Instanciating flask app
app = Flask(__name__)
# Adding secret key to app configuration
app.config.from_object(Config)

# Creating database
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mailjet = Client(auth=(Config.MAIL_API_KEY, Config.MAIL_API_SECRET), version='v3.1')



# this import is placed here to avoid circular imports
# routes uses app and app uses routes
from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)