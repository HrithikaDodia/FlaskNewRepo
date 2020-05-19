from datetime import datetime
from diaryapp import db, login_manager, ma
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(25), unique = True, nullable = False)
	email = db.Column(db.String(100), unique = True, nullable = False)
	image_file = db.Column(db.String(25), default = 'default.jpg', nullable = False)
	password = db.Column(db.String(60), nullable = False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return self.username

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100))
	date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	text_content = db.Column(db.Text, nullable = False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return self.title

class PostSchema(ma.Schema):
	class Meta:
		fields = ('id', 'title', 'text_content', 'user_id')
