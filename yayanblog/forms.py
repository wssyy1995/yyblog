# -*- coding: utf-8 -*-

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, URL



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 16)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()


class CommentForm(FlaskForm):
    author = StringField('Your Name', validators=[DataRequired(), Length(1, 16)])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()


class SearchForm(FlaskForm):
    search_submit=SubmitField(render_kw={'value':''})
    # 解决输入框点击后placeholder不消失的问题：添加onfocus属性:onfocus:"this.placeholder=''"
    search_text=StringField('search_text',render_kw={'placeholder':'Search',"onfocus":"this.placeholder=''"},validators=[DataRequired(), Length(1, 16)])

