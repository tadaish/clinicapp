from flask import render_template, request, redirect
from app import app, login
import data
from flask_login import login_user


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = data.auth_user(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return data.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
