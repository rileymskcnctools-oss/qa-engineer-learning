---
tags: [作业目录]
created: 2026-09-20
---

# 接口自动化测试 - 作业目录

## 目录结构

```
作业/
├── pyproject.toml           # 共享依赖声明（pytest + requests）
├── .python-version          # 锁定 Python 3.12
├── .venv/                   # 共享虚拟环境（gitignore）
├── homework01-api-basic/
├── homework02-api-basic/
├── ...
├── homework15-api-basic/
└── README.md
```

## 共享环境

所有作业共用一个 `.venv`（在 作业/ 根目录），代码仍在各自目录、互不干扰。

## 运行方式

```bash
# 在作业/ 目录下运行
.venv/Scripts/python -m pytest homework01-api-basic -v

# 运行所有作业
.venv/Scripts/python -m pytest -v
```

## PyCharm 解释器

指向：
```
C:\Users\riley\Desktop\code\qa-engineer-learning\02-Course-Notes\接口自动化测试\作业\.venv\Scripts\python.exe
```

## 新增依赖

在 作业/ 根目录执行 `uv add xxx`（写进根目录 pyproject.toml），不要在单个作业目录单独加。

## 打包交付

压缩包内含该作业的 `pyproject.toml` + `.python-version`（依赖声明），接收方解压后 `uv sync` 即可复现环境。
