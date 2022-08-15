from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


# Creating dummy posts to be replaced by database requests later
posts = [
    {
        'author': 'Georges Amine',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'August 13 2022'
    },
    {
        'author': 'Georges Amine',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'August 14 2022'
    }
]

# Home route definition and method to be called
@app.route("/")
@app.route("/home")
def home():
    # Renders the home.html template with passing "posts"
    return render_template('home.html', posts=posts) 

# About route definition and method to be called
@app.route("/about")
def about():
    # Renders the about.html template with passing a "title"
    return render_template('about.html',title = 'About')

# Register route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Creating from based on imported RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        # if valid registration then flash a success message
        # get_flashed_messages(with_categories=true) used in html
        hached_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hached_password )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can login now', category='success')
        # and redirect to home page
        return redirect(url_for('login'))
    # if not valid then stay on registration page 
    return render_template('register.html', title='Register', form=form)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Creating from based on imported LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        # if valid entries then check for authorised access
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            #if not authorized then flash danger and check credentials msg
            flash('Login unsuccessful, Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')     