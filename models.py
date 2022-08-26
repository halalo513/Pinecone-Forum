from exts import db

from datetime import datetime

# 用户模型和用户扩展信息模型一对一
# 用户模型和用户发布问答文章模型一对多
# 用户评论回复模型是用户模型和用户发布问答文章模型的中间表

# 定义用户模型
class UserModel(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    password=db.Column(db.String(128), nullable=False) # 密码进行加密，所有长度必须要足够长
    join_time = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):
        return '<UserModel({email},{password})>'.format(email=self.email, password=self.password)

# 定义用户扩展信息模型
class UserExtendModel(db.Model):
    __tablename__='user_extend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avatar_name=db.Column(db.String(100), default='avatar.jpeg')
    signature = db.Column(db.Text)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship('UserModel', backref=db.backref('extend', uselist=False))

# 定义用户发布问答文章模型
class QuestionModel(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content=db.Column(db.Text, nullable=False)
    create_time=db.Column(db.DateTime, default=datetime.now)
    author_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    author=db.relationship('UserModel', backref=db.backref('questions', order_by=create_time.desc()))

# 定义用户评论回复模型
class AnswerModel(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author=db.relationship('UserModel', backref='answers')
    question=db.relationship('QuestionModel', backref=db.backref('answers', order_by=create_time.desc()))

