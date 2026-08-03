from flask import Flask

# 创建 Flask 应用
app = Flask(__name__)


# 首页路由
@app.route("/")
def index():
    return "<h1>Hello, Flask!</h1><p>我的第一个 Flask Web 应用</p>"


# 另一条路由，演示路由功能
@app.route("/hello/<name>")
def hello(name):
    return f"<h1>你好，{name}！</h1><p>欢迎来到 Flask 世界</p>"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
