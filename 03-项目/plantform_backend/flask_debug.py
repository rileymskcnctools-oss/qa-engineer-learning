# 创建 flask 应用程序实例
from flask import Flask

app = Flask(__name__)

# 定义路由和视图函数
@app.route("/")
def hello():
    return "Hello"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5050,debug=True)