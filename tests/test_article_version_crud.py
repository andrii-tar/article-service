from time import strftime

import pytest
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

article_version_info = {
    "article_version_id": 1,
    "article_id": 1,
    "author_id": 13,
    "moderator_id": None,
    "status": "on_review",
    "text": "Aded new version",
    "title": "Aded new version",
    "last_change": datetime.now().strftime("%Y-%m-%d")
}
av_id = article_version_info['article_version_id']
a_id = article_version_info['article_id']


def test_add_article_version(client, auth_admin_headers):
    # create
    resp = client.post('/article/version', json=article_version_info, headers=auth_admin_headers)
    assert resp.status_code == 200


def test_get_article_version(client):
    resp = client.get(f'/article/{a_id}/version/{av_id}')
    assert resp.json == article_version_info
    assert resp.status_code == 200


def test_update_article_version(client, auth_admin_headers):
    article_version_info['status'] = 'published'
    article_version_info['moderator_id'] = 13
    article_version_info['last_change'] = datetime.now().strftime("%Y-%m-%d")
    resp = client.put(f'/article/{a_id}/version/{av_id}', json=article_version_info, headers=auth_admin_headers)
    assert resp.status_code == 200


def test_update_check_article_version(client, auth_admin_headers):
    resp = client.get(f'/article/{a_id}/version/{av_id}', headers=auth_admin_headers)
    assert resp.json == article_version_info
    assert resp.status_code == 200


def test_get_all_versions(client):
    resp = client.get(f'/article/{a_id}/version')
    assert resp.status_code == 200
    assert resp.json is not None
    assert article_version_info in resp.json


def test_get_versions_by_title(client):
    resp = client.get(f'/article/version/search',
                      query_string={'title': article_version_info['title']})
    assert resp.status_code == 200
    assert resp.json is not None
    assert article_version_info in resp.json


def test_get_versions_by_dif_title(client):
    resp = client.get(f'/article/version/search',
                      query_string={'title': 'No title'})
    assert resp.status_code == 400
    assert resp.json is None


def test_delete_article_version(client, auth_admin_headers):
    resp = client.delete(f'/article/{a_id}/version/{av_id}', headers=auth_admin_headers)
    assert resp.status_code == 200


def test_article_version_not_found(client, auth_admin_headers):
    resp = client.delete(f'/article/{a_id}/version/{av_id}', headers=auth_admin_headers)
    assert resp.status_code == 400

    resp = client.put(f'/article/{a_id}/version/{av_id}',
                      json=article_version_info,
                      headers=auth_admin_headers)
    assert resp.status_code == 400


def test_article_version_not_json(client, auth_admin_headers):
    resp = client.post(
        f'/article/version',
        headers=auth_admin_headers
    )
    assert resp.status_code == 400

    resp = client.put(f'/article/{a_id}/version/{av_id}',
                      headers=auth_admin_headers)
    assert resp.status_code == 400


def test_article_version_no_auth(client):
    resp = client.delete(f'/article/{a_id}/version/{av_id}')
    assert resp.status_code == 401

    resp = client.put(f'/article/{a_id}/version/{av_id}', json=article_version_info)
    assert resp.status_code == 401
