from flask import Flask

# 创建 Flask 应用程序实例
app = Flask(__name__)


# get 请求
@app.route("/get")
def get():
    return f"Method is GET."

@app.route("/get_method", methods=["GET"])
def get_method():
    return f"GET method success."


# post 请求
@app.route("/post", methods=["POST"])
def post():
    return f"Method is POST."

# put 请求
@app.route("/put", methods=["PUT"])
def put():
    return f"Method is PUT."

# delete 请求
@app.route("/delete", methods=["DELETE"])
def delete():
    return f"Method is DELETE."

if __name__ == '__main__':
    app.run()
