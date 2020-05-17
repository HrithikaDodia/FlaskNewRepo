from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class PostForm(FlaskForm):
	title = StringField('Title', validators = [DataRequired()])
	text_content = TextAreaField('Content', validators = [DataRequired()])
	submit = SubmitField('Post')