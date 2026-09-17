---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch17-Pytest测试用例生命周期管理-fixture作用域"
created: 2026-09-17
status: in_progress
---

# Ch17 - Pytest 测试用例生命周期管理 - fixture 作用域

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、fixture 的五种作用域

### 知识点 1：function / class / module / package / session

【课程原话/定义】
pytest 允许控制 fixture 的作用域，通过 @pytest.fixture() 的 scope 参数设置：

| 作用域 | 范围 | 说明 |
|--------|------|------|
| function（默认） | 函数级 | 每个函数/方法都调用，每个测试创建新实例 |
| class | 类级 | 每个测试类运行一次，类内方法共享 |
| module | 模块级 | 每个 py 文件调用一次，模块内共享 |
| package | 包级 | 每个 python 包调用一次 |
| session | 会话级 | 每次会话运行一次，所有测试共享 |

```python
@pytest.fixture(scope="session")   # 整个会话共享
def db_conn():
    conn = connect()
    yield conn
    conn.close()
```

【为什么？】
为什么要理解 fixture 作用域？因为作用域决定了"fixture 多久创建/销毁一次"，直接影响测试性能和资源管理。比如数据库连接：如果每个测试函数都新建连接（function 级），几百条用例就连接几百次，慢且浪费；用 session 级（整个会话建一次连接）就高效得多。反过来，需要"每个用例干净的数据"就应该用 function 级（每个用例新建）。理解五种作用域，才能根据"资源成本 vs 隔离需求"选对作用域。

【必须掌握】
- 五种作用域：function（默认）/class/module/package/session
- scope 参数设置：@pytest.fixture(scope="session")
- function 级：每个用例新实例（隔离最彻底，开销最大）
- session 级：整个会话共享（开销最小，隔离最弱）
- 选择依据：资源成本 vs 数据隔离需求

【企业场景】
你在公司测试平台，数据库连接用 session 级（整个测试会话连一次），登录态用 class 级（每个测试类登录一次），临时测试数据用 function 级（每个用例独立准备）。合理分配作用域，兼顾效率和隔离。

【面试考察】
面试官：「fixture 有哪些作用域？怎么选择？」

参考回答框架：
1. function（默认）/class/module/package/session 五种
2. function 级隔离最彻底、开销最大
3. session 级开销最小、隔离最弱
4. 按资源成本和隔离需求选择

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 数据库连接用 function 级 | 每条用例都连库，慢且浪费，应 session/class 级 |
| 需要隔离的数据用 session 级 | 数据会跨用例污染，应 function 级 |
| 忘默认作用域 | 不写 scope 默认 function |

【我的理解】
> （为什么"作用域越大、隔离越弱"？session 级的 fixture 在多个用例间共享，会带来什么风险？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| fixture 作用域 | function/class/module/package/session | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch13-Pytest测试用例生命周期管理-fixture]]
- [[Ch19-Pytest配置与共享功能]]
