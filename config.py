import os

# 调试设置
ENV = 'development'
DEBUG = 'Ture'

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(basedir, 'datas.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "my first flask project"

# 邮箱配置
MAIL_SERVER='smtp.qq.com'
MAIL_PORT = 465
MAIL_USERNAME = '896322805@qq.com'
MAIL_PASSWORD = 'rgyxoxvlcyhwbeed'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_DEFAULT_SENDER = '896322805@qq.com'

# 文件上传配置
UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}
