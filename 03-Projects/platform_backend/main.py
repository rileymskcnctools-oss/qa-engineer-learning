# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


from flask import Flask

# 创建 flask 应用程序实例
app = Flask(__name__)

# 定义路由和视图函数
@app.route("/")
def hello():
    return "Hello Flask"


if __name__ == "__main__":
    app.run()