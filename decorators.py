from functools import wraps
from flask import g, redirect, url_for
# 自定义装饰器，登录限制
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return wrapper
