import secrets
import hashlib
import struct

from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from flask import current_app

from msu import db
from msu import files

def hash_pwd(pwd, salt):
    return hashlib.pbkdf2_hmac('sha256', pwd, salt, 100_000)

class CongressMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'),
                         nullable=False)
    name = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False, index=True, unique=True)
    url = db.Column(db.Text, nullable=False)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    inserted_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

    def __init__(self, admin_id, name, title, key, data):
        self.admin_id = admin_id
        self.name = name  
        self.title = title
        self.key = key
        self.url = files.upload_image(key, data)

    @property
    def version(self):
        data = struct.pack('f', self.updated_at.timestamp())
        return hashlib.sha1(data).hexdigest()

    @validates('key', 'url')
    def field_readonly(self, key, val):
        if getattr(self, key) is not None:
            raise ValueError(f'{key} is read-only')
        return val

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    salt = db.Column(db.LargeBinary(16), nullable=False)
    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)

    posts = db.relationship('Post', backref='admin')

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.salt = secrets.token_bytes(16)
        self.password = hash_pwd(password.encode('utf-8'), self.salt)

    @validates('password')
    def validate_password(self, key, pwd):
        assert len(pwd) <= 1024
        return pwd

    def password_equals(self, pwd):
        return self.password == hash_pwd(pwd.encode('utf-8'), self.salt)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'),
                         nullable=False)
    archived = db.Column(db.Boolean, nullable=False, default=False)
    inserted_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            server_default=func.now(),
                            onupdate=func.now())

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False, index=True, unique=True)
    url = db.Column(db.Text, nullable=False)
    inserted_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

    def __init__(self, key, desc, data):
        self.key = key
        self.desc = desc
        self.url = files.upload_file(key, data)

    @property
    def version(self):
        data = struct.pack('f', self.updated_at.timestamp())
        return hashlib.sha1(data).hexdigest()

    @validates('key', 'url')
    def field_readonly(self, key, val):
        if getattr(self, key) is not None:
            raise ValueError(f'{key} is read-only')
        return val

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=False)
    inserted_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            server_default=func.now())

    @validates('name')
    def validate_name(self, key, name):
        if name is not None:
            assert len(name) <= 80

        return name

    @validates('subject')
    def validate_subject(self, key, subject):
        assert len(subject) <= 140
        return subject

    def insert(self):
        pass
