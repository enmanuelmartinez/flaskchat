# -*- coding: UTF-8 -*-

from app import db


class BaseModel(db.Model):
    __abstract__  = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


 # User role
ADMIN = 0
STAFF = 1
USER = 2

ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# user status
INACTIVE = 0
ACTIVE = 1

STATUS = {
    INACTIVE: 'inactive',
    ACTIVE: 'active',
}

class User(BaseModel):

    __tablename__ = 'auth_user'

    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name) 