from flask import Flask, url_for, redirect,Blueprint

# 创建 Flask 应用程序实例
app = Flask(__name__)

login_api = Blueprint("login", __name__, url_prefix="/login")
index_api = Blueprint("index", __name__, url_prefix="/index")

@login_api.route("")
def login():
    print("登录，成功后跳转到首页")
    # return url_for("index.index")
    return redirect(url_for("index.index"))

@index_api.route("")
def index():
    print("首页")
    return {"code": 0, "msg": "success"}


# 运行应用程序
if __name__ == '__main__':
    app.register_blueprint(index_api)
    app.register_blueprint(login_api)
    app.run(debug=True, port=5055)

