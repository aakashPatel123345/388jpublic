from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    # Otherwise the user is not logged in and we can proceed with registration
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('movies.index'))

    return render_template("register.html", form=form)


# TODO: implement
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: 
            return redirect(url_for('movies.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            user = User.objects(username = form.username.data).first()

            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('users.account'))
            else:
                # If the user incorrectly enters their credentials, we want to flash a message
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('movies.index'))

def custom_404(errror):
    return render_template("404.html"), 404


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    if request.method == "POST":
        if update_username_form.validate() and update_username_form.submit_username.data:
            # TODO: handle update username form submit
            # We need to make sure that the new username is not already taken
            current_user.modify(username=update_username_form.username.data)
            current_user.save

        if update_profile_pic_form.validate() and update_profile_pic_form.submit_picture.data:
            # TODO: handle update profile pic form submit
            img = update_profile_pic_form.picture.data
            filename = secure_filename(img.filename)
            content_type = f'images/{filename[-3:]}'
            if current_user.profile_pic:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            current_user.save()
        return redirect(url_for('users.account'))

    # TODO: handle get requests
    return render_template("account.html", update_username_form=update_username_form, update_profile_pic_form=update_profile_pic_form, current_username = current_user.username, image=current_user.profile_pic)