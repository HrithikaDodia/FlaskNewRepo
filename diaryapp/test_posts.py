from flask import request, jsonify
from diaryapp import app


def test_create_post():
	app.testing = True
	c = app.test_client()
	rv = c.post('/api/post', json={
    'title': 'abc', 'text_content': 'abc', 'user_id': 1
    })
	json_data = rv.get_json()
	assert rv.status_code == 201
	assert json_data['title'] == 'abc'
	assert json_data['text_content'] == 'abc'