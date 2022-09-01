from flask import(Blueprint, render_template, url_for,
                    flash, redirect, request)
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email                                    

users = Blueprint('users', __name__)

# Register route
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login'))
    # if not valid then stay on registration page 
    return render_template('register.html', title='Register', form=form)

# Login route
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Creating form based on imported LoginForm
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
                return redirect(url_for('main.home'))
        else:
            #if not authorized then flash danger and check credentials msg
            flash('Login unsuccessful, Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                            title='Account',
                            image_file=image_file,
                            form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    # Renders the home.html template with passing "posts"
    return render_template('user_posts.html', posts=posts, user=user) 

@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An reset email has been sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an expired or invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # if valid registration then flash a success message
        # get_flashed_messages(with_categories=true) used in html
        hached_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hached_password
        db.session.commit()
        flash('Your password has been update', category='success')
        # and redirect to home page
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
    