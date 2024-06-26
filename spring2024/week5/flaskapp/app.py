from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from bson import ObjectId
from . import app, bcrypt
from .forms import CreatePostForm, LoginForm, RegistrationForm
from .models import Post, User


@app.route('/')
@app.route('/index')
def index_route():
    posts = list(Post.objects())
    return render_template('index.html', posts=posts, current_user=current_user)

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost_route():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_post = Post(username=current_user.username, text=form.text.data)
            new_post.save()
            # if you want to redirect to the same route the form is on
            # you can use redirect(request.path)
            return redirect(url_for('index_route'))
    return render_template('createpost_form.html', form=form)

@app.route('/user/<username>')
def user_route(username):
    # should convert to list because the return type is a MongoDB Cursor
    user_posts = list(Post.objects(username=username))
    return render_template('user.html', username=username, user_posts=user_posts)

@app.route('/post/<id>')
def post_route(id):
    post = Post.objects(pk=ObjectId(id)).first()
    return render_template('post.html', post=post)

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if current_user.is_authenticated:
        return redirect(url_for('index_route'))

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            user.save()
            return redirect(url_for('login_route'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if current_user.is_authenticated:
        return redirect(url_for('index_route'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.objects(username=form.username.data).first()

            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('user_route', username=user.username))
            # if the user fails to login, we just render the login page again and do nothing
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_route():
    logout_user()
    return redirect(url_for('index_route'))