---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch08-Pytest测试用例生命周期管理-yield"
date: 2026-07-23
status: draft
---

# Ch08 - Pytest 测试用例生命周期管理 - yield

## 课程来源

- 学习日期：

---

## 一、yield 在 fixture 中的工作流程

### 知识点1：yield 的三段式结构

【课程原话/定义】
在 fixture 函数中，使用 `yield` 语句分隔测试代码和清理代码。yield 之前 = 准备工作（Setup），yield 之后 = 清理工作（Teardown）。yield 可以将初始化的资源传递给测试函数。

【为什么？】
把 Setup 和 Teardown 写在同一个函数里用 yield 分隔，比分别写 `setup()` 和 `teardown()` 更内聚。你不需要在两个方法之间跳转才能理解"这个数据库连接在哪打开又在哪关闭的"。Python 的生成器（generator）机制保证了 yield 之后的代码一定会在测试函数执行完后执行——即使测试用例抛异常，teardown 也会执行（pytest 内部用 try/finally 包裹）。

【必须掌握】
- yield 前 = Setup，yield 后 = Teardown
- yield 后面的值会传给测试函数（相当于 return）
- 多个值用 `yield token, username` 返回元组
- 即使测试用例异常，yield 后的清理代码仍会执行
- 三段式流程：初始化 → 测试执行 → 清理

【企业场景】
你写了一个连接数据库的 fixture。测试前需要 `connect()`，测试后必须 `disconnect()` 否则连接池耗尽。你把连接对象放在 yield 前创建，yield 传给测试函数，disconnect 放在 yield 后。即使测试用例中间抛异常崩溃了，pytest 也会保证 disconnect 执行——就像 `try/finally` 一样可靠。

【面试考察】
面试官："fixture 中 yield 的作用是什么？如果测试用例抛异常，yield 后面的代码还会执行吗？"
参考回答框架：① yield 把 fixture 分成两段：前 = setup，后 = teardown ② yield 后的值传给测试函数（替代 return）③ 即使测试抛异常，yield 后面的代码也会执行（pytest 内部 try/finally 保证）④ 这是 fixture 比 setup/teardown 更优雅的地方——setup 和 teardown 写在一个函数里，逻辑内聚

【易错点】

| 常见错误                 | 正确做法                                    |
| -------------------- | --------------------------------------- |
| 把 return 放在 yield 后面 | yield 后不能再有 return 返回给调用方，yield 本身已经返回了 |
| yield 放在 fixture 开头  | yield 前应先执行初始化，否则 fixture 丧失了 setup 的功能 |
| 以为 yield 后不执行        | yield 后代码总是执行（类似 finally），除非进程被 kill    |
| 测试函数没接收 yield 的值     | 测试函数参数接收的是 yield 后面的值，需对应解包             |

【我的理解】

>

---

## 二、实战案例

### 知识点2：登录 + 登出的完整生命周期

【课程原话/定义】
场景：测试方法的前置操作（登录）已解决，运行后销毁清除数据（登出）如何实现？解决方案：在 fixture 函数中加入 yield 关键字，yield 前登录，yield 后登出。

【为什么？】
登录和登出是成对出现的操作（对称操作）。把这对操作放在同一个 fixture 的 yield 前后，保证了：① 只要登录了，就一定会登出 ② 不会出现"只登录忘了登出"的遗漏 ③ 代码审查时一眼就能确认资源管理的对称性。

【必须掌握】
- 完整 fixture 模板：
  ```python
  @pytest.fixture()
  def login():
      # setup
      token = get_token()
      yield token
      # teardown
      logout(token)
  ```
- scope 参数配合 yield 的用法（如 `scope='class'` 时整个类只登录一次）
- 测试函数接收方式：`def test_xxx(login):` 直接用

【企业场景】
你的自动化测试在 CI 里每天跑 500 条用例。有 80 条需要登录态。如果某条用例跑完没登出，session 泄漏会逐渐占满服务器的 session 表，后面所有用例都可能报"too many sessions"错误——你根本不知道是哪条用例导致的。用 yield 的 fixture 保证每条用例登出，session 泄漏问题从根源消除。

【面试考察】
面试官："给你一个场景：测试需要先创建订单，测试完需要删除订单（清理数据）。请用 fixture + yield 实现。"
参考回答框架：
```python
@pytest.fixture()
def order():
    order_id = create_order()      # setup: 创建订单
    yield order_id                  # 传给测试函数
    delete_order(order_id)          # teardown: 删除订单
```

【易错点】

| 场景            | 正确写法                                               | 错误写法                       |
| ------------- | -------------------------------------------------- | -------------------------- |
| 返回单个值         | `yield token` → `def test(token):`                 | `yield token,` → 多余的逗号变成元组 |
| 返回多个值         | `yield token, user` → `def test(login): t,u=login` | 忘记解包直接当单个值用                |
| 不需要返回值        | `yield`（后面不跟值）                                     | 刻意 `yield None`            |
| scope=class 时 | 整个类只 yield 一次，所有方法共享                               | 误解为每个方法都 yield 一次          |

【我的理解】

>

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| yield 三段式结构 | Setup → yield → Teardown | ⭐⭐⭐⭐⭐ |
| 异常安全性 | yield 后代码类似 finally，总是执行 | ⭐⭐⭐⭐ |
| 返回值传递 | yield 值传给测试函数 | ⭐⭐⭐⭐ |
| 实战模式 | 登录/yield/登出 对称操作 | ⭐⭐⭐⭐⭐ |

## 今天没搞懂的问题

-
-

## 关联笔记

- [[Ch07-Pytest测试用例生命周期管理-fixture]]
- [[Ch09-Pytest测试用例生命周期管理-自动注册]]
