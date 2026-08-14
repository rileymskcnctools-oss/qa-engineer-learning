from flask import Flask, render_template, request, redirect, url_for
from platform_backend import db

# flask 的实例化
app = Flask(__name__)


# 首页
@app.route("/")
def index():
    students = db.query_all("SELECT sid,name,age,gender FROM student_0802;")
    return render_template("index.html", students=students)


# 添加
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    name = request.form.get("name", "").split()
    age = request.form.get("age", "")
    gender = request.form.get("gender", "")
    # 数据的合理校验
    if not name:
        return "姓名不能为空", 400
    if not age.isdigit():
        return "年龄必须为数字", 400
    age = int(age)
    if not 0 < age < 150:
        return "年龄超出范围", 400
    if gender not in ("男", "女"):
        return "性别必须是男或者女", 400
    # 提交数据
    db.execute("INSERT INTO student_0802 (name,age,gender) VALUES (%s,%s,%s)", (name, age, gender))
    # 重定向到首页
    return redirect(url_for("index"))


# 修改
@app.route("/change/<int:sid>", methods=["GET", "POST"])
def change(sid):
    # 如果是get请求，反显当前的数据
    if request.method == "GET":
        # 先查询当前的学生信息
        student = db.query_one("SELECT sid,name,age,gender FROM student_0802 WHERE sid = %s;", (sid,))
        return render_template("change.html", student=student)
    # 如果是post，提交当前的form表单
    name = request.form.get("name", "").split()
    age = request.form.get("age", "")
    gender = request.form.get("gender", "")
    # 数据的合理校验
    if not name:
        return "姓名不能为空", 400
    if not age.isdigit():
        return "年龄必须为数字", 400
    age = int(age)
    if not 0 < age < 150:
        return "年龄超出范围", 400
    if gender not in ("男", "女"):
        return "性别必须是男或者女", 400

    # 执行修改操作
    # _rows = db.execute(f"UPDATE student_0802 SET name= {name},age={age},gender={gender} WHERE sid={sid}")  # 错误演示，有SQL注入风险
    _rows = db.execute("UPDATE student_0802 SET name= %s,age=%s,gender=%s WHERE sid=%s", (name, age, gender, sid))
    return redirect("/")


# 删除
# jinja 不支持delete的发起

@app.route("/delete/<int:sid>", methods=["DELETE", "POST"])
def delete(sid):
    _rows = db.execute("DELETE FROM student_0802 WHERE sid=%s", (sid,))
    return redirect("/")


# 启动服务

if __name__ == '__main__':
    app.run()
