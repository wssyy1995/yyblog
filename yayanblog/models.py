# -*- coding: utf-8 -*-

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from yayanblog.extensions import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证传入的明文密码哈希后，是否与存在数据库里的哈希密码一致
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)



# Post与Comment也是一对多关系，也是建立双向联系；并且还建立了联级关系
# cascade联级关系：在操作Post对象时，处于附属地位的comment对象也被响应执行某些操作 ；在父对象Post一侧添加cascade参数；默认值save-update,merge；all是除delete-orphan的所有操作
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')


    # 回复和被回复的comment都放在一个表里了
    # 评论的回复评论：可以在评论模型内建立层级关系；这种在同一模型内的一对多关系在SQLAlchemy中被称为邻接列表关系（adjacency List Relationship）
    # 对于一(replied)对多（replies）,在"多"的这一侧定义外键到远程的"一"的那一侧的id列表。
    # replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 但是在邻接列表关系中，关系的两侧都在同一个模型中，SQLAlchemy无法分辨关系的两侧；所以在定义关系属性时，通过remote_side参数设为id字段，将id字段定义为关系的远程侧，也就是replied_id就变为本地侧
    # replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    # Same with:
    # replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    # cascade='all,delete-orphan')

