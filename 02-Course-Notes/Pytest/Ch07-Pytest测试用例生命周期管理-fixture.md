---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch07-Pytest测试用例生命周期管理-fixture"
date: 2026-07-23
status: draft
---

# Ch07 - Pytest 测试用例生命周期管理 - fixture

## 课程来源

- 学习日期：

---

## 一、测试用例生命周期概念

### 知识点1：生命周期的三阶段

【课程原话/定义】
测试用例生命周期管理指的是测试用例从执行前、执行中到执行后的一系列操作。三阶段：
- **准备（Setup）**：测试执行前初始化工作
- **执行（Test Execution）**：运行测试函数，进行断言验证
- **清理（Teardown）**：测试完成后清理工作

【为什么？】
如果每个测试用例都要自己写"打开浏览器 → 操作 → 关闭浏览器"，100 条用例就有 100 份重复的打开/关闭代码。生命周期管理把 Setup 和 Teardown 提取到框架层，测试用例只关注"操作+断言"，代码量减半、维护点集中。这本质上是 DRY 原则在测试层的应用。

【必须掌握】
- Setup → Execution → Teardown 三阶段模型
- 为什么需要生命周期管理（避免重复、集中维护）
- Pytest 中实现生命周期的两种机制：setup/teardown（类级别） 和 fixture（函数级别+）

【企业场景】
你的自动化测试需要连接测试数据库。100 条用例如果各自写连接代码，哪天数据库地址变了你要改 100 处。用生命周期管理，在 fixture 里集中写一次数据库连接 + 断开，所有用例自动继承。这就是"一处修改、全局生效"。

【面试考察】
面试官："测试用例生命周期包括哪几个阶段？为什么需要管理生命周期？"
参考回答框架：① 三阶段：准备（资源初始化）→ 执行（测试逻辑）→ 清理（资源释放）② 核心价值：避免代码重复、集中管理资源、测试用例聚焦业务逻辑 ③ 类比：餐厅吃饭，Setup = 摆餐具，Execution = 吃饭，Teardown = 收盘子——你不会每道菜都重新摆一遍餐具

【易错点】

| 误区 | 正解 |
|------|------|
| 生命周期 = setup/teardown | setup/teardown 只是 Pytest 的一种实现；fixture 是更灵活的实现 |
| Teardown 不重要 | 不清理会导致资源泄漏（文件未关闭、数据库连接耗尽），后续用例受影响 |
| 每个用例必须三阶段齐全 | 简单用例（如纯函数测试）可能不需要 setup/teardown |

【我的理解】

>

---

## 二、fixture 定义与使用

### 知识点2：@pytest.fixture 核心用法

【课程原话/定义】
fixture 是 pytest 中用于测试前后进行资源准备和清理的机制。定义：函数上方加 `@pytest.fixture()`；使用：将 fixture 函数名作为参数传给测试用例，pytest 自动注入。

【为什么？】
fixture 比 setup/teardown 更灵活的核心原因：**依赖注入**。测试用例声明自己需要什么（通过函数参数），pytest 自动提供，不需要继承任何类、不需要调用任何方法。这是 pytest 区别于 unittest 的核心设计哲学——显式优于隐式。

【必须掌握】
- `@pytest.fixture()` 定义 fixture
- 测试函数参数名 = fixture 函数名，pytest 自动注入
- 默认作用域 `scope='function'`：每个测试函数独立实例
- 不传参数 = 不使用该 fixture，灵活控制

【企业场景】
你的测试套件中，购物车和下单需要登录，搜索和浏览不需要登录。用 setup/teardown 的话，所有测试方法都会执行登录——浪费且不合理。用 fixture，购物车用例的参数里写 `def test_cart(login):`，搜索用例不写 `login` 参数，pytest 自动按需注入，不需要登录的用例跑得更快。

【面试考察】
面试官："fixture 和 setup/teardown 有什么不同？什么时候用 fixture？"
参考回答框架见下方【易错点】对比表。

【易错点】

| 特性 | fixture | setup/teardown |
|------|------|------|
| 定义方式 | `@pytest.fixture()` 装饰器 | 在类中定义 `setup_method` / `teardown_method` |
| 作用范围控制 | `scope` 参数（function/class/module/session） | 需修改方法名（setup_method vs setup_class） |
| 资源清理 | `yield` 分隔 setup 和 teardown | 单独的 `setup` + `teardown` 方法 |
| 参数化支持 | 支持 `params` 参数 | 不支持 |
| 跨文件共享 | 通过 `conftest.py` 自动共享 | 需要继承基类 |
| 依赖注入 | 测试函数声明参数，pytest 自动传入 | 无法声明依赖 |
| **灵活性** | ★★★★★ — 按需使用，不强制 | ★★ — 作用域内全部生效 |
| **适用场景** | 复杂项目、跨模块共享、需要参数化 | 简单场景、传统的 unittest 迁移 |

【我的理解】

>

---

## 三、fixture 作用域

### 知识点3：五种作用域

【课程原话/定义】
pytest 通过 `@pytest.fixture(scope=...)` 控制 fixture 的作用域。五种取值：

| 取值 | 范围 | 说明 |
|------|------|------|
| `function` | 函数级 | **默认值**。每个测试函数都创建一个新的 fixture 实例 |
| `class` | 类级别 | 每个测试类只运行一次，类内所有方法共享同一个实例 |
| `module` | 模块级 | 每个 .py 文件调用一次，模块内所有函数共享同一个实例 |
| `package` | 包级 | 每个 Python 包调用一次，包内所有测试共享同一个实例 |
| `session` | 会话级 | 整个测试会话只运行一次，会话内所有测试共享同一个实例 |

【为什么？】
作用域的核心价值是**性能 vs 隔离性的权衡**。如果一个 fixture 创建数据库连接需要 2 秒，100 条用例都用 scope=function 就是额外 200 秒，改成 scope=session 只需要 2 秒。但作用域越大，测试之间的隔离性越差——session 级别的 fixture 数据可能被前面的用例修改，导致后面用例的行为不可预测。所以 scope 的选择本质上是在"跑得快"和"互不干扰"之间找平衡点。

【必须掌握】
- 五种作用域范围大小：function < class < module < package < session
- 默认 scope='function'，每个测试函数独立实例
- `scope='class'`：类内共享，适用于类级别的资源（如 WebDriver）
- `scope='module'`：模块内共享，适用于模块级资源（如读取配置文件）
- `scope='session'`：全局唯一，适用于昂贵的一次性资源（如数据库连接池）
- 语法：`@pytest.fixture(scope='module')`

【企业场景】
你的 Web 自动化测试有 50 条用例分布在 3 个测试类中。最开始 scope=function，每条用例都重启浏览器 → 50 次启动 × 3 秒 = 150 秒。你改成 scope=class，每个类只启动 1 次 → 3 次 = 9 秒。后来发现 3 个类访问同一个网站，再改成 scope=module → 1 次 = 3 秒。但产品经理说有些用例需要清除缓存独立验证——你又把那部分 fixture 改回 scope=function。scope 的调整不是一次性决策，而是随着用例数量、CI 时限、隔离要求不断调优的过程。

【面试考察】
面试官："fixture 有哪些作用域？你根据什么选择 function 还是 session？"
参考回答框架：① 五种作用域，范围从小到大：function → class → module → package → session ② 决策公式：共享需求越高 → scope 越大；隔离需求越高 → scope 越小 ③ function：每条用例需独立状态（如互不干扰的测试数据）④ class：类内共享，不同类隔离（如 WebDriver 实例）⑤ module：模块级共享读操作（如加载配置文件）⑥ session：全局唯一昂贵资源（如数据库连接池，只创建一次）⑦ 口诀："需要多独立就多小，需要多共享就多大"

【易错点】

| 常见错误 | 正确理解 |
|------|------|
| scope='session' 的 fixture 里存放可变数据 | session 级别 fixture 不应有可变状态，否则用例间互相污染 |
| scope='function' 名为"函数"以为是只执行一次 | function = **每个**函数都执行一次（最频繁的） |
| scope='class' 用在模块级函数上 | scope='class' 只在测试类中生效，模块级函数不归属任何类 |
| 混淆 module 和 package | module = 一个 .py 文件；package = 一个含 `__init__.py` 的目录 |
| scope='session' 跨多次 pytest 命令复用 | 每次 `pytest` 命令 = 一个新 session，session 级 fixture 会被重建 |

【扩展知识】
scope 的包含关系：function ⊂ class ⊂ module ⊂ package ⊂ session。pytest 按这个层级决定 fixture 的创建和销毁时机。**下游可以依赖上游，但上游不能依赖下游**——scope='session' 的 fixture 不能接收 scope='function' 的 fixture 作为参数。

| scope | 创建时机 | 销毁时机 | 典型场景 |
|------|------|------|------|
| function | 每个测试函数前 | 每个测试函数后 | 测试数据准备/临时文件 |
| class | 类中第一个测试前 | 类中最后一个测试后 | WebDriver 实例 |
| module | 模块第一个测试前 | 模块最后一个测试后 | 读取配置文件 |
| package | 包内第一个测试前 | 包内最后一个测试后 | 包级初始化 |
| session | 会话开始时 | 会话结束时 | 数据库连接池、登录 token |

【我的理解】

>

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 生命周期三阶段 | Setup → Execution → Teardown | ⭐⭐⭐⭐ |
| fixture 定义与使用 | @pytest.fixture + 依赖注入 | ⭐⭐⭐⭐⭐ |
| fixture 作用域 | function/class/module/package/session — 性能 vs 隔离性 | ⭐⭐⭐⭐⭐ |
| fixture vs setup/teardown | 灵活性、作用域、参数化、共享 | ⭐⭐⭐⭐⭐ |

## 今天没搞懂的问题

-
-

## 关联笔记

- [[Ch02-Pytest断言与框架结构]]（setup/teardown 部分）
- [[Ch08-Pytest测试用例生命周期管理-yield]]
