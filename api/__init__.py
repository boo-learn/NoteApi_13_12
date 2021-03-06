import logging
from config import Config
from flask import Flask, g, send_from_directory
from flask_restful import Api, Resource, abort, reqparse, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_babel import Babel

app = Flask(__name__, static_folder=Config.UPLOAD_FOLDER)
app.config.from_object(Config)

security_definitions = {
    "basicAuth": {
        "type": "basic"
    }
}

ma_plugin = MarshmallowPlugin()
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Notes Project',
        version='v1',
        plugins=[ma_plugin],
        securityDefinitions=security_definitions,
        security=[],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger',  # URI API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui'  # URI UI of API Doc
})

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
auth = HTTPBasicAuth()
# swagger = Swagger(app)
docs = FlaskApiSpec(app)
babel = Babel(app)

# Общие настройки логера
logging.basicConfig(filename='record.log',
                    level=logging.WARNING,
                    format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')


# Настройка уровня логирования flask
# app.logger.setLevel(logging.DEBUG)
# Настройка уровня логирования сервера-разработки werkzeug
# logging.getLogger('werkzeug').setLevel(logging.DEBUG)

@auth.verify_password
def verify_password(username_or_token, password):
    from api.models.user import UserModel
    # сначала проверяем authentication token
    # print("username_or_token = ", username_or_token)
    # print("password = ", password)
    user = UserModel.verify_auth_token(username_or_token)
    if not user:
        # потом авторизация
        user = UserModel.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    logging.warning("!!!Request with auth User")
    return True


@auth.get_user_roles
def get_user_roles(user):
    return g.user.get_roles()


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
