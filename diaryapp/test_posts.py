from flask import request, jsonify
from diaryapp.models import User
from diaryapp.factories import client, init_database, new_user
from diaryapp import db
from flask_login import current_user, login_user

def test_create_post(client, init_database, new_user):
	login = client.post('/api/login', json={'user_id': new_user.id})
	assert login.status_code==200
	assert b'Success' in login.data

	assert new_user.id == 1
	rv = client.post('/api/post', json={
    	'title': 'abcdef', 'text_content': 'abcdef'
    })
	
	json_data = rv.get_json()
	assert rv.status_code == 201
	assert json_data['title'] == 'abcdef'
	assert json_data['text_content'] == 'abcdef'
	assert json_data['user_id'] == new_user.id

def test_update_post(client, init_database, new_user):
	login = client.post('/api/login', json={'user_id': new_user.id})
	assert login.status_code==200

	create = client.post('/api/post', json={
		'title': 'abcdef', 'text_content': 'abcdef'
	})
	assert create.status_code==201
	
	create_json = create.get_json()
	id = create_json['id']
	rv = client.put(f'/api/update/{id}', json={
    	'title': 'flask post', 'text_content': 'Flask is Awesome!!'
    })

	json_data = rv.get_json()
	assert rv.status_code == 200
	assert json_data['title'] == 'flask post'
	assert json_data['text_content'] == 'Flask is Awesome!!'