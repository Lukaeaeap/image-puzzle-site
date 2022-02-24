from datetime import datetime, timezone
from sqlalchemy.sql.elements import False_
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class MyDateTime(db.TypeDecorator):
    impl = db.DateTime

    def process_bind_param(self, value, dialect):
        if type(value) is str:
            return datetime.strptime(value, '%Y-%m-%d')
        return value


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 150 is the max String length, and it should be an unique email
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    creation_date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
