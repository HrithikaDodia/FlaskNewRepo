from flask import request, jsonify
from diaryapp import app
from diaryapp.factories import new_user

def test_create_post(new_user):
	app.testing = True
	c = app.test_client()
	r = c.post('/api/login', json={
    'user_id': 1})
	assert r.status_code == 200
	rv = c.post('/api/post', json={
    	'title': 'abcdef', 'text_content': 'abcdef', 'user_id': 1
    })
	json_data = rv.get_json()
	assert rv.status_code == 201
	assert json_data['title'] == 'abcdef'
	assert json_data['text_content'] == 'abcdef'