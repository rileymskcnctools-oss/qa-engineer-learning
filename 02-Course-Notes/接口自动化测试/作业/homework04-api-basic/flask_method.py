"""
创建一个 Flask 应用，包含四个路由，分别对应 HTTP 请求方法（GET、POST、PUT、DELETE）。
每个路由只需返回一个简单的字符串响应，描述该请求方法的功能。
GET 请求：返回【这是一个 get 请求！】
POST 请求：返回【这是一个 post 请求"】
PUT 请求：返回【这是一个 put 请求！】
DELETE 请求：返回【这是一个 delete 请求！】
"""
from flask import Flask

# 创建 Flask 应用程序实例
app = Flask(__name__)


# GET 请求
@app.route("/get", methods=["GET"])
def get():
    return "这是一个 get 请求！"


# POST 请求
@app.route("/post", methods=["POST"])
def post():
    return "这是一个 post 请求"


# PUT 请求
@app.route("/put", methods=["PUT"])
def put():
    return "这是一个 put 请求"


# DELETE 请求
@app.route("/delete", methods=["DELETE"])
def delete():
    return "这是一个 delete 请求"


if __name__ == '__main__':
    app.run(debug=True, port=5500)
