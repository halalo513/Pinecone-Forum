from wtforms import Form, StringField, ValidationError, FileField

from flask_wtf.file import FileRequired, FileAllowed

from wtforms.validators import Length, Email, EqualTo, InputRequired

from models import UserModel

from redis_cache import cache

# 注册表单验证
class RegisterForm(Form):
    username = StringField(validators=[Length(5, 20)])
    email = StringField(validators=[Email()])
    captcha=StringField(validators=[InputRequired(), Length(4, 4)])
    password=StringField(validators=[Length(5, 20)])
    password_confirm=StringField(validators=[EqualTo("password")])
    def validate_captcha(self, field):
        captcha=field.data
        email=self.email.data
        raw_captcha=cache.get(email)
        if raw_captcha:
            cache_captcha = raw_captcha.decode()  # 从redis中取出的是b'' 需要decode一下
        else:
            raise ValidationError(u'请先获取验证码')
        if cache_captcha.lower()!=captcha.lower():
            raise ValidationError(u"邮箱验证码错误")

    def validate_email(self,field):
        email=field.data
        user_model=UserModel.query.filter_by(email=email).first()
        if user_model:
            raise ValidationError(u"您已经注册过")

    def validate_username(self,field):
        username=field.data
        user_model=UserModel.query.filter_by(username=username).first()
        if user_model:
            raise ValidationError(u"用户名已被占用")

# 登录表单验证
class LoginForm(Form):
    email = StringField(validators=[Email()])
    password=StringField(validators=[Length(5, 20)])

# 文章发布表单验证
class ReleaseForm(Form):
    title = StringField(validators=[Length(min=3, max=100)])
    content=StringField(validators=[Length(min=5)])

# 评论回复表单验证
class AnswerForm(Form):
    content=StringField(validators=[InputRequired(), Length(min=5)])

# 修改基本信息表单验证
class AlterForm(Form):
    new_username = StringField(validators=[Length(5, 20)])
    new_password = StringField(validators=[Length(5, 20)])
    new_signature = StringField(validators=[Length(min=5)])
    def validate_new_username(self,field):
        new_username=field.data
        user_model=UserModel.query.filter_by(username=new_username).first()
        if user_model:
            raise ValidationError(u"用户名已被占用")
# 上传头像表单验证
class AvatarForm(Form):
    avatar=FileField(validators=[FileRequired(), FileAllowed(['png','jpeg','jpg','bmp', 'gif'])])