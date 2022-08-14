'''
This is the main app file
'''
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import config 

# Instanciating flass app
app = Flask(__name__)

# Adding secret key to app configuration
app.config['SECRET_KEY'] = config.SECRET_KEY

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
    # Creating from based on imported RegistrationForm
    form = RegistrationForm()
    if form.validate_on_submit():
        # if valid registration then flash a success message
        # get_flashed_messages(with_categories=true) used in html
        flash(f'Account created for {form.username.data}!', category='success')
        # and redirect to home page
        return redirect(url_for('home'))
    # if not valid then stay on registration page 
    return render_template('register.html', title='Register', form=form)

# Login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Creating from based on imported LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        # if valid entries then check for authorised access
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            # here dummy authorisation implemented (later a database will be used)
            # if authorized then flash success
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            # if not authorized then flash danger and check credentials msg
            flash('Login unsuccessful, Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# This is used to run the app by: python filename.py
if __name__ == '__main__' :
    # App runs on default addressa and port in debug mode
    # Debug mode supports hot loading
    app.run(debug=True)