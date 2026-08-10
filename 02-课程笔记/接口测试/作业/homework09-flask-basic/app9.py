from flask import request, jsonify,Flask


app = Flask(__name__)
users_db = {
    "admin": {
        "password": "123456"
    }
}

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in users_db:
        return jsonify({"message": "username already exists"})
    if len(password)<6 :
        return jsonify({"message": "password is too short"})
    else:
        users_db[username] = {"password":password}
        # users_db.setdefault(username, {"password":password})

    return jsonify({"message": "register success"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if len(password)<6:
        return jsonify({"message": "password is too short"})
    # get 安全访问 value ，若无返回值，默认返回 None
    elif users_db.get(username) == {"password":password}:
        return jsonify({"message": "login success"})
    else:
        return jsonify({"message": "username or password is wrong"})

if __name__ == "__main__":
    app.run(debug=True,port=5800)