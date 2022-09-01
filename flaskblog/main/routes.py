from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)

# Home route definition and method to be called
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    # Renders the home.html template with passing "posts"
    return render_template('home.html', posts=posts) 

# About route definition and method to be called
@main.route("/about")
def about():
    # Renders the about.html template with passing a "title"
    return render_template('about.html',title = 'About')
