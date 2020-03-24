# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from yayanblog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 16)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    # SelectField类表示<select>标签，下拉列表的选项<option>标签通过参数coices指定
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()



    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # choices必须是一个包含两元素元祖的列表，每个元祖代表一个option，第一个元素是option value值，第二个元素是option的label值
        # 用到了python的for的列表推导式，可以将for in 的每次迭代的数据都依次添加到一个数组中，用逗号隔开： 比如：yuanzu=([1,2,3],[4,5,6],[7,8,9])    list=[l[0]for l in yuanzu]
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField()

    # 自定义表单validator函数，会在验证表单数据时时；同时调用这个验证方法来验证对应的字段；
    # 函数方法名为validate_要验证的字段；
    # 如果验证出错，会将ValidationError 传入错误消息：form.对应字段.errors
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            inputname=field.data
            raise ValidationError('The category name: "%s" already exists.'%(inputname))


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired(), Length(1, 16)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    # site可以为空，所以使用optional()验证器确保输入的数据为有效的url
    site = StringField('Site（optional）', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
