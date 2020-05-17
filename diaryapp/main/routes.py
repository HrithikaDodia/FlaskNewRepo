from flask import Blueprint,render_template, flash, url_for, redirect, request, jsonify
import secrets
import os
from diaryapp import db, bcrypt, ma
from diaryapp.models import Post
from flask_login import login_user, current_user, logout_user, login_required


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
	image_file = url_for('static', filename='profile/' + current_user.image_file)
	return render_template('home.html', posts = Post.query.all(), image_file = image_file)

