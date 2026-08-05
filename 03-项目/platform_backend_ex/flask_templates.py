from flask import Flask, render_template

# 创建 Flask 应用程序实例
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hogwarts.html")

@app.route("/data")
def hogwarts():
    return render_template("hogwarts.html", name="hogwarts")

@app.route("/person")
def person():
    person = {
        "name": "Tom",
        "age": 18,
        "gender": "male"
    }
    return render_template("person.html", person=person)

@app.route("/people")
def people():
    people = [
        {
            "name": "lily",
            "age": 18,
            "gender": "female"
        },
        {
            "name": "tom",
            "age": 19,
            "gender": "male"
        },
    ]
    return render_template("people.html", people=people)


# 运行应用程序
if __name__ == '__main__':
    app.run(port=5055, debug=True)
