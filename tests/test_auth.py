import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) #Ensures files path are accessible to tests

import json
from models import User

def test_user_valid_registration(client):

    payload = json.dumps({'username': 'username', 'password': 'pass1'})

    res = client.post('/auth/register', data=payload, content_type='application/json')
    assert res.status_code == 201

    content = res.get_json()
    assert content["message"] == "User registered successfully"
    
    saved_user = User.query.filter_by(username='username').first()

    assert saved_user is not None, "User is saved to database"
    assert saved_user.password_hash != 'pass1'


def test_user_invalid_registration(client):
    payload = json.dumps({'username': 'invalid_username', 'password': ''})
    res = client.post('/auth/register', data=payload, content_type='application/json')
    assert res.status_code == 400

    saved_user = User.query.filter_by(username='invalid_username').first()
    assert saved_user is None, "No user created in invalid registration process"


def test_user_login_authorization(client):
    #now we validate our test user authorization
    payload = json.dumps({'username': 'username01', 'password': 'pws111'})
    res = client.post('/auth/login', data=payload, content_type="application/json")
    assert res.status_code == 200

def test_user_invalid_login_unauthorization(client):
    """Invalid credentials must not be authorized"""
    payload = json.dumps({'username': 'username01', 'password': 'wrongpwd'})
    res = client.post('/auth/login', data=payload, content_type="application/json")
    assert res.status_code == 401