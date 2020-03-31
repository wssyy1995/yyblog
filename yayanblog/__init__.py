# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import logging
import os,time
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from yayanblog.blueprints.admin import admin_bp
from yayanblog.blueprints.auth import auth_bp
from yayanblog.blueprints.blog import blog_bp
from yayanblog.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate
from yayanblog.models import Admin, Post, Comment
from yayanblog.settings import config

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# 使用工厂函数创建程序实例，使用这个函数可以在任何地方创建多个程序实例
# 比如，可以在测试脚本中，在测试脚本中使用测试配置来调用工厂函数，创建一个单独用于测试的程序实例，而不用从某个模块导入程序实例
# 启动程序:当使用flask run命令启动程序时，flask的自动发现程序实例包含另一种行为：Flask会自动从环境变量FLASK_APP的值定义的模块中寻找名为create_app（）的工程函数，自动调用工厂函数创建程序实例并运行

# 为了支持Flask自动从Flask_App环境变量对应值指向的模块中发现工厂函数，工厂函数中接收的参数必须是设置了默认值的参数
# current_app：在工厂函数创建完程序实例后，如果要在别的模块中使用程序实例，但却无法导入一个固定的程序实例，可以用current_app来表示当前程序实例的代理对象；

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('yayanblog')
    # 创建程序实例后，使用app.config.from_object ，通过传入config_name作为key值，加载存储在config字典的配置类
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)
    register_request_handlers(app)
    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/yayanblog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='yayanblog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)



# 初始化拓展，大部分拓展提供了init_app()方法来支持分离拓展的实例化和初始化操作；
# 1.extensions.py中：先完成拓展类实例化的工作，但是暂时不传入程序实例，先得到这些拓展类的实例化对象
# 2.在工厂函数中，导入所有拓展对象，并完成程序实例化后，再将这些拓展对象使用init_app()方法 ，传入程序实例，完成初始化

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)

'''
创建的蓝本对象要发挥作用，需要将蓝本注册到程序实例上；app.register_blueprint必须传入的参数是上面创建的蓝本对象
url_prefix参数为蓝本下的所有视图url前附加一个前缀

 蓝本的路由端点： URL规则和视图函数并不是直接映射的，而是通过端点作为中间媒介
    1.一般默认视图函数名为端点名，但是实现蓝本后，每个路由的URL规则对应的端点不再仅仅是视图函数名，而是"蓝本名.视图函数名" （蓝本名是我们实例化Blueprint时传入的第一个参数），比如blog_bp蓝本蓝本名就是blog ；
    2.实现了蓝本后怎么调用端点？：要调用admin_bp蓝本下的index端点时，就是"blog.index"
    3.为什么不直接使用视图函数名？：可以实现蓝本的视图函数命名空间，因为不同的蓝本中可能创建同名的视图函数
'''
def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')




def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post,Comment=Comment,time=time)

# app.context_processor 模板上下文处理器下的所有函数，在render_template任意一个html页面时，都会自动执行。
# 并且函数的返回值必须是个dict，dict的key会被当做变量返回到模板中，值为value
# 可以用来定义一个用于所有页面的全局变量
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin,unread_comments=unread_comments,time=time)

# 错误处理函数：将errorhandler注册到蓝本实例上，则会注册一个全局的错误处理器
def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def init(username, password):
        """Building yayanblog, just for you."""

        click.echo('Initializing the database...')
        db.drop_all()
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='yayanblog-title',
                blog_sub_title="Hi,welcome here! this is the yayanblog-sub-title",
                name='YayanAdmin',
                about='WAnything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--post', default=100, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=100, help='Quantity of comments, default is 500.')
    def forge(post, comment):
        """Generate fake data."""
        from yayanblog.fakes import fake_admin,fake_posts, fake_comments

        # db.drop_all()
        # db.create_all()

        #
        #
        # click.echo('Generating the administrator...')
        # fake_admin()




        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)


        click.echo('Done.')


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['YAYANBLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response
