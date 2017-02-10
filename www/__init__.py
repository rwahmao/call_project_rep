# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

bootstrap = Bootstrap(app)
#创建数据库对象
db = SQLAlchemy(app)

#创建flask_login对象
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


#注册蓝图全部文件
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from .controller import controller as controller_blueprint
app.register_blueprint(controller_blueprint,url_prefix='/dashboard')


#print os.environ.keys()
#print os.environ.get('FLASKR_SETTINGS')
#加载配置文件内容
app.config.from_object('www.setting')
#模块下的setting文件名，不用加py后缀
#app.config.from_envvar('FLASKR_SETTINGS')
#环境变量，指向配置文件setting的路径
#print(app.config)

