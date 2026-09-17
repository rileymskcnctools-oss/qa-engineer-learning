---
tags: [课程笔记, Flask, ORM]
course: "Flask"
chapter: "Ch13-ORM中间件配置"
created: 2026-09-17
status: in_progress
---

# Ch12 - ORM 中间件配置（SQLAlchemy）

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 test_platform_backend/flask/L3

---

## 一、SQLAlchemy 安装与使用步骤

### 知识点 1：Base + engine + Session 三步配置

【课程原话/定义】
SQLAlchemy 是 Python 著名的 ORM 工具包，用面向对象方式操作数据库。功能：ORM、SQL 表达式、事务支持、连接池管理、多数据库支持。

安装：pip install sqlalchemy

使用步骤（三个核心对象）：
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# 1. 创建基类（建表时用）
Base = declarative_base()

# 2. 创建引擎（连接数据库）
# SQLite:  sqlite:///数据库db文件路径
# MySQL:   mysql+pymysql://用户名:密码@主机:端口/数据库名
engine = create_engine('mysql+pymysql://root:pwd@127.0.0.1:3306/course')

# 3. 创建 Session 对象（绑定引擎）
DBSession = sessionmaker(bind=engine)
db_session: Session = DBSession()
```

【为什么？】
为什么要 Base + engine + Session 三个对象？因为三者各司其职：Base 是"模型基类"（所有表类都继承它，用于建表）；engine 是"数据库连接"（告诉 SQLAlchemy 连哪个库）；Session 是"操作会话"（真正执行增删改查、管理事务）。这个"基类 + 引擎 + 会话"三件套是 SQLAlchemy 的标准配置，缺一不可。理解它，就理解了 SQLAlchemy 的所有后续操作都是建立在这三者之上。

【必须掌握】
- pip install sqlalchemy
- Base = declarative_base()：模型基类
- engine = create_engine(连接配置)：数据库连接
- Session = sessionmaker(bind=engine)：操作会话
- 连接格式：mysql+pymysql://用户:密码@主机:端口/库名
- SQLite 格式：sqlite:///路径

【企业场景】
你在公司测试平台后端，用 SQLAlchemy 连 MySQL：Base 声明模型基类、engine 连 course 库、session 执行增删改查。这三行配置是每个 ORM 模块的"开头"，后续所有数据库操作都基于这个 session 对象。

【面试考察】
面试官：「SQLAlchemy 怎么配置连接数据库？」

参考回答框架：
1. Base = declarative_base() 声明基类
2. engine = create_engine(连接串) 创建引擎
3. sessionmaker(bind=engine) 创建会话
4. 连接串格式 mysql+pymysql://用户:密码@主机:端口/库

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 忘装 pymysql 驱动 | MySQL 连接要 mysql+pymysql，需 pip install pymysql |
| 连接串格式写错 | 是 mysql+pymysql://，不是 mysql:// |
| 三个对象混淆 | Base 建表、engine 连接、session 操作 |

【我的理解】
> （Base、engine、Session 三个对象分别承担什么职责？为什么 SQLAlchemy 要把"连接"和"操作"分成 engine 和 session 两个对象？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| SQLAlchemy 配置 | Base+engine+Session 三件套 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch11-ORM介绍]]
- [[Ch13-数据库与表管理]]
