from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

app = Flask(__name__)
app.secret_key = '$!$$434@!#$!@#$%!@$da3123@!#!'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/clinicdb?charset=utf8mb4" % quote(
    'Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)


def get_locale():
    return 'vi'


babel.init_app(app, locale_selector=get_locale)
