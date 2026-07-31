---
tags: [Bug, 环境排障, Flask]
bug_id: "BUG-001"
severity: P2
project: "plantform_backend"
date: 2026-07-30
status: fixed
---

# BUG-001 — Flask 启动配置异常：端口和 Debug 不生效

## 现象

代码中明确写了：

```python
app.run(port=5055, debug=True)
```

但实际启动结果：

| 期望 | 实际 |
|------|------|
| `Running on http://127.0.0.1:5055` | `Running on http://127.0.0.1:5000` |
| `Debug mode: on` | `Debug mode: off` |
| 修改代码自动重启 | 不重启，需要手动重启 |
| 浏览器自动刷新 | 不刷新 |

**连带问题**：Blueprint 注册时报 `AssertionError: View function mapping is overwriting an existing endpoint function: user.login`

---

## 复现步骤

1. 在 PyCharm 中打开 Flask 项目 `flask_blueprint.py`
2. 右键 → Run（或点击绿色三角）
3. 观察到控制台输出 `Serving Flask app 'flask_blueprint.py'` 而非执行 `app.run()`
4. 端口始终为 5000，debug 始终为 off

---

## 根因分析

### 问题一：PyCharm 自动使用 Flask Run 模式

```
PyCharm 检测到 Flask 项目
         ↓
自动创建 Flask Configuration
         ↓
使用 flask run 命令启动
         ↓
跳过 app.run() —— 代码中的 port/debug 参数不被读取
```

PyCharm 的 Flask Configuration 本质上执行的是 `flask run`，它：
- 从环境变量（`FLASK_RUN_PORT`、`FLASK_DEBUG`）读取配置
- 完全不执行 `app.run()` 及其参数
- 这就是为什么代码里的 `port=5055, debug=True` 看起来写了但没用

### 问题二：Blueprint endpoint 冲突

```python
@user_router.route("")        # endpoint = user.login
def login():                  # ← 函数名 login
    pass

@user_router.route("/login")  # endpoint = user.login
def login():                  # ← 同样是 login，冲突！
    pass
```

Flask 默认 endpoint 规则：`蓝图名.函数名`。两个路由用了相同函数名 `login` → 生成相同 endpoint `user.login` → 冲突报错。

---

## 修复

### 修复一：改用 Python Run Configuration（推荐）

删除 PyCharm 自动创建的 Flask Configuration，新建 Python Configuration：

```
Run → Edit Configurations → + → Python

Script path:  flask_blueprint.py
Python interpreter:  项目/.venv/Scripts/python.exe
Working directory:   项目根目录
```

这样启动流程变为：

```
PyCharm → python flask_blueprint.py → 执行 app.run() → 读取 port/debug 配置
```

### 修复二：函数名去重

```python
# 修复前（冲突）
@user_router.route("")
def login():        # endpoint → user.login
    ...

@user_router.route("/login")
def login():        # endpoint → user.login ← 重复！
    ...

# 修复后（不冲突）
@user_router.route("")
def user_index():   # endpoint → user.user_index
    ...

@user_router.route("/login")
def login():        # endpoint → user.login
    ...
```

---

## 预防 — 以后遇到类似问题快速检查清单

### Flask 启动异常四步查

| 序号 | 症状 | 检查 | 解决 |
|------|------|------|------|
| ① | 端口不对 | 控制台是否有 `Serving Flask app`？→ 是 Flask Run 模式 | 改用 Python Run Configuration |
| ② | Debug 不生效 | 控制台 `Debug mode: off` | 同上，或设 `FLASK_DEBUG=1` |
| ③ | `Address already in use` | `netstat -ano \| findstr 5055` | `taskkill /PID xxx /F` |
| ④ | Blueprint 注册失败 | 报 `endpoint conflict` | 检查蓝图内是否有同名函数 |

### 排查层级

遇到服务启动异常，按层级排查（不跳跃）：

| 层级 | 检查 |
|------|------|
| IDE | Run Configuration 是 Flask 还是 Python？ |
| Python 环境 | 解释器指向哪个 venv？ |
| 依赖 | Flask 版本是否正确？ |
| 代码 | 路由、函数名、配置参数 |
| 网络 | 端口是否被占用？ |

---

## 面试故事

> 在开发 Flask 项目时，我遇到过 PyCharm 自动使用 Flask Run 模式导致代码中的端口和 Debug 配置不生效的问题。通过检查启动日志发现实际启动方式与预期不同——控制台显示 `Serving Flask app` 而非直接执行 `app.run()`。定位后调整 Run Configuration 使用 Python 解释器直接执行入口文件解决。同时在蓝图注册过程中遇到 endpoint 重复问题，通过分析 Flask 的路由命名规则（`蓝图名.函数名`）定位到函数名冲突并修复。这个经历让我养成了"先看启动日志判断实际运行方式，再排查代码"的习惯。

---

## 关联笔记
- [[../02-课程笔记/接口测试/Ch02-Flask入门]] — 运行方式：`app.run()` vs `flask run`（知识点 3）、404 排查流程（知识点 9）
- [[../02-课程笔记/接口测试/Ch03-请求与响应处理]] — 环境配置 host/port/debug（知识点 12-14）
