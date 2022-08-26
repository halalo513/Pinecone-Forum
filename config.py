import os

from datetime import timedelta

# 开启debug、模板自动加载和解决中文乱码
DEBUG=True
TEMPLATES_AUTO_RELOAD=True
JSON_AS_ASCII=False

# 设置数据库连接
HOSTNAME="127.0.0.1"
PORT=3306
USERNAME="root"  # 你的数据库用户名
PASSWORD=""  # 你的数据库密码
DATABASE="forum"  # 在MYSQL5.7中新建一个forum数据库
DB_URI=f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI=DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=True

# 邮箱设置 使用QQ邮箱
MAIL_SERVER="smtp.qq.com"
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_DEBUG=True
MAIL_USERNAME=""  # 你的邮箱地址
MAIL_PASSWORD=""  # 对应的邮箱授权码
MAIL_DEFAULT_SENDER=""  # 你的邮箱地址

# 设置session密钥和session过期时间
SECRET_KEY=os.urandom(24)
PERMANENT_SESSION_LIFETIME=timedelta(hours=2)