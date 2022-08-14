'''
This file binds the app together and create the packaging
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskblog import config

# Instanciating flask app
app = Flask(__name__)
# Adding secret key to app configuration
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
# Creating database
db = SQLAlchemy(app)

# this import is placed here to avoid circular imports
# routes uses app and app uses routes
from flaskblog import routes