from flask import request, jsonify

from flask_expects_json import expects_json

from Models.article import ArticleModel

article_schema = {
    "type": "object",
    "properties": {
        "article_id": {"type": "integer"},
        "rating": {"type": "integer"},
        "rates_cnt": {"type": "integer"}
    },
    "required": ["article_id", "rating", "rates_cnt"]
}


def load_article_crud(application, database, auth):
    app = application
    db = database

    @app.route('/article')  # View list of all articles
    def GetAllArticles():
        articles = db.session.query(ArticleModel).all()
        if articles:
            j_articles = []
            for a in articles:
                j_articles.append(ArticleModel.info(a))
            return jsonify(j_articles)
        else:
            return "Articles not found", 400

    @app.route('/article', methods=['POST'])  # Create new article
    @auth.login_required(role=['user', 'moderator'])
    @expects_json(article_schema)
    def CreateArticle():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            new_article = ArticleModel(
                article_id=json_data["article_id"],
                rating=json_data["rating"],
                rates_cnt=json_data["rates_cnt"]
            )
            db.session.add(new_article)
            db.session.commit()
            return "Article successfully added", 200
        else:
            return "Wrong content type supplied, JSON expected", 400

    @app.route('/article/<int:articleID>')  # View article by id
    def GetSingleArticleById(articleID):
        article = db.session.query(ArticleModel) \
            .filter_by(article_id=articleID).first()
        if article:
            return ArticleModel.info(article)
        else:
            return "Articles not found", 400

    @app.route('/article/<int:articleID>', methods=['PUT'])  # View article by id
    def UpdateRating(articleID):
        article = db.session.query(ArticleModel) \
            .filter_by(article_id=articleID).first()
        if article:
            json_data= request.get_json()
            article.rating = json_data['rating']
            article.rates_cnt = json_data['rates_cnt']

            db.session.commit()
            return "Rating updated", 200
        else:
            return "Articles not found", 400

    # delete article by id
    # (there is on cascade delete so all versions will be also deleted)
    @app.route('/article/<int:articleID>', methods=['DELETE'])
    @auth.login_required(role=['moderator'])
    def DeleteArticleById(articleID):
        article = db.session.query(ArticleModel) \
            .filter_by(article_id=articleID).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            return 'Deleted', 200
        else:
            return "Articles not found", 400
