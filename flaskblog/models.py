from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedSerializer

# This function is used to manage user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Creating User models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = TimedSerializer(app.config['SECRET_KEY'],'confirmation')
        return s.dumps(self.id)

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = TimedSerializer(app.config['SECRET_KEY'],'confirmation')
        try:
            user_id = s.loads(token, max_age=max_age)
        except:
            return None
        return User.query.get(user_id)

    #This is the representation of a User 
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Creating Post models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(20), nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # This is the representation of a post
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
