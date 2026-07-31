---
tags: [课程笔记, SQL, MySQL]
course: "SQL"
chapter: "Ch01-MySQL基础与SQL入门"
created: 2026-07-31
status: draft
---

# Ch01 - MySQL 基础与 SQL 入门

## 课程来源
- 学习日期：

---

## 一、MySQL 介绍

### 知识点 1：MySQL 是什么

【课程原话/定义】
MySQL 是目前最流行的开源数据库管理系统，完全网络化、跨平台的关系型数据库。由瑞典 MySQL AB 公司开发，现属于 Oracle。象征符号是一只名为 Sakila 的海豚，代表速度、能力、精确和优秀。

MySQL 可以称得上是目前运行速度最快的 SQL 数据库，并且完全免费。

【为什么？】
为什么要学 MySQL 而不是其他数据库？

| 数据库 | 特点 | 测试工程师学它的理由 |
|--------|------|---------------------|
| MySQL | 开源免费、速度快、社区庞大 | 互联网公司首选，面试必考 |
| PostgreSQL | 功能最强、标准兼容最好 | 外企和新兴项目越来越多用 |
| Oracle | 商业数据库、功能全 | 金融/政府/大企业用，贵 |
| SQLite | 嵌入式、零配置 | 本地测试、Mock 数据存储 |

MySQL 是测试工程师的"入门数据库"——不是因为最简单，而是因为最普遍。你面试的 10 家公司里 8 家用 MySQL。掌握了 MySQL，其他数据库触类旁通。

【必须掌握】
- MySQL 是关系型数据库（RDBMS），数据以表的形式存储
- 开源免费，属于 Oracle 公司
- 测试工程师的核心场景：查询测试数据、验证数据落库、构造测试数据

【企业场景】
作为测试工程师，你跟数据库打交道的典型场景：

| 场景 | SQL 操作 |
|------|----------|
| 验证注册功能 | `SELECT * FROM users WHERE username='test'` 确认数据落库 |
| 构造测试数据 | `INSERT INTO orders (...) VALUES (...)` 批量造订单 |
| 清理测试数据 | `DELETE FROM users WHERE username LIKE 'test%'` |
| 定位 bug | 前端显示错误 → 查数据库看实际存了什么 |
| 接口测试断言 | 调了创建接口 → 查数据库确认记录数 +1 |

【面试考察】
面试官："测试工程师为什么要学 SQL？你平时用 SQL 做什么？"

参考回答框架：
1. 验证数据落库：接口测试后查询数据库确认数据正确写入
2. 构造测试数据：批量 INSERT 造数据，覆盖边界场景
3. 定位 bug：对比前端显示和数据库实际值，快速判断问题在哪一层
4. 数据准备和清理：测试前造数据，测试后删数据

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 只关注接口返回，不查数据库验证 | 接口返回成功 ≠ 数据正确落库——必须查数据库二次确认 |
| 测试数据不清理 | 每个测试用例的数据要能独立清理，不要互相污染 |
| 直接在线上数据库操作 | 测试环境用测试库，永远不碰生产库 |

【我的理解】
> （你之前学的 Flask Mock 接口返回数据，和这里 MySQL 数据库中存储数据，两者的关系是什么？一个用户注册的完整流程：前端 → Flask 接口 → MySQL 数据库，每一步分别做了什么？）

---

### 知识点 2：MySQL 目录结构

【课程原话/定义】
MySQL 默认安装目录：`C:\Program Files\MySQL\MySQL Server 8\`

关键目录和文件：

| 路径 | 作用 |
|------|------|
| `my.ini` | MySQL 配置文件（一般不建议修改） |
| `data/` | 数据库文件所在目录（每个数据库一个子目录） |

【为什么？】
理解目录结构的意义在于排障。当 MySQL 启动不了时：
1. 先看 `my.ini` —— 端口、数据目录、字符集配置都在这里
2. 再看 `data/` —— 数据库文件是否完整、权限是否正确
3. `data/` 下每个子目录对应一个数据库——这就是为什么"数据库"在磁盘上是一个文件夹

【必须掌握】
- `my.ini` 是配置文件（端口 3306、字符集 utf8、数据目录路径等）
- `data/` 目录存所有数据库的实际数据文件
- 数据库 = `data/` 下的子目录 = 磁盘上的文件夹

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 直接修改 `my.ini` 然后 MySQL 起不来 | 改配置前先备份原文件 |
| 手动删除 `data/` 下的文件来"清空数据库" | 用 `DROP DATABASE`，不要手动删文件 |
| 重装 MySQL 后找不到之前的数据库 | 旧 `data/` 目录如果不备份，重装会丢失 |

【我的理解】
> （找到你电脑上 MySQL 的 `data/` 目录，看看里面有哪些子目录。每个子目录的名字和你在 Workbench 中看到的数据库名对应吗？打开一个数据库子目录，看看里面有哪些文件——`.frm` 和 `.ibd` 分别是干什么的？）

---

### 知识点 3：数据库表的基本概念

【课程原话/定义】

| 术语 | 定义 |
|------|------|
| 表（Table） | 包含数据库中所有数据的数据库对象 |
| 表名 | 每个表的唯一标识 |
| 模式（Schema） | 关于数据库和表的布局及特性的信息 |
| 列（Column） | 表中每列称为一个字段（Field） |
| 行（Row） | 表中的一个记录（Record） |

【为什么？】
理解这些术语是读懂 SQL 文档的前提。关系型数据库的"关系"指的就是表与表之间的关联（通过外键）。一张表就像一个 Excel 表格：
- 列 = Excel 的列（字段名 + 数据类型）
- 行 = Excel 的行（一条数据）
- 表名 = Excel 文件名

但数据库比 Excel 强在：可以定义约束（主键、外键、唯一、非空），保证数据一致性。

【必须掌握】
- 表 = 列的集合 + 行的集合
- Schema = 数据库（在 MySQL 中 Schema 和 Database 同义）
- 列有数据类型（INT、VARCHAR、DATE 等）
- 行是实际存储的数据记录

【企业场景】
测试数据管理的思维模型：把测试数据当成"表的行"来管理。

```
users 表
+----+----------+-------------+
| id | username | email       |
+----+----------+-------------+
| 1  | alice    | a@test.com  |  ← 一行 = 一条测试用户数据
| 2  | bob      | b@test.com  |
+----+----------+-------------+
```

写测试用例时思考：这个用例需要 users 表里有什么数据？执行完后 users 表会多/少/改哪些行？

【面试考察】
面试官："数据库中的 Schema 是什么？和 Database 有什么区别？"

参考回答框架：
1. 在 MySQL 中，Schema 和 Database 是同义词，`CREATE SCHEMA` = `CREATE DATABASE`
2. Schema 描述了数据库的结构：有哪些表、每个表有哪些列、列的类型和约束
3. 在其他数据库（如 Oracle）中 Schema 和 Database 有区别——Schema 是用户下的对象集合

【我的理解】
> （用 Excel 创建一个"学生表"：列是学号、姓名、年龄、成绩，填 5 行数据。然后对比数据库中的表，两者的区别是什么？数据库的表比 Excel 多了什么能力？）

---

## 二、数据库客户端工具

### 知识点 4：MySQL Workbench

【课程原话/定义】
Workbench 是 MySQL 官方提供的图形界面（GUI）交互工具。可以创建、浏览数据库结构，完成对数据库的各种操作和设计。

**连接信息：**
| 字段 | 值 |
|------|-----|
| Hostname | `127.0.0.1`（本机） |
| Port | `3306`（MySQL 默认端口） |
| Username | 合法用户名 |
| Password | 用户口令 |

**操作流程：**
- 创建数据库（Schema）：`Create Schema` → 输入名称 → Apply
- 创建表：右键 Tables → `Create Table` → 设置字段 → Apply
- 添加数据：右键表 → `Select Rows - Limit 5000` → 在表格中直接编辑 → Apply
- 查看表结构：表节点上的三个快捷按钮（设置信息 / 字段信息 / 数据）

【为什么？】
Workbench 的价值是"可视化"——同样的操作，用命令行需要记语法，用 Workbench 点几下就行。但作为测试工程师，你要做到：**Workbench 会操作，SQL 命令行也会写**。面试不会问你"怎么用 Workbench 建表"，而是考你 `CREATE TABLE` 语法。

【必须掌握】
- 连接信息四要素：Host + Port + User + Password
- `Create Schema` = 创建数据库
- 建表要设置：表名、字符集（utf8）、存储引擎（InnoDB/MyISAM）、字段
- 添加数据后要点 Apply 才会真正写入

【企业场景】
测试工程师用 Workbench 的场景：
1. **快速查看测试数据**：右键 → Select Rows，看测试是否产生了正确数据
2. **手动造边界数据**：直接在表格里编辑，比写 INSERT 语句更快（少量数据时）
3. **导出测试用例数据**：Workbench 有 Data Export 功能，导出 SQL 文件给其他测试环境用

【面试考察】
面试官："你用 Workbench 建过表吗？建表时需要设置哪些关键参数？"

参考回答框架：
1. 表名、字符集（utf8mb4）、存储引擎（InnoDB 支持事务）
2. 字段名、数据类型、是否允许 NULL、默认值
3. 主键（PRIMARY KEY）设置
4. Workbench 的 Apply 按钮背后生成的是 SQL 语句

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 改了数据但没点 Apply | Workbench 的编辑是"离线"的，必须 Apply 才写入 |
| 字符集选 latin1 | 中文数据必须选 utf8 或 utf8mb4 |
| 存储引擎选 MyISAM | 现代项目默认用 InnoDB（支持事务、行级锁、外键） |

【我的理解】
> （用 Workbench 完成一遍完整操作：创建数据库 → 创建表 → 添加 3 条数据 → 查看数据。然后找到 Workbench 生成的 SQL 语句——每次点 Apply 时 Workbench 会在弹窗里显示对应的 SQL，把这些 SQL 记下来，这就是你接下来要学的 DDL 和 DML。）

---

### 知识点 5：Navicat

【课程原话/定义】
Navicat 是一套商业数据库管理工具，支持 MySQL、Oracle、PostgreSQL、SQLite、SQL Server、MariaDB、MongoDB 等多种数据库，以及阿里云、腾讯云等云数据库。Navicat Premium 可以跨数据库系统传输数据。

连接信息与 Workbench 一致：Hostname `127.0.0.1`，Port `3306`。

【为什么？】
Navicat 和 Workbench 的对比：

| 对比维度 | Workbench | Navicat |
|----------|-----------|---------|
| 价格 | 免费 | 付费（有试用期） |
| 数据库支持 | 仅 MySQL | MySQL + PostgreSQL + Oracle + SQLite + ... |
| 数据导入导出 | 基础功能 | 更强大（Excel/CSV/JSON 导入导出向导） |
| 界面 | 功能型 | 更美观直观 |
| 适用场景 | 个人学习、MySQL 专用 | 企业多数据库管理 |

测试工程师用 Navicat 的优势：数据导入导出功能强大——可以把测试数据从 Excel 一键导入数据库，也可以把查询结果导出为 Excel 给开发看。

【必须掌握】
- Navicat 是付费工具，Workbench 是免费替代
- 连接信息与 Workbench 完全一致
- Navicat 的核心优势：多数据库支持 + 强大的导入导出

【企业场景】
测试工程师用 Navicat 的典型工作流：
1. 用 Excel 准备测试数据（100 条用户记录）
2. Navicat 导入向导 → 选择 Excel 文件 → 映射列 → 一键导入
3. 跑完测试后，Navicat 导出查询结果为 Excel → 发给开发作为 bug 证据

```sql
-- Navicat 中保存的常用查询
-- 查询今天创建的测试用户
SELECT * FROM users WHERE username LIKE 'test%' AND DATE(created_at) = CURDATE();

-- 清理今天的所有测试数据
DELETE FROM orders WHERE remark = 'auto_test';
```

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 付费软件过期了才发现 | 提前了解 Workbench 作为替代方案 |
| Navicat 导入时字符集不匹配导致中文乱码 | 导入前确认源文件和目标表的字符集都是 utf8 |
| 在 Navicat 里直接编辑线上数据 | 明确区分测试库和线上库——颜色标记连接 |

【我的理解】
> （分别用 Workbench 和 Navicat 连接同一个数据库，各创建一个表。对比两者的操作流程：哪个步骤更少？哪个更直观？你认为测试工程师日常用哪个更高效？）

---

## 三、SQL 简介

### 知识点 6：SQL 是什么及通用语法

【课程原话/定义】
SQL（Structured Query Language）是结构化查询语言，用来存取数据以及查询、更新和管理关系数据库系统。SQL 是所有关系型数据库的统一查询规范，不同数据库之间的 SQL 有一些区别但大体相同。

**通用语法规则：**
- 单行或多行书写，以分号 `;` 结尾
- 空格和缩进增加可读性
- MySQL 中不区分大小写，一般关键字大写、数据库名/表名/列名小写
- 注释方式：`-- 单行注释`、`/* 多行注释 */`

【为什么？】
SQL 是测试工程师的"第二语言"——你写的测试脚本用 Python，但你查的数据用 SQL。理解 SQL 的通用语法规则能让你在 MySQL、PostgreSQL、Oracle 之间切换时快速适应。

大小写规则不是强制语法，而是团队约定：

```sql
-- 推荐写法（关键字大写，名称小写）
SELECT id, username, email
FROM users
WHERE status = 'active';

-- 也能跑但不推荐
select id, username, email from users where status = 'active';
```

【必须掌握】
- SQL 语句以 `;` 结尾
- 关键字推荐大写（SELECT、FROM、WHERE），名称小写
- 单行注释 `--`，多行注释 `/* */`
- SQL 不区分大小写（但区分字符串内容）

【企业场景】
写测试脚本时，Python 里嵌入 SQL 的格式规范：

```python
# 好的写法——多行字符串 + 清晰的格式
sql = """
    SELECT id, username, email
    FROM users
    WHERE status = %s
      AND created_at > %s
    ORDER BY id DESC
    LIMIT 100
"""
cursor.execute(sql, ('active', '2026-01-01'))
```

【面试考察】
面试官："SQL 的注释有哪几种写法？Python 代码中怎么嵌入 SQL 语句比较规范？"

参考回答框架：
1. `--` 单行注释、`/* */` 多行注释
2. Python 中用三引号多行字符串，保持 SQL 的缩进和可读性
3. 参数化查询（`%s` 占位符）防止 SQL 注入

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| SQL 语句忘记分号 | 每条 SQL 以 `;` 结尾（某些客户端不强制但规范要求） |
| 字符串用双引号 | MySQL 中字符串用单引号 `'value'`，双引号在某些模式下当标识符 |
| Python 中拼接 SQL 字符串 | 用参数化查询（`%s`），不要用 f-string 拼接（SQL 注入风险） |

【我的理解】
> （打开 Workbench 或命令行，执行以下 SQL，观察结果：`SELECT 'Hello SQL';` `SELECT 1 + 1;` `SELECT NOW();`。这说明 SQL 不仅能查表，还能做计算和调用函数——你能想到测试中怎么用这些能力吗？）

---

### 知识点 7：SQL 四大分类

【课程原话/定义】
SQL 按功能分为四大类：

| 分类 | 全称 | 用途 | 核心关键字 |
|------|------|------|-----------|
| DDL | Data Definition Language | 定义数据库对象（库、表、列） | CREATE、ALTER、DROP |
| DML | Data Manipulation Language | 操作表中记录 | INSERT、UPDATE、DELETE |
| DQL | Data Query Language | 查询表中记录 | SELECT |
| DCL | Data Control Language | 定义访问权限和安全级别 | GRANT、REVOKE |

【为什么？】
这四类的划分不是学术概念——它们对应测试工程师的四类日常操作：

| 分类 | 测试场景 |
|------|----------|
| DDL | 搭建测试数据库结构（创建测试用的表和字段） |
| DML | 造测试数据（INSERT）、修改测试数据（UPDATE）、清理测试数据（DELETE） |
| DQL | 验证数据落库（SELECT）、定位 bug（查数据对不对） |
| DCL | 很少用到（通常是 DBA 的工作） |

测试工程师 90% 的 SQL 操作集中在 DQL（查）和 DML（增删改）。

【必须掌握】
- DDL：CREATE（建库建表）、ALTER（修改表结构）、DROP（删除）
- DML：INSERT（插入）、UPDATE（更新）、DELETE（删除记录）
- DQL：SELECT（查询）——最常用
- DCL：GRANT（授权）、REVOKE（回收权限）——测试工程师少用

【企业场景】
一个测试用例的全生命周期 SQL：

```sql
-- 1. DDL：搭建测试环境（建表——通常提前建好，测试中不重复建）
CREATE TABLE test_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    email VARCHAR(100)
);

-- 2. DML：准备测试数据
INSERT INTO test_users (username, email) VALUES ('test_user', 'test@test.com');

-- 3. 执行测试（调用接口、操作页面...）

-- 4. DQL：验证结果
SELECT * FROM test_users WHERE username = 'test_user';
-- 预期：返回 1 条记录，email = 'test@test.com'

-- 5. DML：清理测试数据
DELETE FROM test_users WHERE username = 'test_user';
```

这就是"测试数据管理"的完整闭环。

【面试考察】
面试官："SQL 的 DDL 和 DML 有什么区别？测试工程师主要用哪几类？"

参考回答框架：
1. DDL 定义结构（建库建表），DML 操作数据（增删改），DQL 查询数据
2. 测试工程师主要用 DQL（验证数据）和 DML（造数据、清理数据）
3. DDL 在搭建测试环境时用，日常测试中用得较少
4. DCL 是 DBA 的工作，测试工程师基本不用

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| DELETE 和 DROP 混淆 | DELETE 删记录（DML），DROP 删表/库（DDL） |
| 认为 SELECT 是 DML | SELECT 单独分类为 DQL，因为它不修改数据 |
| 在测试中频繁执行 DDL | 建表建库是一次性的，测试循环中只做 DML + DQL |

【我的理解】
> （不看书，写出每条 SQL 属于哪个分类：① `CREATE DATABASE test;` ② `INSERT INTO users VALUES (1, 'a');` ③ `SELECT * FROM users;` ④ `DROP TABLE users;` ⑤ `UPDATE users SET name='b' WHERE id=1;` ⑥ `GRANT SELECT ON *.* TO 'user';`。全部答对才算掌握。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| MySQL 介绍 | 开源 RDBMS、测试工程师的数据库场景 | ★★★☆☆ |
| 目录结构 | `my.ini`、`data/` 目录 | ★★☆☆☆ |
| 表的概念 | 表/列/行/Schema、和 Excel 的类比 | ★★★★☆ |
| Workbench | 连接信息、建库建表、添加数据、Apply 机制 | ★★★☆☆ |
| Navicat | 多数据库支持、导入导出优势 | ★★☆☆☆ |
| SQL 通用语法 | 分号结尾、大小写规范、注释 | ★★★★☆ |
| SQL 四大分类 | DDL/DML/DQL/DCL、测试工程师侧重 | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[../接口测试/Ch03-请求与响应处理]] — request.json 获取请求体
