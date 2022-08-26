from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

# 定义一个SQLAlchemy对象，用来操纵数据库
db=SQLAlchemy()

# 定义一个Mail对象，用来操纵邮箱
mail=Mail()