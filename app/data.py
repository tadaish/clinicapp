import hashlib

from app.models import User


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)
