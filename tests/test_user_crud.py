import pytest
from flask_sqlalchemy import SQLAlchemy

from conftest import user_id

user_info = {
    "user_id": 7,
    "user_name": "testUser",
    "email": "testUser@gmail.com",
    "password": "pass",
    "role_id": 1
}
u_id = user_info['user_id']


def test_add_user(client):
    resp = client.post('/user', json=user_info)
    assert resp.status_code == 200


def test_wrong_add_user(client):
    t_email = user_info['email']
    del user_info['email']
    resp = client.post(f'/user', json=user_info)
    user_info["email"] = t_email

    assert resp.status_code == 400

def test_add_duplicate_user(client):
    resp = client.post('/user', json=user_info)
    assert resp.status_code == 400

def test_get_current_user(client, auth_headers):
    resp = client.get(f'/user', headers=auth_headers)
    resp_json = resp.json
    assert resp.status_code == 200

    assert resp_json['password'] != user_info["password"]

    resp_json['password'] = user_info["password"]
    user_info['user_id'] = user_id(client=client, auth_headers=auth_headers)
    assert resp_json == user_info


def test_get_user(client, auth_headers):
    u_id =user_id(client=client, auth_headers=auth_headers)
    resp = client.get(f'/user/{u_id}', headers=auth_headers)
    assert resp.status_code == 200

    resp_json = resp.json
    resp_json['password'] != user_info["password"]

    resp_json['password'] = user_info["password"]
    user_info['user_id'] = user_id(client=client, auth_headers=auth_headers)
    assert resp_json == user_info


def test_update_user(client, auth_headers):
    del user_info['user_id']

    user_info["email"] = 'testUserName@gmail.com'

    resp = client.put(f'/user', json=user_info, headers=auth_headers)
    assert resp.status_code == 200


def test_wrong_update_user(client, auth_headers):
    t_email = user_info['email']
    del user_info['email']
    resp = client.put(f'/user', json=user_info, headers=auth_headers)
    user_info["email"] = t_email

    assert resp.status_code == 400

def test_update_check_user(client, auth_headers):
    u_id = user_id(client=client, auth_headers=auth_headers)

    resp = client.get(f'/user/{u_id}', headers=auth_headers)
    assert resp.status_code == 200

    assert resp.json['user_id'] == u_id
    assert resp.json['user_name'] == user_info["user_name"]
    assert resp.json['email'] == user_info["email"]
    assert resp.json['password'] != user_info["password"]
    assert resp.json['role_id'] == user_info["role_id"]


def test_user_not_json(client, auth_admin_headers):
    resp = client.put(f'/user', headers=auth_admin_headers)
    assert resp.status_code == 400

    resp = client.post('/user')
    assert resp.status_code == 400


def test_delete_user(client, auth_headers):
    resp = client.delete(f'/user', headers=auth_headers)
    assert resp.status_code == 200


def test_user_not_found(client, auth_admin_headers):
    assert client.get(f'/user/{u_id}', headers=auth_admin_headers).status_code == 400


def test_user_no_auth(client):
    assert client.get(f'/user/{u_id}').status_code == 401
    assert client.get(f'/user').status_code == 401
    assert client.delete(f'/user').status_code == 401
    assert client.put(f'/user', json=user_info).status_code == 401
