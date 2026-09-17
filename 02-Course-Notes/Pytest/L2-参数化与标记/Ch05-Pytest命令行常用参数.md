---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch05-Pytest命令行常用参数"
created: 2026-09-17
status: in_progress
---

# Ch05 - Pytest 命令行常用参数

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L2

---

## 一、用命令行参数控制测试运行

### 知识点 1：-v / -s / -k / -x / --maxfail / --collect-only

【课程原话/定义】
Pytest 支持多种命令行参数控制测试运行：

| 参数 | 作用 |
|------|------|
| --help | 查看所有参数 |
| -m | 执行某个标签的用例 |
| -v | 打印详细日志 |
| -s | 打印输出日志（常 -vs 连用） |
| -k | 执行包含某关键字的用例 |
| -x | 遇到第一个失败就停止 |
| --maxfail=num | 失败数达 num 后停止 |
| --collect-only | 只收集不执行 |

```bash
pytest test_double.py -vs            # 详细日志 + 打印输出
pytest test_double.py -k "str"       # 只执行含 str 的用例
pytest test_double.py -x             # 失败即停
pytest test_double.py --maxfail=3    # 失败 3 条后停
pytest --collect-only                # 只收集
```

【为什么？】
为什么要学命令行参数？因为"跑测试"不是只有 `pytest` 一种姿势——调试时想"只看失败"（-x）、"只看某个用例"（-k）、"看详细输出"（-vs）、"先收集不执行"（--collect-only）。这些参数让你能精准控制"跑哪些、怎么跑、什么时候停"，是日常调试和 CI 里高频使用的。理解它们，才能高效地"选择性执行"测试，而不是每次全量跑。

【必须掌握】
- -v 详细日志、-s 打印输出（常 -vs 连用）
- -k 关键字筛选用例
- -x 失败即停、--maxfail=num 失败 N 条停
- --collect-only 只收集不执行
- -m 按标签筛选（配合 mark）

【企业场景】
你在公司 CI 里跑测试，用例上千条，全量跑太慢。调试时用 -k "login" 只跑登录相关用例，用 -x 遇到失败就停快速定位问题，用 -vs 看详细输出。这些参数让"精准调试"成为可能。

【面试考察】
面试官：「pytest 常用命令行参数有哪些？」

参考回答框架：
1. -v/-s：详细日志和打印输出
2. -k：关键字筛选
3. -x/--maxfail：失败停止策略
4. --collect-only：只收集
5. -m：按标签筛选

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| -v 和 -s 分不清 | -v 是详细（verbosity），-s 是打印输出（show），常 -vs 连用 |
| -x 和 --maxfail 混用 | -x 遇第一个失败停，--maxfail 容忍 N 条失败 |
| -k 参数不加引号 | -k "str" 关键字要加引号 |

【我的理解】
> （-x 和 --maxfail=3 的区别是什么？分别适合什么场景？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 命令行参数 | -v/-s/-k/-x/--maxfail | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch10-Pytest运行用例]]
- [[Ch07-Pytest标记测试用例]]
