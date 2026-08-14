---
tags: [Flask, Blueprint, Postman, 问题总结]
created: 2026-08-03
status: completed
---

# Flask + 接口测试作业问题总结

> 昨天遇到的：Blueprint 结构、数据结构设计、request.json、模板渲染、redirect、Postman 与 Flask 的关系。

---

## 一、Flask 蓝图（Blueprint）项目结构

推荐结构：

```
hw05-flask-basic/
├── app.py              ← 启动入口
├── database.py         ← 数据存储
├── user/
│   ├── __init__.py
│   └── views.py        ← 注册、登录
└── task/
    ├── __init__.py
    └── views.py        ← 创建任务、查看任务、查看详情
```

> `__init__.py` 可以是空文件，让 Python 把目录识别为包。

---

## 二、为什么 `users_db = {"username":"admin"}` 不合理？

```python
# ❌ 这是一个用户对象，不是用户数据库
users_db = {
    "username": "admin",
    "password": ""
}
```

问题：只能存一个用户。多用户（admin、riley、tom）无法保存。

```python
# ✅ 字典嵌套 — key 是用户名，value 是该用户的信息
users_db = {
    "admin": {"password": "123456"},
    "riley": {"password": "888888"}
}
```

访问：`users_db["admin"]["password"]` → `"123456"`

---

## 三、如何判断用户名是否存在？

```python
if username in users_db:
```

Python 判断的是：`username` 这个 key 是否在字典里。

```python
users_db = {"admin": {...}, "riley": {...}}

if "admin" in users_db:   # True — 在 key 里面
```

> ❌ 不要用 `if username in users_db.values()`  
> 因为 `.values()` 返回的是 `{"password": "123456"}` 这些值，不是用户名。

---

## 四、Blueprint 导入报错

错误：

```
ImportError: attempted relative import beyond top-level package
```

原因：用了相对导入 `from ..database import users_db`，但项目不是以包形式运行的。

| 错误 | 正确 |
|------|------|
| `from ..database import users_db` | `from database import users_db` |

---

## 五、`request.json` 获取不到数据

注册接口返回 `"username": null`，说明 `data.get("username")` 没取到值。

原因：**Postman 发送的字段名和代码不一致。**

```python
# 代码期望
username = data.get("username")
```

```json
// Postman 必须发送
{"username": "riley", "password": "123456"}
```

> 字段名必须完全一致：`username` ≠ `name` ≠ `userName`。

---

## 六、Postman 和 Flask 的关系

```
Postman → HTTP 请求 → Flask 路由 → 视图函数 → 返回响应 → Postman 显示
```

Postman 本质是 **HTTP 客户端**，它发送请求、接收响应。和浏览器做的事一样，只是不渲染 HTML。

---

## 七、`render_template` 页面不显示

错误：

```
jinja2.exceptions.TemplateNotFound: show.html
```

Flask 默认找 `templates/` 目录。必须：

```
项目/
├── user.py
└── templates/       ← 不能有空格、不能改名
    └── show.html
```

> 常见坑：目录名前多了空格 → ` templates` ≠ `templates`。

---

## 八、为什么 Postman 返回的是 HTML 源码？

```python
return render_template("show.html", name=name, age=age)
```

| 客户端 | 行为 |
|--------|------|
| 浏览器 | 解析 HTML → 渲染页面 |
| Postman | 显示 HTML 源码（它是 HTTP 工具，不是浏览器） |

浏览器访问需要 HTML 表单或前端页面发起 POST，地址栏只能发 GET。

---

## 九、CSS 速查

```css
body {
    max-width: 800px;
    font-size: 20px;           /* 字号 */
    font-family: "Microsoft YaHei";
    color: #333;               /* 文字颜色 */
    background-color: #f5f5f5; /* 背景色 */
}
```

---

## 十、Flask 常见错误

### redirect 没生效

```python
# ❌ 没有 return
redirect("/login")

# ✅
return redirect("/login")
```

Flask 必须 `return` 响应，`redirect()` 只是生成了重定向对象。

### request.args 取值

```python
# ❌ — args 是字典，不能 .username 访问
request.args.username

# ✅
request.args.get("username")
```

---

## 十一、Flask + Pytest 测试思维

```python
def test_register():
    response = client.post("/register", json={
        "username": "riley",
        "password": "123456"
    })
    assert response.status_code == 200
```

任何接口测试本质都一样：

```
发送请求 → Flask 接收 → 执行函数 → 返回结果 → assert 验证
```

---

## 十二、技能链全景

```
Python 基础
    ↓
pytest 测试
    ↓
Flask 接口开发（理解接口原理）
    ↓
Postman 调试
    ↓
数据库验证（SQL）
    ↓
自动化测试框架
```

> 现在卡的地方主要不是技术难，而是**从需求到代码的拆解能力**——通过小项目练习提升最快。
