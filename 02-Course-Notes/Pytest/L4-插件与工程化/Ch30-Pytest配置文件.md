---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch30-Pytest配置文件"
created: 2026-09-17
status: in_progress
---

# Ch30 - Pytest 配置文件（pytest.ini）

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L4

---

## 一、pytest.ini 集中配置

### 知识点 1：运行规则 + 默认参数 + 目录 + 日志

【课程原话/定义】
pytest.ini 是 pytest 配置文件，集中管理测试运行设置。

```ini
[pytest]
; 改变运行规则（执行哪些文件/类/方法）
python_files = check_* test_*
python_classes = Test* Check*
python_functions = test_* check_*

; 添加默认参数（每次运行自动带上）
addopts = -v --cache-clear

; 指定/忽略目录
testpaths = bilibili baidu
norecursedirs = result logs datas test_demo*

; 日志配置
log_cli = true
log_cli_level = info
log_file = ./log/test.log
log_file_level = info
log_file_format = %(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)
```

【为什么？】
为什么要 pytest.ini？因为"配置和代码分离"——测试规则、默认参数、目录、日志这些"配置"不该硬编码在命令或代码里。pytest.ini 集中管理，一次配置处处生效：addopts 让每次运行自动带默认参数（不用每次敲 -v），testpaths 指定测试目录，日志配置统一输出。这呼应了"配置集中管理、易维护、可复用"的工程化思想，也是 CI 里统一测试行为的基础。

【必须掌握】
- pytest.ini 放在项目根目录
- python_files/classes/functions：改变收集规则
- addopts：默认命令行参数
- testpaths：指定测试目录，norecursedirs：忽略目录
- 日志：log_cli/log_file 等
- Windows 注意：ini 里中文注释要去掉（避免编码报错）

【企业场景】
你在公司测试项目根目录放 pytest.ini：统一测试文件命名规则、addopts 默认 -v、testpaths 指定测试目录、日志统一输出到 log 文件。团队所有人跑测试行为一致，CI 配置也基于这个文件。

【面试考察】
面试官：「pytest.ini 能配置什么？」

参考回答框架：
1. python_files/classes/functions 收集规则
2. addopts 默认参数
3. testpaths/norecursedirs 目录控制
4. 日志配置
5. 集中管理，配置与代码分离

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| pytest.ini 放错位置 | 放项目根目录，pytest 向上查找 |
| Windows 中文注释 | ini 里中文注释会报错，去掉 |
| addopts 忘写 | 默认参数要 addopts 配置 |

【扩展知识】
pytest.ini 是 pytest 配置的三种方式之一（还有 setup.cfg、pyproject.toml 的 [tool.pytest.ini_options]）。现代项目常用 pyproject.toml 统一管理（和 uv/poetry 一致），但 pytest.ini 仍是最简单直接的。理解 pytest.ini，是理解"pytest 配置体系"的入口。

【我的理解】
> （为什么"配置和代码分离"是工程化的核心？pytest.ini 相比"每次敲命令行参数"好在哪？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 配置文件 | pytest.ini 集中管理 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch05-Pytest命令行常用参数]]
- [[Ch25-Pytest插件]]
