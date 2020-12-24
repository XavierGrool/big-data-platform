import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from big_data.db import get_db

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('hi/')
def say_hi():
    return "First Try!~"

@bp.route('api/')
def api_test():
    return {
        "username": "Xavier",
        "id": "161730309"
    }

@bp.route('sql/')
def sql_test():
    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES ('xavier', '123')"
    )
    db.commit()
    return {
        'status': True
    }