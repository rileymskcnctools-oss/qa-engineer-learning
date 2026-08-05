from flask import Flask

# 创建flask应用实例
app = Flask(__name__)

@app.route("/get", methods=["GET"])
def get():
    return "这是一个get 请求！"

# 浏览器地址栏只能发送 GET 请求，所以 /get 可以直接访问；
# POST、PUT、DELETE 需要通过表单、Postman、requests 等工具主动指定 HTTP 方法，
# 否则浏览器发送的仍然是 GET，Flask 就无法匹配对应路由

@app.route("/post", methods=["POST"])
def post():
    return "这是一个 post请求"

@app.route("/put", methods=["PUT"])
def put():
    return "这是一个 put请求！"


@app.route("/delete", methods=["DELETE"])
def delete():
    return "这是一个delete 请求！"

if __name__ == "__main__":
    app.run(debug=True)