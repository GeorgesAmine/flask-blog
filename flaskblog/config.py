
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_API_KEY = os.environ.get('MAIL_API_KEY')
    MAIL_API_SECRET = os.environ.get('MAIL_API_SECRET')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
