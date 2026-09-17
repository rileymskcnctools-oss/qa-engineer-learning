---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch26-Pytest内置插件hook体系"
created: 2026-09-17
status: in_progress
---

# Ch26 - Pytest 内置插件 hook 体系

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L4

---

## 一、hook 钩子函数

### 知识点 1：自动触发 + 预定义名称 + 执行顺序

【课程原话/定义】
Pytest 提供钩子（hook）函数扩展和自定义测试执行行为。钩子是在特定事件点自动调用的函数。

优点：自动触发（无需显式调用）、预定义名称、自定义操作、扩展性强、丰富的钩子库。

常见钩子及执行顺序：
```python
# 添加命令行参数（运行时先读取）
pytest_addoption
# 收集测试用例后（改编码、改执行顺序）
pytest_collection_modifyitems
# 收集完成后
pytest_collection_finish
# 运行测试前
pytest_runtest_setup
# 运行测试，返回 setup/call/teardown 结果
pytest_runtest_makereport
```

【为什么？】
为什么要理解 hook 体系？因为它是 pytest"可扩展性"的核心机制——测试框架本身行为（收集、执行、报告）都可以通过 hook 自定义。比如改测试用例名编码（pytest_collection_modifyitems）、添加自定义命令行参数（pytest_addoption）、自定义报告（pytest_runtest_makereport）。理解 hook 的"自动触发 + 预定义名称"，就理解了"pytest 插件为什么能无缝集成"——插件就是实现了这些预定义名称的函数。

【必须掌握】
- hook = 特定事件点自动调用的函数
- 自动触发，无需显式调用
- 预定义名称（pytest_xxx），pytest 自动识别
- 常见：pytest_addoption（命令行参数）、pytest_collection_modifyitems（收集后修改）、pytest_runtest_makereport（报告）
- hook 是插件开发的基础

【企业场景】
你在公司开发 pytest 插件，用 pytest_collection_modifyitems 修改测试用例名（解决中文乱码）、用 pytest_addoption 添加 --env 参数切换环境、用 pytest_runtest_makereport 自定义测试报告。hook 让你能定制 pytest 的行为。

【面试考察】
面试官：「pytest hook 是什么？有哪些常用 hook？」

参考回答框架：
1. hook 是特定事件点自动调用的函数
2. 预定义名称 pytest_xxx，自动识别
3. pytest_addoption 命令行参数
4. pytest_collection_modifyitems 收集后修改
5. 插件开发的基础

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| hook 函数名写错 | 必须用 pytest 预定义的名称 |
| 以为 hook 要显式调用 | 自动触发，无需调用 |
| 不知道执行顺序 | hook 按测试阶段触发（收集→执行→报告） |

【我的理解】
> （为什么"预定义名称"让 hook 能"自动触发"？pytest 是怎么找到并调用这些函数的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| hook 体系 | 自动触发 + 预定义名称 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch27-Pytest插件开发]]
- [[Ch25-Pytest插件]]
