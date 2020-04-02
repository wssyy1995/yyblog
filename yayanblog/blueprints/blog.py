# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
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



@blog_bp.route('/search',methods=['GET', 'POST'])
def search():
    q=request.args.get('search_text')
    search_post = Post.query.filter(Post.title.like('%' + q + '%')).all()
    return render_template('blog/post_search.html', search_post=search_post)






@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['YAYANBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        from_admin = True
    else:
        form = CommentForm()
        from_admin = False

    if form.validate_on_submit():
        author = form.author.data
        body = form.body.data
        comment = Comment(
            author=author, body=body,
            from_admin=from_admin, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment published.', 'success')
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)

