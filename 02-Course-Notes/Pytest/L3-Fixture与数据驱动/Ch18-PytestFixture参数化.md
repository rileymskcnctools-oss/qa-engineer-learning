---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch18-PytestFixture参数化"
created: 2026-09-17
status: in_progress
---

# Ch18 - Pytest Fixture 参数化

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、params 实现 fixture 参数化

### 知识点 1：params + request.param + indirect

【课程原话/定义】
fixture 支持参数化：为 fixture 提供多个值，让多个用例使用不同数据。

基本语法：
```python
import pytest

@pytest.fixture(params=[1, 2, 3])     # params 传列表
def number(request):
    return request.param             # request.param 取当前参数

def test_number(number):
    assert number > 0
```

与 parametrize 结合（indirect=True 把参数传给 fixture）：
```python
@pytest.fixture
def database(request):
    return f"连接数据库: {request.param}"

@pytest.mark.parametrize("database", ["test_db1", "test_db2"], indirect=True)
def test_database_connection(database):
    assert "连接数据库" in database
```

【为什么？】
为什么要 fixture 参数化？因为有时候"被测环境"需要多组配置——比如测试要连多个数据库、多个用户角色、多个环境。普通 parametrize 是"给测试函数传参数"，而 fixture 参数化是"给 fixture 传参数"，让 fixture 本身能动态生成不同的环境。indirect=True 则是桥梁：把 parametrize 的数据传给 fixture 而不是直接给测试函数。理解"fixture 参数化"和"函数参数化"的区别，是理解"测试环境动态化"的关键。

【必须掌握】
- @pytest.fixture(params=[...]) 传多组参数
- request.param 取当前参数值
- 多参数：params 传嵌套列表
- indirect=True：把 parametrize 数据传给 fixture
- 用途：多数据库/多角色/多环境的测试

【企业场景】
你在公司测多环境（test/dev 数据库），用 fixture 参数化：fixture 的 params 传多个数据库配置，每个用例自动跑一遍不同环境。或者用 parametrize(indirect=True) 把环境名传给 fixture，fixture 根据环境加载对应配置。

【面试考察】
面试官：「fixture 怎么参数化？indirect 是什么？」

参考回答框架：
1. @pytest.fixture(params=[...]) + request.param
2. params 传列表，每个值生成一个用例
3. indirect=True 把 parametrize 数据传给 fixture
4. 用途：多环境/多配置测试

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 忘 request 参数 | fixture 参数化要加 request 形参取 request.param |
| indirect 和普通 parametrize 混淆 | indirect=True 传给 fixture，False（默认）传给函数 |
| params 和 parametrize 混用 | fixture 用 params，测试函数用 parametrize |

【我的理解】
> （fixture 参数化和函数参数化（parametrize）有什么本质区别？indirect=True 为什么能"把数据传给 fixture"？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| fixture 参数化 | params + request.param + indirect | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch13-Pytest测试用例生命周期管理-fixture]]
- [[Ch04-Pytest参数化用例]]
