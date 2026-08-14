---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch09-Pytest测试用例生命周期管理-自动注册"
date: 2026-07-23
status: draft
---

# Ch09 - Pytest 测试用例生命周期管理 - 自动注册（conftest.py）

## 课程来源

- 学习日期：

---

## 一、conftest.py 概念与运行机制

### 知识点1：conftest.py 是什么

【课程原话/定义】
conftest.py 是 pytest 中的特殊配置文件，用于定义共享的 fixture、hooks 或全局设置。文件名固定不可变。pytest 自动搜索并加载当前目录及上层目录中的 conftest.py，不需要显式导入。

【为什么？】
如果团队有 50 个测试文件都需要"登录"这个 fixture，每个文件都写一遍 `from common import login` 不仅麻烦，而且一旦 fixture 改名就要全局搜索替换。conftest.py 提供**隐式自动注入**——pytest 在启动时扫描目录树，找到所有 conftest.py 中的 fixture，测试函数直接用参数名引用，零导入、零配置。

【必须掌握】
- `conftest.py` 文件名固定，不可改名
- 自动加载：pytest 自动搜索并加载，无需显式 import
- 作用范围：conftest.py 作用于其所在目录及所有子目录
- 层级叠加：子目录的 conftest.py 会叠加父目录的（不是覆盖）
- 可以定义 fixture、hook 函数、pytest 插件配置

【企业场景】
你的项目结构如下：
```
tests/
├── conftest.py          ← 定义 login、connectDB（全局共享）
├── api/
│   ├── conftest.py      ← 定义 api_client（仅 api/ 子目录使用）
│   └── test_user.py
└── web/
    ├── conftest.py      ← 定义 browser（仅 web/ 子目录使用）
    └── test_homepage.py
```
全局 fixture（login）放在根 conftest.py，API 专属 fixture 放在 api/conftest.py，Web 专属 fixture 放在 web/conftest.py。不同团队的测试文件各取所需，互不干扰。这就是 conftest.py 的分层管理能力。

【面试考察】
面试官："conftest.py 的作用是什么？pytest 如何发现它？多个 conftest.py 的层级关系是怎样的？"
参考回答框架：① conftest.py 是 pytest 的全局配置/共享文件，存放 fixture 和 hook ② 文件名固定，pytest 运行时自动扫描当前目录及所有父目录 ③ 子目录的 conftest.py 会叠加父目录的（不会覆盖，是合并）④ 作用范围：当前目录及子目录 ⑤ 使用场景：团队共享 fixture、全局配置、pytest 插件

【易错点】

| 易混淆 | 正确理解 |
|------|------|
| conftest.py vs 普通 Python 模块 | conftest.py 不需要 import，pytest 自动加载；普通模块需显式导入 |
| 子 conftest.py 会覆盖父的吗？ | **不会覆盖，是叠加。** 子目录的测试可以同时使用父和子的 fixture |
| conftest.py 能改名吗？ | **不能。** 必须叫 conftest.py |
| conftest.py 放哪？ | 放在需要共享 fixture 的最顶层目录（通常是 tests/ 或项目根） |

【我的理解】

>

---

## 二、实战案例

### 知识点2：conftest.py 团队共享 fixture

【课程原话/定义】
在项目根目录下创建 conftest.py，在其中定义登录和连接数据库两个 fixture。测试用例直接传入 fixture 名称即可使用，不需要导入。

【为什么？】
团队协作中最常见的痛点：A 写了一个 login fixture 在 test_a.py 里，B 在 test_b.py 里想用但不知道该从哪导入（或者导入了发现依赖路径不对）。conftest.py 解决了"发现性"问题——所有人都知道去 tests/conftest.py 找全局 fixture，新成员 on-board 时打开一个文件就能看到所有可用的共享资源。

【必须掌握】
- conftest.py 中定义的 fixture 自动对所有子目录测试生效
- 测试文件不需要 `from conftest import xxx`
- 多个 fixture 可以组合使用：`def test_xxx(login, connectDB):`
- conftest.py 可以定义 hook（如 `pytest_collection_modifyitems`）

【企业场景】
你们的自动化测试框架有一个 `tests/conftest.py`，里面定义了 10 个全局 fixture：`login`、`connectDB`、`api_client`、`clean_data`、`mock_server` 等。新来的 QA 同事虽然不熟悉框架，但只要打开 conftest.py 就能看到所有可用的 fixture 和它们的 docstring，写新用例时在参数里声明需要的 fixture 即可，不需要追着同事问"这个怎么用、那个在哪导入"。

【面试考察】
面试官："你的团队有 30 个测试文件都需要用到登录 fixture，你怎么组织代码？"
参考回答框架：① 在 `tests/conftest.py` 中定义 `@pytest.fixture() def login():` ② 所有测试文件在测试函数参数中写 `def test_xxx(login):` 即可，pytest 自动注入 ③ 不需要在任何文件中 import ④ 如果某几个文件需要特殊的登录逻辑，可以在子目录建 conftest.py 覆盖/叠加

【易错点】

| 常见错误 | 正确做法 |
|------|------|
| 在测试文件中 `from conftest import login` | 不需要 import，直接声明参数即可 |
| 把 conftest.py 放在 src/ 下 | conftest.py 应放在 tests/ 目录或其父目录下 |
| 子 conftest.py 里定义同名 fixture | 会覆盖父 conftest 的同名 fixture（叠加但优先级更高） |
| conftest.py 里写测试用例 | conftest.py 只放 fixture/hook/配置，不放测试函数 |

【我的理解】

>

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| conftest.py 运行机制 | 自动加载、层级叠加、无需导入 | ⭐⭐⭐⭐⭐ |
| 团队共享实战 | 根 conftest.py 统一管理全局 fixture | ⭐⭐⭐⭐⭐ |
| 作用范围 | 当前目录 + 所有子目录 | ⭐⭐⭐⭐ |

## 今天没搞懂的问题

-
-

## 关联笔记

- [[Ch07-Pytest测试用例生命周期管理-fixture]]
- [[Ch08-Pytest测试用例生命周期管理-yield]]
- [[Ch10-Pytest测试用例生命周期管理-自动生效]]
