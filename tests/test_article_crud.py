import pytest
from flask_sqlalchemy import SQLAlchemy

article_info = {
    "article_id": 8,
    "rating": 0,
    "rates_cnt": 0
}
a_id = article_info["article_id"]


def test_add_article(client, auth_admin_headers):
    resp = client.post('/article', json=article_info, headers=auth_admin_headers)
    assert resp.status_code == 200


def test_get_article(client):
    resp = client.get(f'/article/{a_id}')
    assert resp.json['article_id'] == article_info["article_id"]
    assert resp.json['rating'] == article_info["rating"]
    assert resp.json['rates_cnt'] == article_info["rates_cnt"]


def test_get_all_articles(client):
    resp = client.get('/article')
    assert resp.json is not None
    assert article_info in resp.json


def test_update_article(client, auth_headers):
    resp = client.put(f'/article/{a_id}', json={
        "rating": 10,
        "rates_cnt": 1
    }, headers=auth_headers)


    assert resp.status_code == 200

def test_update_check_article(client):
    resp = client.get(f'/article/{a_id}')
    article_info = {
        "article_id": 8,
        "rating": 10,
        "rates_cnt": 1
    }
    assert resp.json == article_info



article_info = {
    "article_id": 8,
    "rating": 0,
    "rates_cnt": 0
}

def test_delete_article(client, auth_admin_headers):
    resp = client.delete(f'article/{a_id}', headers=auth_admin_headers)
    assert resp.status_code == 200


def test_article_not_found(client, auth_admin_headers):
    assert client.get(f'/article/{a_id}', headers=auth_admin_headers).status_code == 400
    assert client.delete(f'article/{a_id}', headers=auth_admin_headers).status_code == 400
    assert client.get(f'article/{a_id}', headers=auth_admin_headers).status_code == 400


def test_article_not_json(client, auth_admin_headers):
    resp = client.post('/article', headers=auth_admin_headers)
    assert resp.status_code == 400


def test_article_no_auth(client):
    assert client.delete(f'article/{a_id}').status_code == 401
