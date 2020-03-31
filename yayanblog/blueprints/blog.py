# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import time,datetime
from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user

from yayanblog.emails import send_new_comment_email, send_new_reply_email
from yayanblog.extensions import db
from yayanblog.forms import CommentForm, AdminCommentForm
from yayanblog.models import Post,Comment
from yayanblog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    # url_for的参数，第一个参数为endpoint,第二个参数可以为变量）
    # url_for的变量参数可以是已经在route中定义的变量；比如 ： @app.route('/user/<username>') > url_for('profile', username='John Doe') 那么在调用url_for 的时候将变量的具体指传入url中
    #url_for的变量参数 如果是route中没有的未知参数，那么会作为查询参数，加在url末尾
    # url路径： /?page=3  则page得到3
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['YAYANBLOG_POST_PER_PAGE']
    # 查询方法 paginate（第几页，每页显示多少个）；得到一个pagination实例，即某一页的分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    # 将这个pagination调用items属性，则返回一个post数组，数组元素是每个post的db对象
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['YAYANBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = True

    if form.validate_on_submit():
        author = form.author.data
        # email = form.email.data
        # site = form.site.data
        body = form.body.data
        # comment = Comment(
        #     author=author, email=email, site=site, body=body,
        #     from_admin=from_admin, post=post, reviewed=reviewed)
        comment = Comment(
            author=author, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        # replied_id = request.args.get('reply')
        # if replied_id:
        #     replied_comment = Comment.query.get_or_404(replied_id)
        #     comment.replied = replied_comment
        #     给被回复的用户发送email
        #     send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        flash('Comment published.', 'success')
        # if current_user.is_authenticated:  # send message based on authentication status
        #     flash('Comment published.', 'success')
        # else:
        #     flash('Thanks, your comment will be published after reviewed.', 'info')
        #     send_new_comment_email(post)  # send notification email to admin
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)

#
# @blog_bp.route('/reply/comment/<int:comment_id>')
# def reply_comment(comment_id):
#     comment = Comment.query.get_or_404(comment_id)
#     if not comment.post.can_comment:
#         flash('Comment is disabled.', 'warning')
#         return redirect(url_for('.show_post', post_id=comment.post.id))
#     # 点击reply之后，重定向到带有查询字符串的新url
#     return redirect(
#         url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


# @blog_bp.route('/change-theme/<theme_name>')
# def change_theme(theme_name):
#     if theme_name not in current_app.config['YAYANBLOG_THEMES'].keys():
#         abort(404)
#
#     response = make_response(redirect_back())
#     response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
#     return response
