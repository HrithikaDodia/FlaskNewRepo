from flask import Blueprint, render_template, flash, url_for, redirect, request, jsonify
import secrets
import os
from diaryapp import db, bcrypt, ma
from diaryapp.posts.forms import PostForm
from diaryapp.models import Post, PostSchema, User
from flask_login import login_user, current_user, logout_user, login_required


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_page():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, text_content = form.text_content.data, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created')
		return redirect(url_for('main.home'))
	return render_template('create_page.html', title='New Page', form=form)

@posts.route('/post/<post_id>')
def fetch_post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('fetch.html', post = post)


@posts.route('/post/update/<post_id>', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.text_content = form.text_content.data
		db.session.commit()
		flash('Your post has been updated')
		return redirect(url_for('main.home'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.text_content.data = post.text_content
	return render_template('update.html', form = form)

@posts.route('/post/delete/<post_id>', methods = ['GET'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted')
	return redirect(url_for('main.home'))

post_schema = PostSchema()
posts_schema = PostSchema(many = True)

@posts.route('/api/post', methods = ['POST'])
@login_required
def create_post_api():
	title = request.json['title']
	text_content = request.json['text_content']

	post = Post(title=title, text_content=text_content, author=current_user)

	db.session.add(post)

	db.session.commit()

	return post_schema.jsonify(post), 201

@posts.route('/api/post', methods = ['GET'])
def list_post_api():
	posts = Post.query.all()
	result = posts_schema.dump(posts)
	return jsonify(result)

@posts.route('/api/login', methods = ['GET', 'POST'])
def login_api():
	user = db.session.query(User).filter_by(id = request.json['user_id']).first()
	login_user(user)
	return jsonify({'Success':True})

@posts.route('/api/update/<int:post_id>', methods = ['PUT'])
def update_post_api(post_id):
	post = Post.query.get_or_404(post_id)
	post.title = request.json['title']
	post.text_content = request.json['text_content']
	db.session.commit()
	return post_schema.jsonify(post)