import string

from redis_cache import cache

from flask import (Blueprint,
                   render_template,
                   request, redirect,
                   url_for, jsonify,
                   session, flash)

from exts import mail

from flask_mail import Message

import random

from models import UserModel, UserExtendModel

from datetime import datetime

from exts import db

from forms import RegisterForm, LoginForm

from werkzeug.security import generate_password_hash, check_password_hash # 加密明文密码

user_bp=Blueprint('user', __name__, url_prefix='/user')

# 登录功能视图函数
@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        form=LoginForm(request.form)
        if form.validate():
            email=form.email.data
            password=form.password.data
            user_model=UserModel.query.filter_by(email=email).first()
            if user_model and check_password_hash(user_model.password, password):
                # 如果登录成功，就设置session, 方便钩子函数before_request()处理
                session['user_id']=user_model.id
                return redirect(url_for('QA.index'))
            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for('user.login'))
        else:
            flash("邮箱或者密码格式错误！")
            return redirect(url_for('user.login'))

# 注册功能视图函数
@user_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        form=RegisterForm(request.form)
        if form.validate():
            username=form.username.data
            email=form.email.data
            password=form.password.data
            # 加密明文密码
            hash_password=generate_password_hash(password)
            user=UserModel(username=username, email=email, password=hash_password)
            user_extend=UserExtendModel()
            user_extend.user=user
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            print(form.errors)
            flash('注册失败！请重试！')
            return redirect(url_for('user.register'))

# 获取验证码视图函数
@user_bp.route('/captcha/', methods=['POST'])
def get_captcha():
    email=request.form.get('email')
    if email:
        letters=string.ascii_letters+string.digits  # a-zA-z0-9
        captcha="".join(random.sample(letters, 4))
        message=Message(
            subject=u'松果论坛验证码',
            recipients=[email],
            body=u'【松果论坛】 您的注册验证码是：{captcha}'.format(captcha=captcha),
        )
        # 发送邮件
        mail.send(message)
        # 将验证码存进redis缓存中，过期时间设置为60s
        cache.set(email, captcha, ex=60)
        # 200表示邮箱验证码：Ajax发送成功
        return jsonify({"code":200})
    else:
        # 400表示客户端错误
        return jsonify({"code":400, "message":"请先传递邮箱"})

# 退出登录视图函数
@user_bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('QA.index'))

