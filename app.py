import config
from flask import Flask, session, g
from flask_migrate import Migrate
from exts import db, mail
from models import UserModel
from blueprint import qa_bp
from blueprint import user_bp


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)        # 数据库绑定app
migrate = Migrate(app, db)      # 数据库迁移绑定app和数据库
mail.init_app(app)      # 邮箱绑定app
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


# 一个请求 -> before request -> 视图函数 -> 视图函数中返回模板 -> context processor
@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            # 给g绑定一个user的变量
            # setattr(g, "user", user)
            g.user = user
        else:
            g.user = None


@app.context_processor   # 上下文处理，渲染的所有模板都执行这个代码
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
