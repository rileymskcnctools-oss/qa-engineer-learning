from flask import Flask, jsonify, make_response, render_template

# 创建 Flask 应用程序实例
app = Flask(__name__)


# 定义路由和视图函数
@app.route('/text')
def text_res():
    return '返回文本'

@app.route('/tuple')
def tuple_res():
    return "你好呀", 200, {"hogwarts": "Harry"}

@app.route('/json')
def get_json():
    # jsonify({'status': 0})
    return jsonify(status=1, name="lily", age=20)
# 定义路由和视图函数
@app.route('/dict')
def get_dict():
    print("进入dict接口")
    return {'status': 0}

@app.route('/html')
def get_html():
    return render_template('demo.html')

@app.route('/')
def index():
    resp = make_response(render_template('demo.html'))
    # 设置 Cookie
    resp.set_cookie('username', 'the username')
    # 设置自定义响应头
    resp.headers["hogwarts"] = "Hary"
    return resp


# 运行应用程序
if __name__ == '__main__':
    print(app.url_map)
    app.run()
