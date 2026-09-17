---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch06-Pytest异常处理"
created: 2026-09-17
status: in_progress
---

# Ch06 - Pytest 异常处理

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L2

---

## 一、pytest.raises 断言异常

### 知识点 1：try/except 与 pytest.raises

【课程原话/定义】
异常处理是捕获代码抛出的异常。Pytest 提供 pytest.raises 上下文管理器捕获特定异常并断言。

```python
import pytest

def test_raise():
    # 捕获 ValueError，且消息匹配 "must be 0 or None"
    with pytest.raises(ValueError, match='must be 0 or None'):
        raise ValueError("value must be 0 or None")

def test_raise1():
    # 用 exc_info 获取异常详情，断言类型和消息
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("value must be 42")
    assert exc_info.type is ValueError
    assert exc_info.value.args[0] == "value must be 42"
```

【为什么？】
为什么要专门用 pytest.raises 断言异常？因为测试"异常场景"是单元测试的重要部分——不仅要测"正常输入返回正确结果"，还要测"非法输入抛出正确异常"。传统 try/except 能捕获异常，但"断言异常类型和消息"要手写；pytest.raises 把"捕获 + 断言"合二为一：如果抛出的异常类型/消息符合预期，测试通过，否则失败。这是"验证代码是否正确处理异常"的标准工具。

【必须掌握】
- pytest.raises(异常类型)：捕获并断言异常
- match 参数：断言异常消息包含某字符串
- as exc_info：获取异常详情（type、value）
- exc_info.value.args[0] 取异常消息
- 发生异常后 with 块内代码不再执行

【企业场景】
你在公司测除法函数，要验证"除数为 0 抛 ZeroDivisionError"。用 pytest.raises(ZeroDivisionError) 包住调用，异常抛出即测试通过。这比 try/except + 手动 assert 更简洁、更清晰。

【面试考察】
面试官：「pytest 怎么测试异常场景？」

参考回答框架：
1. 用 pytest.raises(异常类型) 上下文管理器
2. match 参数断言异常消息
3. as exc_info 获取异常详情
4. 异常类型/消息符合预期则测试通过

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| try/except 里吞掉异常不当失败 | pytest.raises 让"没抛异常"自然失败 |
| match 参数写错 | match 是正则匹配异常消息子串 |
| 忘 as exc_info | 要断言异常详情时用 as exc_info 接收 |

【我的理解】
> （pytest.raises 相比 try/except，为什么更适合"断言异常"？它内部是怎么判断"抛出的异常符合预期"的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 异常处理 | pytest.raises 捕获断言异常 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch02-Pytest断言与框架结构]]
- [[Ch09-Pytest设置跳过、预期失败用例]]
