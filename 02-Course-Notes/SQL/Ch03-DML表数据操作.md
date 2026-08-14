---
tags: [课程笔记, SQL, MySQL]
course: "SQL"
chapter: "Ch03-DML表数据操作"
created: 2026-07-31
status: draft
---

# Ch03 - DML 表数据操作

> 前置：[[Ch02-DDL数据库与表操作]] — 建库建表
> 后置：[[Ch04-DQL表查询操作]] — 查询数据

## 课程来源
- 学习日期：

---

## 一、DML 概述

### 知识点 1：DML 是什么、测试工程师用它做什么

【课程原话/定义】
DML（Data Manipulation Language）数据操作语言，主要对数据库中的数据进行操作：插入（INSERT）、更新（UPDATE）、删除（DELETE）。和 DDL 的区别：DDL 操作表结构，DML 操作表里的数据。

【为什么？】
测试工程师的 DML 占比仅次于 DQL（查询）。日常工作中 DML 的使用频率：

| 操作       | 频率    | 典型场景     |
| -------- | ----- | -------- |
| INSERT   | 每天    | 造测试数据    |
| UPDATE   | 经常    | 修改测试数据状态 |
| DELETE   | 每次测试后 | 清理测试数据   |
| TRUNCATE | 偶尔    | 批量清空测试表  |

没有 DML，你的测试数据管理就是纯手工——在 Workbench 里一行行点。有了 DML，一条 SQL 批量造 1000 条数据，测试完一条 SQL 清理干净。

【必须掌握】
- DML 三类：INSERT（增）、UPDATE（改）、DELETE（删）
- 和 DDL 的区别：DDL 管结构（CREATE/ALTER/DROP），DML 管数据
- 所有 DML 操作需要 COMMIT（在非自动提交模式下）

【企业场景】
一个接口测试用例的完整数据生命周期：

```
1. INSERT 造测试用户          -- 准备数据
2. 调接口（被测功能）           -- 执行测试
3. SELECT 验证数据落库          -- 断言
4. DELETE 清理测试数据          -- 还原环境
```

这就是"数据驱动测试"的基本模式——测试数据由 SQL 管理，测试逻辑由 Python 控制。

【面试考察】
面试官："DDL 和 DML 的区别是什么？DELETE 和 DROP 分别属于哪一类？"

参考回答框架：
1. DDL 定义结构（CREATE/ALTER/DROP 表），DML 操作数据（INSERT/UPDATE/DELETE 记录）
2. DELETE 是 DML（删记录，可回滚），DROP 是 DDL（删表，不可回滚）
3. 测试中 DDL 用于搭环境，DML 用于造数据和清理数据

【易错点】

| 常见错误               | 正确做法                          |
| ------------------ | ----------------------------- |
| DELETE 和 DROP 混为一谈 | DELETE 删行（DML），DROP 删表（DDL）   |
| 认为 TRUNCATE 是 DML  | TRUNCATE 实际是 DDL（删除后重建表，不可回滚） |
| DML 操作后忘记 COMMIT   | 非自动提交模式下必须 commit，否则数据不持久化    |

【我的理解】
> （回顾 Ch01 知识点 7 的 SQL 四大分类。现在你学的 DML 包含 INSERT/UPDATE/DELETE。TRUNCATE 虽然"效果上"是删数据，但为什么它被归类为 DDL 而不是 DML？提示：想想 TRUNCATE 能不能回滚，以及它是怎么实现的。）

---

## 二、插入数据 — INSERT

### 知识点 2：INSERT 基本语法

【课程原话/定义】

```sql
INSERT INTO 表名 (列名1, 列名2, ...)
VALUES (值1, 值2, ...);
```

三种写法：

```sql
-- 完整写法：指定所有列
INSERT INTO user (id, name, age, sex, address)
VALUES (1, '张三', 20, '男', '北京');

-- 省略列名：必须按表定义的列顺序提供所有值
INSERT INTO user
VALUES (2, '李四', 22, '女', '上海');

-- 部分列：只插入指定列，其余列用默认值或 NULL
INSERT INTO user (id, name, address)
VALUES (3, '王五', '深圳');
```

【为什么？】
INSERT 的三种写法对应三种场景：
1. **指定列名**：最推荐——代码可读性好，表结构变了也不容易出错
2. **省略列名**：省打字但危险——表加了一列，你的 INSERT 就会报错（列数不匹配）
3. **部分列**：只插需要的数据，其余用默认值——造测试数据时最常用（id 自增不用写）

测试工程师的命令：**始终用指定列名的写法**。省略列名省的那几秒，不如未来排查 bug 花的几十分钟。

【必须掌握】
- `INSERT INTO 表名 (列1, 列2) VALUES (值1, 值2)`
- 值要和列的个数、顺序、数据类型匹配
- VARCHAR/CHAR/DATE 类型的值用单引号包裹
- 自增列（AUTO_INCREMENT）可以不写，让 MySQL 自动生成
- 允许 NULL 的列可以省略或显式写 NULL

【企业场景】
批量造测试数据——最常用的测试技巧之一：

```sql
-- 一次插入多条（比逐条 INSERT 快 10 倍以上）
INSERT INTO student (id, name, sex, age, city)
VALUES
    (1, '小李', '男', 18, '北京'),
    (2, '小白', '女', 20, '成都'),
    (3, '小王', '男', 23, '上海'),
    (4, '小赵', '女', 21, '深圳'),
    (5, '小周', '男', 25, '杭州');
```

接口压测前，先批量 INSERT 10000 条数据——这是测试数据准备的基本功。

【面试考察】
面试官："INSERT 语句中，列名可以省略吗？省略有什么风险？"

参考回答框架：
1. 可以省略——但必须按表定义的列顺序提供所有列的值
2. 风险：表结构改变（加列/改顺序）后，省略列名的 INSERT 可能报错或插入错误数据
3. 推荐始终写列名——可读性好、维护性好

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 值个数和列个数不匹配 | INSERT INTO t(a,b) VALUES(1) → 少了一个值 |
| VARCHAR 类型的值没加引号 | `VALUES(1, 张三, 20)` → `'张三'` 必须加引号 |
| 自增列手动指定了重复值 | 自增列可以不写，或用 NULL 让 MySQL 自动生成 |
| 一次插入多条时最后一个 VALUES 后面加了逗号 | `VALUES(1,'a'),(2,'b'),` → 最后不能有逗号 |

【我的理解】
> （创建一张 student 表，分别用三种 INSERT 写法各插入一条数据。然后给表加一列 phone VARCHAR(20)，再用省略列名的写法插入——会报错吗？为什么指定列名的写法不受影响？）

---

### 知识点 3：INSERT 注意事项

【课程原话/定义】

| 规则 | 说明 |
|------|------|
| 值与字段对应 | 个数相同、数据类型相同 |
| 值的大小 | 必须在字段指定的长度范围内 |
| 字符串和日期 | VARCHAR、CHAR、DATE 类型必须用单引号包裹 |
| 空值 | 可以忽略不写（用默认值），或显式插入 NULL |
| 指定字段 | 如果只插入部分字段，必须写列名 |

【为什么？】
这些规则背后是数据库的"类型安全"机制——MySQL 不会像 Python 那样自动转换类型。你往 INT 列插 `'abc'`，MySQL 直接报错而不是默默转成 0。这是数据库的严谨性——宁可报错，也不存入脏数据。

测试工程师要利用这个特性：**故意插错误类型的数据，验证系统的容错能力**。

【必须掌握】
- 值的个数、顺序、类型必须和列匹配
- 字符串和日期用单引号（MySQL 中双引号在特定模式下当标识符）
- 插入空值：忽略该列或写 NULL
- 部分列插入：必须写列名

【企业场景】
测试数据构造时的"坏数据"测试：

```sql
-- 正常数据
INSERT INTO student VALUES (1, '张三', '男', 20, '北京');

-- 边界测试：名字超长
INSERT INTO student VALUES (2, '这是一个超级超级超级超级超级超级长的名字', '男', 20, '北京');
-- 预期：报错或截断（取决于 SQL 模式）

-- 类型测试：年龄插入字符串
INSERT INTO student VALUES (3, '王五', '男', 'abc', '北京');
-- 预期：报错 Data truncation
```

这就是测试工程师用 SQL 做"数据层测试"——不通过接口，直接在数据库层面验证约束是否生效。

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 用双引号包裹字符串 `"张三"` | MySQL 中用单引号 `'张三'` |
| 插入的数据超过字段长度 | 先 `DESC 表名` 确认字段长度 |
| 插入 NULL 但不允许 NULL 的列 | 检查表定义中的 NOT NULL 约束 |

【我的理解】
> （在 student 表中故意插入一条违反约束的数据——比如在 age（INT）列插入 `'测试'`，或者在 name（VARCHAR(20)）列插入一个 30 个字符的名字。观察 MySQL 报什么错。这能帮你理解"数据库层面的数据校验"。）

---

## 三、更新数据 — UPDATE

### 知识点 4：UPDATE 基本语法与 WHERE 的重要性

【课程原话/定义】

```sql
UPDATE 表名
SET 列名1 = 值1, 列名2 = 值2, ...
[WHERE 条件表达式];
```

SET 子句：指定要修改的列和新值。WHERE 子句：限定要修改的行。不写 WHERE = 修改全表。

```sql
-- 更新指定行
UPDATE student SET sex = '女' WHERE id = 1;

-- 更新多列
UPDATE student SET age = 21, city = '广州' WHERE name = '张三';

-- 不带 WHERE = 全表更新（极度危险！）
UPDATE student SET sex = '女';
```

【为什么？】
UPDATE 不带 WHERE 是数据库操作中最经典的"删库跑路"事故之一。真实案例：

> 某测试工程师在测试环境执行 `UPDATE orders SET status = 'cancelled'` 忘了加 `WHERE order_id = 123`，导致整张订单表的几万条数据全部变成 cancelled。虽然没有影响生产，但测试团队花了两天恢复数据。

**铁律**：写 UPDATE 和 DELETE 之前，先用同样的 WHERE 条件执行 SELECT，确认要影响的行是你想要的那些行。

```sql
-- 安全做法：先 SELECT 确认，再 UPDATE
SELECT * FROM student WHERE id = 1;           -- 确认只有 1 行
UPDATE student SET sex = '女' WHERE id = 1;   -- 再更新
```

【必须掌握】
- `UPDATE 表名 SET 列=值 WHERE 条件`
- 可以同时更新多列：`SET 列1=值1, 列2=值2`
- **WHERE 是必选项**——不写 WHERE 全表更新
- SET 的值可以是表达式：`SET age = age + 1`
- 更新后建议 SELECT 验证结果

【企业场景】
测试数据状态切换——接口测试中的常见操作：

```sql
-- 场景：测试"订单取消"接口
-- 1. 先造一个待支付的订单
INSERT INTO orders (id, status) VALUES (1001, 'pending');

-- 2. 执行测试：调用取消接口

-- 3. 验证：订单状态应该变成 cancelled
SELECT status FROM orders WHERE id = 1001;
-- 预期：'cancelled'

-- 4. 清理
DELETE FROM orders WHERE id = 1001;
```

有时为了方便，直接用 UPDATE 快速切换测试数据的状态，而不是重新 INSERT：

```sql
-- 把测试订单从 pending 改为 shipped（测试发货流程）
UPDATE orders SET status = 'shipped' WHERE id = 1001;
```

【面试考察】
面试官："写 UPDATE 语句时，如果忘了加 WHERE 会怎样？怎么预防？"

参考回答框架：
1. 不带 WHERE 的 UPDATE 会修改全表所有行——这是灾难性的
2. 预防：先 SELECT 确认影响行数，再 UPDATE
3. 预防：开启事务（BEGIN），UPDATE 后先 SELECT 确认，正确则 COMMIT，错误则 ROLLBACK
4. 预防：生产环境开启 sql_safe_updates 模式（禁止不带 WHERE 的 UPDATE/DELETE）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| UPDATE 忘加 WHERE | 先 SELECT 同条件确认，再用事务保护 |
| SET 多个列时用 AND 连接 | 用逗号：`SET a=1, b=2`，不是 `SET a=1 AND b=2` |
| WHERE 条件写错导致更新了不该更新的行 | 先在 SELECT 中验证 WHERE 条件 |
| 更新后没验证 | UPDATE 后立即 SELECT 确认结果 |

【扩展知识】
`sql_safe_updates` 模式——MySQL 的安全保护机制：
```sql
SET sql_safe_updates = 1;  -- 开启：禁止不带 WHERE 或 WHERE 不用索引的 UPDATE/DELETE
```
在这种模式下，`UPDATE t SET col=1`（无 WHERE）和 `DELETE FROM t WHERE name='a'`（name 无索引）都会被拒绝。生产环境强烈建议开启。

【我的理解】
> （创建一张 orders 表，插入 5 条数据。先用 SELECT 确认你要更新的行，再用 UPDATE 更新。然后试试不带 WHERE 的 UPDATE，观察结果。最后用 BEGIN → UPDATE → SELECT → ROLLBACK 体验事务回滚的保护效果。你感受到"先 SELECT 再 UPDATE"这个习惯的重要性了吗？）

---

## 四、删除数据 — DELETE 与 TRUNCATE

### 知识点 5：DELETE — 删除指定行

【课程原话/定义】

```sql
DELETE FROM 表名
[WHERE 条件表达式];
```

不写 WHERE = 删除全表所有行（逐行删除）。

```sql
-- 删除指定行
DELETE FROM student WHERE id = 1;

-- 删除全表（危险！）
DELETE FROM student;
```

【为什么？】
DELETE 的底层实现是**逐行删除**——每一行都记录到事务日志中（为了回滚）。如果你要删除全表 100 万行，DELETE 会执行 100 万次删除操作，非常慢。这时候应该用 TRUNCATE。

DELETE vs TRUNCATE vs DROP 的完整对比：

| | DELETE | TRUNCATE | DROP |
|------|--------|----------|------|
| 分类 | DML | DDL | DDL |
| 删除对象 | 行（数据） | 全表数据 | 整张表 |
| 可回滚 | ✅（事务中） | ❌（隐式提交） | ❌（隐式提交） |
| WHERE | ✅ 支持 | ❌ 不支持 | ❌ 不支持 |
| 速度 | 慢（逐行） | 快（重建表） | 快 |
| 自增归零 | 不归零 | 归零 | — |
| 触发器 | 触发 | 不触发 | 不触发 |

【必须掌握】
- `DELETE FROM 表名 WHERE 条件` — 删除指定行
- DELETE 是 DML，可以回滚（事务中）
- DELETE 不带 WHERE = 删除全表所有行
- DELETE 逐行删除，大数据量时慢
- 和 UPDATE 一样的安全原则：先 SELECT 再 DELETE

【企业场景】
测试数据清理的标准做法：

```sql
-- 每条测试用例执行完后清理自己的数据
DELETE FROM orders WHERE remark = 'auto_test_case_001';
DELETE FROM users WHERE username LIKE 'test_%';

-- 或者在测试套件开始时统一清理
-- 但更推荐"谁创建谁清理"——每条用例独立管理自己的数据
```

企业级的测试数据清理策略：
1. **测试前清理**：跑测试前 `DELETE WHERE test_data = 1` 清掉上次残留
2. **测试后清理**：tearDown 中删除本次测试创建的数据
3. **标记法**：测试数据加 `test_flag = 1` 标记，定期统一清理

【面试考察】
面试官："DELETE、TRUNCATE、DROP 有什么区别？分别适用于什么场景？"

参考回答框架：
1. DELETE：DML，删除行，支持 WHERE，可回滚，慢——适合删除特定数据
2. TRUNCATE：DDL，清空全表，不可回滚，快（重建表），自增归零——适合批量清空测试表
3. DROP：DDL，删除整张表（结构和数据都没了），不可回滚——适合删除废弃的表
4. 测试中：日常清理用 DELETE（可控），批量重置用 TRUNCATE（快），删表用 DROP

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| DELETE 忘加 WHERE | 同 UPDATE：先 SELECT 确认，再用事务保护 |
| 用 DELETE 清空百万行数据的表 | 用 TRUNCATE（快几百倍） |
| 认为 TRUNCATE 可以回滚 | TRUNCATE 是 DDL，隐式提交，不可回滚 |
| DELETE 后自增 ID 没归零 | DELETE 不重置 AUTO_INCREMENT，TRUNCATE 会重置 |

【我的理解】
> （创建一张 test_table，插入 3 条数据。分别用 DELETE（带 WHERE）、DELETE（不带 WHERE）、TRUNCATE 三种方式操作，观察自增 ID 的变化。DELETE 后插入新数据，ID 从哪开始？TRUNCATE 后呢？这个区别在测试数据管理中有什么影响？）

---

## 五、DML 操作安全原则

### 知识点 6：DML 安全操作四步法

【课程原话/定义】
所有 DML 操作（特别是 UPDATE 和 DELETE）都应遵循安全操作流程。

【为什么？】
这不是语法要求，而是工程实践。测试工程师操作数据库时，一条写错的 SQL 可能毁掉整个测试环境的数据——虽然不是生产，但重建测试数据也浪费时间。

【必须掌握】
安全四步法：

```
1. BEGIN;                          -- 开启事务
2. SELECT ... WHERE 条件;          -- 先看要影响哪些行
3. UPDATE/DELETE ... WHERE 条件;   -- 确认无误后执行
4. SELECT ... WHERE 条件;          -- 验证结果
   → 正确：COMMIT;
   → 错误：ROLLBACK;
```

【企业场景】
测试环境中真实发生过的事：

> "我在测试库执行 DELETE，忘了加 WHERE，把整张配置表清空了。还好有备份，但恢复花了半小时。"

有了事务保护：
```sql
BEGIN;
DELETE FROM config;       -- 一顿操作
SELECT COUNT(*) FROM config;  -- 0？！不对！
ROLLBACK;                  -- 撤回，数据恢复
```

几秒钟的事，而不是半小时。

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 直接执行 UPDATE/DELETE 不先看看 | 先 SELECT 确认行数和内容 |
| 知道事务但不习惯用 | 养成肌肉记忆：写 DML 前先打 BEGIN |
| 在自动提交模式下操作 | `SET autocommit = 0` 或显式 BEGIN |

【我的理解】
> （模拟一次"误操作"：BEGIN → DELETE 全表 → 发现不对 → ROLLBACK。再模拟正确流程：BEGIN → SELECT 确认 → DELETE → SELECT 验证 → COMMIT。对比两种体验，哪个让你更安心？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| DML 概述 | INSERT/UPDATE/DELETE、vs DDL 区别 | ★★★★☆ |
| INSERT 语法 | 三种写法、指定列名最安全、批量插入 | ★★★★★ |
| INSERT 注意事项 | 类型匹配、单引号、NULL 处理 | ★★★☆☆ |
| UPDATE 语法 | SET/WHERE、全表更新风险、先 SELECT 再 UPDATE | ★★★★★ |
| DELETE 语法 | DELETE vs TRUNCATE vs DROP 对比表 | ★★★★★ |
| 安全四步法 | BEGIN → SELECT → DML → 验证 → COMMIT/ROLLBACK | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch02-DDL数据库与表操作]] — 建表后才能 INSERT
- [[Ch04-DQL表查询操作]] — SELECT 验证 DML 结果
- [[Ch01-MySQL基础与SQL入门]] — DML 在 SQL 四大分类中的位置
