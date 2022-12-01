from flask import Flask
from flask_bcrypt import check_password_hash
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

import attributes as atr

from flask_cors import CORS

from CRUDs.article_crud import load_article_crud
from CRUDs.article_version_crud import load_article_version_crud
from CRUDs.user_crud import load_user_crud
from Models.role import RoleModel
from Models.user import UserModel


def create_app():
    app = Flask(__name__)

    app.config['TESTING'] = True

    conn = 'mysql+pymysql://{}:{}@{}/{}' \
        .format(atr.dbuser, atr.dbpass, atr.dbhost, atr.dbname)
    app.config['SQLALCHEMY_DATABASE_URI'] = conn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    db = SQLAlchemy(app)
    auth = HTTPBasicAuth()

    CORS(app)

    @auth.verify_password
    def verify_password(username, password):
        user = db.session.query(UserModel).filter_by(user_name=username).first()
        if user and username == user.user_name:
            if check_password_hash(user.password, password):
                return username

    @auth.get_user_roles
    def get_user_roles(username):
        user_info = db.session.query(UserModel)\
            .filter_by(user_name=username).first()
        role = db.session.query(RoleModel)\
            .filter_by(role_id=user_info.role_id).first()
        return role.title

    load_article_crud(app, db, auth)
    load_article_version_crud(app, db, auth)
    load_user_crud(app, db, auth)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
