from sqlalchemy.orm import validates

from msu import db

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, index=True, unique=True)

    def get_by_username(username):
        pass

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def get_all(archived=False):
        pass

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def get_all():
        pass

class Forms(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text)
    subject = db.Column(db.Text)
    message = db.Column(db.Text)

    @validates('name')
    def validate_name(self, key, name):
        assert len(name) <= 80
        return name

    @validates('subject')
    def validate_subject(self, key, subject):
        assert len(subject) <= 140
        return subject

    def insert():
        pass
