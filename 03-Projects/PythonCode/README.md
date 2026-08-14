---
tags: [项目, Python]
project: "PythonCode"
start_date: 2026-07-13
end_date:
status: in_progress
---

# Python 练习代码

## 概述

- **目标**：存放 Python 学习过程中的所有练习代码，和 `02-Course-Notes/Python/` 的笔记一一对应
- **我的角色**：测试工程师方向学习者，代码围绕自动化测试场景编写

## 目录结构

```
PythonCode/
├── README.md
├── ch01_pycharm/          ← 对应 Ch01-PyCharm常用快捷键（无代码）
├── ch02_xxx/              ← 对应 Ch02，每章一个文件夹
│   ├── exercise_01.py
│   ├── exercise_02.py
│   └── exercise_03.py
└── ...
```

## 命名规则

| 规则 | 示例 |
|------|------|
| 文件夹 | `chXX_主题英文`，如 `ch03_string/` |
| 练习文件 | `exercise_序号.py` |
| 笔记对应 | `02-Course-Notes/Python/ChXX-章节名.md` 的实战练习 |

## 技术选型

| 技术 | 版本 | 原因 |
|------|------|------|
| Python | 3.x | 测试领域主流语言 |
| PyCharm | Community | 免费、Python 首选 IDE |

## 踩坑记录

| 问题 | 根因 | 方案 | 耗时 |
|------|------|------|------|
| | | | |

## 关键决策

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-07-13 | 练习代码放 03-Projects而非和笔记混放 | 笔记和代码分离，方便 git 管理和复盘 |

## 面试可讲

> "我的 Python 学习采用笔记+代码分离的方式：笔记在 Obsidian 里用测试视角整理，所有练习代码按章节归档到项目目录，每个练习都围绕测试场景（用户名校验、数据处理、批量执行），不做脱离测试的纯语法练习。"
