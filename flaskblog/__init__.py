from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config

# Instanciating flass app
app = Flask(__name__)
# Adding secret key to app configuration
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
# Creating database
db = SQLAlchemy(app)

from flaskblog import routes