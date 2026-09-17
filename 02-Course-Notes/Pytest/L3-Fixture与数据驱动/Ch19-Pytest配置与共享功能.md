---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch19-Pytest配置与共享功能"
created: 2026-09-17
status: in_progress
---

# Ch19 - Pytest 配置与共享功能（conftest.py）

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、conftest.py 共享配置

### 知识点 1：自动加载 + 作用范围 + 目录层级

【课程原话/定义】
conftest.py 是 pytest 的特殊配置文件，用于定义共享的 fixture、hooks 或全局设置。文件名固定，不可变化。

运行机制：
- **自动加载**：pytest 自动搜索并加载当前目录及上层目录的 conftest.py，无需显式导入
- **作用范围**：conftest.py 内容有全局作用，应用于当前目录及子目录所有测试文件
- **目录层级**：逐级向上查找 conftest.py（子目录 → 父目录 → 根目录）

```python
# conftest.py
import pytest
@pytest.fixture(scope="class")
def login():
    print("完成登录操作")
    token = "abcd"
    yield token
    print("完成登出操作")

# test_xxx.py（无需导入，直接使用）
def test_get_product(login):
    print("验证获取单品信息")
```

【为什么？】
为什么要 conftest.py？因为团队开发时有很多公共操作（登录、连数据库）多个测试文件都要用，如果每个文件都重复定义，冗余且难维护。conftest.py 让这些公共 fixture 集中定义一处，测试文件无需导入直接使用。它的"自动加载 + 逐级向上查找"机制，还支持"分层共享"——根目录的 conftest 全局共享，子目录的 conftest 局部共享。这是"配置集中管理 + 自动注入"的典型模式。

【必须掌握】
- conftest.py 文件名固定，不可改
- 自动加载，无需显式导入 fixture
- 作用范围：当前目录及子目录
- 逐级向上查找（子目录 → 父目录 → 根）
- 用途：团队共享的登录/数据库连接等公共 fixture

【企业场景】
你在公司测试平台，把登录 fixture、数据库连接 fixture 都放根目录 conftest.py，几十个测试文件直接使用，不用重复定义。某模块需要特殊 fixture，就在该模块目录下放自己的 conftest.py。这就是"集中 + 分层"的共享配置。

【面试考察】
面试官：「conftest.py 的作用和加载机制？」

参考回答框架：
1. conftest.py 定义共享 fixture/hooks
2. 文件名固定，自动加载无需导入
3. 应用于当前目录及子目录
4. 逐级向上查找，支持分层共享

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 改 conftest.py 文件名 | 文件名固定，改了 pytest 不识别 |
| 测试文件里导入 conftest 的 fixture | 无需导入，pytest 自动注入 |
| 放错位置 | conftest 作用范围是所在目录及子目录 |

【我的理解】
> （conftest.py 的"逐级向上查找"意味着什么？子目录和根目录各放一个 conftest，测试文件会加载哪个？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| conftest 共享 | 自动加载 + 分层共享 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch15-Pytest测试用例生命周期管理-自动注册]]
- [[Ch13-Pytest测试用例生命周期管理-fixture]]
