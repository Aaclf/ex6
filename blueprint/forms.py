import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel




class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=5, max=20)])
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=5, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_captcha(self, field):  # 邮箱验证码的验证
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误！")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("该邮箱已被注册！")


class LoginForm(wtforms.Form):
    password = wtforms.StringField(validators=[length(min=5, max=20)])
    email = wtforms.StringField(validators=[email()])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=100)])
    content = wtforms.StringField(validators=[length(min=5)])


class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=5)])
    question_id = wtforms.StringField(validators=[InputRequired()])


class CollectForm(wtforms.Form):
    question_id = wtforms.StringField(validators=[InputRequired()])


