---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch04-Pytest标记测试用例"
date: 2026-07-21
status: draft
---

# Ch04 - Pytest 标记测试用例

> 前置：[[Ch01-Pytest入门]] / [[Ch02-Pytest断言与框架结构]] / [[Ch03-Pytest参数化用例]]

## 课程来源
- 学习日期：

---

## 一、什么是标记测试用例

### 知识点1：标记的定义与核心思想

【课程原话/定义】
在测试过程中，有时需要对测试用例进行标记，以便在运行测试时选择性地执行或跳过某些测试。Pytest 提供了灵活的测试标记功能，通过自定义标记标签来对测试用例进行分类。

【为什么？】
一个项目可能有几百上千条测试用例，你不能每次都全跑——时间不允许、也没有必要。你需要在不同场景下跑不同的用例子集：
- 提交代码后 → 只跑冒烟测试（5 分钟）
- 合并到主分支 → 跑全量回归（30 分钟）
- 凌晨定时任务 → 跑慢速/性能测试（2 小时）

标记（marker）就是给每条用例打标签，让你能像筛邮件一样筛选要跑的用例。没有标记 = 每次全跑或手动挑 = 低效且不可靠。

【必须掌握】
- `@pytest.mark.标签名` 装饰器给用例打标签
- `pytest -m 标签名` 命令行筛选
- 自定义 marker 必须在 `pytest.ini` 中注册
- 常用逻辑：`-m "smoke"` / `-m "smoke and not slow"` / `-m "smoke or regression"`

【企业场景】
> 你的 CI 流水线有三步：① 每次 git push → `pytest -m "smoke"`（必须 2 分钟跑完）② PR 合并前 → `pytest -m "smoke or regression"`（10 分钟）③ 凌晨 3 点 → `pytest -m "slow"`（跑大数据量场景，随便多久）。没有标记体系，这三步无法自动化区分。

【面试考察】
面试官："你们的测试用例怎么分类执行的？"
参考回答：① 用 Pytest 的 marker 机制，定义了 smoke/regression/slow 等标记 ② CI 中分阶段执行：提交跑 smoke，合并跑 regression，夜间跑 slow ③ 标记统一在 pytest.ini 中注册，防止拼写错误

【易错点】

| 易混淆                 | 区别            |
| ------------------- | ------------- |
| `@pytest.mark.skip` | 内置标记，跳过测试     |
| `@pytest.mark.自定义名` | 自定义标记，用于分类筛选  |
| `-m "标记"`           | 命令行列筛选        |
| `-k "关键词"`          | 按用例名筛选（不是按标记） |

【我的理解】
>

---

### 知识点2：标记的优点

【课程原话/定义】
1. 组织和分类测试：将用例分组归类，便于管理
2. 灵活选择测试：选择性执行或跳过特定用例

【为什么？】
标记本质上是给测试用例加了"元数据（metadata）"——不属于测试逻辑本身，但描述了测试的属性（快/慢/核心/边缘）。这让你在不修改测试代码的情况下，通过命令行控制执行范围。这是"关注点分离"原则在测试领域的应用。

【必须掌握】
- 标记 vs 文件名分类：文件名分类是物理分组（一个大目录），标记是逻辑分组（可以跨文件）
- 一条用例可以有多个标记：`@pytest.mark.smoke` + `@pytest.mark.regression`

【我的理解】
>

---

## 二、标记使用方法

### 知识点3：注册自定义标记

【课程原话/定义】
在测试用例方法上加 `@pytest.mark.标签名`。命令行执行用例时使用 `-m 标签名`。

【为什么？】
不注册会怎样？可以运行，但 pytest 会输出 Warning：
```
PytestUnknownMarkWarning: Unknown pytest.mark.xxx - is this a typo?
```
这看起来无害，但在企业项目中 Warning 通常是"待清理的技术债"——当 Warning 多了（100+），真正重要的 Warning 会被淹没。所以最佳实践：**所有自定义标记必须在 pytest.ini 中注册**。

【必须掌握】
在 `pytest.ini` 中：
```ini
[pytest]
markers =
    smoke: 冒烟测试 — 核心功能快速验证
    regression: 回归测试 — 全量功能验证
    slow: 慢速测试 — 大数据量/性能相关
```
格式：`标记名: 描述文字`（描述用 `--markers` 可查看）

命令行用法：
```bash
pytest -m "smoke"              # 只跑 smoke 标记
pytest -m "smoke and not slow" # smoke 但不含 slow
pytest -m "smoke or regression" # smoke 或 regression
pytest -m "not slow"           # 除了 slow 全跑
```

【企业场景】
> 新人入职第一周，你给 CI 流水线加了一个新的 marker `@pytest.mark.p0` 表示 P0 级别用例。你没在 pytest.ini 中注册，CI 日志里多了 200 条 Warning。TL 在 Code Review 时指出：先把 marker 注册了，再跑一遍确认 Warning 消失——这是基本规范。

【面试考察】
面试官："`-m` 和 `-k` 的区别是什么？"
参考回答：① `-m` 按标记筛选（需要先打标记），`-k` 按用例名称中的关键词筛选（不需要标记，模糊匹配）② `-m` 是与非的表达式，`-k` 只支持简单匹配 ③ 大项目用 `-m`（体系化），小项目/临时调试用 `-k`（方便快捷）

【易错点】

| 错误 | 后果 |
|------|------|
| 不注册 marker | pytest Warning，CI 日志噪音 |
| marker 名拼错 | `pytest -m "smok"` 匹配不到任何用例（静默跳过！） |
| `-m "smoke and slow"` | 只跑同时有 smoke 和 slow 标签的用例（通常很少） |

【我的理解】
>

---

### 知识点4：实战案例

【课程原话/定义】
给 `double(a)` 函数的不同测试场景打上不同标记（int/minus/float/zero/bignum/str），然后用 `-m` 筛选执行。

【为什么？】
这个案例展示了标记的典型用法：**按测试场景分类**。`double` 函数对于整数、负数、浮点、零、大数、字符串等场景，测试的"重要性"和"稳定性"不同。标记让你可以：
- 快速验证：`-m "int or zero"`（核心场景）
- 边界检查：`-m "minus or float"`（容易出错）
- 非主流：`-m "str"`（可能不支持，先标记再决定）

【必须掌握】
```python
import pytest

def double(a):
    return a * 2

@pytest.mark.int
def test_double_int():
    assert 2 == double(1)

@pytest.mark.minus
def test_double1_minus():
    assert -2 == double(-1)

@pytest.mark.float
def test_double_float():
    assert 0.2 == double(0.1)

@pytest.mark.zero
def test_double_0():
    assert 0 == double(0)

@pytest.mark.str
def test_double_str():
    assert 'aa' == double('a')
```

执行：`pytest -m "str"` → 只跑带 `str` 标记的用例

【企业场景】
> 你的项目有 500 条测试用例。产品经理说"这周只改了支付模块，确认一下没影响到其他地方"。你不用跑全部 500 条，跑 `pytest -m "payment or core"` 就够了——20 条用例，2 分钟出结果。这种效率提升是标记机制的核心价值。

【面试考察】
面试官："如果一个测试用例同时有 smoke 和 slow 标记，`pytest -m 'smoke and not slow'` 会执行吗？"
参考回答：不会。`smoke and not slow` 要求同时满足有 smoke 且没有 slow，而它两个都有，所以被排除。这是面试中常考的布尔逻辑。

【扩展知识】
Pytest 内置标记（无需注册）：
- `@pytest.mark.skip` — 无条件跳过
- `@pytest.mark.skipif` — 条件跳过
- `@pytest.mark.xfail` — 预期失败
- `@pytest.mark.usefixtures` — 使用 fixture
- `@pytest.mark.filterwarnings` — 过滤警告

【我的理解】
>

---

## 今日课程总结

| 模块        | 核心内容                      | 面试权重  |
| --------- | ------------------------- | ----- |
| 标记概念      | 元数据、逻辑分组、分类执行             | ★★★★  |
| 注册 marker | pytest.ini 中注册，避免 Warning | ★★★★★ |
| -m 筛选     | 标签表达式（and/or/not）         | ★★★★★ |
| 实战案例      | 按场景打标签 + 选择性执行            | ★★★★  |

---

## 今天没搞懂的问题

-
-
-

## 关联笔记
- [[Ch01-Pytest入门]]
- [[Ch02-Pytest断言与框架结构]]
- [[Ch03-Pytest参数化用例]]
