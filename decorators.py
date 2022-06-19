from flask import g, redirect, url_for, render_template
from functools import wraps


def login_required(func):   # func: 传递进来的函数
    @wraps(func)
    def wrapper(*args, **kwargs):   # *args, **kwargs：代表你要传递的所有参数
        if hasattr(g, "user"):
            return func(*args, **kwargs)
        else:
            return render_template("go_login.html")

    return wrapper


