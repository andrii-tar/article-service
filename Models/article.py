from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import declarative_base
import attributes as atr

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

engine = create_engine('mysql+pymysql://{}:{}@{}/{}'
                       .format(atr.dbuser, atr.dbpass, atr.dbhost, atr.dbname))

Base = declarative_base()

Base.metadata.create_all(bind=engine)


class ArticleModel(Base):
    __tablename__ = 'article'

    article_id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    rates_cnt = Column(Integer, nullable=False)

    def __repr__(self):
        return str(ArticleSchema().dump(self))

    def info(self):
        return ArticleSchema().dump(self)


class ArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ArticleModel
        include_relationships = True
        load_instance = True
        include_fk = True
