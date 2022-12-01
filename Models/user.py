from sqlalchemy import ForeignKey
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import sqlalchemy as db

from Models.role import Base


class UserModel(Base):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.VARCHAR(45), nullable=False, unique=True)
    email = db.Column(db.VARCHAR(45), nullable=False)
    password = db.Column(db.VARCHAR(100), nullable=False)
    role_id = db.Column(db.Integer, ForeignKey("role.role_id"), nullable=False)

    def __repr__(self):
        return str(UserSchema().dump(self))

    def info(self):
        return UserSchema().dump(self)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_fk = True
        include_relationships = True
        load_instance = True
