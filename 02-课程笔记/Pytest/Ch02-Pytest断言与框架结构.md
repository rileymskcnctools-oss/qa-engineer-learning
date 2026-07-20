---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch02-Pytest断言与框架结构"
created: 2026-07-20
status: draft
---

# Ch02 - Pytest 断言与框架结构

> 前置：[[Ch01-Pytest入门]] — 命名规则、用例三段式

## 课程来源
- 学习日期：

---

## 一、Pytest 测试用例断言

### 知识点 1：assert 断言基础

【课程原话/定义】
在 Pytest 中，断言（assert）是用来验证测试结果是否符合预期的基本手段。Pytest 使用 Python 内置的 `assert` 语句，用于验证期望结果与实际结果是否相符。

如果条件为 True，测试通过；如果条件为 False，抛出 `AssertionError` 异常，测试失败。

语法：
```python
assert <表达式>
assert <表达式>, <描述信息>
```

【为什么？】
unittest 提供了 30+ 种断言方法：`assertEqual`、`assertNotEqual`、`assertTrue`、`assertFalse`、`assertIn`、`assertNotIn`、`assertIsNone`、`assertRaises`……要记住这么多方法名本身就是负担。

Pytest 的做法：一个 `assert` 关键字 + Python 原生表达式，覆盖所有情况。Pytest 内部用"断言重写"（assertion rewriting）技术，在运行前把你的 `assert` 语句转换成带详细信息的等价代码。

对比：
```python
# unittest 风格
self.assertEqual(result, expected)
self.assertIn("hello", text)
self.assertTrue(user.is_active)

# Pytest 风格
assert result == expected
assert "hello" in text
assert user.is_active
```

哪个更像你平时写的 Python？显然是后者。

【必须掌握】
- `assert <条件>`：条件为 True 通过，False 失败
- `assert <条件>, <描述>`：失败时显示自定义信息
- 一个用例可以有多个 assert（但注意：第一个失败后后面的不会执行）

【企业场景】
你在写接口测试：
```python
def test_get_user_api():
    response = requests.get("https://api.example.com/users/1")
    # 多个断言——验证不同维度
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    data = response.json()
    assert "name" in data, "响应中缺少 name 字段"
    assert data["id"] == 1, f"用户 ID 不正确: {data['id']}"
```

三个断言分别验证状态码、字段存在性、字段值。任何一个失败都能通过自定义消息快速定位问题——这就是 assert + 描述信息的实际价值。

【面试考察】
面试官："为什么 Pytest 推荐用 `assert` 而不是 `self.assertEqual`？"

参考回答框架：
1. Pytest 使用 Python 原生 `assert`，不需要记一堆方法名
2. Pytest 内部做了"断言重写"（assertion rewriting），失败时自动展示详细 diff
3. 支持自定义错误消息 `assert x == y, "message"`
4. 如果项目中有 unittest 旧代码，也能兼容运行

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| 一个函数里写 10 个 assert | 一个用例测太多，早的失败后面全不执行 | 一个用例聚焦一个测试点 |
| `assert function_call()` 忘了函数需要括号 | 写成了 `assert func`（判断函数对象是否为真，永远 True） | `assert func() == expected` |
| `assert result = 5` 用了赋值 | Python 语法混淆 | `assert result == 5`（双等号） |

【我的理解】
> （用 `assert` 写三个测试：一个等于、一个包含、一个带自定义错误消息。把代码和 `pytest -v` 运行结果贴在这里）

---

### 知识点 2：assert 六种常见用法

【课程原话/定义】

**1. 断言等于：**
```python
def test_equal():
    assert 1 + 1 == 2
```

**2. 断言不等于：**
```python
def test_not_equal():
    assert 2 + 2 != 5
```

**3. 断言大于/小于：**
```python
def test_greater_than():
    assert 3 > 2

def test_less_than():
    assert 2 < 3
```

**4. 断言包含：**
```python
def test_in():
    fruits = ['apple', 'banana', 'cherry']
    assert 'apple' in fruits
```

**5. 断言为空/非空：**
```python
def test_is_none():
    value = None
    assert value is None

def test_is_not_empty():
    value = "hello"
    assert value   # 非空字符串为 True
```

**6. 自定义错误消息：**
```python
def test_addition():
    result = 1 + 1
    assert result == 3, f"预期结果是 3，不是 {result}"
```

【为什么？】
六种用法其实是 Python 比较运算符的六个维度：

| 用法 | Python 机制 | 用途 |
|------|-----------|------|
| `==` | `__eq__` 魔术方法 | 值比较 |
| `!=` | `__ne__` | 不等比较 |
| `>` `<` | `__gt__` `__lt__` | 数量/顺序比较 |
| `in` | `__contains__` | 成员检查 |
| `is None` / 真值 | 身份/布尔判断 | 空值检查 |
| `, "msg"` | assert 第二个参数 | 失败诊断 |

每种用法映射到 unittest 对应方法：`assertEqual`、`assertNotEqual`、`assertGreater`、`assertIn`、`assertIsNone`、`assertTrue`。但 Pytest 不强制你记这些——你会 Python 就会写断言。

自定义错误消息最容易被忽略但最实用：
```python
# 没有自定义消息 → 失败信息不够直观
assert response.status_code == 200
# AssertionError: assert 500 == 200

# 有自定义消息 → 一眼看出问题
assert response.status_code == 200, f"期望 200，实际 {response.status_code}，响应: {response.text[:100]}"
# AssertionError: 期望 200，实际 500，响应: {"error": "Internal Server Error"}
```

【必须掌握】
- 六种用法对应六个 Python 运算符：`==` `!=` `>` `<` `in` `is`
- 自定义错误消息用 f-string，把关键变量值放进去
- `assert value` 判断真值（空字符串/None/0/空列表为 False）
- `assert value is None` 判断是否为 None（不用 `== None`）

【企业场景】
你写的接口测试突然在 CI 上红了。打开日志看到：
```
assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
E   AssertionError: 期望 200，实际 500
```
有自定义消息：3 秒定位是服务端 500 错误，不是测试代码问题。

如果没有自定义消息：
```
E   assert 500 == 200
```
只知道 500≠200，不知道是哪个接口、什么请求参数——排查多花 10 分钟。

> 自定义错误消息 = 给未来的自己（和同事）写的情书。

【面试考察】
面试官："`assert x is None` 和 `assert x == None` 有什么区别？"

参考回答：`is` 检查身份（是否同一个对象），`==` 检查值（是否相等）。对于 `None` 两者等价，但 PEP 8 推荐 `is None`（性能更好、更 Pythonic）。此外，某些自定义类可能重写 `__eq__` 让 `== None` 返回奇怪的结果，但 `is None` 绝对不会。

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| `assert x == None` | 能用但不规范 | `assert x is None` |
| `assert []` 期待测试通过 | 空列表为 False | `assert len([]) == 0` 或 `assert not []` |
| `assert "err" in response` | response 可能是对象不是字符串 | `assert "err" in response.text` |

【我的理解】
> （设计一个测试场景：验证一个包含 5 个元素的列表，分别用四种断言验证——长度等于 5、包含某元素、第一个元素大于 0、列表非空。贴代码和运行结果）

---

## 二、Pytest 测试框架结构

### 知识点 3：基本项目结构

【课程原话/定义】
```
my_project/
├── src/
│   └── my_module.py
├── tests/
│   ├── test_my_module.py
│   └── test_another.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

【为什么？】
这个结构不是 Pytest 强制的，而是 Python 社区的最佳实践：

- `src/` 和 `tests/` 分离：代码和测试物理隔离，部署时不带测试文件
- `conftest.py`：Pytest 的特殊文件，存放共享的 fixture（插件自动加载）
- `pytest.ini`：Pytest 配置文件（命令行默认参数、路径、标记等）
- `tests/` 放测试文件：CI 只需要 `pytest tests/`，不需要关心项目其他目录

对比反模式——代码和测试混在一起：
```
my_project/
├── my_module.py
├── test_my_module.py     # ❌ 混在一起，部署时容易误带
```

【必须掌握】
- `tests/` 目录独立存放测试代码
- `conftest.py` 放共享 fixture（Pytest 自动加载）
- `pytest.ini` 放项目级配置
- 这只是一个推荐结构，不是 Pytest 强制要求

【企业场景】
你 clone 了一个项目，看到 `tests/` 目录就知道测试在哪。CI 配置直接写：
```yaml
script:
  - pytest tests/ -v --cov=src/
```
结构化的项目让 CI 配置、代码 review、新人上手都简单很多。

【面试考察】
面试官："`conftest.py` 是干什么的？"

参考回答：conftest.py 是 Pytest 的特殊配置文件，放在测试目录下。用于存放共享的 fixture 和 hooks。Pytest 会自动加载执行目录及其所有父目录中的 conftest.py，不需要手动 import。不同层级的 conftest.py 可以定义不同作用域的 fixture。

【我的理解】
> （用自己的话画一下"代码和测试分离"的好处。如果你有一个 Flask 项目，你会怎么组织目录？）

---

### 知识点 4：setup 与 teardown

【课程原话/定义】
测试装置（测试夹具）用于为测试提供固定的测试环境或资源。在测试执行前准备资源，执行后清理资源。

Pytest 兼容 unittest 的 setup/teardown 用法，也提供更灵活的 fixture。

**setup/teardown 作用域：**

| 类型 | 规则 |
|------|------|
| `setup_module` / `teardown_module` | 全局模块级（模块执行前后各一次） |
| `setup_class` / `teardown_class` | 类级（类中所有用例前后各一次） |
| `setup_function` / `teardown_function` | 函数级（类外的函数用例前后） |
| `setup_method` / `teardown_method` | 方法级（类中每个方法前后） |

完整示例：
```python
def setup_module():
    print("资源准备：setup module")

def teardown_module():
    print("资源清理：teardown module")

def setup_function():
    print("资源准备：setup function")

def teardown_function():
    print("资源销毁：teardown function")

def test_func1():
    assert True

class TestDemo:
    def setup_class(self):
        print("TestDemo setup_class")

    def teardown_class(self):
        print("TestDemo teardown_class")

    def setup_method(self):
        print("TestDemo setup_method")

    def teardown_method(self):
        print("TestDemo teardown_method")

    def test_method1(self):
        assert True

    def test_method2(self):
        assert False
```

【为什么？】
setup/teardown 的本质是"生命周期钩子"——让你在测试运行的不同阶段插入自定义逻辑。

为什么需要不同作用域？因为资源的"重量"不同：

- **连接数据库**（模块级）→ 跑 100 个用例只需要连 1 次
- **创建测试数据**（类级）→ 每个测试类一套数据
- **打开浏览器**（方法级）→ 每个用例一个干净的浏览器实例（用例间隔离）

如果用方法级去连数据库 → 100 个用例连 100 次数据库 → 慢且浪费连接池。

如果用模块级去开浏览器 → 100 个用例共享一个浏览器 → 前一个用例的 cookie/缓存污染后一个 → 测试结果不可靠。

作用域选择原则：**越重越往上提，需要隔离就越往下放。**

执行顺序（从外到内）：
```
setup_module          ← 1. 模块开始
  setup_function      ← 2. 函数用例前
    test_func1        ← 3. 执行
  teardown_function   ← 4. 函数用例后
  setup_class         ← 5. 类开始
    setup_method      ← 6. 每个方法前
      test_method1    ← 7. 执行
    teardown_method   ← 8. 每个方法后
    setup_method      ← 9. 下一个方法前
      test_method2    ← 10. 执行
    teardown_method   ← 11. 方法后
  teardown_class      ← 12. 类结束
teardown_module       ← 13. 模块结束
```

【必须掌握】
- 四种作用域：module > class > function/method
- module 级：整个 .py 文件执行前后
- class 级：测试类中所有方法前后
- method 级：类中每个测试方法前后
- function 级：类外的测试函数前后
- setup 做资源准备，teardown 做资源回收（必须配对）

【企业场景】
你在写 UI 自动化测试：

```python
def setup_module():
    """整个测试模块开始前，启动 WebDriver 服务"""
    print("启动 chromedriver 服务")

def teardown_module():
    """整个测试模块结束后，关闭 WebDriver 服务"""
    print("关闭 chromedriver 服务")

class TestLogin:
    def setup_class(self):
        """登录相关测试开始前，准备测试账号"""
        self.test_user = {"username": "test001", "password": "Test@123"}
        print("准备测试账号")

    def setup_method(self):
        """每个登录用例前，打开浏览器并访问登录页"""
        self.driver = webdriver.Chrome()
        self.driver.get("https://test.example.com/login")
        print("打开浏览器")

    def test_login_success(self):
        self.driver.find_element("id", "username").send_keys(self.test_user["username"])
        self.driver.find_element("id", "password").send_keys(self.test_user["password"])
        self.driver.find_element("id", "login-btn").click()
        assert "Welcome" in self.driver.page_source

    def test_login_wrong_password(self):
        self.driver.find_element("id", "username").send_keys(self.test_user["username"])
        self.driver.find_element("id", "password").send_keys("wrong_password")
        self.driver.find_element("id", "login-btn").click()
        assert "Invalid" in self.driver.page_source

    def teardown_method(self):
        """每个登录用例后，关闭浏览器"""
        self.driver.quit()
        print("关闭浏览器")
```

三层 setup 各司其职：
- module 级：系统级资源（只做一次）
- class 级：测试数据（复用）
- method 级：用例环境（隔离）

这是工业级测试代码的标准写法。

【面试考察】
面试官："setup/teardown 有哪几种作用域？执行顺序是什么？"

参考回答框架：
1. 四种作用域：module > class > method/function
2. 执行顺序：setup_module → setup_function/method → test → teardown_function/method → teardown_module
3. class 级：setup_class → (setup_method → test → teardown_method) × N → teardown_class
4. 选型原则：重资源往上提（module/class），需要隔离往下放（method/function）

面试官追问："为什么要区分 module 级和 method 级？"

答：性能 vs 隔离的权衡。module 级只执行一次，性能好但用例间共享状态；method 级每个用例独立，隔离好但开销大。比如数据库连接用 module 级（复用连接池），浏览器实例用 method 级（避免 cookie 污染）。

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| setup 里开了资源，teardown 里忘了关 | 只写 setup 不写 teardown | setup 和 teardown 必须配对 |
| 把轻量操作放 module 级 | 不理解作用域选型原则 | 只有真的"重"且"不要求隔离"的操作才放 module 级 |
| 不同用例共享一个有状态的资源，导致相互影响 | 把应 method 级的放 class 级 | 涉及可变状态的资源用 method 级隔离 |
| 用 setup 替代 conftest.py 的 fixture | 不理解 fixture 更灵活 | fixture 可以跨文件共享，setup 只能在当前文件 |

【扩展知识】
setup/teardown 是 unittest 风格的写法。Pytest 更推荐的写法是 fixture：
```python
import pytest

@pytest.fixture
def driver():
    """等价于 setup_method + teardown_method"""
    d = webdriver.Chrome()
    yield d        # yield 之前 = setup，yield 之后 = teardown
    d.quit()

def test_login(driver):   # fixture 作为参数注入
    driver.get("https://example.com")
    assert "Example" in driver.title
```
fixture 比 setup/teardown 更灵活：可以跨文件共享、可以参数化、可以组合。后面课程会详细讲。

【我的理解】
> （把上面的执行顺序示例代码复制到 `test_order.py`，运行 `pytest -v -s test_order.py`，观察打印顺序，验证是否和上面列出的顺序一致。把输出贴在这里）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| assert 断言基础 | `assert` vs unittest 断言方法，断言重写机制 | ⭐⭐⭐⭐⭐ |
| assert 六种用法 | `==` `!=` `>` `<` `in` `is` + 自定义消息 | ⭐⭐⭐⭐⭐ |
| 项目结构 | `tests/` + `conftest.py` + `pytest.ini` | ⭐⭐⭐ |
| setup/teardown | 四种作用域 + 执行顺序 | ⭐⭐⭐⭐⭐ |

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-Pytest入门]] — 前置知识
- [[../Python/Ch24-封装继承多态]] — setup/teardown 用到了类的继承
