---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch01-Pytest入门"
created: 2026-07-20
status: draft
---

# Ch01 - Pytest 入门

## 课程来源
- 学习日期：

---

## 一、Pytest 简介

### 知识点 1：什么是 Pytest

【课程原话/定义】
Pytest 是一个非常流行的 Python 测试框架，兼容 unittest 框架，用于编写简单的单元测试和复杂的功能测试。它广泛用于自动化测试、回归测试等各种场景。

Pytest 可以结合 Requests 实现接口测试；结合 Selenium、Appium 实现自动化功能测试。使用 Pytest 结合 Allure 集成到 Jenkins 中可以实现持续集成。

【为什么？】
为什么有了 unittest 还要学 Pytest？对比一下就清楚了：

| 特性      | unittest                 | Pytest          |
| ------- | ------------------------ | --------------- |
| 断言写法    | `self.assertEqual(a, b)` | `assert a == b` |
| 用例发现    | 需手动加载 TestSuite          | 自动发现            |
| 插件生态    | 几乎没有                     | 1000+ 插件        |
| 错误报告    | 简单                       | 详细 diff 对比      |
| fixture | setUp/tearDown 固定        | fixture 灵活可组合   |

核心差异：unittest 是 Java 风格的 Python 测试框架（模仿 JUnit），Pytest 是 Pythonic 的测试框架（充分利用 Python 语言特性）。`assert` 就是最典型的例子——直接用 Python 内置关键字，不需要记一堆 assertEqual/assertTrue/assertIn 方法名。

【必须掌握】
- Pytest 是 Python 主流测试框架，兼容 unittest
- 三大应用：接口测试（+Requests）、UI 自动化（+Selenium/Appium）、持续集成（+Allure+Jenkins）
- 核心优势：简洁断言、自动发现用例、丰富插件、详细错误报告

【企业场景】
你入职后接手一个自动化测试项目。打开 CI 流水线看到：
```
pytest tests/ --alluredir=reports/
```
然后 Jenkins 自动把 Allure 报告发到团队 Slack。这条命令背后就是 Pytest + Allure + Jenkins 的协作——三个工具各司其职：
- Pytest：执行测试
- Allure：生成可视化报告
- Jenkins：定时触发 + 通知

你写测试时只需关心 Pytest 部分，集成交给流水线自动完成。

【面试考察】
面试官："为什么现在企业测试框架大多选 Pytest 而不是 unittest？"

参考回答框架：
1. 语法简洁：`assert` 代替 `self.assertXxx()`，降低学习成本
2. 自动发现：按命名规则自动扫描用例，不需要手动组装 TestSuite
3. 插件生态：pytest-xdist（并行）、pytest-cov（覆盖率）、pytest-html（报告）等
4. fixture 机制：比 setUp/tearDown 更灵活，支持依赖注入和参数化
5. 生态兼容：完美兼容 unittest 写的旧用例，迁移成本为零

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| 认为 Pytest 和 unittest 是互斥的 | 不了解 Pytest 可以运行 unittest 用例 | Pytest 直接运行 unittest 写的 TestCase，无需改代码 |
| 学了 Pytest 就觉得 unittest 没用 | 不理解历史遗留 | 很多老项目还是 unittest，维护时需要能读懂 |

【扩展知识】
Pytest 常用插件：
- `pytest-xdist`：多进程并行执行用例
- `pytest-cov`：代码覆盖率
- `pytest-html`：HTML 测试报告
- `pytest-rerunfailures`：失败用例自动重跑
- `pytest-ordering`：控制用例执行顺序

【我的理解】
> （用自己的话解释：为什么 Pytest 的 `assert` 比 unittest 的 `self.assertEqual` 更好？不只是"简洁"，从 Python 语言特性角度思考）

---

### 知识点 2：Pytest 安装与准备

【课程原话/定义】
安装前提：Python 版本 > 3.6。

安装命令：
```bash
pip install pytest
```
若已有 Pytest，更新命令：
```bash
pip install -U pytest
```
也可通过 PyCharm 界面化安装。

【为什么？】
`pip install pytest` 背后发生了什么？pip 从 PyPI（Python Package Index）下载 Pytest 包及其依赖（py、pluggy、iniconfig 等），安装到当前 Python 环境的 site-packages 目录。安装完成后可以在终端直接使用 `pytest` 命令——因为 pip 会把可执行脚本注册到环境变量 PATH 中。

`-U` 是 `--upgrade` 的缩写。为什么需要升级？Pytest 版本迭代快，新版本修复 bug、增加特性，保持最新版本避免遇到已知问题。

【必须掌握】
- `pip install pytest`：安装
- `pip install -U pytest`：升级到最新版
- 安装后终端可执行 `pytest --version` 验证
- Python 版本要求 > 3.6

【企业场景】
你在新公司拿到一台新电脑，环境从零开始搭。第一步就是装 Pytest：
```bash
pip install pytest
pytest --version   # pytest 8.x.x
```
然后 clone 项目代码，跑 `pytest` 看用例能不能通过——环境问题通常是第一个要排除的因素。

【面试考察】
面试官："怎么确认 Pytest 安装成功？"

参考回答：`pytest --version` 查看版本号；或者在 Python 中 `import pytest` 不报错即可。

【易错点】

| 常见错误                  | 错误原因                    | 正确做法                                  |
| --------------------- | ----------------------- | ------------------------------------- |
| 系统有多个 Python，装到了不对的环境 | pip 绑定的 Python 不是当前项目用的 | 用 `python -m pip install pytest` 明确指定 |
| 在虚拟环境外安装，污染全局         | 不习惯用 venv               | 项目先创建虚拟环境，再 pip install               |
| 版本太旧导致某些新特性不可用        | 安装后从不升级                 | 定期 `pip install -U pytest`            |

【我的理解】
> （在终端执行 `pytest --version`，把结果写在这里。如果失败，描述你的排查过程）
     pytest 9.0.2
---

## 二、Pytest 命名规则

### 知识点 3：命名规则与自动发现

【课程原话/定义】
Pytest 以特定规则识别测试用例。不遵循命名规则会导致 Pytest 识别不到测试用例。

| 类型    | 规则                     |
| ----- | ---------------------- |
| 文件    | `test_` 开头或 `_test` 结尾 |
| 类     | `Test` 开头              |
| 方法/函数 | `test_` 开头             |

注意：测试类中不可以添加 `__init__` 构造函数。

示例：
```python
# 文件：test_example.py

# 类名
class TestExample:
    # 方法名
    def test_case1(self):
        pass
    def test_case2(self):
        pass

# 函数名
def test_addition():
    pass

def test_subtraction():
    pass
```

【为什么？】
这不仅仅是"记住规则"——背后是 Pytest 的测试发现机制：

1. Pytest 从当前目录递归遍历所有 `.py` 文件
2. 对每个文件检查文件名是否符合 `test_*.py` 或 `*_test.py`
3. 对符合的文件，用 Python 反射机制扫描其中的类和函数
4. 类：以 `Test` 开头，忽略 `__init__`（如果有则跳过，不会实例化）
5. 函数：以 `test_` 开头

为什么测试类不能有 `__init__`？因为 Pytest 自己管理测试类的实例化（为每个测试方法创建独立实例，保证用例隔离）。如果你写了 `__init__`，Pytest 不知道如何传参，会直接跳过这个类。

命名规则的三个价值：
- **约定优于配置**：不需要写配置文件声明哪些是测试，命名本身就是声明
- **团队协作**：任何人看文件名就知道这是测试代码
- **工具兼容**：CI 工具、IDE 插件都按这个规则识别

【必须掌握】
- 文件：`test_*.py` 或 `*_test.py`
- 类：`Test*`，不能有 `__init__`
- 方法/函数：`test_*`
- 违反规则 = 用例不被执行（静默跳过，不报错！）

【企业场景】
你写了一个测试文件叫 `login_test.py`：

```python
class LoginTestCase:      # ❌ 不是 Test 开头
    def check_login(self):  # ❌ 不是 test_ 开头
        assert True
```

跑 `pytest` 发现 "collected 0 items"——一个用例都没找到。新人排查半天以为 Pytest 坏了，最后发现是命名不对。

> 这就是为什么命名规则排在第一章——它是 90% 新人遇到的第一个坑。

【面试考察】
面试官："Pytest 怎么找到你的测试用例？"

参考回答框架：
1. 从当前目录开始递归扫描 `.py` 文件
2. 过滤文件名：`test_*.py` 或 `*_test.py`
3. 扫描类：`Test` 开头且无 `__init__`
4. 扫描函数：`test_` 开头
5. 收集完成后生成用例队列，按顺序执行

面试官追问："如果我写了一个叫 `login.py` 的文件，里面有 `test_login()` 函数，会被执行吗？"
答：不会。文件名不符合 `test_*.py` 或 `*_test.py`，Pytest 根本不会扫描它。

面试官再追问："如果测试类写了 `__init__`，会报错吗？"
答：不会报错，但该类会被静默跳过，不执行任何用例。

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| `class LoginTest:` | 类名不以 Test 开头 | `class TestLogin:` |
| `def login_test(self):` | 方法名不以 test_ 开头 | `def test_login(self):` |
| `testclass.__init__` | 不知道 Pytest 排斥 `__init__` | 去掉 `__init__`，用 setup_method 代替 |
| 0 collected 以为 Pytest 坏了 | 命名不符合规则 | 逐条检查文件/类/方法命名 |

【我的理解】
> （用你自己的话总结 Pytest 的三级命名规则，然后写一个简单的测试文件 `test_demo.py` 验证——里面放一个正确的和一个故意写错的用例，跑 `pytest -v` 看结果）

---

## 三、PyCharm 配置与界面化运行

### 知识点 4：PyCharm 配置 Pytest

【课程原话/定义】
通过 PyCharm 界面配置 Pytest 为默认测试执行器：
1. 进入 File → Settings → Tools → Python Integrated Tools
2. Default test runner 选择 `pytest`
3. 点击 OK

配置完成后，测试用例左侧会出现绿色三角按钮，点击即可运行。

【为什么？】
PyCharm 默认测试执行器是 unittest。如果不切换，PyCharm 会按 unittest 规则运行你的 Pytest 用例——大部分能跑，但 fixture、参数化等 Pytest 特性不生效，错误信息也很难看。

切换后 PyCharm 内部调用 `pytest` 命令执行，完整享受 Pytest 所有特性。

这也是 GUI vs CLI 的平衡：日常开发点绿色三角方便，CI 流水线用命令行 `pytest`。

【必须掌握】
- Settings → Tools → Python Integrated Tools → Default test runner: pytest
- 绿色三角 = 运行单个用例
- 右键 = 运行整个文件/目录
- 这不是"必须"的（终端 `pytest` 也可以），但能显著提升效率

【企业场景】
你在 IDE 里调试一个失败的用例，点绿色三角 → 直接进入 Debug 模式 → 断点停在第 42 行 → 发现预期值和实际值不一致 → 修 bug → 再点绿色三角 → 通过。

如果每次都要切到终端打 `pytest tests/test_login.py::TestLogin::test_valid_login -v`，效率差距巨大。

【面试考察】
面试官一般不直接问 PyCharm 配置，但可能问："你日常怎么运行测试用例？"

参考回答：开发时用 PyCharm 界面运行单个用例（效率高），CI 环境用 `pytest` 命令行（可脚本化）。

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| 绿色三角不出现 | Default test runner 还是 unittest | 去 Settings 切换到 pytest |
| 点绿色三角报错 | 项目解释器没装 pytest | 先 pip install pytest |
| 终端 pytest 能跑但 IDE 不能 | IDE 使用的 Python 环境不同 | 检查 PyCharm 右下角的解释器 |

【我的理解】
> （打开 PyCharm，确认 Default test runner 已切换到 pytest。如果还没切，现在切。然后运行之前写的 `test_demo.py`，描述你的操作过程和结果）

---

## 四、测试用例结构

### 知识点 5：测试用例三段式

【课程原话/定义】
测试用例由三部分组成：用例名称、用例步骤、用例断言。

```python
# 用例名称
def test_xxx():
    # 测试步骤1
    # 测试步骤2
    # 断言：实际结果 对比 预期结果
    assert ActualResult == ExpectedResult
```

测试类形式：
```python
class TestXxx:
    def setup_method(self):
        # 资源准备
        pass
    def teardown_method(self):
        # 资源销毁
        pass
    def test_xxx(self):
        # 测试步骤1
        # 测试步骤2
        assert ActualResult == ExpectedResult
```

【为什么？】
三段式结构不是 Pytest 的规定，而是测试工程的最佳实践：

- **用例名称**（test_xxx）：一眼看出测什么。好的命名 = 活的文档。`test_1` 是坏命名，`test_login_with_valid_credentials` 是好命名。
- **用例步骤**：Arrange-Act-Assert（AAA 模式）的 Arrange+Act。准备数据 → 执行操作。
- **用例断言**：AAA 模式的 Assert。没有断言的测试是"假测试"——永远通过，毫无价值。

setup/teardown 解决的是"重复准备"的问题：5 个用例都需要 driver，与其每个用例写一遍，不如放在 setup 里自动执行。

【必须掌握】
- 三段式：名称、步骤、断言
- 没有断言的用例毫无意义
- 函数名应用下划线描述测试场景
- setup_method：每个用例前执行（资源准备）
- teardown_method：每个用例后执行（资源清理）

【企业场景】
你在测试登录功能，写了 5 个用例：

```python
class TestLogin:
    def setup_method(self):
        """每个用例执行前：打开浏览器，访问登录页"""
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com/login")

    def test_login_success(self):
        self.driver.find_element("id", "username").send_keys("admin")
        self.driver.find_element("id", "password").send_keys("123456")
        self.driver.find_element("id", "login-btn").click()
        assert "Welcome" in self.driver.page_source

    def test_login_wrong_password(self):
        self.driver.find_element("id", "username").send_keys("admin")
        self.driver.find_element("id", "password").send_keys("wrong")
        self.driver.find_element("id", "login-btn").click()
        assert "Invalid password" in self.driver.page_source

    def teardown_method(self):
        """每个用例执行后：关闭浏览器"""
        self.driver.quit()
```

5 个用例 × 省去 2 行准备代码 = 省 10 行重复代码。100 个用例就是 200 行——setup/teardown 的价值显而易见。

【面试考察】
面试官："描述一个完整的测试用例由哪些部分组成？"

参考回答框架：
1. 用例名称：`test_` 开头，描述测试场景（如 `test_login_with_wrong_password`）
2. 用例步骤：准备测试数据 → 执行被测操作（Arrange → Act）
3. 用例断言：验证实际结果是否等于预期（Assert），没有断言 = 假测试
4. 可选：setup/teardown 做资源的准备和清理

【易错点】

| 常见错误 | 错误原因 | 正确做法 |
|---------|---------|---------|
| 写了一个测试函数，里面只有 print 没有 assert | 不理解断言的必要性 | 必须写 assert 验证预期结果 |
| 函数名叫 `test_1`, `test_2` | 偷懒，不利于维护 | `test_login_success` 见名知意 |
| setup 里初始化资源，teardown 里忘记清理 | 资源泄漏 | 每次写 setup 马上写对应的 teardown |

【我的理解】
> （用三段式结构写一个测试用例：测试"字符串的 upper() 方法"。先写名称，再写步骤，最后写断言。然后把你的代码贴在这里）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Pytest 简介 | 什么是 Pytest，vs unittest 优势 | ⭐⭐⭐⭐ |
| 安装与准备 | pip install/upgrade，环境验证 | ⭐⭐ |
| 命名规则 | 文件/类/方法三级命名 + `__init__` 禁忌 | ⭐⭐⭐⭐⭐ |
| PyCharm 配置 | Default test runner 切换 | ⭐⭐ |
| 用例结构 | 三段式：名称→步骤→断言 + setup/teardown | ⭐⭐⭐⭐ |

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch02-Pytest断言与框架结构]]
- [[../Python/Ch22-面向对象入门]] — setup/teardown 就是面向对象的实际应用
