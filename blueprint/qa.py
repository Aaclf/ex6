from flask import Blueprint, render_template, g, request, redirect, url_for, flash, send_from_directory
from decorators import login_required
from .forms import QuestionForm, CommentForm
from models import QuestionModel, CommentModel, CollectModel, UserModel, FileModel
from exts import db
from sqlalchemy import or_, and_
import os
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

bp = Blueprint("qa", __name__, url_prefix='/')


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = QuestionModel.query.order_by(db.text('-id')).paginate(page, per_page=5, error_out=False)
    questions = pagination.items
    users = UserModel.query.order_by(db.text('-id')).all()
    return render_template('index.html', questions=questions, users=users, pagination=pagination)


@bp.route('/question/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("标题或内容格式错误!")
            return redirect(url_for("qa.public_question"))


@bp.route('/question/<int:question_id>')
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)


@bp.route('/comment/<int:question_id>', methods=['POST'])
@login_required
def comment(question_id):
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        comment_model = CommentModel(content=content, author=g.user, question_id=question_id)
        db.session.add(comment_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        flash("表单验证失败")
        return redirect(url_for("qa.question_detail", question_id=question_id))


@bp.route('/search')
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q)))
    return render_template('index.html', questions=questions)


@bp.route('/collect/<int:question_id>', methods=['GET'])
@login_required
def collect(question_id):
    ids = CollectModel.query.filter(
        and_(CollectModel.question_id.contains(question_id), CollectModel.user_id.contains(g.user.id))).first()
    print(type(ids))
    if ids:
        return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        question = QuestionModel.query.filter_by(id=question_id).first()
        collect_model = CollectModel(question_id=question_id, author_id=question.author_id, user_id=g.user.id)
        db.session.add(collect_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/python_file', methods=['GET', 'POST'])
@login_required
def python_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_model = FileModel(filename=filename)
            db.session.add(file_model)
            db.session.commit()
            flash("上传成功!")
            return redirect(url_for('qa.python_file', name=filename))
    page = request.args.get('page', 1, type=int)
    pagination = FileModel.query.order_by(db.text('id')).paginate(page, per_page=5, error_out=False)
    files = pagination.items
    return render_template('python_file.html', files=files, pagination=pagination)


@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)


@bp.route('/course')
def course():
    return render_template('course.html')

# 装饰器的使用；
# 装饰器login_required 将函数public_question作为参数传递给 decorators中的login_required函数
# 执行login_required函数 并返回到login_required函数中的 wrapper函数中
# 执行wrapper函数 并返回
