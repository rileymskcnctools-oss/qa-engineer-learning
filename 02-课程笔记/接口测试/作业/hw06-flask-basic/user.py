from flask import Flask,request, render_template

app=Flask(__name__)

@app.route("/user")
def show_user():
    # request.args.get('key')— key不存在时返回None，不会崩溃
    name = request.args.get("name")
    age = request.args.get("age")
    return render_template(
        "show_info.html",
        name=name,
        age=age
    )


if __name__ == '__main__':
    app.run(debug=True, port=5700)