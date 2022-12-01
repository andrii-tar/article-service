from flask import request
from flask_bcrypt import Bcrypt

from Models.user import UserModel, UserSchema


def load_user_crud(application, database, auth):
    app = application
    db = database

    bcryptor = Bcrypt(app)

    @app.route('/user', methods=['POST'])
    def CreateUser():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            errors = UserSchema().validate(data=json_data, session=db.session)
            if errors:
                return "Missing or incorrect information", 400
            existing_user = db.session.query(UserModel) \
                .filter_by(user_name=json_data["user_name"]).first()
            if existing_user:
                print(existing_user)
                return "Username already exists", 400
            hashed_password = bcryptor.generate_password_hash(json_data['password'])

            new_user = UserModel(
                user_id=None,  # json_data["user_id"],
                user_name=json_data["user_name"],
                email=json_data["email"],
                password=hashed_password,
                role_id=json_data["role_id"]
            )

            db.session.add(new_user)
            db.session.commit()
            return "Registration successful", 200
        else:
            return 'Content-Type not supported!', 400

    @app.route('/user')  # Retrieve current user
    @auth.login_required(role=['user', 'moderator'])
    def RetrieveCurrentUserInfo():
        user = db.session.query(UserModel) \
            .filter_by(user_name=auth.current_user()).first()
        if user:
            return UserModel.info(user)
        else:
            return "User not found", 400

    @app.route('/user/<int:user_id>')  # Retrieve single user
    @auth.login_required(role=['user', 'moderator'])
    def RetrieveSingleUserInfo(user_id):
        user = db.session.query(UserModel) \
            .filter_by(user_id=user_id).first()
        if user:
            return UserModel.info(user)
        else:
            return "User not found", 400

    @app.route('/user', methods=['PUT'])  # update user
    @auth.login_required(role=['user', 'moderator'])
    def UpdateUserInfo():
        user = db.session.query(UserModel).filter_by(user_name=auth.current_user()).first()
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            errors = UserSchema().validate(data=json_data, session=db.session)
            if errors:
                print(errors)
                return "Missing or incorrect information", 400
            if user:
                hashed_password = bcryptor.generate_password_hash(json_data['password'])
                user.user_name = json_data['user_name']
                user.email = json_data['email']
                user.password = hashed_password
                user.role_id = json_data['role_id']

                db.session.commit()
                return "Change successful", 200
            else:
                return "User not found", 400
        else:
            return "Wrong content type supplied, JSON expected", 400

    @app.route('/user', methods=['DELETE'])  # delete user
    @auth.login_required(role=['user', 'moderator'])
    def DeleteUser():
        user = db.session.query(UserModel) \
            .filter_by(user_name=auth.current_user()).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User successfully deleted", 200
        else:
            return "User not found", 400
