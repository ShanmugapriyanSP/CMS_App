from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from cms import bcrypt, mongo
from cms.models import DB, User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from .utils import save_picture

user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    '''
    Validates the registration details and stores
    the user data into database

    :return: success or error message and redirect to login page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        picture = 'default.jpg'
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        DB.create_user(name=form.username.data, email=form.email.data, hashed_password=hashed_password, image_file=picture)
        flash(f'Account is created for {form.username.data}! You can now login', 'success')
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Register', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Authenticates the user information and redirects to home page

    :return: home page
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = DB.retrieve_user(name=form.username.data)
        if user is not None and bcrypt.check_password_hash(user['password'], form.password.data):
            user_data = User(user)
            login_user(user_data, remember=form.remember.data)
            previous_page = request.args.get('next')
            return redirect(previous_page) if previous_page else redirect(url_for('main.home'))
        else:
            flash("Invalid Username or Password", 'danger')
    return render_template('login.html', title='Login', form=form)


@user.route('/logout')
def logout():
    '''
    Removes the user from session

    '''
    logout_user()
    return redirect(url_for('main.home'))


@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    '''
    Updates the account details

    :return: success message
    '''
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.user_json['image_file'] = picture
        current_user.user_json['name'] = form.username.data
        current_user.user_json['email'] = form.email.data
        DB.update_account(current_user)
        flash("Your account updated successfully", 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.user_json['name']
        form.email.data = current_user.user_json['email']
    image_file = url_for('static', filename='display_pics/' + current_user.user_json['image_file'])
    return render_template('account.html', title='Account', image_file=image_file, form=form)
