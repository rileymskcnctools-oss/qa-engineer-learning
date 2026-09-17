---
tags: [课程笔记, Flask, ORM]
course: "Flask"
chapter: "Ch16-数据CRUD"
created: 2026-09-17
status: in_progress
---

# Ch15 - 数据 CRUD（增删改查）

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 test_platform_backend/flask/L3

---

## 一、增删改查四大操作

### 知识点 1：add / query / update / delete

【课程原话/定义】
CRUD = Create（增）、Read（查）、Update（改）、Delete（删）。

**新增**：
```python
user1 = User(id=1, username="张三", email="123@123.com")
db_session.add(user1)          # 单条添加
db_session.add_all([user2, user3])  # 批量添加
db_session.commit()            # 提交
db_session.close()             # 关闭
```

**查询**：
```python
db_session.query(User).all()                     # 查所有
db_session.query(User).filter_by(name="tom").all()  # 单条件
db_session.query(User).filter_by(name="tom").filter_by(id=2).all()  # 多条件
db_session.query(User).filter_by(id=1).first()   # 查单条
```

**修改**（两种方式）：
```python
# 方式一：查出来改对象属性
obj = db_session.query(User).filter_by(id=1).first()
obj.name = "Lily"
db_session.commit()

# 方式二：直接 update
db_session.query(User).filter_by(id=1).update({'name': "Harry"})
db_session.commit()
```

**删除**（两种方式）：
```python
# 方式一：查出来 delete
user = db_session.query(User).filter_by(id=1).first()
db_session.delete(user)
db_session.commit()

# 方式二：直接 delete
db_session.query(User).filter_by(id=1).delete()
db_session.commit()
```

【为什么？】
为什么要理解 CRUD？因为它是所有数据库操作的基础——测试平台后端不管多复杂，本质都是对数据做增删改查。而 SQLAlchemy 的 CRUD 有个关键规律：**增删改都要 commit() 才生效**（查不用），因为 Session 是"工作单元"模式，add/update/delete 只是把操作暂存，commit 才真正写库。理解这个规律，就不会犯"改了没 commit 结果没生效"的错误。查询的 filter_by（等值条件）+ first/all（单条/多条）是最常用的组合。

【必须掌握】
- 新增：add / add_all + commit
- 查询：query + filter_by（条件）+ first/all（单/多）
- 修改：对象属性改 / update(字典) + commit
- 删除：delete(对象) / query.delete() + commit
- 增删改必须 commit 才生效，查不需要
- 操作完建议 close 关闭 session

【企业场景】
你在公司测试平台，课程管理的增删改查就是这四组操作：新增课程 add+commit、查课程 filter_by(id).first()、改课程 update、删课程 delete。掌握这四个模板，就能写出任何数据的后端接口。

【面试考察】
面试官：「SQLAlchemy 怎么做增删改查？」

参考回答框架：
1. 增：add/add_all + commit
2. 查：query().filter_by().first()/all()
3. 改：对象改属性 / update() + commit
4. 删：delete() / query.delete() + commit
5. 增删改要 commit，查不用

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 增删改忘 commit | 不 commit 不生效，只是暂存在 session |
| 查询忘 first/all | query 返回 Query 对象，要 first()/all() 才出结果 |
| filter_by 和 filter 混淆 | filter_by 等值条件（filter_by(id=1)），filter 可复杂表达式 |

【我的理解】
> （为什么"增删改要 commit、查询不用"？这背后的 Session"工作单元"机制是怎么运作的？commit 之前的数据修改存在哪里？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| CRUD | add/query/update/delete + commit | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch14-对象与数据模型]]
- [[Ch16-多表关系-一对多]]
