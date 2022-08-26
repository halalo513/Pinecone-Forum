import random, string, os, time

from flask import Blueprint, render_template, request, flash, redirect, url_for, g, jsonify

from decorators import login_required

from forms import ReleaseForm, AnswerForm, UserModel, AvatarForm, AlterForm

from models import QuestionModel, AnswerModel

from exts import db

from sqlalchemy import or_

from werkzeug.security import generate_password_hash

from werkzeug.utils import secure_filename

from echarts import Answers_Bar_Chart, WordCloud_Chart

qa_bp=Blueprint("QA", __name__)

# 定义上传头像文件的路径
UPLOAD_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/img/avatars')

# 首页视图函数
@qa_bp.route('/')
def index():
    page_index=request.args.get('page_index', 1)
    questions=QuestionModel.query.order_by(db.text('-create_time')).paginate(page=int(page_index), per_page=6)
    return render_template('index.html', questions=questions)

# 发布问答视图函数
@qa_bp.route('/release/', methods=['GET', 'POST'])
@login_required
def release():
    if request.method=='GET':
        return render_template('release.html')
    else:
        form=ReleaseForm(request.form)
        if form.validate():
            title=form.title.data
            content=form.content.data
            question=QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('QA.index'))
        else:
            flash("标题或内容格式错误！")
            return redirect(url_for('QA.release'))

# 问答文章详情视图函数
@qa_bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question=QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)

# 回复问答视图函数
@qa_bp.route('/answer/<int:question_id>/', methods=['POST'])
@login_required
def answer(question_id):
    form=AnswerForm(request.form)
    if form.validate():
        content=form.content.data
        answer_model=AnswerModel(content=content,question_id=question_id, author=g.user)
        db.session.add(answer_model)
        db.session.commit()
        flash('评论成功！')
    else:
        flash('表单验证失败！')
    return redirect(url_for('QA.detail', question_id=question_id))

# 搜索功能视图函数
@qa_bp.route('/search/', methods=['POST'])
def search():
    q=request.form.get('q')
    questions=QuestionModel.query.filter\
        (or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q)))\
        .order_by(db.text('-create_time')).all()
    return render_template('search.html', questions=questions)

# 个人中心视图函数
@qa_bp.route('/center/')
@login_required
def center():
    bar_line=Answers_Bar_Chart()
    wordcloud=WordCloud_Chart()
    context={
        "bar_option": bar_line.dump_options(),
        "wordcloud_option": wordcloud.dump_options()
    }
    return render_template('person_center.html', **context)

# 修改个人基本信息视图函数
@qa_bp.route('/alter_basic_info/', methods=['POST'])
@login_required
def alter_basic_info():
    form=AlterForm(request.form)
    if form.validate():
        user=UserModel.query.get(g.user.id)
        user.username=request.form.get('new_username')
        user.password=generate_password_hash(request.form.get('new_password'))
        user.extend.signature=request.form.get('new_signature')
        db.session.commit()
        return jsonify({'code':200, 'message':'修改成功'})
    else:
        return jsonify({'code':400, 'message':'修改失败'})

# 上传头像文件视图函数
@qa_bp.route('/upload_avatar/', methods=['POST'])
@login_required
def upload():
    form=AvatarForm(request.files)
    if form.validate():
        avatar=request.files.get('avatar')
        timestamp=str(int((time.time())*1000))
        letters = string.ascii_letters + string.digits  # a-zA-z0-9
        words = "".join(random.sample(letters, 4))
        suffix=os.path.splitext(avatar.filename)[1]
        avatar.filename=timestamp+words+suffix
        avatar.save(os.path.join(UPLOAD_PATH, secure_filename(avatar.filename)))
        user=UserModel.query.get(g.user.id)
        user.extend.avatar_name=avatar.filename
        db.session.commit()
        return jsonify({'code':200, 'message':'上传成功'})
    else:
        return jsonify({'code':400, 'message':'上传失败'})

