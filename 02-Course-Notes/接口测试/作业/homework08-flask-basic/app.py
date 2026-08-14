from flask import Flask, redirect, request

app=Flask(__name__)

users_list=[
    {'username':'admin','password':'123123'},
    {'username':'riley','password':'999999'}
]

@app.route('/home/user',methods=['GET'])
def index():
    username = request.args.get('username') #获取浏览器传的用户名
    for user in users_list:
        if username == user.get("username"):
            return redirect(f"/dashboard?username={username}")

    return redirect("/login")

@app.route('/login')
def login():
    return "Please log in"

@app.route('/dashboard')
def dashboard():
    return f"Welcome to the Dashboard,{request.args.get('username')}"

if __name__=='__main__':
    app.run(debug=True,port=5600)
