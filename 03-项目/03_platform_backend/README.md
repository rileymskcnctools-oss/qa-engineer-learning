# Platform Backend - 学生管理系统

基于 Flask 的学生信息管理系统，提供学生数据的增删改查功能。

## 文档

| 文档 | 说明 |
|------|------|
| [[架构分析-请求流程]] | 从整体架构到逐请求流程的深度分析，包含设计原理、面试要点、测试视角 |

## 功能特性

- 查看所有学生列表
- 添加新学生
- 修改学生信息
- 删除学生记录
- 数据输入校验
- 防止 SQL 注入

## 技术栈

- Python >= 3.13
- Flask >= 3.1.3
- PyMySQL >= 1.2.0
- MySQL 数据库
- HTML/CSS

## 项目结构

```
platform_backend/
├── pyproject.toml          # 项目配置和依赖
├── src/
│   ├── server.py           # Flask 主程序
│   ├── db.py               # 数据库操作模块
│   ├── templates/          # HTML 模板
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add.html
│   │   └── change.html
│   └── static/
│       └── css/
│           └── style.css
```

## 安装与运行

### 1. 安装依赖

```bash
uv sync
```

### 2. 运行项目

```bash
cd src
uv run server.py
```

### 3. 访问应用

浏览器打开: http://127.0.0.1:5000

## API 接口

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 学生列表 |
| `/add` | GET/POST | 添加学生 |
| `/change/<sid>` | GET/POST | 修改学生 |
| `/delete/<sid>` | DELETE/POST | 删除学生 |

## 数据库

- 服务器: `mysql.hogwarts.ceshiren.com:3306`
- 数据库: `hogwarts_stu`
- 数据表: `student_0802`

## 作者

蚊子