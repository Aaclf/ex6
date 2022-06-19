from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
    session,
    g,
)
import os
from exts import db, mail
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, QuestionModel, CollectModel, FileModel
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from decorators import login_required


bp = Blueprint("user", __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login_form = LoginForm(request.form)
        # print(login_form.validate())
        if login_form.validate():
            email = login_form.email.data
            password = login_form.password.data
            model = UserModel.query.filter_by(email=email).first()
            if model and check_password_hash(model.password, password):
                session['user_id'] = model.id
                return redirect(url_for('qa.index'))
            else:
                flash("密码或邮箱输入错误！")
                return redirect(url_for("user.login"))
        else:
            flash("请输入密码和邮箱！")
            return redirect(url_for("user.login"))


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        register_form = RegisterForm(request.form)
        if register_form.validate():
            email = register_form.email.data
            username = register_form.username.data
            password = register_form.password.data

            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            flash("注册失败, 邮箱已被使用, 请重新注册")
            return redirect(url_for("user.register"))


@bp.route('/logout')
def logout():
    # 清除session
    session.clear()
    return redirect(url_for("user.login"))


@bp.route('/captcha', methods=['POST'])
def get_captcha():
    email = request.form.get("email")
    letters = string.ascii_letters + string.digits
    captcha = "".join(random.sample(letters, 4))
    print(captcha)
    if email:
        message = Message(
            subject="【小白】",
            recipients=[email],
            body=f'你的注册验证码是：{captcha}'
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        # code: 200, 正常的，成功的请求
        return jsonify({"code": 200})
    else:
        # code: 400, 客户端错误
        return jsonify({"code": 400, "message": "请先输入邮箱"})


@bp.route('/user_center')
@login_required
def user_center():
    questions = QuestionModel.query.filter_by(author_id=g.user.id).all()
    collects = CollectModel.query.filter_by(user_id=g.user.id).all()
    users = UserModel.query.order_by(db.text('id')).all()
    return render_template('user_center.html', questions=questions, collects=collects, users=users)


# 删除用户
@bp.route('/delete/<int:user_id>')
def delete(user_id):
    user = UserModel.query.get(user_id)
    collects = CollectModel.query.filter(
        or_(CollectModel.question_id.contains(user_id), CollectModel.user_id.contains(user_id)))
    db.session.delete(user, collects)
    db.session.commit()
    return redirect(url_for('user.user_center'))


# 修改头像
# @bp.route('/user_center/change_icon', methods=['POST', 'GET'])
# def change_icon():
#     if request.method == 'POST':
#         if 'image' in request.files:
#             objFile = request.files.get('image')
#             strFileName = objFile.filename
#             strFilePath = "./static/upload/"+strFileName
#             objFile.save(strFilePath)
#     return render_template('change_icon.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=['GET', 'POST'])
def change_icon():
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
            return redirect(url_for('user.change_icon', name=filename))
    files = FileModel.query.all()
    return render_template('change_icon.html', files=files)


