from flask import request, jsonify
from diaryapp import app
from diaryapp.factories import new_user, client

def test_create_post(new_user, client):
	app.testing = True
	r = client.post('/api/login', json={
    'user_id': 1})
	assert r.status_code == 200
	rv = client.post('/api/post', json={
    	'title': 'abcdef', 'text_content': 'abcdef', 'user_id': 1
    })
	json_data = rv.get_json()
	assert rv.status_code == 201
	assert json_data['title'] == 'abcdef'
	assert json_data['text_content'] == 'abcdef'

def test_update_post(new_user, client):
	app.testing = True
	r = client.post('/api/login', json={
    'user_id': 1})
	assert r.status_code == 200
	rv = client.put('/api/update/10', json={
    	'title': 'flask post', 'text_content': 'Flask is Awesome!!', 'user_id': 1
    })
	json_data = rv.get_json()
	assert rv.status_code == 200
	assert json_data['title'] == 'flask post'
	assert json_data['text_content'] == 'Flask is Awesome!!'