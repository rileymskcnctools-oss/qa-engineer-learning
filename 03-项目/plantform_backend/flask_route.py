from flask import Flask

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 定义基本路由
@app.route("/")
def index():
    return "Home Page"

@app.route("/about")
def about():
    return "About Page"

# 定义动态路由
@app.route("/user/<username>")
def user_info(username):
    return f"User {username} is select info."

# 限定类型的动态路由
# 类型限定为整型
@app.route("/user/<int:user_id>")
def user_id(user_id):
    # 展示给定的用户 ID，ID 为整型
    return f"User ID is {user_id}"

# 类型限定为 path（可以包含 /）
@app.route('/path/<path:sub_path>')
def show_subpath(sub_path):
    # 展示 path 后的子路由
    return f'Subpath is {sub_path}'

@app.route('/hogwarts/')
def hello_hogwarts():
   return 'Hello Hogwarts'

# 运行应用程序
if __name__ == '__main__':
    app.run()
