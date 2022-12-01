from sqlalchemy import ForeignKey
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import sqlalchemy as db

from Models.article import Base


class ArticleVersionModel(Base):
    __tablename__ = "article_version"
    article_version_id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, ForeignKey("article.article_id"), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey("user.user_id"), nullable=False)
    moderator_id = db.Column(db.Integer, ForeignKey("user.user_id"), nullable=True)
    status = db.Column(db.VARCHAR(45), nullable=False)
    text = db.Column(db.VARCHAR(2500), nullable=False)
    title = db.Column(db.VARCHAR(45), nullable=False)
    last_change = db.Column(db.VARCHAR(45), nullable=False)

    def __repr__(self):
        return str(ArticleVersionSchema().dump(self))

    def info(self):
        return ArticleVersionSchema().dump(self)


class ArticleVersionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ArticleVersionModel
        include_relationships = True
        load_instance = True
        include_fk = True
