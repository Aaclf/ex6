from exts import db
from datetime import datetime


class EmailCaptchaModel(db.Model):
    __tablename__ = 'emile_captcha'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    captcha = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    author = db.relationship("UserModel", backref="questions")


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel", backref="comments")
    author = db.relationship("UserModel", backref="comments")


class CollectModel(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    question = db.relationship("QuestionModel", backref="collects")
    author = db.relationship("UserModel", backref="collects")


class FileModel(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), nullable=False, unique=True)



