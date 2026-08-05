from flask import request, jsonify

from . import user_blueprint

from database import users_db


# 注册接口
@user_blueprint.route("/register", methods=["POST"])
def register():

    data = request.json

    username = data.get("username")
    password = data.get("password")


    if username in users_db:
        return jsonify({
            "message": "用户已经存在"
        })


    users_db[username] = password


    return jsonify({
        "message": "注册成功",
        "username": username
    })



# 登录接口
@user_blueprint.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")
    password = data.get("password")


    if users_db.get(username) == password:

        return jsonify({
            "message": "登录成功"
        })


    return jsonify({
        "message": "用户名或密码错误"
    })