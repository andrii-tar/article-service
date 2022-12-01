from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import sqlalchemy as db

from Models.article import Base


class RoleModel(Base):
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(45), nullable=False)

    def __repr__(self):
        return str(RoleSchema().dump(self))

    def info(self):
        return RoleSchema().dump(self)


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoleModel
        include_relationships = True
        load_instance = True
        include_fk = True
