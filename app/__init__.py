from flask import Flask
from flaskext.mysql import MySQL


mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'website_crawl'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    from .controllers import api_blueprint

    app.register_blueprint(api_blueprint)

    return app