from flask import Flask, session, g

from exts import db, mail

from blueprints import user_bp, qa_bp

from models import UserModel, UserExtendModel

import config

app = Flask(__name__)

# 添加配置信息
app.config.from_object(config)

# 注册user蓝图
app.register_blueprint(user_bp)

# 注册QA蓝图
app.register_blueprint(qa_bp)

# 初始化数据库对象，配置数据库信息
db.init_app(app)

# 初始化邮箱对象
mail.init_app(app)

# 定义钩子函数，用户如果登录，则从数据库中查询该用户的所有信息，并绑定到g对象上
@app.before_request
def before_request():
    user_id=session.get('user_id')
    if user_id:
        try:
            user=UserModel.query.get(user_id)
            g.user=user
        except Exception as e:
            print(e)
    else:
        user=None
# get/post --> before_request -->视图函数 -->上下文处理 -->渲染模板
@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user':g.user}
    else:
        return {'user':None}

# 自定义时间过滤器
@app.template_filter('to_date')
def to_date(value):
    return value.date()


if __name__ == '__main__':
    app.run()
