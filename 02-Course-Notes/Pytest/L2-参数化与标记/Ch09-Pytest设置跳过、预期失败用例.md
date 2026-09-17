---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch09-Pytest设置跳过、预期失败用例"
created: 2026-09-17
status: in_progress
---

# Ch09 - Pytest 设置跳过、预期失败用例

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L2

---

## 一、skip / skipif / xfail

### 知识点 1：跳过和预期失败三种标记

【课程原话/定义】
有些用例无法通过或暂时不想执行，可以跳过或标记预期失败。

- **skip**：无条件跳过（装饰器或方法中）
- **skipif**：条件满足时跳过
- **xfail**：标记预期失败（失败不算真失败，意外通过显示 XPASS）

```python
import pytest, sys

@pytest.mark.skip                          # 无条件跳过
def test_a():
    assert True

@pytest.mark.skip(reason="代码没有实现")    # 带原因
def test_b():
    assert False

def test_skip_example():
    print("方法中设置跳过用例")
    pytest.skip("跳过这个用例")             # 方法中跳过

@pytest.mark.skipif(sys.platform == 'darwin', reason="mac 跳过")  # 条件跳过
def test_case1():
    assert True

@pytest.mark.xfail                          # 预期失败
def test_xfail():
    assert 1 == 2
```

【为什么？】
为什么要"跳过"和"预期失败"？因为真实项目里总有"还没实现的功能"、"某平台不支持的用例"、"已知的 bug"。如果这些用例硬跑，会让整个测试红一片，掩盖真正的新问题。skip 让"暂时不跑的"不执行，xfail 让"已知会失败的"执行但不算失败——这样测试结果才能准确反映"真正新增的问题"。区分 skip（不执行）和 xfail（执行但预期失败）是理解的关键。

【必须掌握】
- skip：无条件跳过（装饰器 @pytest.mark.skip 或 pytest.skip()）
- skipif：条件满足才跳过（@pytest.mark.skipif(条件, reason)）
- xfail：预期失败（@pytest.mark.xfail），失败记 xfail、意外通过记 XPASS
- reason 参数说明跳过原因
- skip 不执行，xfail 执行但不算失败

【企业场景】
你在公司测试，某功能还在开发、对应用例先 @pytest.mark.skip 跳过；某用例在 Mac 上跑不了，用 skipif 按平台跳过；某已知 bug 的用例标 xfail，等修好再去掉。这样测试结果干净，能快速看出"有没有新问题"。

【面试考察】
面试官：「skip、skipif、xfail 有什么区别？」

参考回答框架：
1. skip：无条件跳过，不执行
2. skipif：满足条件才跳过
3. xfail：预期失败，执行但失败不算失败（意外通过显示 XPASS）
4. 用途：管理未完成/平台限制/已知 bug 的用例

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| skip 和 xfail 混为一谈 | skip 不执行，xfail 执行但预期失败 |
| xfail 意外通过不知道 | xfail 用例通过会显示 XPASS（unexpectedly passed） |
| skipif 条件写反 | 条件为 True 时跳过，别写反 |

【我的理解】
> （为什么 xfail 用例"意外通过"会显示 XPASS 而不是 PASS？这提醒测试工程师什么？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 跳过/预期失败 | skip/skipif/xfail | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch07-Pytest标记测试用例]]
- [[Ch06-Pytest异常处理]]
