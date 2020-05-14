from flask import render_template, flash, url_for, redirect, request, jsonify
import secrets
import os

from diaryapp import app, db, bcrypt, ma
from diaryapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from diaryapp.models import User, Post, PostSchema
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
	image_file = url_for('static', filename='profile/' + current_user.image_file)
	return render_template('home.html', posts = Post.query.all(), image_file = image_file)

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data)
		user = User(username = form.username.data, 
					email = form.email.data, 
					password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account Created')
		return redirect(url_for('login'))
	return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('account'))
		else:
			flash('Login Unsuccessful')
	return render_template('login.html', form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	name, ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + ext
	picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)
	form_picture.save(picture_path)
	return picture_fn

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			current_user.image_file = save_picture(form.picture.data)
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file = image_file, form=form)


@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_page():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, text_content = form.text_content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created')
		return redirect(url_for('home'))
	return render_template('create_page.html', title='New Page', form=form)

@app.route('/post/<post_id>')
def fetch_post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('fetch.html', post = post)


@app.route('/post/update/<post_id>', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.text_content = form.text_content.data
		db.session.commit()
		flash('Your post has been updated')
		return redirect(url_for('home'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.text_content.data = post.text_content
	return render_template('update.html', form = form)

@app.route('/post/delete/<post_id>', methods = ['GET'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted')
	return redirect(url_for('home'))

post_schema = PostSchema()
posts_schema = PostSchema(many = True)

@app.route('/api/post', methods = ['POST'])
@login_required
def create_post():
	title = request.json['title']
	text_content = request.json['text_content']
	user_id = request.json['user_id']

	post = Post(title=title, text_content=text_content, user_id=user_id)

	db.session.add(post)

	db.session.commit()

	return post_schema.jsonify(post), 201

@app.route('/api/post', methods = ['GET'])
def list_post():
	posts = Post.query.all()
	result = posts_schema.dump(posts)
	return jsonify(result)

