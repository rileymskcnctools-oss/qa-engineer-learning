from flask import Flask,request

app = Flask(__name__)

@app.route("/json",methods=["POST"])

def json_response():
    data=request.json
    name=data.get("name")
    gender=data.get("gender")
    return f"name:{name},gender:{gender}"

if __name__ == "__main__":
    app.run(debug=True)