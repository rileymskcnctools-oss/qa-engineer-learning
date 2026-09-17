---
tags: [课程笔记, Flask, 插件]
course: "Flask"
chapter: "Ch23-Flask插件-鉴权"
created: 2026-09-17
status: in_progress
---

# Ch23 - Flask 插件 - 鉴权（JWT）

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 test_platform_backend/flask/L5

---

## 一、Flask-JWT 实现接口鉴权

### 知识点 1：authenticate + identity + jwt_required

【课程原话/定义】
鉴权 = 验证用户身份，确保只有授权用户能访问敏感资源。JWT 是在各方之间作为 JSON 对象安全传输信息的标准（传输用户身份和授权信息）。

Flask-JWT 集成三步：
```python
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity

# 1. 编写鉴权函数（验证用户名密码）
def authenticate(username, password):
    user = username_table.get(username, None)
    if user and user.password == password:
        return user

# 2. 编写返回用户标识的函数（从 token 载荷取 identity）
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=360)   # 过期时间

# 3. 绑定到 Flask 应用
jwt = JWT(app, authenticate, identity)

# 需要鉴权的接口加装饰器
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity
```

流程：POST /auth 传 username/password 拿 access_token → 后续请求带 Authorization: JWT <token> 访问受保护接口。

【为什么？】
为什么要 JWT 鉴权？因为测试平台的接口不能谁都能调——用户信息、数据管理都要登录后才能访问。JWT 的核心是"登录拿 token，请求带 token，服务端校验 token"：authenticate 负责"验证账密对不对"，identity 负责"从 token 反查出用户"，jwt_required 负责"标记哪些接口要鉴权"。这套机制让"无状态的 token 鉴权"在 Flask 里变得简单——服务端不用存 session，靠 token 里的签名就能验证合法性。

【必须掌握】
- JWT = 无状态 token 鉴权标准
- 三步：authenticate（验证账密）+ identity（token 反查用户）+ JWT(app, ...) 绑定
- @jwt_required() 标记受保护接口
- POST /auth 拿 token，请求头 Authorization: JWT <token>
- SECRET_KEY 密钥、JWT_EXPIRATION_DELTA 过期时间

【企业场景】
你在公司测试平台，登录接口 /auth 验证账密返回 token，用户列表、数据管理等接口加 @jwt_required()，前端每次请求带 Authorization: JWT <token>。这样没有 token 的人访问不了敏感接口。这是测试平台"登录鉴权"的标准实现。

【面试考察】
面试官：「Flask 怎么做接口鉴权？JWT 的流程是什么？」

参考回答框架：
1. 用 Flask-JWT（或 Flask-JWT-Extended）
2. authenticate 验证账密，identity 反查用户
3. 登录拿 token，请求带 Authorization: JWT <token>
4. @jwt_required() 标记受保护接口
5. JWT 无状态，服务端靠签名校验

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 请求头不带 JWT 前缀 | 要 Authorization: JWT <token>，不是直接 token |
| pyjwt 版本不对 | flask-jwt 依赖 pyjwt==1.7.1，新版会有编码问题 |
| 忘 SECRET_KEY | JWT 签名需要 SECRET_KEY 密钥 |

【我的理解】
> （authenticate 和 identity 两个函数分别在哪一步被调用？为什么 JWT 鉴权需要这两个函数，而不是一个函数搞定？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| JWT 鉴权 | authenticate + identity + jwt_required | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch25-Flask插件-集成Swagger]]
- [[Ch18-实战课程管理平台后端开发]]
