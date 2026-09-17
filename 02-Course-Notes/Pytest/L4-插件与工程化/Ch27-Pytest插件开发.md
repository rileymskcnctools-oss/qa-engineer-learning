---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch27-Pytest插件开发"
created: 2026-09-17
status: in_progress
---

# Ch27 - Pytest 插件开发

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L4

---

## 一、用 hook 开发插件

### 知识点 1：改编码 + 命令行参数 + 打包发布

【课程原话/定义】
插件开发用 hook 定制 pytest 行为：

1. **修改默认编码**（解决中文用例名乱码）：
```python
# conftest.py
def pytest_collection_modifyitems(session, config, items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
```

2. **添加命令行参数**（--env 切换环境）：
```python
def pytest_addoption(parser):
    mygroup = parser.getgroup("hogwarts")
    mygroup.addoption("--env", default='test', dest='env', help='set your run env')

@pytest.fixture(scope='session')
def cmdoption(request):
    myenv = request.config.getoption("--env", default='test')
    ...
```

3. **打包发布**：setup.py（entry_points 声明插件入口）→ 打包 → twine 上传 PyPI。

```python
# setup.py 关键配置
entry_points={'pytest11': ['pytest_encode = pytest_encode.main']}
```

【为什么？】
为什么要自己开发插件？因为团队有"通用但 pytest 没有内置"的需求——比如中文用例名乱码、按环境加载配置。插件开发用 hook 把这些通用逻辑封装成可复用组件，多个项目共享，不用重复写。setup.py 的 entry_points（pytest11）是插件的"注册入口"，让 pip 安装后 pytest 自动加载插件。理解"hook 实现逻辑 + entry_points 注册"，就理解了"pytest 插件"的完整开发链路。

【必须掌握】
- pytest_collection_modifyitems：收集用例后修改（改编码/顺序）
- pytest_addoption：添加命令行参数
- request.config.getoption 获取参数值
- setup.py entry_points pytest11 注册插件入口
- 打包：setup.py sdist bdist_wheel，发布 twine

【企业场景】
你在公司开发 pytest_encode 插件：用 pytest_collection_modifyitems 解决中文用例名乱码，用 pytest_addoption 加 --env 参数切换测试环境，打包发布到公司私有 PyPI 供团队复用。这就是"通用测试能力插件化"。

【面试考察】
面试官：「怎么开发一个 pytest 插件？」

参考回答框架：
1. 用 hook 实现功能（pytest_collection_modifyitems / pytest_addoption）
2. setup.py 的 entry_points pytest11 注册插件
3. 打包 sdist bdist_wheel
4. twine 发布 PyPI

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 忘 entry_points 注册 | 插件要 entry_points pytest11 声明，否则 pytest 不加载 |
| hook 函数签名不对 | pytest_collection_modifyitems(session, config, items) 参数要写对 |
| 插件逻辑直接写测试文件 | 应封装成插件复用 |

【我的理解】
> （为什么 entry_points 的 pytest11 是插件"被 pytest 识别"的关键？pytest 是怎么通过 entry_points 发现插件的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 插件开发 | hook + entry_points 打包 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch26-Pytest内置插件hook体系]]
- [[Ch25-Pytest插件]]
