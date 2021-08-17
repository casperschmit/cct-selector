from functools import wraps
from flask import url_for, redirect, request, flash
from flaskdss.models import User, Role
from flask_login import login_user, logout_user, current_user
from flaskdss import db


def logout():
    logout_user()


def register(user):
    users = db.session.query(User).filter_by(username=user.username, email=user.email, password=user.password).all()
    print(users)
    if users:
        return False
    else:
        db.session.add(user)
        db.session.commit()
        return True


def login(user_info, remember):
    user_email = user_info.email
    users = db.session.query(User).filter_by(email=user_email).all()

    if users:
        for user in users:
            if user.password == user_info.password:
                login_user(user, remember=remember)
                return True
    return False


def requires_access(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated:
                if not current_user.has_role(access_level):
                    flash('You do not have access to this area', 'info')
                    return redirect(request.referrer)
            if not current_user.is_authenticated:
                flash('You do not have access to this area', 'info')
                return redirect(url_for('login'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
