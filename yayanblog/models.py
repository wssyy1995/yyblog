# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
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

# category与post是一对多并建立双向关系：
#   （1）1个post实体对应唯一的category_id；Category是"一"侧，Post是"多"侧
#   （2）建立外键：在post表中建立categoty_id外键，指向Category表的id列
#   （3）在category侧建立关系:添加posts关系属性，指向Post表 ：当某个category对象调用这个posts属性，SQLAlchemy会找Post表中的外键字段，找到与这个category对象匹配的记录，返回包含这些记录的列表
#    (4) 建立双向联系：在Post侧添加category关系属性，指定back_populates参数 ;category这侧的post关系属性也添加back_populates参数
#     （5）建立双向联系之后：可以通过两种方式来为这两个表添加联系 1： category实例对象.append(post实例对象) 2： <post实例对象>.category=<category实例对象>
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

# Post与Comment也是一对多关系，也是建立双向联系；并且还建立了联级关系
# cascade联级关系：在操作Post对象时，处于附属地位的comment对象也被响应执行某些操作 ；在父对象Post一侧添加cascade参数；默认值save-update,merge；all是除delete-orphan的所有操作
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

# 个人感觉comment和reply应该分开设计：所有reply应该在集合在最高层的comment下面
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    # 评论的回复评论：可以在评论模型内建立层级关系；这种在同一模型内的一对多关系在SQLAlchemy中被称为邻接列表关系（adjacency List Relationship）
    # 对于一(replied)对多（replies）,在"多"的这一侧定义外键到远程的"一"的那一侧的id列表。
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 但是在邻接列表关系中，关系的两侧都在同一个模型中，SQLAlchemy无法分辨关系的两侧；所以在定义关系属性时，通过remote_side参数设为id字段，将id字段定义为关系的远程侧，也就是replied_id就变为本地侧
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    # Same with:
    # replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    # cascade='all,delete-orphan')


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
