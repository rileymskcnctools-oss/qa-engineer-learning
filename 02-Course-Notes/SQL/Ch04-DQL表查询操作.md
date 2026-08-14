---
tags: [课程笔记, SQL, MySQL]
course: "SQL"
chapter: "Ch04-DQL表查询操作"
created: 2026-07-31
status: draft
---

# Ch04 - DQL 表查询操作

> ⚠️ **本章是 SQL 课程最重要的章节。** 测试工程师 90% 的 SQL 操作都是 DQL（SELECT 查询），面试中至少 60% 的 SQL 题都考查询。学完这一章，你就能独立完成数据验证、bug 定位、测试数据准备等日常工作。

## 课程来源
- 学习日期：
- 参考数据库：employees test database (https://github.com/datacharmer/test_db)

---

## 前言：employees 测试数据库介绍

本章所有 SQL 示例均基于 GitHub 开源的 employees 测试数据库（300,024 条员工记录，约 2,844,047 条薪资记录），数据库结构如下：

```
employees 表          departments 表        dept_emp 表（员工-部门关联）
├─ emp_no (PK)        ├─ dept_no (PK)       ├─ emp_no (FK)
├─ birth_date         ├─ dept_name          ├─ dept_no (FK)
├─ first_name                              ├─ from_date
├─ last_name          dept_manager 表        ├─ to_date
├─ gender             ├─ emp_no (FK)
├─ hire_date          ├─ dept_no (FK)       titles 表
                       ├─ from_date          ├─ emp_no (FK)
salaries 表            ├─ to_date            ├─ title
├─ emp_no (FK)                              ├─ from_date
├─ salary                                    ├─ to_date
├─ from_date
├─ to_date
```

---

## 一、基础查询

### 知识点 1：SELECT * 和 SELECT 列名

【课程原话/定义】

`SELECT` 是 DQL（Data Query Language）的核心语句，用于从表中查询数据。最基础的两种写法：

```sql
-- 查询所有列
SELECT * FROM employees;

-- 查询指定列
SELECT emp_no, first_name, last_name FROM employees;
```

- `SELECT *` 返回表中所有列
- `SELECT 列1, 列2, ...` 只返回指定的列
- 列名之间用逗号分隔

【为什么？】

**永远不要在正式代码中用 `SELECT *`！** 原因有三：

| 原因 | 说明 |
|------|------|
| 性能浪费 | 传输不需要的列，增加网络和内存开销 |
| 列顺序依赖 | 代码依赖 `*` 的列顺序，表结构一变就崩 |
| 可读性差 | 读代码的人不知道你实际需要哪些列 |

但在测试场景中 `SELECT *` 有一个合法用途：**快速预览**。比如你刚造了 10 条测试数据，想快速看一眼全貌，`SELECT *` 比写 20 个列名快得多。

【必须掌握】

- `SELECT *` 查询所有列（仅用于临时的数据预览）
- `SELECT col1, col2` 查询指定列（生产代码中的标准写法）
- 多条 SQL 语句用 `;` 分隔

【企业场景】

作为测试工程师，你查询数据库时的心态和开发不一样：

```sql
-- ❌ 开发写的接口返回 {user_id, name, email, phone, address, ...}
--    你说"接口返回不对"，开发让你查数据库验证

-- ✅ 直接查相关字段，不关心全表
SELECT emp_no, first_name, last_name, hire_date
FROM employees
WHERE emp_no = 10001;
-- 结果: 10001 | Georgi | Facello | 1986-06-26
-- 然后跟接口返回对比——这就是数据验证
```

```sql
-- 测试中的数据验证模式：接口返回什么，你就 SELECT 什么列
-- Python 中的典型写法：
cursor.execute("""
    SELECT emp_no, first_name, last_name, gender
    FROM employees
    WHERE emp_no = %s
""", (emp_id,))
row = cursor.fetchone()
assert row['first_name'] == api_response['first_name']  # 数据库对比接口
```

【面试考察】

面试官："`SELECT *` 和 `SELECT 列名` 有什么区别？项目中你为什么不用 `SELECT *`？"

参考回答框架：
1. `SELECT *` 返回所有列，`SELECT 列名` 只返回指定列
2. 不用 `*` 的原因：性能（传输多余数据）、健壮性（表结构变化时不会意外错位）、可读性
3. 测试场景中偶尔用 `*` 快速预览数据，但测试脚本中一定指定列名

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 自动化脚本中写 `SELECT *` | 明确列出需要的列名 |
| 列名拼写错误（MySQL 不报错？） | MySQL 会报 "Unknown column"，但大小写问题可能被忽略 |
| 以为 `SELECT *` 列顺序永远不变 | 表结构 ALTER 后列顺序可能变化，导致代码取错值 |
| 忘记加 `;` 结尾 | 多条语句必须用 `;` 分隔 |

【我的理解】

> （打开 Workbench 或命令行，对 employees 数据库执行：① `SELECT * FROM employees LIMIT 5;` 观察所有列；② `SELECT emp_no, first_name, last_name FROM employees LIMIT 5;` 只显示三列。对比两个结果——你能感受到 `*` 返回了多少你不需要的列吗？）

---

### 知识点 2：字段别名（AS）

【课程原话/定义】

`AS` 关键字用于给列或表达式起别名，让查询结果更可读。AS 可以省略（但建议保留）。

```sql
-- 完整写法
SELECT emp_no AS 员工编号, first_name AS 名, last_name AS 姓
FROM employees;

-- AS 可省略（但不推荐）
SELECT emp_no 员工编号, first_name 名, last_name 姓
FROM employees;
```

别名也可以用于计算列：

```sql
SELECT emp_no, salary, salary * 12 AS 年薪
FROM salaries;
```

【为什么？】

别名在测试工程师的工作中有三个重要用途：

1. **让查询结果直接对应接口字段名**：接口返回 `employee_id`，但数据库列名是 `emp_no`，加个别名就能对上

2. **计算列必须有别名**，否则列名显示为表达式本身（如 `salary * 12`），代码里很难引用

3. **导出的测试报告更可读**：给开发看数据时列名是中文，一目了然

【必须掌握】

- `AS '别名'`（推荐）或 `AS 别名`
- 别名中有空格或特殊字符时用引号包裹：`AS 'Annual Salary'`
- AS 可以省略但强烈建议保留
- 别名在 WHERE 中不能用，在 ORDER BY 中可以用

【企业场景】

```sql
-- 场景1：数据导出给开发看——用中文别名，一眼看懂
SELECT
    emp_no        AS '员工编号',
    first_name    AS '名',
    last_name     AS '姓',
    hire_date     AS '入职日期'
FROM employees
WHERE hire_date >= '1999-01-01'
ORDER BY hire_date DESC;

-- 场景2：测试脚本中让数据库列名和接口字段对齐
SELECT
    emp_no      AS employee_id,
    first_name  AS firstName,
    last_name   AS lastName,
    gender      AS gender
FROM employees
WHERE emp_no = 10001;
-- Python: row['employee_id'] == api_resp['employee_id']  ← 字段名一致
```

【面试考察】

面试官："SQL 中 AS 的作用是什么？别名能在 WHERE 中使用吗？"

参考回答框架：
1. AS 给列或表达式起别名，让结果集列名更可读
2. 别名不能用在 WHERE 中（执行顺序：WHERE 先于 SELECT 执行，此时别名还未生效）
3. 别名可以用在 ORDER BY 中（ORDER BY 在 SELECT 之后执行）
4. 别名可以用在 GROUP BY 中（MySQL 扩展支持）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 在 WHERE 中使用别名 | `WHERE 年薪 > 100000` 报错，改用 `WHERE salary * 12 > 100000` |
| 别名含空格但没加引号 | `AS Annual Salary` 报错，应写 `AS 'Annual Salary'` |
| 中文别名在某些客户端乱码 | 确认客户端字符集是 utf8mb4 |

【我的理解】

> （执行以下 SQL，观察每次结果列名的变化：① `SELECT emp_no, salary * 12 FROM salaries LIMIT 3;` 列名是什么？② `SELECT emp_no, salary * 12 AS 年薪 FROM salaries LIMIT 3;` 列名变化了吗？③ 试试 `SELECT emp_no, salary * 12 AS 年薪 FROM salaries WHERE 年薪 > 500000;` —— 能执行吗？为什么？）

---

### 知识点 3：DISTINCT 去重

【课程原话/定义】

`DISTINCT` 关键字用于去除查询结果中的重复行，只返回唯一值。

```sql
-- 查询所有不重复的姓氏
SELECT DISTINCT last_name FROM employees;

-- 多列去重：组合值全部相同才算重复
SELECT DISTINCT first_name, last_name FROM employees;
```

【为什么？】

测试工程师经常需要回答"有哪些"类的问题——这时必须去重：

| 问题 | 需要 DISTINCT？ |
|------|----------------|
| "系统里有多少个部门？" | ✅ `SELECT DISTINCT dept_no FROM dept_emp;` |
| "这个部门有哪些职称？" | ✅ `SELECT DISTINCT title FROM titles WHERE emp_no IN (SELECT emp_no FROM dept_emp WHERE dept_no='d005');` |
| "员工表有多少行？" | ❌ `SELECT COUNT(*) FROM employees;` |
| "1990年后入职的有多少人？" | ❌ 不需要去重，COUNT 就行 |

关键判断：**你关心的是"有哪些值"还是"有多少条记录"**——前者用 DISTINCT，后者用 COUNT。

【必须掌握】

- `SELECT DISTINCT col1 FROM table`：对单列去重
- `SELECT DISTINCT col1, col2 FROM table`：对多列组合去重
- DISTINCT 作用于所有选择的列，不能 `DISTINCT col1, col2` 只对 col1 去重
- DISTINCT 和 `SELECT *` 一起用时，所有列完全相同的行才算重复

【企业场景】

```sql
-- 场景1：验证数据——系统有多少个部门？部门名称是什么？
SELECT DISTINCT d.dept_no, d.dept_name
FROM departments d
JOIN dept_emp de ON d.dept_no = de.dept_no;

-- 场景2：bug 定位——用户反馈下拉框里的部门有重复
-- 先查数据库确认：部门表中 dept_name 是否有重复？
SELECT dept_name, COUNT(*) AS cnt
FROM departments
GROUP BY dept_name
HAVING cnt > 1;
-- 如果返回空 → 数据库没问题，bug 在前端

-- 场景3：测试数据准备——我需要 5 个不同的职位名称来构造测试数据
SELECT DISTINCT title FROM titles LIMIT 5;
-- 结果: Senior Engineer, Staff, Engineer, Senior Staff, Assistant Engineer
```

【面试考察】

面试官："DISTINCT 去重的原理是什么？多列去重是怎么判断重复的？"

参考回答框架：
1. DISTINCT 对 SELECT 后的所有列进行组合去重
2. 只有所有选择的列值完全相同时，才视为重复行
3. `DISTINCT col1, col2` 表示 col1 和 col2 的组合值唯一，不是单独对 col1 去重
4. 如果只需要对某列去重并查看该列的值，应该 `SELECT DISTINCT col1 FROM table`

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 `SELECT DISTINCT col1, col2` 只对 col1 去重 | DISTINCT 对所有选择的列组合去重 |
| 用 DISTINCT 替代 COUNT | `SELECT DISTINCT COUNT(*)` 是错误的语法 |
| DISTINCT 后接多个列导致"看起来没去重" | 因为组合值不同，不是 DISTINCT 失效 |

【我的理解】

> （在 employees 库中：① `SELECT DISTINCT title FROM titles;` 看有多少种职位；② `SELECT DISTINCT first_name, last_name FROM employees;` 和 ③ `SELECT DISTINCT first_name FROM employees;` 的结果数量有什么不同？为什么？）

---

### 知识点 4：查询中的算术运算

【课程原话/定义】

SQL 中可以在 SELECT 中对数值列进行算术运算：`+`、`-`、`*`、`/`、`%`（取模）和 `DIV`（整数除法）。

```sql
-- 基本运算
SELECT emp_no, salary, salary * 12     AS 年薪,
                      salary / 12      AS 月均,
                      salary * 0.2     AS 奖金
FROM salaries;

-- 运算符组合
SELECT emp_no, salary, (salary * 12) + 5000 AS 年薪加补贴
FROM salaries;
```

【为什么？】

测试工程师的"计算验证"场景：

| 场景 | 算术用途 |
|------|----------|
| 验证薪资计算 | 接口返回年薪=月薪×12？`SELECT salary*12 vs api_response` |
| 验证折扣计算 | 订单金额×折扣率=实付金额？ |
| 构造边界数据 | 最大值+1，最小值-1 |
| 验证统计值 | AVG 的结果和你手算的一致吗？ |

记住：**数据验证不只是"查出来看一眼"，而是用 SQL 做计算验证！**

【必须掌握】

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `+` | 加法 | `salary + 1000` |
| `-` | 减法 | `salary - 500` |
| `*` | 乘法 | `salary * 12` |
| `/` | 除法（浮点结果） | `salary / 12` |
| `DIV` | 整数除法 | `10 DIV 3` → 3 |
| `%` 或 `MOD` | 取模（取余） | `10 % 3` → 1 |

- `NULL` 参与任何算术运算结果都是 `NULL`
- 运算可以加括号改变优先级

【企业场景】

```sql
-- 场景1：验证接口返回的年薪是否正确
-- 接口说员工 10001 年薪是 720000，验证：
SELECT emp_no, salary, salary * 12 AS calculated_annual
FROM salaries
WHERE emp_no = 10001
  AND to_date = '9999-01-01';  -- 当前薪资
-- 如果 calculated_annual ≠ 720000 → 接口计算有 bug 或数据不一致

-- 场景2：找出薪资涨幅最大的员工
-- (当前薪资 - 入职时薪资) / 入职时薪资 * 100
-- 这个涉及子查询，展示思路即可

-- 场景3：构造测试边界值
-- 找出最高薪资，然后用 max+1 作为边界测试数据
SELECT MAX(salary) AS max_salary, MAX(salary) + 1 AS boundary_value
FROM salaries;
```

【面试考察】

面试官："SQL 中 NULL 参与算术运算的结果是什么？"

参考回答框架：
1. 任何值与 NULL 进行算术运算，结果都是 NULL
2. 例如 `100 + NULL` → NULL，`NULL * 0` → NULL
3. 如果需要 NULL 参与运算时当 0 处理，用 `COALESCE(col, 0)` 或 `IFNULL(col, 0)`

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 `NULL + 100 = 100` | NULL 参与运算结果为 NULL，需用 IFNULL 处理 |
| `salary / 12` 结果被截断 | MySQL 中整数除法结果是浮点数，不会截断（跟其他 DB 可能不同） |
| 运算忘记加括号 | `salary * 12 + bonus` 和 `salary * (12 + bonus)` 结果完全不同 |

【我的理解】

> （在 salaries 表中：① `SELECT emp_no, salary, salary * 12 AS annual FROM salaries LIMIT 5;` 验证结果；② 试试 `SELECT 10 / 3, 10 DIV 3, 10 % 3;` 观察三个结果的区别；③ 思考：如果 salary 是 NULL，`salary * 12` 会返回什么？你能想到测试中什么情况下会碰到 NULL？）

---

## 二、条件查询（WHERE）

### 知识点 5：WHERE 子句与比较运算符

【课程原话/定义】

`WHERE` 子句用于过滤数据，只返回满足条件的行。比较运算符如下：

| 运算符 | 含义 | 示例 |
|--------|------|------|
| `=` | 等于 | `WHERE emp_no = 10001` |
| `<>` 或 `!=` | 不等于 | `WHERE gender <> 'M'` |
| `>` | 大于 | `WHERE salary > 100000` |
| `<` | 小于 | `WHERE hire_date < '1990-01-01'` |
| `>=` | 大于等于 | `WHERE salary >= 80000` |
| `<=` | 小于等于 | `WHERE hire_date <= '2000-12-31'` |
| `BETWEEN...AND` | 在范围内（含边界） | `WHERE salary BETWEEN 60000 AND 80000` |
| `IN (...)` | 在列表中 | `WHERE dept_no IN ('d001','d002','d003')` |
| `IS NULL` | 为空 | `WHERE to_date IS NULL` |
| `IS NOT NULL` | 不为空 | `WHERE title IS NOT NULL` |

```sql
-- 基本比较
SELECT * FROM employees WHERE emp_no = 10001;
SELECT * FROM employees WHERE hire_date >= '1995-01-01';

-- BETWEEN（等价于 >= AND <=）
SELECT * FROM salaries WHERE salary BETWEEN 70000 AND 90000;
-- 等价于: WHERE salary >= 70000 AND salary <= 90000

-- IN（等价于多个 OR）
SELECT * FROM departments WHERE dept_no IN ('d001', 'd005', 'd008');

-- IS NULL（注意：不能用 = NULL）
SELECT * FROM titles WHERE to_date IS NULL;
```

【为什么？】

WHERE 是测试工程师最重要的 SQL 子句——没有之一。你几乎从不查全表，你总是"查某个条件的记录"：

| 测试活动 | WHERE 条件 |
|----------|------------|
| 验证用户注册 | `WHERE username = 'test_user_001'` |
| 查今天创建的订单 | `WHERE DATE(created_at) = CURDATE()` |
| 清理测试数据 | `WHERE username LIKE 'test_%'` |
| 查异常数据 | `WHERE amount < 0 OR amount IS NULL` |
| 定位 bug | `WHERE order_id = 12345` → 看实际存了什么 |

【必须掌握】

- `=` 是等于（不是 `==`）
- `<>` 和 `!=` 都是不等于（推荐 `<>`，兼容性更好）
- `BETWEEN a AND b` 包含 a 和 b（闭区间）
- `IN (v1, v2, ...)` 等价于 `= v1 OR = v2 OR ...`
- 判断 NULL **必须用 `IS NULL`**，不能用 `= NULL`
- 字符串和日期用单引号 `'value'`

【企业场景】

```sql
-- 场景1：接口测试——调了创建员工接口，验证数据落库
SELECT emp_no, first_name, last_name, gender, hire_date
FROM employees
WHERE emp_no = 500000;  -- 假设接口返回的 emp_no
-- 预期：返回 1 行且各列值与接口入参一致

-- 场景2：bug 定位——运营说"1999年之后入职的员工统计少了"
-- 先查数据本身：
SELECT COUNT(*) FROM employees WHERE hire_date >= '1999-01-01';
-- 再查是不是有人 hire_date 为空：
SELECT COUNT(*) FROM employees WHERE hire_date IS NULL;
-- 对比接口返回的统计值，定位在哪一层出了问题

-- 场景3：测试数据准备——我需要 d001~d005 部门下 1995 年后入职的员工
SELECT emp_no, first_name, last_name, hire_date
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no
WHERE de.dept_no IN ('d001', 'd002', 'd003', 'd004', 'd005')
  AND e.hire_date >= '1995-01-01'
ORDER BY e.hire_date DESC
LIMIT 20;
```

【面试考察】

面试官："`BETWEEN 10 AND 20` 包含 10 和 20 吗？`IN` 和 `OR` 有什么区别？"

参考回答框架：
1. BETWEEN 是闭区间，包含边界值（≥10 且 ≤20）
2. IN 等价于多个 OR：`IN (1,2,3)` = `=1 OR =2 OR =3`
3. IN 的优势：更简洁、执行计划可能更优、可接子查询
4. `IS NULL` 不能用 `= NULL` 替代，因为在 SQL 中 NULL 表示"未知"，未知不等于任何值，包括不等于自己

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `WHERE gender = NULL` | 永远查不出结果！改用 `WHERE gender IS NULL` |
| `WHERE salary = '70000'` | 数值列不要加引号，虽然 MySQL 会隐式转换但性能差 |
| `WHERE hire_date = 1990-01-01` | 日期必须加引号：`'1990-01-01'` |
| `BETWEEN 80000 AND 60000` | 小值在前，大值在后，反过来查不出数据 |
| `IN (1,2,3)` 中有 NULL 时要注意 | `IN` 列表中的 NULL 会被忽略 |

【我的理解】

> （执行以下查询并思考：① `SELECT * FROM employees WHERE hire_date >= '2000-01-01';` ② `SELECT * FROM employees WHERE emp_no BETWEEN 10001 AND 10010;` 结果包含 10001 和 10010 吗？③ `SELECT * FROM departments WHERE dept_no IN ('d001', 'd005');` ④ 试试 `SELECT * FROM titles WHERE to_date = NULL;` 和 `IS NULL` 的区别——为什么前者查不出？）

---

### 知识点 6：逻辑运算符（AND / OR / NOT）

【课程原话/定义】

逻辑运算符用于组合多个条件：

| 运算符 | 含义 | 优先级 |
|--------|------|--------|
| `NOT` | 条件取反 | 最高 |
| `AND` | 所有条件都满足 | 中 |
| `OR` | 任一条件满足 | 最低 |

```sql
-- AND：两个条件都满足
SELECT * FROM employees
WHERE gender = 'F' AND hire_date >= '1995-01-01';

-- OR：满足任一条件
SELECT * FROM employees
WHERE first_name = 'Georgi' OR first_name = 'Bezalel';

-- NOT：条件取反
SELECT * FROM employees
WHERE NOT gender = 'M';  -- 等价于 WHERE gender <> 'M' 或 gender = 'F'

-- 复杂组合：括号明确优先级
SELECT * FROM employees
WHERE (gender = 'F' AND hire_date >= '1995-01-01')
   OR (gender = 'M' AND hire_date >= '2000-01-01');
```

【为什么？】

测试中最典型的组合：测试工程师查数据几乎从来不用单一条件。

```
单一条件：WHERE username = 'test'
现实需求：WHERE username LIKE 'test_%' AND created_at > '2026-01-01' AND status != 'deleted'
```

AND 和 OR 的优先级问题是**面试经典陷阱题**：

```sql
-- 看这两条 SQL，结果一样吗？
SELECT * FROM employees WHERE gender = 'F' AND first_name = 'Mary' OR first_name = 'John';
SELECT * FROM employees WHERE gender = 'F' AND (first_name = 'Mary' OR first_name = 'John');

-- 第一条等价于：
-- WHERE (gender='F' AND first_name='Mary') OR first_name='John'
-- → 返回所有 John（不论性别）+ 女性 Mary

-- 第二条等价于：
-- WHERE gender='F' AND (first_name='Mary' OR first_name='John')
-- → 只返回女性 Mary 和女性 John
```

**结论：AND 优先级高于 OR。不确定时加括号——永远不会错。**

【必须掌握】

- `AND`：所有条件同时满足才返回
- `OR`：任一条件满足即返回
- `NOT`：对条件取反
- **AND 优先级高于 OR**（这在笔试中反复考）
- 复杂条件用 `()` 明确优先级——不要靠记忆，靠括号

【企业场景】

```sql
-- 场景1：多条件数据验证
-- 注册接口创建的用户，验证：用户名、邮箱、状态全部正确
SELECT * FROM users
WHERE username = 'test_user'
  AND email = 'test@example.com'
  AND status = 'active'
  AND created_at >= CURDATE();
-- 只有全部条件命中才说明数据正确——缺一条就有 bug

-- 场景2：查找可疑数据（bug 定位）
-- 薪资为空或是负数的异常记录
SELECT * FROM salaries
WHERE salary IS NULL OR salary <= 0;

-- 场景3：构造复杂的测试数据筛选条件
-- 筛选"高薪女性工程师"或"高薪男性高级工程师"
SELECT e.emp_no, e.first_name, e.last_name, e.gender, t.title, s.salary
FROM employees e
JOIN titles t ON e.emp_no = t.emp_no
JOIN salaries s ON e.emp_no = s.emp_no
WHERE s.salary > 100000
  AND s.to_date = '9999-01-01'
  AND t.to_date = '9999-01-01'
  AND (
      (e.gender = 'F' AND t.title = 'Engineer')
      OR (e.gender = 'M' AND t.title = 'Senior Engineer')
  )
LIMIT 10;
```

【面试考察】

面试官（笔试题）："下面 SQL 返回什么？`SELECT * FROM t WHERE a=1 OR a=2 AND b=3;`"

参考回答框架：
1. AND 优先级高于 OR，等价于 `WHERE a=1 OR (a=2 AND b=3)`
2. 返回：所有 a=1 的行 + a=2 且 b=3 的行
3. 实际开发中加括号避免歧义：`WHERE a=1 OR (a=2 AND b=3)`
4. 同理 `NOT a=1 AND b=2` 等价于 `(NOT a=1) AND b=2`，因为 NOT 优先级最高

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 不加括号导致逻辑错误 | `a=1 OR a=2 AND b=3` ≠ `(a=1 OR a=2) AND b=3` |
| `WHERE NOT gender = 'M'` 漏掉 NULL | NOT 只对 TRUE/FALSE 取反，NULL 不匹配——如果有 NULL 行不会返回 |
| OR 连接太多条件性能差 | 考虑用 IN 替代多个 OR |

【我的理解】

> （不看书，写出以下业务需求的 SQL：① 查询 1990 年到 2000 年之间入职的女性员工；② 查询姓 'Facello' 或 'Simmel' 的员工；③ 查询不是男性且在 d005 部门的员工。然后想想：条件 ③ 中如果 gender 是 NULL，会被查出来吗？）

---

### 知识点 7：LIKE 模糊匹配

【课程原话/定义】

`LIKE` 用于模糊匹配字符串。配合两个通配符使用：

| 通配符 | 含义 | 示例 |
|--------|------|------|
| `%` | 匹配 0 个或多个任意字符 | `'a%'` → 以 a 开头 |
| `_` | 匹配 1 个任意字符 | `'a_'` → a 开头且总长 2 个字符 |

```sql
-- % 通配符
SELECT * FROM employees WHERE first_name LIKE 'Geo%';    -- 以 Geo 开头
SELECT * FROM employees WHERE first_name LIKE '%son';    -- 以 son 结尾
SELECT * FROM employees WHERE first_name LIKE '%ar%';    -- 包含 ar

-- _ 通配符
SELECT * FROM employees WHERE first_name LIKE 'M____';   -- M 开头共 5 个字符
SELECT * FROM employees WHERE first_name LIKE '__n%';    -- 第 3 个字符是 n

-- NOT LIKE
SELECT * FROM employees WHERE first_name NOT LIKE 'A%';  -- 不以 A 开头
```

【为什么？】

`LIKE` 是测试工程师最常用的模糊查询工具，场景无处不在：

| 场景 | LIKE 用法 |
|------|-----------|
| 清理测试数据 | `WHERE username LIKE 'test_%'` |
| 查特定格式的数据 | `WHERE phone LIKE '138%'` |
| 验证命名规则 | `WHERE email NOT LIKE '%@%'`（找出异常邮箱） |
| 模糊搜索功能测试 | 测搜索框时对照数据库验证 |

特别提醒：**`%` 可以匹配 0 个字符，`_` 必须匹配 1 个字符。** 这是面试常考点。

【必须掌握】

- `%` = 0~N 个任意字符，`_` = 恰好 1 个任意字符
- `LIKE` 默认不区分大小写（取决于字符集排序规则 collation）
- `NOT LIKE` 取反
- `LIKE` 的模式中如果要匹配 `%` 或 `_` 本身，用 `ESCAPE`：`LIKE '100\%' ESCAPE '\'`
- `LIKE` 前置 `%` 时无法使用索引（`LIKE '%abc'` 全表扫描）

【企业场景】

```sql
-- 场景1：测试完成后清理测试数据（最常用的 LIKE 场景）
-- 约定：所有测试数据的用户名的以 'test_' 开头
DELETE FROM users WHERE username LIKE 'test\_%';  -- 注意反斜杠转义下划线

-- 场景2：验证邮箱格式
-- 找所有邮箱不是 @company.com 域名的员工数据
SELECT * FROM employees WHERE email NOT LIKE '%@company.com';

-- 场景3：模糊搜索功能的测试验证
-- 前端搜索框输入 "Ge"，返回 5 条结果
-- 后端验证：数据库实际有多少？
SELECT COUNT(*) FROM employees WHERE first_name LIKE 'Ge%';
-- 如果数据库返回 12 条但前端只显示 5 条 → 前端分页或截断问题

-- 场景4：数据质量检查——找出 t 开头共 4 个字符的 first_name
SELECT DISTINCT first_name FROM employees WHERE first_name LIKE 't___';
```

【面试考察】

面试官："`%` 和 `_` 的区别是什么？`LIKE '%a'` 能用到索引吗？"

参考回答框架：
1. `%` 匹配 0 到多个字符，`_` 匹配恰好 1 个字符
2. `LIKE '%a'` 的前置 `%` 导致索引失效（无法确定匹配起点），全表扫描
3. `LIKE 'a%'` 可以使用索引（匹配起点确定）
4. 模糊搜索性能优化：大批量数据建议用全文索引（FULLTEXT）代替 LIKE

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 `_` 也可以匹配 0 个字符 | `_` 必须匹配恰好 1 个字符，不能多也不能少 |
| `LIKE '%'` 期望匹配包含 `%` 的数据 | 需要转义：`LIKE '%\%%' ESCAPE '\'` |
| 忘记转义下划线 | `LIKE 'test_%'` 会匹配 `testA`, `test1` 等，而非字面的 `test_` |
| 线上环境大量使用 `LIKE '%keyword%'` | 全表扫描，可能导致数据库 CPU 飙升 |

【我的理解】

> （在 employees 库中：① `SELECT * FROM employees WHERE first_name LIKE 'A%' LIMIT 10;` ② `SELECT * FROM employees WHERE first_name LIKE '%son' LIMIT 10;` ③ `SELECT * FROM employees WHERE first_name LIKE 'J___' LIMIT 10;` — J 开头、总共 4 个字符的名字。④ 查询 first_name 中第 3 个字母是 'r' 的员工，怎么写？）

---

## 三、排序与分页

### 知识点 8：ORDER BY 排序

【课程原话/定义】

`ORDER BY` 对查询结果进行排序。

```sql
-- 单列排序
SELECT * FROM employees ORDER BY hire_date ASC;   -- 升序（默认）
SELECT * FROM employees ORDER BY hire_date DESC;  -- 降序

-- 多列排序
SELECT * FROM employees ORDER BY last_name ASC, first_name ASC;

-- 用列序号排序（不推荐）
SELECT emp_no, first_name FROM employees ORDER BY 2;  -- 按第2列 (first_name)
```

- `ASC` = 升序（Ascending），从小到大，默认值，**可省略**
- `DESC` = 降序（Descending），从大到小，**不可省略**
- 多列排序：先按第一列排，相同再按第二列排

【为什么？】

ORDER BY 在测试中的三个核心用途：

1. **验证列表顺序**：前端列表按入职时间排序，查数据库验证顺序是否正确
2. **取最新/最旧的 N 条**：ORDER BY + LIMIT = 最常用组合
3. **找边界值**：ORDER BY salary DESC LIMIT 1 → 最高薪资

【必须掌握】

- `ASC` 升序（默认），`DESC` 降序
- 多列排序时每列各自指定 ASC/DESC
- 可以用列别名排序：`ORDER BY 年薪 DESC`
- 可以用列序号排序：`ORDER BY 2`（不推荐，列顺序变化就错）
- NULL 在 MySQL 中升序排在最前面

【企业场景】

```sql
-- 场景1：验证前端列表排序
-- 前端员工列表按 hire_date 降序显示，验证数据库真实排序
SELECT emp_no, first_name, last_name, hire_date
FROM employees
ORDER BY hire_date DESC
LIMIT 20;
-- 把结果截图和前端列表对比

-- 场景2：找最近入职的员工（测试数据验证）
SELECT emp_no, first_name, last_name, hire_date
FROM employees
ORDER BY hire_date DESC
LIMIT 5;

-- 场景3：多级排序——同名员工按入职时间排
SELECT first_name, last_name, hire_date
FROM employees
ORDER BY last_name ASC, first_name ASC, hire_date DESC;
-- 先按姓氏升序，同姓按名字升序，同名按入职降序

-- 场景4：找薪资最高的 10 个人
SELECT e.emp_no, e.first_name, e.last_name, s.salary
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
WHERE s.to_date = '9999-01-01'
ORDER BY s.salary DESC
LIMIT 10;
```

【面试考察】

面试官："`ORDER BY` 多列排序的规则是什么？NULL 值是怎么排序的？"

参考回答框架：
1. 多列排序按顺序：先按第一列排，第一列相同的行再按第二列排
2. 每列可以独立指定 ASC 或 DESC
3. MySQL 中 NULL 在升序时排在最前面，降序时排在最后面
4. `ORDER BY 列名 ASC` 中的 ASC 可省略，但 DESC 不可省略

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `ORDER BY hire_date DESC ASC` | 每列只能有一个排序方向 |
| 以为 `ORDER BY a, b DESC` 对 a 和 b 都降序 | DESC 只作用于它前面的 b，a 仍是默认 ASC |
| 用列序号排序但 SELECT 列变了 | 明确写列名，不用序号 |
| 排序后发现结果"不对"——因为有 NULL | NULL 参与的排序规则需要特别注意 |

【我的理解】

> （执行以下查询：① `SELECT emp_no, first_name, last_name FROM employees ORDER BY first_name DESC LIMIT 10;` ② `SELECT emp_no, first_name, last_name FROM employees ORDER BY last_name, first_name LIMIT 20;` 观察多列排序的效果——同姓的人是否按名字排序了？③ 试试 `SELECT emp_no, salary FROM salaries ORDER BY salary DESC LIMIT 1;` 最高薪资是多少？）

---

### 知识点 9：LIMIT 与 OFFSET 分页

【课程原话/定义】

`LIMIT` 限制查询返回的行数，`OFFSET` 指定跳过的行数。两者组合实现分页。

```sql
-- 只返回前 10 行
SELECT * FROM employees LIMIT 10;

-- 跳过前 5 行，返回接下来 10 行（第 6~15 行）
SELECT * FROM employees LIMIT 10 OFFSET 5;

-- 简写形式（MySQL 特有）
SELECT * FROM employees LIMIT 5, 10;  -- 等价于 LIMIT 10 OFFSET 5
```

分页公式：
```
第 N 页 = LIMIT 每页条数 OFFSET (N-1) * 每页条数

第 1 页：LIMIT 20 OFFSET 0
第 2 页：LIMIT 20 OFFSET 20
第 3 页：LIMIT 20 OFFSET 40
```

【为什么？】

LIMIT 在测试工作中是最实用的关键字之一：

| 场景 | 用法 |
|------|------|
| 快速预览数据 | `SELECT * FROM huge_table LIMIT 5` |
| 验证"最新一条" | `ORDER BY created_at DESC LIMIT 1` |
| 验证分页功能 | 对比前端每页和数据库每页的数据 |
| 取 TOP N | `ORDER BY score DESC LIMIT 100` |
| 子查询中限制数量 | `WHERE id IN (SELECT id FROM t LIMIT 100)` |

**特别注意：测试分页功能时，不仅查第一页，还要查最后一页、中间页、超出页——这是标准测试思维。**

【必须掌握】

- `LIMIT n`：只返回 n 行
- `LIMIT n OFFSET m`：跳过 m 行，返回 n 行
- MySQL 简写 `LIMIT m, n`（m=offset, n=limit）
- LIMIT 通常配合 ORDER BY 使用（否则分页结果不稳定）
- 大数据量下 OFFSET 越大越慢（因为数据库仍需扫描跳过的行）

【企业场景】

```sql
-- 场景1：验证前端分页功能
-- 前端第 3 页，每页 20 条，按 emp_no 排序
-- 数据库验证：第 3 页应该是什么数据？
SELECT emp_no, first_name, last_name
FROM employees
ORDER BY emp_no ASC
LIMIT 20 OFFSET 40;  -- 第3页：跳过前 40 条

-- 场景2：数据抽样验证
-- 随机看 10 条数据，快速检查质量
SELECT * FROM employees ORDER BY RAND() LIMIT 10;

-- 场景3：测试数据准备——只需要 100 条有效员工
INSERT INTO test_users (emp_no, name)
SELECT emp_no, CONCAT(first_name, ' ', last_name)
FROM employees
LIMIT 100;

-- 场景4：验证"最新N条"功能
-- 接口返回最近注册的 5 个用户
SELECT username, created_at FROM users
ORDER BY created_at DESC LIMIT 5;
-- 和接口返回对比
```

【面试考察】

面试官："LIMIT 100000, 20 为什么慢？如何优化深度分页？"

参考回答框架：
1. OFFSET 大的时候慢的原因：数据库需要扫描并丢弃前 100000 行，才能返回接下来的 20 行
2. 优化方式一（游标分页）：用上一页最后一条的主键作为条件，`WHERE id > last_id LIMIT 20`
3. 优化方式二：先查主键再关联（子查询分页）
4. 优化方式三：业务上限制最大页数，配合搜索引擎做大数据量搜索

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 分页不排序 | LIMIT 不加 ORDER BY，两页之间可能有重复或遗漏 |
| `LIMIT 10 OFFSET 10` 和 `LIMIT 10, 10` 混淆 | MySQL 简写中第一个是 offset、第二个是 limit |
| 认为 `LIMIT 0` 等于不限制 | `LIMIT 0` 返回空结果（0 行），不等于不加 LIMIT |
| 深度分页导致慢查询 | 用游标分页替代大 OFFSET |

【我的理解】

> （① `SELECT * FROM employees LIMIT 10;` 看前 10 条；② `SELECT * FROM employees LIMIT 10 OFFSET 20;` 看第 21~30 条；③ 把 employees 表当成前端列表，写出查询第 5 页（每页 15 条）的 SQL；④ 思考：如果第 3 步的结果和前端不一致，你会检查哪些地方？）

---

## 四、聚合函数

### 知识点 10：聚合函数（COUNT / MAX / MIN / SUM / AVG）

【课程原话/定义】

聚合函数对一组值执行计算，返回一个单一结果。

| 函数 | 作用 | 示例 |
|------|------|------|
| `COUNT(*)` | 统计行数（包括 NULL） | `SELECT COUNT(*) FROM employees;` |
| `COUNT(列名)` | 统计该列非 NULL 的行数 | `SELECT COUNT(to_date) FROM titles;` |
| `COUNT(DISTINCT 列)` | 统计该列不重复的非 NULL 值个数 | `SELECT COUNT(DISTINCT title) FROM titles;` |
| `MAX(列)` | 返回最大值 | `SELECT MAX(salary) FROM salaries;` |
| `MIN(列)` | 返回最小值 | `SELECT MIN(salary) FROM salaries;` |
| `SUM(列)` | 返回总和 | `SELECT SUM(salary) FROM salaries;` |
| `AVG(列)` | 返回平均值 | `SELECT AVG(salary) FROM salaries;` |

```sql
-- 行数统计
SELECT COUNT(*) FROM employees;                           -- 总员工数
SELECT COUNT(DISTINCT last_name) FROM employees;          -- 有多少个不同的姓氏

-- 数值统计
SELECT MAX(salary), MIN(salary), AVG(salary), SUM(salary)
FROM salaries
WHERE to_date = '9999-01-01';                             -- 当前薪资的统计

-- 组合使用
SELECT
    COUNT(*)        AS 总人数,
    MAX(salary)     AS 最高薪资,
    MIN(salary)     AS 最低薪资,
    ROUND(AVG(salary), 2) AS 平均薪资,
    SUM(salary)     AS 薪资总和
FROM salaries
WHERE to_date = '9999-01-01';
```

【为什么？】

测试工程师用聚合函数做"数据统计验证"——这是从"手动点点看看"到"自动化数据校验"的关键一步。

| 测试场景 | 聚合函数应用 |
|----------|-------------|
| 验证数据总数 | `SELECT COUNT(*)` vs 前端显示的"共 X 条" |
| 验证数据范围 | `MAX(col)`, `MIN(col)` vs 业务规则边界 |
| 验证金额计算 | `SUM(amount)` vs 前端/接口返回的总额 |
| 验证平均值 | `AVG(score)` vs 报表的均分 |
| 验证唯一约束 | `COUNT(DISTINCT col)` vs `COUNT(*)` 是否相等 |

**`COUNT(*)` 和 `COUNT(列名)` 的区别**是面试必考题：

```sql
-- titles 表：to_date 列有的行是 NULL（表示当前职位）
SELECT COUNT(*) FROM titles;          -- 返回所有行数
SELECT COUNT(to_date) FROM titles;    -- 不包含 to_date 为 NULL 的行
-- 两者不相等！因为 to_date 有 NULL 值
```

【必须掌握】

- `COUNT(*)` 统计所有行，**包括 NULL 行**
- `COUNT(列名)` 只统计该列**非 NULL**的行
- `COUNT(DISTINCT 列)` 统计不重复的非 NULL 值
- `MAX/MIN/SUM/AVG` 自动忽略 NULL 值
- 聚合函数不能用在 WHERE 中（那是 HAVING 的活）
- SUM 和 AVG 只对数值有效

【企业场景】

```sql
-- 场景1：数据总量验证——前端说"共 300,024 条员工记录"
SELECT COUNT(*) AS actual_count FROM employees;
-- 如果返回值不是 300024 → 数据没导全或前端统计逻辑有 bug

-- 场景2：薪资范围验证——业务规则"最低薪资不得低于 30000"
SELECT MIN(salary) AS min_salary FROM salaries;
-- 如果 min_salary < 30000 → 数据异常或业务规则未落地

-- 场景3：金额验证——"本月订单总金额和前端报表对不上"
SELECT SUM(amount) AS db_total FROM orders
WHERE MONTH(created_at) = MONTH(CURDATE())
  AND YEAR(created_at) = YEAR(CURDATE());
-- 对比报表返回的总额，差异在哪？

-- 场景4：数据质量检查——titles 表有多少条数据 to_date 为 NULL？
SELECT
    COUNT(*)              AS total_rows,
    COUNT(to_date)        AS non_null_to_date,
    COUNT(*) - COUNT(to_date) AS null_to_date
FROM titles;
-- 用 COUNT(*) - COUNT(列) 快速统计 NULL 数量

-- 场景5：唯一性验证——first_name 中是否有重复的名？
SELECT COUNT(*) AS total, COUNT(DISTINCT first_name) AS unique_names
FROM employees;
-- total 300024, unique_names 1275 → 说明有很多同名
```

【面试考察】

面试官："`COUNT(*)` 和 `COUNT(1)` 和 `COUNT(列名)` 有什么区别？哪个更快？"

参考回答框架：
1. `COUNT(*)` 统计所有行，包括所有列为 NULL 的行
2. `COUNT(1)` 与 `COUNT(*)` 在 MySQL 中完全等价，没有性能差异
3. `COUNT(列名)` 只统计该列非 NULL 的行，可能比 `COUNT(*)` 少
4. 性能：MySQL 中 `COUNT(*)` 和 `COUNT(1)` 一样快，`COUNT(列名)` 在有索引时也很快
5. 如果需要统计行数，用 `COUNT(*)` ——语义最清晰

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 `COUNT(*)` 和 `COUNT(col)` 永远相等 | col 有 NULL 时两者不等 |
| `WHERE AVG(salary) > 80000` | 聚合函数不能出现在 WHERE 中，用 HAVING |
| `SUM(gender)` | SUM 只能用于数值列，对字符串列无意义 |
| AVG 结果精度问题 | `AVG(INT)` 返回小数，MySQL 自动处理；如需精确位数用 `ROUND(AVG(col), 2)` |
| 聚合函数 + 非聚合列混写不报错 | MySQL 允许但结果不可预测，应配合 GROUP BY 使用 |

【我的理解】

> （在 employees 库中：① `SELECT COUNT(*) FROM employees;` 总员工数；② `SELECT COUNT(DISTINCT title) FROM titles;` 有多少种职位；③ `SELECT MAX(salary), MIN(salary), AVG(salary) FROM salaries;` 薪资统计；④ `SELECT COUNT(*) FROM titles WHERE to_date IS NULL;` 当前有多少人还在职？⑤ 思考：如果用 `COUNT(DISTINCT emp_no)` 和 `COUNT(*)` 查 titles 表，结果为什么不相等？）

---

## 五、分组查询

### 知识点 11：GROUP BY 分组与 HAVING 过滤

【课程原话/定义】

`GROUP BY` 将数据按指定列分组，然后对每组使用聚合函数。`HAVING` 用于**分组后**的过滤。

```sql
-- 基本分组：每个部门的员工数
SELECT dept_no, COUNT(*) AS emp_count
FROM dept_emp
WHERE to_date = '9999-01-01'      -- 只看当前在职
GROUP BY dept_no;

-- 带 HAVING 过滤：员工数超过 20000 的部门
SELECT dept_no, COUNT(*) AS emp_count
FROM dept_emp
WHERE to_date = '9999-01-01'
GROUP BY dept_no
HAVING emp_count > 20000;

-- 多列分组
SELECT dept_no, gender, COUNT(*) AS cnt
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no
WHERE de.to_date = '9999-01-01'
GROUP BY dept_no, gender;
```

【为什么？】

GROUP BY 解决的是"分类统计"问题——这是测试验证中最常见的需求之一：

| 测试场景 | GROUP BY 应用 |
|----------|---------------|
| 每类数据各有多少？ | `GROUP BY category` + `COUNT(*)` |
| 各部门平均薪资 | `GROUP BY dept_no` + `AVG(salary)` |
| 每天的订单数 | `GROUP BY DATE(created_at)` + `COUNT(*)` |
| 每个状态的记录数 | `GROUP BY status` + `COUNT(*)` |
| 找出重复数据 | `GROUP BY col HAVING COUNT(*) > 1` |

**`WHERE` 和 `HAVING` 的区别**是重中之重：

| 维度 | WHERE | HAVING |
|------|-------|--------|
| 作用时机 | **分组前**过滤原始行 | **分组后**过滤聚合结果 |
| 能否用聚合函数 | ❌ 不能 | ✅ 可以 |
| 执行顺序 | 第二步（FROM 之后） | 第四步（GROUP BY 之后） |
| 典型用法 | `WHERE salary > 50000` | `HAVING AVG(salary) > 80000` |
| 性能 | 优先用 WHERE 过滤（减少分组数据量） | HAVING 用于聚合条件 |

```sql
-- WHERE vs HAVING 对比
-- ❌ 错误：WHERE 中不能使用聚合函数
SELECT dept_no, AVG(salary) FROM salaries GROUP BY dept_no
WHERE AVG(salary) > 80000;  -- 报错！

-- ✅ 正确：聚合条件放在 HAVING
SELECT dept_no, AVG(salary) AS avg_sal
FROM salaries
GROUP BY dept_no
HAVING AVG(salary) > 80000;

-- ✅ 可以 WHERE 和 HAVING 同时使用
SELECT dept_no, AVG(salary) AS avg_sal
FROM salaries
WHERE salary > 50000             -- 先过滤：只看薪资 > 5w 的记录
GROUP BY dept_no                 -- 再分组
HAVING AVG(salary) > 80000;      -- 再过滤：平均薪资 > 8w 的部门
```

【必须掌握】

- `GROUP BY` 后的列必须在 SELECT 中出现（或被聚合函数包裹）
- `HAVING` 用于过滤分组后的结果，可以使用聚合函数
- `WHERE` 在分组前过滤，`HAVING` 在分组后过滤
- 聚合条件必须用 HAVING，普通条件优先用 WHERE
- 分组后 SELECT 中的非聚合列必须包含在 GROUP BY 中

【企业场景】

```sql
-- 场景1：验证每个部门的在职人数（和前端仪表盘对比）
SELECT
    d.dept_no,
    d.dept_name,
    COUNT(*) AS current_employees
FROM departments d
JOIN dept_emp de ON d.dept_no = de.dept_no
WHERE de.to_date = '9999-01-01'
GROUP BY d.dept_no, d.dept_name
ORDER BY current_employees DESC;

-- 场景2：找出有人数异常的部门（人数太少或太多）
SELECT dept_no, COUNT(*) AS cnt
FROM dept_emp
WHERE to_date = '9999-01-01'
GROUP BY dept_no
HAVING cnt < 10000 OR cnt > 50000;
-- 如果返回空行 → 正常；如果返回行 → 这些部门需要人工确认

-- 场景3：验证薪资统计报表（各部门的薪资范围）
SELECT
    dept_no,
    COUNT(*)        AS 人数,
    MIN(salary)      AS 最低,
    MAX(salary)      AS 最高,
    ROUND(AVG(salary), 2) AS 平均,
    SUM(salary)      AS 总额
FROM salaries s
JOIN dept_emp de ON s.emp_no = de.emp_no
WHERE de.to_date = '9999-01-01'
  AND s.to_date = '9999-01-01'
GROUP BY dept_no
ORDER BY 平均 DESC;

-- 场景4：找出重复的 title（每个员工有多个 title 历史是正常的，但检查异常）
SELECT emp_no, COUNT(*) AS title_count
FROM titles
GROUP BY emp_no
HAVING title_count > 5;  -- 一个人换过 5 次以上 title？检查一下

-- 场景5：多维度分组——每个部门分别有多少男/女员工？
SELECT dept_no, gender, COUNT(*) AS cnt
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no
WHERE de.to_date = '9999-01-01'
GROUP BY dept_no, gender
ORDER BY dept_no, gender;
```

【面试考察】

面试官："WHERE 和 HAVING 的区别是什么？能否用 WHERE 替代 HAVING？"

参考回答框架：
1. WHERE 在 GROUP BY 之前过滤原始数据行，HAVING 在 GROUP BY 之后过滤分组结果
2. WHERE 中不能使用聚合函数（COUNT、SUM、AVG 等），HAVING 可以使用聚合函数
3. 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
4. 能用 WHERE 过滤的条件就放在 WHERE 中（减少分组的数据量以提升性能）
5. 只有涉及聚合函数的条件才需要放在 HAVING 中

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `WHERE COUNT(*) > 5` | 聚合条件用 HAVING：`HAVING COUNT(*) > 5` |
| GROUP BY 后 SELECT 中包含不在此列的非聚合列 | MySQL 不报错但结果不可预测，标准 SQL 会报错 |
| 把应该放 WHERE 的条件放 HAVING | 能用 WHERE 过滤的不要推到 HAVING——性能差 |
| 忘记加 GROUP BY 就写 HAVING | HAVING 必须配合 GROUP BY 使用（MySQL 允许不写但结果怪异） |

【我的理解】

> （① `SELECT dept_no, COUNT(*) FROM dept_emp WHERE to_date='9999-01-01' GROUP BY dept_no;` 每个部门当前多少人；② `SELECT dept_no, AVG(salary) FROM salaries GROUP BY dept_no HAVING AVG(salary) > 70000;` 平均薪资 > 7w 的部门；③ 思考：把 HAVING 中的 `AVG(salary) > 70000` 改成 WHERE 条件放在 GROUP BY 前面，结果会一样吗？为什么？）

---

## 六、SQL 执行顺序（核心知识点）

### 知识点 12：完整的 SQL 执行顺序

【课程原话/定义】

SQL 的书写顺序和执行顺序**完全不同**。这是面试最高频考点之一。

**书写顺序**（你打字的顺序）：

```sql
SELECT [DISTINCT] 列1, 列2, 聚合函数
FROM 表名
[JOIN 其他表 ON 条件]
WHERE 条件
GROUP BY 列
HAVING 聚合条件
ORDER BY 列 [ASC|DESC]
LIMIT n OFFSET m;
```

**执行顺序**（数据库引擎实际处理的顺序）：

```
  FROM        ← ① 确定数据来源（表 + JOIN）
    ↓
  WHERE       ← ② 过滤原始数据行（不能用聚合函数）
    ↓
  GROUP BY    ← ③ 对数据分组
    ↓
  HAVING      ← ④ 过滤分组后的结果（可以用聚合函数）
    ↓
  SELECT      ← ⑤ 选择要输出的列、计算表达式/聚合函数
    ↓
  DISTINCT    ← ⑥ 去重（如果有）
    ↓
  ORDER BY    ← ⑦ 排序
    ↓
  LIMIT       ← ⑧ 限制返回行数
```

【为什么？】

理解执行顺序能解释你遇到的所有"奇怪"现象：

| 现象 | 执行顺序给出的解释 |
|------|-------------------|
| WHERE 中不能用别名 | WHERE 在步骤②，别名在步骤⑤才定义 |
| ORDER BY 能用别名 | ORDER BY 在步骤⑦，别名已在步骤⑤定义 |
| WHERE 中不能用聚合函数 | 聚合函数在 GROUP BY（步骤③）之后才有意义，WHERE 在步骤② |
| HAVING 能用聚合函数 | HAVING 在步骤④，此时分组已存在，聚合有值 |
| LIMIT 影响最终输出 | LIMIT 是最后一步⑧，之前的所有逻辑已完成 |

**面试中 100% 会考的对照表**：

| 子句 | 书写位置 | 执行步骤 | 能用列别名？ | 能用聚合函数？ |
|------|---------|---------|------------|--------------|
| FROM | 第2行 | ① 第一步 | ❌ | ❌ |
| WHERE | 第4行 | ② 第二步 | ❌ | ❌ |
| GROUP BY | 第5行 | ③ 第三步 | ❌（MySQL 扩展支持） | ❌ |
| HAVING | 第6行 | ④ 第四步 | ❌（MySQL 扩展支持） | ✅ |
| SELECT | 第1行 | ⑤ 第五步 | — | ✅ |
| ORDER BY | 第7行 | ⑦ 第七步 | ✅ | ✅ |
| LIMIT | 第8行 | ⑧ 第八步 | ✅ | ✅ |

【必须掌握】

- 完整顺序：**FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT**
- 必须**能默写**这 8 个步骤的顺序
- 能解释为什么 WHERE 中不能用别名，但 ORDER BY 可以
- 能解释为什么 HAVING 能用聚合函数，WHERE 不能

【企业场景】

```sql
-- 实际工作中的一条完整查询，按执行顺序标注每一步做了什么

SELECT
    d.dept_no,                        -- ⑤-SELECT：选择输出列
    d.dept_name,
    COUNT(*) AS emp_cnt,
    AVG(s.salary) AS avg_sal
FROM employees e                      -- ①-FROM：确定员工表
JOIN dept_emp de                      -- ①-FROM：关联部门-员工表
    ON e.emp_no = de.emp_no
JOIN departments d                    -- ①-FROM：关联部门信息表
    ON de.dept_no = d.dept_no
JOIN salaries s                       -- ①-FROM：关联薪资表
    ON e.emp_no = s.emp_no
WHERE de.to_date = '9999-01-01'       -- ②-WHERE：只看当前在职的员工
  AND s.to_date = '9999-01-01'        --     + 当前有效薪资
  AND e.gender = 'F'                  --     + 只看女性
GROUP BY d.dept_no, d.dept_name       -- ③-GROUP BY：按部门分组
HAVING avg_sal > 60000                -- ④-HAVING：只保留平均薪资 > 6w 的部门
ORDER BY avg_sal DESC                 -- ⑦-ORDER BY：按平均薪资降序
LIMIT 5;                              -- ⑧-LIMIT：只取前 5 个部门
```

```sql
-- 场景：用执行顺序排错
-- Bug: 以下 SQL 为什么报错？
SELECT dept_no, AVG(salary) AS avg_sal
FROM salaries
WHERE avg_sal > 80000        -- 报错！Unknown column 'avg_sal'
GROUP BY dept_no;

-- 原因：WHERE 在步骤②执行，avg_sal 别名在步骤⑤才定义
-- 修复：把条件移到 HAVING
SELECT dept_no, AVG(salary) AS avg_sal
FROM salaries
GROUP BY dept_no
HAVING avg_sal > 80000;      -- HAVING 在步骤④，别名已可用
```

【面试考察】

面试官："写出 SQL 的完整执行顺序，并解释为什么 `WHERE` 中不能用别名但 `ORDER BY` 可以？"

参考回答框架：
1. 完整顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
2. 别名在 SELECT（第⑤步）中才定义，WHERE（第②步）此时别名还不存在
3. ORDER BY（第⑦步）在 SELECT 之后执行，别名已经存在，所以可以使用
4. 可以进一步说明：理解执行顺序对写出正确 SQL 和排查 SQL 错误非常重要

【易错点】

| 常见错误 | 正确做法/原因 |
|----------|--------------|
| 以为 SQL 按书写顺序执行 | 书写顺序 ≠ 执行顺序，执行顺序是 FROM→WHERE→...→LIMIT |
| WHERE 使用别名 | 别名在 SELECT 步骤定义，WHERE 步骤还不可用 |
| 混淆 HAVING 和 WHERE | 记住位置：WHERE 在 GROUP BY 前，HAVING 在 GROUP BY 后 |
| 忘记 DISTINCT 的执行位置 | DISTINCT 在 SELECT 之后、ORDER BY 之前 |

【我的理解】

> （拿出一张白纸，不看书默写 SQL 执行顺序的 8 个步骤。然后对着每一步，写出它的作用。最后回答：① 如果有 JOIN，它在哪一步？在 FROM 步骤中一起处理；② 为什么 GROUP BY 可以用 SELECT 中出现的列别名？MySQL 对标准 SQL 的扩展，实际执行中 MySQL 会特殊处理，但严格来说别名不可用；③ 如果一个查询既有 WHERE 又有 HAVING，先执行哪个？为什么？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 | 测试工作使用频率 |
|------|----------|----------|-----------------|
| 基础 SELECT | `SELECT *` vs `SELECT 列名`、AS 别名 | ★★★☆☆ | ★★★★★（天天用） |
| DISTINCT | 去重、单列/多列去重、COUNT(DISTINCT) | ★★★☆☆ | ★★★★☆ |
| 算术运算 | `+ - * /`、NULL 参与运算 | ★★☆☆☆ | ★★★☆☆ |
| WHERE 比较运算符 | `= <> != > < >= <= BETWEEN IN IS NULL` | ★★★★★ | ★★★★★ |
| 逻辑运算符 | AND/OR/NOT、优先级、括号 | ★★★★☆ | ★★★★★ |
| LIKE 模糊匹配 | `%` 和 `_` 通配符、转义 | ★★★★☆ | ★★★★★ |
| ORDER BY | ASC/DESC、多列排序、NULL 排序 | ★★★★☆ | ★★★★★ |
| LIMIT/OFFSET | 分页公式、深度分页问题 | ★★★★☆ | ★★★★☆ |
| 聚合函数 | COUNT/MAX/MIN/SUM/AVG、COUNT(*) vs COUNT(列) | ★★★★★ | ★★★★★ |
| GROUP BY + HAVING | 分组统计、WHERE vs HAVING 区别 | ★★★★★ | ★★★★☆ |
| SQL 执行顺序 | FROM→WHERE→...→LIMIT 8 步顺序 | ★★★★★ | ★★★★★ |

> 测试工程师的 DQL 能力水平自测：
> - 入门：能用 SELECT + WHERE 查数据
> - 熟练：能用 GROUP BY + HAVING + 聚合函数做数据统计验证
> - 进阶：能默写 SQL 执行顺序，能用 SQL 做复杂的数据一致性校验
> - 专家：能优化慢查询、能设计测试数据的 SQL 生成脚本

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-MySQL基础与SQL入门]] — SQL 四大分类、DQL 的定义
- [[Ch02-DDL数据库操作]] — 表结构设计影响查询
- [[Ch03-DML数据操作]] — INSERT/UPDATE/DELETE 造测试数据后用 SELECT 验证
- [[../接口测试/Ch03-请求与响应处理]] — 接口返回数据 vs 数据库数据对比
- employees test database: https://github.com/datacharmer/test_db
