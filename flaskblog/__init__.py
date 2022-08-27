'''
This file binds the app together and create the packaging
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from mailjet_rest import Client

# Instanciating flask app
app = Flask(__name__)
# Adding secret key to app configuration
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI

# Creating database
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mailjet = Client(auth=(config.MAIL_API_KEY, config.MAIL_API_SECRET), version='v3.1')



# this import is placed here to avoid circular imports
# routes uses app and app uses routes
from flaskblog import routes