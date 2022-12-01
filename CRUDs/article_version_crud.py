import datetime

from flask import request, jsonify

from flask_expects_json import expects_json

from Models.articleversion import ArticleVersionModel
from Models.user import UserModel

article_version_schema = {
    "type": "object",
    "properties": {
        "article_version_id": {"type": "integer"},
        "article_id": {"type": "integer"},
        "text": {"type": "string"},
        "title": {"type": "string"},
    },
    "required": ["article_id", "text", "title"]
}


def load_article_version_crud(application, database, auth):
    app = application
    db = database

    # View list of all versions of article
    @app.route('/article/<int:articleID>/version')
    def GetAllArticlesVersions(articleID):
        article_versions = db.session.query(ArticleVersionModel) \
            .filter_by(article_id=articleID).all()
        if article_versions:
            j_versions = []
            for a in article_versions:
                j_versions.append(ArticleVersionModel.info(a))
            return jsonify(j_versions)
        else:
            return "Articles not found", 400

    @app.route('/article/version', methods=['POST'])  # Create new version of article
    @auth.login_required(role=['user', 'moderator'])
    def CreateArticleVersion():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            cur_user = db.session.query(UserModel) \
                .filter_by(user_name=auth.current_user()).first()

            new_article_version = ArticleVersionModel(
                article_version_id=json_data["article_version_id"],
                article_id=json_data["article_id"],
                author_id=cur_user.user_id,
                moderator_id=None,
                status="on_review",
                text=json_data["text"],
                title=json_data["title"],
                last_change=datetime.datetime.now().date()
            )
            db.session.add(new_article_version)
            db.session.commit()
            return "Article version successfully added", 200
        else:
            return "Wrong content type supplied, JSON expected", 400

    @app.route('/article/version/search', methods=['GET'])  # View articles by title
    def GetArticlesByTitle():
        target_title = request.args.get('title')
        versions = db.session.query(ArticleVersionModel) \
            .filter(ArticleVersionModel.title.contains(target_title)) \
            .order_by(ArticleVersionModel.last_change.desc()) \
            .all()

        if versions:
            j_versions = []
            for v in versions:
                j_versions.append(ArticleVersionModel.info(v))
            return jsonify(j_versions)
        else:
            return "Articles not found", 400

    # View list of particular article version
    @app.route('/article/<int:articleID>/version/<int:versionID>')
    def GetArticleVersionById(articleID, versionID):
        article_version = db.session.query(ArticleVersionModel) \
            .filter_by(
            article_id=articleID,
            article_version_id=versionID
        ).first()
        if article_version:
            return ArticleVersionModel.info(article_version)
        else:
            return "Article version not found", 400

    # update article version
    @app.route('/article/<int:articleID>/version/<int:versionID>', methods=['PUT'])
    @auth.login_required(role=['moderator'])
    def UpdateArticleVersionStatus(articleID, versionID):
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            json_data = request.get_json()
            article_version = db.session.query(ArticleVersionModel) \
                .filter_by(
                article_id=articleID,
                article_version_id=versionID
            ).first()
            if article_version:
                cur_user = db.session.query(UserModel) \
                    .filter_by(user_name=auth.current_user()).first()

                article_version.status = json_data["status"]
                article_version.moderator_id = cur_user.user_id
                article_version.last_change = datetime.datetime.now().date()

                db.session.add(article_version)
                db.session.commit()
                return "Article version status successfully updated", 200
            else:
                return "Article version not found", 400
        else:
            return "Wrong content type supplied, JSON expected", 400

    @app.route('/article/<int:articleID>/version/<int:versionID>', methods=['DELETE'])
    @auth.login_required(role=['moderator'])
    def DeleteArticleVersionById(articleID, versionID):
        article_version = db.session.query(ArticleVersionModel) \
            .filter_by(article_id=articleID, article_version_id=versionID).first()
        if article_version:
            db.session.delete(article_version)
            db.session.commit()
            return 'Deleted', 200
        else:
            return "Articles not found", 400
