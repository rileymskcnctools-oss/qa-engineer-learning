from flask import Flask
from user import user_blueprint
from task import task_blueprint


app = Flask(__name__)
# 解决中文JSON转义
app.json.ensure_ascii = False

# 注册蓝图

app.register_blueprint(
    user_blueprint
)

app.register_blueprint(
    task_blueprint
)


@app.route("/")
def index():
    return "Flask Blueprint Demo"


if __name__ == "__main__":

    app.run(debug=True,port=5500)