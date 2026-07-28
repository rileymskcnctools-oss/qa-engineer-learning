---
tags: [课程笔记, 接口测试, Flask]
course: "接口测试"
chapter: "Ch02-Flask入门"
created: 2026-07-28
status: draft
---

# Ch02 - Flask 环境安装与配置

> 前置：[[Ch01-接口协议基础]] — HTTP、RESTful、GET/POST

## 课程来源
- 学习日期：

---

## 一、Flask 简介

### 知识点 1：Flask 是什么、为什么学它

【课程原话/定义】
Flask 是一个轻量级的 Python Web 开发框架，依赖 Jinja2（模板引擎）和 Werkzeug WSGI（路由模块）两个核心。有丰富的第三方插件生态：Flask-mail、Flask-login、SQLAlchemy、Flask-RESTful 等。

【为什么？】
选 Flask 而不是 Django 学接口测试：

| 对比 | Flask | Django |
|------|-------|--------|
| 定位 | 微框架（轻量） | 全栈框架（重） |
| 学习曲线 | 低，一个文件就能跑 | 高，要理解 MTV 模式 |
| 适合场景 | API 服务、Mock 服务、微服务 | 大型 Web 应用 |
| 接口测试相关性 | 极高——快速搭建 Mock Server | 中——功能过剩 |

**学 Flask 的核心价值**：你在测试中经常需要 Mock 一个后端服务（比如上游接口还没开发完），Flask 10 行代码就能搭一个假接口返回你需要的测试数据。

【必须掌握】
- Flask 是微框架：核心很小，功能靠插件扩展
- Werkzeug：处理 HTTP 请求/响应的 WSGI 工具库
- Jinja2：模板引擎（接口测试中不太用，做页面渲染时才用到）
- Flask 安装：`pip install flask`

【企业场景】
测试场景：你要测一个功能，但它依赖"用户中心"的接口——而用户中心还没开发完。怎么办？

```python
# 用 Flask 搭一个 Mock 接口，10 行代码搞定
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/api/user/<int:uid>")
def get_user(uid):
    return jsonify({"id": uid, "name": "MockUser", "status": "active"})

app.run(port=5678)
```

你的测试代码把 `base_url` 指向 `http://localhost:5678` 就能继续写用例了。这就是接口测试工程师学 Flask 的真正价值。

【面试考察】
面试官："Flask 和 Django 有什么区别？为什么做接口测试更推荐学 Flask？"

参考回答框架：
1. Flask 轻量、灵活，一个文件就能搭建 API 服务
2. Django 功能全但重，适合大型 Web 项目
3. 测试工程师常用 Flask 搭建 Mock Server、编写测试辅助工具
4. 学习成本低，能快速进入接口测试实战

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 认为 Flask 只能做小项目 | Flask 加插件可以支撑生产级项目（如 Pinterest、LinkedIn 部分服务） |
| 把 Flask 当成唯一选择 | FastAPI 是新兴替代（性能更好、自带参数校验），但 Flask 生态更成熟 |

【我的理解】
> （对比 Flask 和之前学的 Python 基础：Flask 里的 `@app.route("/")` 装饰器是怎么把 URL 和函数绑定在一起的？这跟面向对象中的装饰器概念有什么关系？）

---

## 二、Flask 最小应用

### 知识点 2：第一个 Flask 应用

【课程原话/定义】
最小 Flask 应用只需要三步：导入 Flask → 创建实例 → 定义路由和视图函数 → 运行。

```python
from flask import Flask

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 定义路由和视图函数
@app.route("/")
def hello():
    return "Hello Flask!"

# 运行应用程序
if __name__ == '__main__':
    app.run()
```

访问 `http://localhost:5000/` 即可看到 "Hello Flask!"。

【为什么？】
逐行解释这个"最小应用"的每个部分：

1. `app = Flask(__name__)` — `__name__` 告诉 Flask 当前模块名，用于定位静态文件和模板
2. `@app.route("/")` — 装饰器语法，把 URL 路径 `/` 和函数 `hello()` 绑定
3. `def hello()` — 视图函数，返回值就是 HTTP 响应体
4. `app.run()` — 启动内置开发服务器（默认 `127.0.0.1:5000`）

这就是一个完整的 Web 应用！没有配置文件、没有数据库、没有中间件——Flask 的"轻"体现在这里。

【必须掌握】
- `Flask(__name__)` 创建应用实例
- `@app.route()` 绑定 URL 和视图函数
- 视图函数 return 的内容就是 HTTP 响应体
- `app.run()` 启动服务器（开发环境）

【企业场景】
每当你需要验证一个 HTTP 概念（比如"302 重定向到底怎么工作的？"）——最快的学习方式不是看书，是写一个 3 行的 Flask 应用自己测试。Flask 让 HTTP 从抽象变成可以动手验证的东西。

【面试考察】
面试官："`Flask(__name__)` 中的 `__name__` 参数是什么作用？"

参考回答框架：
1. `__name__` 是当前 Python 模块的名称
2. Flask 用这个参数确定应用的根路径（找静态文件、模板文件的位置）
3. 如果是主模块运行（`python app.py`），`__name__` 就是 `"__main__"`

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 视图函数同名 | 每个视图函数名必须唯一（Flask 用函数名做 URL 映射） |
| 改了代码没重启 | 开发服务器不会自动重载——要么手动重启，要么用 `debug=True` |
| `app.run()` 放在 `@app.route` 前面 | `app.run()` 会阻塞，放前面会导致后面的路由注册不执行 |

【我的理解】
> （把最小应用代码手敲一遍（不要复制粘贴），运行起来，用浏览器和 curl 各访问一次。观察：curl 能看到完整的 HTTP 响应报文吗？怎么看？）

---

### 知识点 3：运行方式 — `app.run()` vs `flask run`

【课程原话/定义】
两种运行方式：

**方式一：代码调用** `app.run()`
```python
if __name__ == '__main__':
    app.run()
```

**方式二：命令行** `flask run`
```bash
# Linux / Mac
$ export FLASK_APP=hello.py
$ flask run

# Windows (cmd)
> set FLASK_APP=hello.py
> flask run
```

【为什么？】
`app.run()` 简单直接，适合学习调试。`flask run` 是生产推荐方式：可以配合环境变量控制 host、port、debug 模式，不需要改代码。

【必须掌握】
- `app.run()` 默认 `127.0.0.1:5000`
- `flask run` 需要设置 `FLASK_APP` 环境变量
- 开发模式建议 `debug=True`（代码改动自动重载 + 错误页面有调试信息）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `flask run` 报 "Could not locate a Flask application" | 没设 `FLASK_APP` 环境变量，或者文件名不对 |
| Windows 下用了 `export` | Windows cmd 用 `set`，PowerShell 用 `$env:FLASK_APP="hello.py"` |
| `app.run()` 后代码不往下执行 | `run()` 会阻塞（一直监听请求），这是正常行为 |

【我的理解】
> （在你的电脑上分别用两种方式各启动一次 Flask 应用。哪种更方便？你觉得写测试脚本时该用哪种？）

---

## 三、接口路由技术

### 知识点 4：基本路由

【课程原话/定义】
路由是将 URL 地址与应用程序中的函数相映射的过程。Flask 使用 `@app.route()` 装饰器定义路由。

```python
@app.route("/")
def index():
    return "Home Page"

@app.route("/about")
def about():
    return "About Page"
```

`/` 访问 `http://127.0.0.1:5000/`，`/about` 访问 `http://127.0.0.1:5000/about`。

【为什么？】
路由是 Web 框架最核心的概念。每一个 URL 对应一个处理函数——这就是后端开发的基本模型。理解了路由，就理解了"浏览器输入一个地址后发生了什么"中"服务器端"的部分。

【必须掌握】
- `@app.route("/路径")` 定义路由
- 不同路径对应不同视图函数
- 路由是 URL → 函数的映射

【我的理解】
> （创建 3 个路由分别返回不同的字符串，用浏览器逐一访问验证。）

---

### 知识点 5：动态路由

【课程原话/定义】
URL 中的可变部分用 `<变量名>` 表示，Flask 会自动提取并作为参数传给视图函数。

```python
@app.route("/user/<username>")
def user_info(username):
    return f"User {username} is select info."
```

访问 `/user/Harry` → `username = "Harry"`；访问 `/user/Ron` → `username = "Ron"`。

【为什么？】
实际项目中最常见的场景：`/user/1`、`/user/2`、`/user/999`——不可能为每个用户 ID 都写一个路由。动态路由让一个路由规则匹配一组 URL。接口测试中，80% 的接口都包含动态参数（用户 ID、订单号等）。

【必须掌握】
- `<变量名>` 定义动态路由，变量值自动传入视图函数的同名参数
- 变量默认是字符串类型

【企业场景】
Mock 一个用户查询接口：不管传什么 `uid`，都返回固定结构——这样你的前端/测试代码可以用不同 ID 测试分页、异常等场景。

```python
@app.route("/api/user/<int:uid>")
def mock_user(uid):
    if uid == 0:
        return {"error": "user not found"}, 404
    return {"id": uid, "name": f"user_{uid}", "status": "active"}
```

【我的理解】
> （写一个动态路由 `/product/<name>`，根据不同的产品名返回不同的描述信息。试试中文参数能正常传递吗？）

---

### 知识点 6：限定类型的动态路由

【课程原话/定义】
使用 `<类型:变量名>` 限定动态字段的类型。Flask 支持的类型：`int`、`float`、`string`（默认）、`path`（可包含 `/` 的字符串）。

```python
# 限定为整数
@app.route("/user/<int:user_id>")
def user_id(user_id):
    return f"User ID is {user_id}"

# path 类型：可以包含 /
@app.route('/path/<path:sub_path>')
def show_subpath(sub_path):
    return f'Subpath is {sub_path}'
```

【为什么？】
类型限定不只是"方便"——它是安全保障。如果只定义 `<user_id>`（默认 string），用户访问 `/user/abc` 也能匹配，但后续代码可能 `int(user_id)` 报 500。用 `<int:user_id>` 后，`/user/abc` 直接返回 404（不匹配路由规则），避免代码崩溃。

【必须掌握】
- `int`：只匹配整数
- `float`：只匹配浮点数
- `string`：默认类型，不含 `/` 的字符串
- `path`：可包含 `/` 的字符串

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 用 `string` 存 ID 然后手动转 int | 直接用 `<int:id>`，让 Flask 做类型校验 |
| `path` 和 `string` 混用 | `path` 能匹配 `/`，适合文件路径；普通动态参数用 `string` |

【面试考察】
面试官："Flask 路由中 `<int:id>` 和 `<string:id>` 有什么区别？如果传入非法类型会发生什么？"

参考回答框架：
1. `<int:id>` 只匹配整数字符串，传入 `abc` 直接 404
2. `<string:id>` 匹配不含 `/` 的任意字符串
3. 类型限定在路由层就完成了校验，不需要在视图函数里手动判断

【我的理解】
> （分别测试传入正确类型和错误类型时，Flask 返回什么？用 curl 看一下 404 时的完整响应报文。）

---

### 知识点 7：路由末尾 `/` 的规则

【课程原话/定义】
两个路由定义看起来类似但不一样：

```python
@app.route('/about')      # 尾部没有 /
def about():
    return 'About Page'

@app.route('/hogwarts/')  # 尾部有 /
def hello_hogwarts():
    return 'Hello Hogwarts'
```

有 `/` 的是"规范 URL"：访问时不带 `/`，Flask 会自动 308 重定向到带 `/` 的地址。没有 `/` 的：访问时带 `/` 会返回 "Not Found"。

【为什么？】
这是 Flask（底层 Werkzeug）的设计规则——保持 URL 唯一性。类比文件系统：`/about` 像文件，`/hogwarts/` 像目录。访问目录时不加 `/`，系统自动帮你加上。

【必须掌握】
- 路由定义尾部有 `/` → 类似目录，访问时不带 `/` 自动重定向
- 路由定义尾部没有 `/` → 类似文件，访问时带 `/` 会 404
- 这是 Werkzeug 的路由规则，不是 Flask 独有的

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 访问 `/about/` 报 404，以为代码有 bug | 检查路由定义有没有尾部 `/` |
| API 设计时混用带/和不带/ | 团队应统一风格（RESTful 通常不带尾部 `/`） |

【我的理解】
> （在 Flask 中同时定义 `/test` 和 `/test/` 会发生什么？试试看，解释结果。）

---

## 四、请求方法

### 知识点 8：Flask 中设置请求方法

【课程原话/定义】
Flask 默认只支持 GET 请求。通过 `methods` 参数指定支持的请求方法。

```python
# 默认只支持 GET
@app.route("/get")
def get():
    return f"Method is GET."

# 显式指定 GET
@app.route("/get_method", methods=["GET"])
def get_method():
    return f"GET method success."

# POST
@app.route("/post", methods=["POST"])
def post():
    return f"Method is POST."

# PUT
@app.route("/put", methods=["PUT"])
def put():
    return f"Method is PUT."

# DELETE
@app.route("/delete", methods=["DELETE"])
def delete():
    return f"Method is DELETE."
```

【为什么？】
RESTful 架构的核心：同一个 URL，不同 HTTP Method 对应不同操作。比如 `/user/1`：
- GET → 查询用户
- PUT → 更新用户
- DELETE → 删除用户

Flask 的 `methods` 参数让一个路由支持多种方法。

【必须掌握】
- 不指定 `methods` 时默认 `["GET"]`
- `methods` 参数是列表：`methods=["GET", "POST"]`
- 用不支持的 Method 访问会返回 405 Method Not Allowed
- 测试非 GET 方法：浏览器地址栏只能发 GET，需用 curl 或 Postman

【企业场景】
接口测试中，最常见的 bug 之一：API 文档说这个接口支持 POST，但你用 POST 请求返回 405——说明开发只配了 GET。这时候你能定位到是 `methods` 参数漏配了。

```bash
# curl 测试不同请求方法
curl -X POST http://127.0.0.1:5000/post    # POST
curl -X PUT http://127.0.0.1:5000/put      # PUT
curl -X DELETE http://127.0.0.1:5000/delete # DELETE
```

【面试考察】
面试官："Flask 中如何让一个路由同时支持 GET 和 POST？不指定 methods 时默认是什么？"

参考回答框架：
1. `@app.route("/path", methods=["GET", "POST"])`
2. 不指定时默认为 GET
3. 方法不对返回 405 Method Not Allowed

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 用浏览器直接访问 POST 路由 | 浏览器地址栏只能发 GET，用 curl/Postman 测试 POST |
| `methods="POST"`（不是列表） | 必须是列表：`methods=["POST"]` |
| 同一路由定义了两次 GET | 后定义的会覆盖先定义的 |

【我的理解】
> （创建 4 个路由分别处理 GET/POST/PUT/DELETE，用 curl 逐一测试。观察 405 错误的响应状态码和响应体长什么样。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Flask 简介 | 微框架；Werkzeug + Jinja2；vs Django | ★★★☆☆ |
| 最小应用 | `Flask(__name__)` + `@app.route` + `app.run()` | ★★★★☆ |
| 运行方式 | `app.run()` vs `flask run` + `FLASK_APP` | ★★★☆☆ |
| 基本路由 | `@app.route("/path")` → 视图函数 | ★★★★★ |
| 动态路由 | `<变量名>` 提取 URL 参数 | ★★★★★ |
| 类型限定 | `<int:x>` `<float:x>` `<path:x>` | ★★★★☆ |
| 路由 `/` 规则 | 有 `/` 自动重定向；无 `/` 严格匹配 | ★★★☆☆ |
| 请求方法 | `methods=["GET","POST","PUT","DELETE"]` | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-接口协议基础]]
- [[../Python/Ch04-函数定义与调用]]
- [[../Python/Ch22-面向对象入门]]
- [[../Python/Ch23-面向对象进阶]]
