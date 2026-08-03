---
tags: [课程笔记, SQL, Python]
course: "SQL"
chapter: "Ch05-Python操作MySQL"
created: 2026-07-31
status: draft
---

# Ch05 - Python 操作 MySQL

## 课程来源
- 学习日期：

---

## 一、PyMySQL 概述

### 知识点 1：PyMySQL 是什么

【课程原话/定义】
PyMySQL 是一个纯 Python 实现的 MySQL 客户端库，用于在 Python 代码中连接和操作 MySQL 数据库。它完全用 Python 编写，不依赖 C 扩展库，安装简单、跨平台兼容。

安装命令：
```bash
pip install pymysql
```

在 Python 代码中导入：
```python
import pymysql
```

PyMySQL 兼容 Python 3.x，遵循 Python Database API Specification v2.0（PEP 249），这意味着它的接口和 Python 内置的 sqlite3 模块风格一致——学会一个，其他数据库库也能触类旁通。

【为什么？】
测试工程师用 Python 操作数据库，而不是直接在 Workbench 里写 SQL：

| 方式                  | 场景           | 局限性               |
| ------------------- | ------------ | ----------------- |
| Workbench / Navicat | 手工查数据、临时验证   | 无法自动化、无法批量操作      |
| Python + PyMySQL    | 自动化测试脚本中验证数据 | 需要写代码，但可以复用、批量、定时 |

测试工程师的核心场景：
- 接口测试后自动查数据库验证数据落库（不用手动打开 Workbench）
- 数据驱动测试：从数据库读测试数据，驱动用例执行
- 批量造测试数据：用 Python 循环 + INSERT 在 1 秒内生 10000 条数据
- 测试前后自动清理数据：setUp 插入，tearDown 删除

【必须掌握】
- PyMySQL 是纯 Python 的 MySQL 客户端，pip install 即用
- 遵循 PEP 249 标准，接口和 sqlite3 一致
- 测试工程师用它实现"自动化验证数据"——从手动查库变成代码自动查

【企业场景】
一个完整的接口自动化测试用例（以注册接口为例）：

```python
import pymysql
import requests

class TestRegister:
    def test_register_success(self):
        # 1. 调用注册接口
        response = requests.post("http://api.example.com/register", json={
            "username": "test_user_001",
            "password": "Test@123",
            "email": "test001@example.com"
        })
        assert response.status_code == 200

        # 2. 查数据库验证数据落库
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="123456",
            database="cms"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username=%s",
            ("test_user_001",)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        # 3. 断言数据库中的数据正确
        assert row is not None, "用户数据未落库！"
        assert row[1] == "test_user_001"
        assert row[2] == "test001@example.com"

        # 4. 清理测试数据
        # ... (见后续 DML 章节)
```

这就是"接口返回成功 ≠ 数据正确落库"的自动化验证方案。

【面试考察】
面试官："你在自动化测试中怎么验证数据落库？" / "为什么要用 Python 操作数据库而不是手动查？"

参考回答框架：
1. 调用接口后，用 PyMySQL 连接数据库执行 SELECT 查询
2. 用 fetchone/fetchall 获取结果，断言字段值与预期一致
3. 这样做的好处：自动化、可重复、能集成到 CI/CD 流水线
4. 比手动打开 Workbench 查效率高 10 倍以上

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 只测接口返回 200，不查数据库 | 接口返回成功 ≠ 数据正确落库——必须查库二次确认 |
| PyMySQL 和 mysql-connector-python 混淆 | PyMySQL 是纯 Python（推荐），mysql-connector 是 Oracle 官方（有 C 扩展） |
| 忘记 import pymysql | 每个用到数据库的测试文件都要导入 |

【我的理解】
> （之前学的 requests 库验证接口返回，现在学 pymysql 验证数据库落库——两者组合起来就是接口自动化测试的完整闭环。画出你理解的流程图：测试用例 → requests 调接口 → PyMySQL 查数据库 → assert 断言。每一步的输入和输出分别是什么？）

---

## 二、连接数据库

### 知识点 2：connect() 参数详解

【课程原话/定义】
`pymysql.connect()` 用于创建与 MySQL 数据库的连接，返回一个 Connection 对象。核心参数如下：

```python
conn = pymysql.connect(
    host="127.0.0.1",      # 数据库服务器地址，本机用 127.0.0.1 或 localhost
    port=3306,             # MySQL 端口，默认 3306
    user="root",           # 数据库用户名
    password="123456",     # 数据库密码
    database="cms",        # 要连接的数据库名
    charset="utf8mb4"      # 字符集，推荐 utf8mb4（支持 emoji）
)
```

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `host` | str | 否 | 数据库服务器地址 | `"localhost"` |
| `port` | int | 否 | MySQL 端口号 | `3306` |
| `user` | str | 否 | 登录用户名 | `""` |
| `password` | str | 否 | 登录密码 | `""` |
| `database` | str | 否 | 连接后直接选中的数据库 | `None` |
| `charset` | str | 否 | 客户端字符集 | `"utf8mb4"` |
| `autocommit` | bool | 否 | 是否自动提交事务 | `False` |
| `connect_timeout` | int | 否 | 连接超时秒数 | `10` |
| `cursorclass` | class | 否 | 游标类型（默认 Tuple，可用 DictCursor） | `Cursor` |

【为什么？】
参数的默认值意味着最简单的连接写法可以非常精简：

```python
# 极简写法（本地开发、默认端口、无密码的 root 用户）
conn = pymysql.connect(database="cms")

# 显式写法（生产环境、远程连接——推荐写全，清晰明了）
conn = pymysql.connect(
    host="192.168.1.100",
    port=3306,
    user="qa_tester",
    password="Qa@2026!",
    database="cms",
    charset="utf8mb4"
)
```

测试工程师推荐**显式写法**：虽然多写几行，但参数一目了然，换了环境（测试库 → 预发布库）只需要改 host/database 就行。

`charset="utf8mb4"` 很重要：utf8（3 字节）不支持 emoji 和部分生僻字，utf8mb4（4 字节）完全兼容。如果你的测试数据包含中文特殊字符，用 utf8 会导致 `Incorrect string value` 错误。

【必须掌握】
- 连接五要素：host + port + user + password + database
- charset 推荐 `utf8mb4`（不是 `utf8`）
- `autocommit=False` 是默认值——这意味着 INSERT/UPDATE/DELETE 之后必须手动 `commit()`
- 连接对象使用完毕后要 `conn.close()` 释放资源

【企业场景】
测试环境的多数据库切换模式：

```python
# 配置文件（config.py）——根据环境切换数据库连接
import os

DB_CONFIG = {
    "dev": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "dev123",
        "database": "cms_dev",
        "charset": "utf8mb4"
    },
    "test": {
        "host": "192.168.1.50",
        "port": 3306,
        "user": "qa",
        "password": "qa123",
        "database": "cms_test",
        "charset": "utf8mb4"
    },
    "staging": {
        "host": "10.0.1.100",
        "port": 3306,
        "user": "qa_readonly",
        "password": "qa_ro_2026",
        "database": "cms_staging",
        "charset": "utf8mb4"
    }
}

# 通过环境变量切换
env = os.getenv("TEST_ENV", "dev")
config = DB_CONFIG[env]
conn = pymysql.connect(**config)  # ** 解包字典为关键字参数
```

【面试考察】
面试官："pymysql.connect() 有哪些参数？autocommit 默认是什么？"

参考回答框架：
1. 核心参数：host、port、user、password、database、charset
2. autocommit 默认 False——DML 操作需要手动 commit
3. 实际项目中通常把连接参数放在配置文件里，通过环境变量切换不同环境

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `charset="utf8"` | 用 `charset="utf8mb4"`，支持完整 Unicode |
| 连接远程数据库填 `localhost` | 远程数据库必须填 IP 地址，localhost = 本机 |
| password 硬编码在代码里提交到 git | 用环境变量或配置文件（.env 不提交到 git） |
| 每次操作都重新 connect() | 复用连接对象，或者用连接池（测试中通常一个用例一个连接） |

【我的理解】
> （对比 pymysql.connect() 的参数和 Workbench 的连接界面：你发现了吗？host、port、user、password 完全对应。这说明不管是 GUI 工具还是 Python 代码，连接数据库的本质信息是一样的。请找出你电脑上 MySQL 的实际连接信息，用 Python 代码尝试连接一次。）

---

### 知识点 3：连接的生命周期

【课程原话/定义】
Python 操作 MySQL 的标准五步流程：

```python
# ① 导入
import pymysql

# ② 建立连接
conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    database="cms",
    charset="utf8mb4"
)

# ③ 创建游标（Cursor）
cursor = conn.cursor()

# ④ 执行 SQL
cursor.execute("SELECT * FROM class")
rows = cursor.fetchall()

# ⑤ 关闭资源（先关游标，再关连接）
cursor.close()
conn.close()
```

流程口诀：**导入 → 连接 → 游标 → 执行 → 关闭**

【为什么？】
游标（Cursor）是什么？为什么不能直接在 Connection 上执行 SQL？

| 概念 | 类比 | 作用 |
|------|------|------|
| Connection | 电话线 | 建立与数据库的物理连接 |
| Cursor | 听筒 | 通过这条线发送 SQL、接收结果 |

Connection 只管"连接"，Cursor 才管"对话"。一个 Connection 可以创建多个 Cursor，但通常一个操作一个 Cursor 就够了。

关闭顺序必须是**先关 Cursor，再关 Connection**——就像挂电话前先把听筒放回去。如果先关 Connection，Cursor 就成"悬空指针"了。

正确做法（推荐用 `with` 语句自动管理资源）：
```python
# 不推荐：手动 close()，容易忘
conn = pymysql.connect(...)
cursor = conn.cursor()
# ... 操作 ...
cursor.close()   # ← 忘了写？资源泄漏！
conn.close()

# 推荐：连接用 try-finally，游标用 with
conn = pymysql.connect(...)
try:
    with conn.cursor() as cursor:  # with 自动关闭游标
        cursor.execute("SELECT * FROM class")
        rows = cursor.fetchall()
finally:
    conn.close()  # finally 保证连接一定关闭
```

【必须掌握】
- 五步：import → connect → cursor → execute → close
- 游标（Cursor）是执行 SQL 和获取结果的"中介"
- 关闭顺序：先 cursor.close()，再 conn.close()
- 一个 Cursor 对应一次操作（或一组操作），用完即关

【企业场景】
测试用例中标准的数据验证模板：

```python
import pymysql
import pytest

class TestUserAPI:
    """用户接口测试——含数据库验证"""

    DB_CONFIG = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "database": "cms",
        "charset": "utf8mb4"
    }

    def get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(**self.DB_CONFIG)

    def test_create_user_data_integrity(self):
        """测试：创建用户后数据库中的数据完整性"""
        # Step 1: 调用接口创建用户
        # response = requests.post(...)

        # Step 2: 查数据库验证
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT username, email, status FROM users WHERE username=%s",
                    ("test_user",)
                )
                row = cursor.fetchone()

                # Step 3: 断言
                assert row is not None
                assert row[0] == "test_user"
                assert row[1] == "test@example.com"
                assert row[2] == "active"
        finally:
            conn.close()

    def test_query_all_active_users(self):
        """测试：查询所有活跃用户"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM users WHERE status='active'")
                count = cursor.fetchone()[0]
                assert count >= 0
        finally:
            conn.close()
```

【面试考察】
面试官："Python 操作 MySQL 的流程是什么？游标（Cursor）的作用是什么？"

参考回答框架：
1. 五步：import pymysql → connect → cursor → execute → close
2. Cursor 是 SQL 执行的载体：发送 SQL、接收结果、控制读取位置
3. 一个 Connection 可以有多个 Cursor，但通常一个操作用一个
4. 关闭顺序：先 cursor 后 connection

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 忘记 close() | 用 `with conn.cursor()` 或 `try-finally` 保证关闭 |
| 先关 conn 再关 cursor | 顺序一定是：cursor.close() → conn.close() |
| 整个测试类共用一个 cursor | 每个方法用完即关，不要跨方法复用游标 |
| connect() 写在测试方法外面 | 每个测试方法内部自己 connect，用完即关——避免用例间数据污染 |

【我的理解】
> （画出 Connection 和 Cursor 的关系图。如果把数据库比作图书馆，Connection 是你的借书证（证明你有权限进入），Cursor 是你每次借书时填的索书单（告诉管理员你要什么），fetchone/fetchall 就是管理员把书递给你。这个比喻能帮你记住两者的区别和生命周期。）

---

## 三、查询操作（DQL）

### 知识点 4：参数化查询与 SQL 注入防护

【课程原话/定义】
参数化查询是指：SQL 语句中用占位符 `%s` 代替实际值，实际值通过 execute() 的第二个参数（元组）传入。这是**防止 SQL 注入的唯一正确方式**。

```python
# ✅ 正确：参数化查询——安全
username = "test' OR '1'='1"  # 恶意输入
cursor.execute(
    "SELECT * FROM users WHERE username=%s",
    (username,)  # 注意：单参数也要写成元组，逗号不能省
)

# ❌ 错误：字符串拼接——SQL 注入风险！
cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
# 实际执行的 SQL：
# SELECT * FROM users WHERE username='test' OR '1'='1'
# 结果：返回所有用户数据！
```

参数化查询的工作原理：PyMySQL 不会简单地把 `%s` 替换成字符串然后拼接到 SQL 里——它会把参数**转义**后安全地插入，恶意字符会被转义为普通字符串。

```python
# 多个参数
cursor.execute(
    "SELECT * FROM users WHERE username=%s AND status=%s",
    ("test_user", "active")  # 元组元素数量和顺序必须匹配占位符
)

# 命名参数风格（PyMySQL 也支持）
cursor.execute(
    "SELECT * FROM users WHERE username=%(name)s AND status=%(status)s",
    {"name": "test_user", "status": "active"}
)
```

| 占位符风格 | 示例 | 参数格式 |
|------------|------|----------|
| `%s`（format） | `WHERE id=%s` | 元组 `(value,)` 或列表 |
| `%(name)s`（pyformat） | `WHERE id=%(id)s` | 字典 `{"id": value}` |

【为什么？】
SQL 注入是 OWASP Top 10 排名前三的安全漏洞。作为测试工程师，你不仅要"测出"注入漏洞，更要"写出"安全的测试代码。

SQL 注入攻击场景还原：

```python
# 假设前端登录接口接收 username 和 password
# 攻击者输入：username = "admin' --"
#            password = "anything"

# ❌ 拼接方式
sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
# 变成：SELECT * FROM users WHERE username='admin' --' AND password='anything'
#                              注释符 ↑   ↑ 后面的被注释掉了
# 结果：绕过密码验证，直接以 admin 登录！

# ✅ 参数化查询——攻击者输入被转义
cursor.execute(
    "SELECT * FROM users WHERE username=%s AND password=%s",
    (username, password)
)
# PyMySQL 将 'admin'' --' 中的单引号转义为 \'，恶意 SQL 失效
```

面试高频：**PyMySQL 中 `%s` 不是 Python 的字符串格式化 `%`**，它是 DB-API 2.0 规范的参数占位符，PyMySQL 会在服务端做类型安全的参数绑定。其他数据库库的占位符不同：sqlite3 用 `?`，psycopg2 用 `%s`。

【必须掌握】
- **永远不要用 f-string 或 `%` 拼接 SQL 字符串**
- 占位符是 `%s`（单个）或 `%(name)s`（命名），不用 `?`
- execute(sql, params) 第二个参数是元组——单个参数也要逗号：`(value,)`
- 参数化查询是防御 SQL 注入的唯一方式

【企业场景】
测试工程师的 SQL 注入测试用例：

```python
import pytest

# SQL 注入攻击载荷列表
SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "admin' --",
    "'; DROP TABLE users; --",
    "' UNION SELECT * FROM users --",
    "1' OR '1' = '1",
]

@pytest.mark.parametrize("payload", SQL_INJECTION_PAYLOADS)
def test_login_sql_injection(payload):
    """安全测试：验证登录接口是否防御 SQL 注入"""
    response = requests.post("http://api.example.com/login", json={
        "username": payload,
        "password": "anything"
    })
    # 预期：接口不应该返回认证成功
    assert response.status_code != 200 or response.json().get("token") is None, \
        f"SQL 注入漏洞！载荷: {payload}"
```

同时，你自己的测试代码也必须安全——不要在自动化脚本里拼接 SQL。

【面试考察】
面试官："怎么防止 SQL 注入？`%s` 和 Python 的 `%` 格式化有什么区别？"

参考回答框架：
1. 使用参数化查询——execute() 的第二个参数传值，不用字符串拼接
2. `%s` 是 DB-API 2.0 的占位符，PyMySQL 会在服务端做安全的参数绑定
3. Python 的 `%` 是客户端字符串操作，恶意字符不会被转义
4. 任何时候传入用户输入到 SQL，都必须参数化

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| f-string 拼接 SQL | 用参数化查询：`cursor.execute(sql, (val,))` |
| 单参数忘记逗号：`(val)` | 单参数元祖：`(val,)`——逗号是元组语法的关键 |
| `%s` 写成 `?` | PyMySQL 占位符是 `%s`（不是 sqlite3 的 `?`） |
| 表名/列名也用 `%s` | `%s` 只能用于值，表名/列名不能参数化（需要白名单校验） |

【我的理解】
> （打开 Python 交互环境，分别用"参数化查询"和"字符串拼接"执行一条带恶意输入的 SELECT。对比两者的结果——你看到了什么？再想一想：如果测试代码本身有 SQL 注入漏洞，攻击者可以通过你的测试脚本攻击数据库吗？）

---

### 知识点 5：查询方法（fetchone / fetchall / fetchmany）

【课程原话/定义】
Cursor 提供三个获取查询结果的方法：

| 方法 | 返回值 | 说明 |
|------|--------|------|
| `fetchone()` | 单条记录的元组，或 `None` | 游标指针向后移动一行 |
| `fetchall()` | 所有记录的元组嵌套 `((),(),...)` | 一次性读取全部（大数据量时可能 OOM） |
| `fetchmany(size)` | 指定数量的记录 `((),...())` | 分批读取，类似分页 |

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="123456",
                       database="cms", charset="utf8mb4")

with conn.cursor() as cursor:
    cursor.execute("SELECT id, name, age FROM class ORDER BY id")

    # === fetchone：逐行读取 ===
    row = cursor.fetchone()
    print(row)  # (1, '张三', 20)
    print(row[0], row[1], row[2])  # 1 张三 20

    # === fetchall：一次读完 ===
    cursor.execute("SELECT id, name FROM class WHERE age > %s", (18,))
    rows = cursor.fetchall()
    print(rows)  # ((1, '张三'), (3, '王五'), ...)
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}")

    # === fetchmany：分批读取 ===
    cursor.execute("SELECT * FROM class")
    batch = cursor.fetchmany(3)  # 每次取 3 条
    while batch:
        for row in batch:
            print(row)
        batch = cursor.fetchmany(3)  # 继续取下一批
```

【为什么？】
三种方法的选择策略：

| 场景 | 推荐方法 | 原因 |
|------|----------|------|
| 按唯一键查询（用户名、ID） | `fetchone()` | 最多一条结果，语义清晰 |
| 查所有测试数据（几十条） | `fetchall()` | 数据量小，一次读完方便遍历 |
| 做数据驱动测试（可能上万条） | `fetchmany()` | 分批读，避免内存爆炸 |
| 验证记录不存在（预期查不到） | `fetchone()` + `assert result is None` | fetchone 找不到返回 None |

Cursor 内部有一个"行指针"——每次调用 fetch 方法，指针自动前移。这意味着**同一次 execute 后，fetchone 只能逐行前进，不能回退**。要重新读？再 execute 一次。

```python
cursor.execute("SELECT * FROM class LIMIT 5")

row1 = cursor.fetchone()  # 第 1 行
row2 = cursor.fetchone()  # 第 2 行
row3 = cursor.fetchone()  # 第 3 行

# 想回到第 1 行？不能！指针已经过去了。
# 解决方案：
cursor.execute("SELECT * FROM class LIMIT 5")  # 重新执行
row1_again = cursor.fetchone()  # 又是第 1 行
```

【必须掌握】
- `fetchone()`：取一行，无结果返回 `None`
- `fetchall()`：取全部，返回嵌套元组 `((),())`
- `fetchmany(n)`：取 n 行，返回嵌套元组
- 游标指针单向移动，不能回退——要重读就重新 execute
- 测试中最常用的是 `fetchone()`（验证单条数据）和 `fetchall()`（遍历检查）

【企业场景】

场景一：接口测试验证单条数据（最常见）

```python
def test_user_registration(self):
    # 调用注册接口...
    username = "new_user_001"

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, email, status FROM users WHERE username=%s",
                (username,)
            )
            row = cursor.fetchone()

            assert row is not None, f"用户 {username} 未在数据库中找到"
            assert row[3] == "active", f"预期 status=active，实际 {row[3]}"
    finally:
        conn.close()
```

场景二：数据驱动测试——从数据库读取测试数据

```python
@pytest.mark.parametrize("user_data", get_test_users_from_db())
def test_batch_user_login(self, user_data):
    """从数据库读取用户数据，驱动批量登录测试"""
    user_id, username, password, expected_status = user_data

    response = requests.post("http://api.example.com/login", json={
        "username": username,
        "password": password
    })
    assert response.json()["status"] == expected_status, \
        f"用户 {username} 登录状态不符预期"

def get_test_users_from_db():
    """从数据库获取测试用户数据集"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password, expected_status "
                "FROM test_data_login WHERE is_active=1"
            )
            return cursor.fetchall()
    finally:
        conn.close()
```

场景三：验证记录数为 0（存量数据检查）

```python
def test_cleanup_deleted_users(self):
    """验证：已删除的用户在数据库中不存在"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM users WHERE username=%s",
                ("deleted_user",)
            )
            row = cursor.fetchone()
            assert row is None, "已删除的用户仍存在于数据库中！"
    finally:
        conn.close()
```

【面试考察】
面试官："fetchone 和 fetchall 有什么区别？什么场景用哪个？查询结果为空时它们返回什么？"

参考回答框架：
1. fetchone 返回一行（元组）或 None，fetchall 返回所有行（嵌套元组）
2. 按唯一键查询用 fetchone，需要遍历所有结果用 fetchall
3. 大数据量用 fetchmany 分批读防止内存溢出
4. 无结果时：fetchone → None，fetchall → `()`（空元组），fetchmany → `()`

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| fetchall 后直接当列表取 `rows[0]` | `rows[0]` 是第一行元组，`rows[0][0]` 才是第一个字段 |
| fetchone 无结果不判断 None | 总是先 `if row is None` 再访问字段 |
| 忘记 execute 直接 fetch | 必须先 execute 才能 fetch，否则报错 |
| SELECT * 后取 count | 用 `SELECT COUNT(*)` 而不是 fetchall 后 `len(rows)` |

【我的理解】
> （对比 cursor 的"行指针"和文件的"读指针"——它们是不是很像？文件读完要 seek(0) 回到开头，cursor 读完要重新 execute。写出 3 个你在测试中最可能用到 SELECT 的场景，并为每个场景选择正确的 fetch 方法。）

---

## 四、修改操作（DML）

### 知识点 6：INSERT / UPDATE / DELETE 与 commit()

【课程原话/定义】
INSERT、UPDATE、DELETE 会修改数据库中的数据。由于 PyMySQL 默认 `autocommit=False`，这些操作执行后**必须调用 `conn.commit()` 才会真正写入数据库**。如果不 commit，数据只在当前会话（事务）中可见，关掉连接后丢失。

```python
import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="123456",
                       database="cms", charset="utf8mb4")

try:
    with conn.cursor() as cursor:
        # === INSERT ===
        sql = "INSERT INTO class (name, age, gender) VALUES (%s, %s, %s)"
        cursor.execute(sql, ("李四", 22, "男"))
        # cursor.rowcount → 受影响的行数（这里 = 1）

        # === UPDATE ===
        sql = "UPDATE class SET age=%s WHERE name=%s"
        cursor.execute(sql, (23, "李四"))
        # cursor.rowcount → 如果存在则 = 1，不存在则 = 0

        # === DELETE ===
        sql = "DELETE FROM class WHERE name=%s"
        cursor.execute(sql, ("test_temp",))
        # cursor.rowcount → 被删除的行数

    # ⚠️ 关键：提交事务
    conn.commit()
    print("数据修改已提交")

except Exception as e:
    conn.rollback()  # 失败则回滚
    print(f"操作失败，已回滚: {e}")
    raise

finally:
    conn.close()
```

| 操作 | SQL | commit 是否必须 | cursor.rowcount |
|------|-----|----------------|-----------------|
| SELECT | `SELECT ...` | ❌ 不需要 | 返回行数（不是所有驱动都支持） |
| INSERT | `INSERT INTO ...` | ✅ 必须 | 插入的行数 |
| UPDATE | `UPDATE ... SET ...` | ✅ 必须 | 更新的行数 |
| DELETE | `DELETE FROM ...` | ✅ 必须 | 删除的行数 |

【为什么？】
为什么查询不需要 commit，修改需要 commit？

这是数据库**事务（Transaction）**机制：修改操作不是直接写入磁盘，而是先写入"事务日志"，commit 后才持久化。这保证了：
1. **原子性**：多条 SQL 要么全部生效，要么全部不生效
2. **一致性**：commit 前其他连接看不到你的修改
3. **隔离性**：你的修改不影响别人，别人的也不影响你
4. **持久性**：commit 后即使断电数据也不会丢

```
你的代码                          MySQL 服务器
   │                                │
   │  INSERT INTO ...               │
   ├──────────────────────────────►│ 写入事务日志（暂存）
   │                                │
   │  UPDATE ...                    │
   ├──────────────────────────────►│ 写入事务日志（暂存）
   │                                │
   │  conn.commit()                 │
   ├──────────────────────────────►│ 持久化到磁盘！ ✅
   │                                │
   │  conn.rollback()               │
   ├──────────────────────────────►│ 撤销所有暂存修改 ❌
```

测试中最常见的 bug 之一：**INSERT 执行了，但数据库里查不到——因为你忘了 commit！**

```python
# ❌ 经典错误
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()
cursor.execute("INSERT INTO class (name) VALUES ('test')")
cursor.close()
conn.close()  # 没 commit！数据丢失！

# ✅ 正确写法
conn = pymysql.connect(**DB_CONFIG)
try:
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO class (name) VALUES ('test')")
    conn.commit()  # ← 必须 commit
finally:
    conn.close()
```

【必须掌握】
- SELECT 不需要 commit——只读不写
- INSERT / UPDATE / DELETE 必须 commit——修改数据
- `cursor.rowcount` 返回受影响的行数——用于断言"确实改了 N 行"
- 异常时调用 `conn.rollback()` 回滚——保证数据不被部分修改
- 批量操作在循环结束后统一 commit——不要每行都 commit（性能差）

【企业场景】

场景一：批量造测试数据

```python
def create_test_orders(count=100):
    """批量创建测试订单——数据工厂模式"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            for i in range(count):
                cursor.execute(
                    "INSERT INTO orders (order_no, user_id, amount, status) "
                    "VALUES (%s, %s, %s, %s)",
                    (f"TEST{20260801:06d}{i:04d}",  # 如 TEST202608010001
                     10000 + i,
                     round(99.9 + i * 0.5, 2),
                     "pending")
                )
        conn.commit()  # ← 批量提交，不是每条都 commit
        print(f"成功创建 {count} 条测试订单")
    except Exception as e:
        conn.rollback()
        print(f"批量创建失败: {e}")
        raise
    finally:
        conn.close()
```

场景二：清理测试数据（tearDown 模式）

```python
import pytest

class TestOrderAPI:

    TEST_ORDER_NO = "TEST_DEL_001"

    def setup_method(self):
        """测试前置：创建一条测试数据"""
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO orders (order_no, user_id, amount, status) "
                    "VALUES (%s, %s, %s, %s)",
                    (self.TEST_ORDER_NO, 10001, 299.0, "pending")
                )
            conn.commit()
        finally:
            conn.close()

    def teardown_method(self):
        """测试后置：清理测试数据"""
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM orders WHERE order_no=%s",
                    (self.TEST_ORDER_NO,)
                )
                deleted = cursor.rowcount
            conn.commit()
            print(f"清理了 {deleted} 条测试数据")
        finally:
            conn.close()

    def test_cancel_order(self):
        """测试取消订单"""
        # 调用取消订单接口...
        # response = requests.put(f"http://api.example.com/orders/{self.TEST_ORDER_NO}/cancel")

        # 验证数据库状态变化
        conn = pymysql.connect(**DB_CONFIG)
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT status FROM orders WHERE order_no=%s",
                    (self.TEST_ORDER_NO,)
                )
                row = cursor.fetchone()
                assert row is not None
                assert row[0] == "cancelled"  # 预期状态改为 cancelled
        finally:
            conn.close()
```

场景三：UPDATE 后用 rowcount 验证影响行数

```python
def test_update_user_status(self):
    """测试：更新用户状态，验证只影响目标用户"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        # 先确认当前状态
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE status='active'"
            )
            active_before = cursor.fetchone()[0]

        # 执行批量更新
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET status='inactive' "
                "WHERE last_login < %s AND status='active'",
                ("2025-01-01",)
            )
            affected = cursor.rowcount
        conn.commit()

        print(f"更新了 {affected} 行")

        # 验证变化量
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE status='active'"
            )
            active_after = cursor.fetchone()[0]

        assert active_after == active_before - affected, \
            f"状态更新行数不符！预期减少 {affected}，实际减少 {active_before - active_after}"
    finally:
        conn.close()
```

【面试考察】
面试官："INSERT 执行后为什么要 commit？rollback 在什么情况下用？"

参考回答框架：
1. PyMySQL 默认 autocommit=False——DML 操作在事务中暂存
2. commit() 将事务持久化到磁盘，不 commit 则连接关闭后数据丢失
3. rollback() 在异常时撤销所有未提交的修改——保证数据一致性
4. SELECT 不需要 commit，因为它不修改数据

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| INSERT 后忘记 commit | DML 三兄弟（INSERT/UPDATE/DELETE）必须 commit |
| SELECT 也写 commit | SELECT 不需要——写了也不会报错但浪费一次网络往返 |
| 每行 INSERT 都 commit | 循环结束后统一 commit，性能提升 10-100 倍 |
| 忘记 cursor.rowcount | rowcount 可以断言"确实影响了 N 行"，增强测试稳定性 |
| 不写 rollback | `try-except` 中加 `conn.rollback()`——防止脏数据残留 |

【我的理解】
> （写一段代码：先 INSERT 一条数据，不 commit 直接关连接。然后用 Workbench 或其他连接查这张表——你能找到刚插入的数据吗？再写一段：INSERT 后 commit，再查——数据在了吗？这个实验帮你彻底理解 commit 的作用。）

---

### 知识点 7：查询 vs 修改操作总结

【课程原话/定义】

| 对比维度 | 查询（SELECT） | 修改（INSERT/UPDATE/DELETE） |
|----------|---------------|------------------------------|
| SQL 类型 | DQL（Data Query Language） | DML（Data Manipulation Language） |
| 是否修改数据 | ❌ 只读 | ✅ 写操作 |
| 是否需要 commit | ❌ 不需要 | ✅ 必须 commit |
| 获取结果方式 | fetchone / fetchall / fetchmany | cursor.rowcount |
| 事务回滚影响 | 不适用 | rollback 撤销修改 |
| 锁机制 | 共享锁（允许别人读） | 排他锁（阻止别人写） |
| 性能考虑 | 关注查询效率（索引） | 关注批量 commit（减少网络往返） |

核心一句话：**查用 fetch，改用 commit**。

测试中的记忆口诀：
```
SELECT → execute → fetchXXX → 断言
INSERT/UPDATE/DELETE → execute → commit → cursor.rowcount → 断言
```

【为什么？】
这个区别不是 PyMySQL 的特有行为，而是关系型数据库的通用设计。面试中常问"事务的 ACID 特性"，commit 和 rollback 就是 ACID 中 A（原子性）和 D（持久性）的体现。

测试工程师要特别注意：当你写"接口测试 + 数据库验证"时，同一个测试方法里可能既有 SELECT 也有 INSERT：

```python
def test_register_and_verify(self):
    conn = pymysql.connect(**DB_CONFIG)
    try:
        # Step 1: 准备数据（可选，INSERT 测试用户）
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s)",
                ("test_register", "test_reg@test.com")
            )
        conn.commit()  # ← INSERT 必须 commit！

        # Step 2: 调用注册接口（略）

        # Step 3: 验证数据（SELECT）
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username FROM users WHERE username=%s",
                ("test_register",)
            )
            row = cursor.fetchone()  # ← SELECT 用 fetch，不用 commit
            assert row is not None

        # Step 4: 清理数据（DELETE）
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE username=%s",
                ("test_register",)
            )
        conn.commit()  # ← DELETE 必须 commit！

    finally:
        conn.close()
```

【必须掌握】
- 记忆规则：查 = fetch，改 = commit
- 一个测试方法中的完整流程：INSERT(commit) → 调接口 → SELECT(fetch) → DELETE(commit)
- 批量操作在循环外统一 commit，不要在循环内逐条 commit

【企业场景】
数据驱动测试的完整模板——从数据库读数据，执行测试，将结果写回数据库：

```python
import pytest
import pymysql
from datetime import datetime

DB_CONFIG = {
    "host": "127.0.0.1", "port": 3306,
    "user": "root", "password": "123456",
    "database": "cms", "charset": "utf8mb4"
}

def get_test_cases():
    """从数据库读取测试用例——数据驱动"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password, expected_result "
                "FROM test_cases_login WHERE is_active=1"
            )
            return cursor.fetchall()  # SELECT → fetch，不 commit
    finally:
        conn.close()

def update_test_result(case_id, result, error_msg=None):
    """将测试结果写回数据库——方便出报告"""
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE test_cases_login "
                "SET last_result=%s, last_run_time=%s, error_msg=%s "
                "WHERE id=%s",
                (result, datetime.now(), error_msg, case_id)
            )
        conn.commit()  # UPDATE → 必须 commit！
    finally:
        conn.close()

@pytest.mark.parametrize("case_id,username,password,expected", get_test_cases())
def test_login_data_driven(case_id, username, password, expected):
    """数据驱动登录测试"""
    try:
        response = requests.post("http://api.example.com/login", json={
            "username": username,
            "password": password
        })
        actual = "success" if response.status_code == 200 else "fail"
        assert actual == expected
        update_test_result(case_id, "PASS")
    except AssertionError as e:
        update_test_result(case_id, "FAIL", str(e))
        raise
```

【面试考察】
面试官："在一个测试用例中，既有 SELECT 又有 INSERT，commit 应该怎么写？"

参考回答框架：
1. SELECT 部分不需要 commit——执行后直接 fetch 获取结果
2. INSERT/UPDATE/DELETE 后必须 conn.commit()
3. 通常的模式：INSERT(commit) → 调接口 → SELECT(fetch) → 验证 → DELETE(commit)
4. 异常处理中用 rollback() 回滚，保证测试数据不留脏数据

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| SELECT 后写 commit | 不需要——写了也不报错，但暴露你不理解事务机制 |
| commit 写在循环里 | 批量操作在循环结束后统一 commit |
| INSERT 和 SELECT 之间切换不关游标 | 同一个 Connection 可以用多个 Cursor，用完即关 |
| 忘记 DELETE/UPDATE 的条件 `WHERE` | 没有 WHERE 的 DELETE 会清空整张表——测试中极度危险 |

【我的理解】
> （整理一份"测试脚本中 SQL 操作检查清单"：□ INSERT 后有 commit 吗？□ UPDATE/DELETE 有 WHERE 条件吗？□ SELECT 后用 fetch 获取结果了吗？□ 异常分支有 rollback 吗？□ 测试数据有清理步骤吗？每次写数据库操作的测试代码时对照检查。）

---

### 知识点 8：游标生命周期与最佳实践

【课程原话/定义】
游标（Cursor）的生命周期管理原则：**一个操作一个游标，用完即关**。

```python
# ✅ 推荐：每次操作创建新游标
conn = pymysql.connect(**DB_CONFIG)
try:
    # 操作 1：查询
    with conn.cursor() as cur1:
        cur1.execute("SELECT * FROM class")
        rows = cur1.fetchall()
    # cur1 已自动关闭

    # 操作 2：插入
    with conn.cursor() as cur2:
        cur2.execute("INSERT INTO class (name) VALUES (%s)", ("test",))
    conn.commit()
    # cur2 已自动关闭

finally:
    conn.close()
```

游标状态变化：

```
创建游标 → execute(SQL) → [fetch 读取] → 游标耗尽 → 关闭游标
                ↑                              │
                └──── 可重新 execute ──────────┘
```

一个 Cursor 可以多次 execute，但前一次 execute 的结果集会被清空：

```python
with conn.cursor() as cursor:
    cursor.execute("SELECT id FROM class WHERE age > 20")
    rows = cursor.fetchall()  # 获得年龄大于 20 的
    print(len(rows))

    cursor.execute("SELECT id FROM class WHERE age <= 20")
    rows = cursor.fetchall()  # 获得年龄 <= 20 的（前一个结果集已清除）
    print(len(rows))
```

【为什么？】
为什么要"一个操作一个游标"而不是复用一个游标？

| 做法 | 优点 | 缺点 |
|------|------|------|
| 每次创建新游标 | 隔离性好、不会混淆结果集、代码清晰 | 微小的创建开销（可忽略） |
| 复用游标 | 少写一行 `cursor()` | 结果集混淆、状态难追踪、容易 fetch 到上一次的残留数据 |

测试代码中最危险的就是"不确定的状态"——你 fetchone 回来的数据是这次 execute 的还是上次残留的？新游标消除了这个不确定性。

【必须掌握】
- 原则：一个游标对应一次 SQL 操作（或一组相关的操作）
- 用 `with conn.cursor()` 自动管理游标生命周期
- 游标关闭后不能再使用——会报 `ProgrammingError`
- 不要在方法之间传递游标对象——只传数据（元组/列表）

【企业场景】
测试框架中数据库操作的封装模式：

```python
class DatabaseHelper:
    """测试专用数据库操作封装——每个公共方法自己管理游标"""

    def __init__(self, config):
        self.config = config

    def get_connection(self):
        return pymysql.connect(**self.config)

    def query_one(self, sql, params=None):
        """查询单条记录"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchone()
        finally:
            conn.close()

    def query_all(self, sql, params=None):
        """查询所有记录"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        finally:
            conn.close()

    def execute_dml(self, sql, params=None):
        """执行 INSERT/UPDATE/DELETE，返回受影响行数"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                affected = cursor.rowcount
            conn.commit()
            return affected
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute_many(self, sql, params_list):
        """批量执行 INSERT——executemany 性能更优"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(sql, params_list)
                affected = cursor.rowcount
            conn.commit()
            return affected
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

# 使用示例
db = DatabaseHelper(DB_CONFIG)

# 查询
user = db.query_one("SELECT * FROM users WHERE id=%s", (1,))
assert user is not None

# 插入
rows = db.execute_dml(
    "INSERT INTO users (username) VALUES (%s)",
    ("batch_user",)
)
assert rows == 1

# 批量插入
data = [("user1",), ("user2",), ("user3",)]
db.execute_many("INSERT INTO users (username) VALUES (%s)", data)
```

【面试考察】
面试官："为什么要用完游标就关？一个连接可以同时打开多个游标吗？"

参考回答框架：
1. 用完即关避免资源泄漏和结果集混淆
2. 一个 Connection 可以同时打开多个 Cursor——MySQL 协议支持
3. 但测试中推荐一个操作用一个游标，代码更清晰、更安全
4. 用 `with conn.cursor()` 自动管理，不用手动 close

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 跨方法传递 cursor 对象 | 只传数据（fetch 后的元组），不传 cursor |
| cursor.close() 后继续使用 | 关闭后不能再 execute——如需继续操作，创建新游标 |
| 整个测试类共用一个 cursor | 每个方法内创建自己的 cursor，用完即关 |
| `with conn.cursor() as cur: return cur` | with 块结束后 cur 已关闭——在 with 块内 fetch 完再返回数据 |

【我的理解】
> （写一个 DatabaseHelper 类，封装 query_one、query_all、execute_dml 三个方法。然后用这个类完成：查询 class 表所有记录 → 插入一条测试记录 → 查询确认插入成功 → 删除测试记录 → 查询确认删除成功。全程不直接操作 cursor——这就是"封装"的力量。）

---

## 五、Cursor 类型进阶

### 知识点 9：DictCursor —— 用字典返回结果

【课程原话/定义】
默认的 Cursor 返回元组（tuple），需要用索引访问：`row[0]`、`row[1]`。PyMySQL 还提供了 `DictCursor`，返回字典：`row["id"]`、`row["name"]`。

```python
import pymysql.cursors

# 连接时指定 cursorclass
conn = pymysql.connect(
    host="127.0.0.1", port=3306,
    user="root", password="123456",
    database="cms", charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor  # ← 关键
)

with conn.cursor() as cursor:
    cursor.execute("SELECT id, name, age FROM class WHERE id=%s", (1,))
    row = cursor.fetchone()
    print(row)           # {'id': 1, 'name': '张三', 'age': 20}
    print(row["name"])   # '张三' —— 按列名访问，可读性高
    print(row["age"])    # 20
```

| Cursor 类型 | 返回格式 | 访问方式 | 适用场景 |
|-------------|----------|----------|----------|
| `Cursor`（默认） | 元组 `(1, '张三', 20)` | `row[0]`, `row[1]` | 列少、性能优先 |
| `DictCursor` | 字典 `{'id':1, 'name':'张三'}` | `row['name']` | 列多、可读性优先 |
| `SSCursor` | 元组（流式） | `row[0]` | 超大数据集、内存敏感 |

【为什么？】
DictCursor 在测试代码中的价值：

```python
# ❌ 元组访问——如果表结构变了（加了一列），索引全乱
row = cursor.fetchone()
assert row[0] == 1       # 这是 id 还是什么？
assert row[7] == "active"  # 第 7 列是什么？不查表结构不知道

# ✅ 字典访问——表结构变了也不怕，列名不变就行
row = cursor.fetchone()
assert row["id"] == 1
assert row["status"] == "active"  # 一眼就知道在断言什么
```

测试代码最重要的是**可读性和可维护性**——DictCursor 让断言一目了然。推荐在测试代码中默认使用 DictCursor。

【必须掌握】
- 指定方式：`cursorclass=pymysql.cursors.DictCursor`
- 返回值：字典列表，`row["列名"]` 访问
- 测试代码推荐默认使用，元组模式仅在列少且性能敏感时用

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| SQL 用 `SELECT *`，几天后表加了一列，元组索引全乱 | 改用 DictCursor 按列名访问，或者明确列出所需列 |
| DictCursor 中用 `row.get("col")` | DictCursor 返回的字典，键名是列名——大小写和 SQL 中一致 |

【我的理解】
> （用 DictCursor 重写之前的查询代码。对比两种方式：哪个代码一眼就能看出在验证什么字段？如果面试官问你"测试代码中 SQL 结果怎么访问字段"，你会推荐哪个？为什么？）

---

## 今日课程总结

| 模块           | 核心内容                                         | 面试权重  |
| ------------ | -------------------------------------------- | ----- |
| PyMySQL 概述   | 纯 Python 客户端、pip install、PEP 249 标准          | ★★★☆☆ |
| connect() 参数 | host/port/user/password/database/charset，五要素 | ★★★★☆ |
| 连接生命周期       | import → connect → cursor → execute → close  | ★★★★☆ |
| 参数化查询        | `%s` 占位符、防止 SQL 注入、execute(sql, params)      | ★★★★★ |
| 查询方法         | fetchone / fetchall / fetchmany，游标指针单向移动     | ★★★★★ |
| DML 与 commit | INSERT/UPDATE/DELETE 必须 commit，rowcount 验证行数 | ★★★★★ |
| 查 vs 改区别     | SELECT 不 commit，DML 必须 commit / rollback     | ★★★★★ |
| 游标生命周期       | 一个操作一个游标，with 自动管理                           | ★★★☆☆ |
| DictCursor   | 字典返回，可读性优先                                   | ★★★☆☆ |
| 测试工程师场景      | 接口验证、数据驱动、批量造数据、清理数据                         | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[../接口测试/Ch03-请求与响应处理]] — requests 库发送 HTTP 请求
- [[Ch01-MySQL基础与SQL入门]] — SQL 基础语法和 Workbench 操作
- [[Ch02-数据库与表操作]] — DDL 建库建表
- [[Ch03-DML数据操作语言]] — INSERT/UPDATE/DELETE 语法
- [[Ch04-DQL数据查询语言]] — SELECT 查询语法
