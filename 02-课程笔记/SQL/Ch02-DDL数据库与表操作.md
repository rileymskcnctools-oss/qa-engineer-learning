---
tags: [课程笔记, SQL, MySQL]
course: "SQL"
chapter: "Ch02-DDL数据库与表操作"
created: 2026-07-31
status: draft
---

# Ch02 - DDL 数据库与表操作

## 课程来源
- 学习日期：

---

## 一、DDL 数据库操作

### 知识点 1：CREATE DATABASE — 创建数据库

【课程原话/定义】
`CREATE DATABASE` 用于创建新数据库，是学习 SQL 的第一条 DDL 语句。

```sql
-- 最基本创建
CREATE DATABASE mydb;

-- 最优创建写法（推荐）
CREATE DATABASE IF NOT EXISTS mydb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

各子句的含义：

| 子句 | 作用 | 不写时的默认值 |
|------|------|--------------|
| `IF NOT EXISTS` | 库存在时跳过不报错 | 库存在直接报 ERROR 1007 |
| `CHARACTER SET` | 指定字符集 | 取决于服务器配置（通常 latin1） |
| `COLLATE` | 指定排序规则 | 取决于字符集的默认排序规则 |

【为什么？】
为什么需要 `IF NOT EXISTS`？ 在实际工作中，建库脚本可能被执行多次（部署、迁移、队友也在跑）。不加这个子句，第二次跑就报错，脚本中止。加了之后幂等——跑多少次结果都一样。

为什么一定要指定 `CHARACTER SET utf8mb4`？ MySQL 默认字符集是 latin1，不支持中文。如果不指定，存中文数据时全部变成 `???`。utf8mb4 是真正的 UTF-8（MySQL 的 utf8 是阉割版，最多 3 字节，不支持 emoji 和部分生僻字）。

```sql
-- 验证：latin1 的灾难
CREATE DATABASE test_latin1 CHARACTER SET latin1;
-- 在这个库里建表存 '你好' → 查询结果: ???
```

【必须掌握】
- 完整建库语法：`CREATE DATABASE [IF NOT EXISTS] 库名 [CHARACTER SET 字符集] [COLLATE 排序规则];`
- `IF NOT EXISTS` 让脚本可重复执行
- 字符集选 utf8mb4（不是 utf8，不是 latin1）
- 排序规则 `utf8mb4_unicode_ci`：ci = case insensitive（大小写不敏感）

【企业场景】

| 场景 | 操作 |
|------|------|
| 新项目搭建测试环境 | 执行建库脚本，创建 test 库和 dev 库 |
| CI/CD 自动化测试 | 每次跑测试前 `CREATE DATABASE IF NOT EXISTS`，确保库存在 |
| 多套环境同步 | 开发/测试/预发布/生产环境的建库脚本完全一致 |
| Docker 初始化 | `docker-compose` 中 MySQL 容器启动时自动执行建库 SQL |

```sql
-- 企业级建库脚本模板
CREATE DATABASE IF NOT EXISTS myapp_test
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

【面试考察】
面试官："建库时你会指定字符集吗？为什么？utf8 和 utf8mb4 有什么区别？"

参考回答框架：
1. 必须指定 `CHARACTER SET utf8mb4`，否则可能默认 latin1，中文乱码
2. MySQL 的 `utf8` 最多存 3 字节，emoji（如 😊 占 4 字节）存不了
3. `utf8mb4` 是真正的 UTF-8，支持 4 字节字符
4. 排序规则选 `utf8mb4_unicode_ci`（通用）或 `utf8mb4_general_ci`（较快但不够准）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `CREATE DATABASE mydb;` 重复执行报错 | 加 `IF NOT EXISTS` |
| 不指定字符集，中文变 `???` | 必须指定 `CHARACTER SET utf8mb4` |
| 以为 `CHARACTER SET utf8` 就行了 | MySQL 的 utf8 ≠ 真正 UTF-8，要用 utf8mb4 |
| 排序规则和字符集不匹配 | 用和字符集配套的 COLLATE（如 utf8mb4 + utf8mb4_unicode_ci） |

【扩展知识】
MySQL 8.0 开始，默认字符集改为了 utf8mb4，但老版本/定制镜像仍可能是 latin1。最安全的做法永远是显式指定。

```sql
-- 查看 MySQL 默认字符集
SHOW VARIABLES LIKE 'character_set_%';
SHOW VARIABLES LIKE 'collation_%';
```

【我的理解】
> （在你的电脑上用命令行完成以下操作，记录每一步的结果：
> ① `CREATE DATABASE test_ch02 CHARACTER SET utf8mb4;`
> ② 再执行一次相同命令 → 为什么会报错？加 `IF NOT EXISTS` 后再试
> ③ `CREATE DATABASE test_latin1 CHARACTER SET latin1;` 然后在里面建表存一条中文数据，查询时能看到什么？
> ④ 最后 `DROP DATABASE test_ch02; DROP DATABASE test_latin1;` 清理掉。你能用一句话说清楚 `CHARACTER SET` 和 `COLLATE` 的关系吗？）

---

### 知识点 2：SHOW DATABASES / USE / SHOW CREATE DATABASE — 查看与切换

【课程原话/定义】
这三个命令是数据库操作的"查"功能——查看、切换、查看定义。

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 切换到指定数据库
USE mydb;

-- 查看某个数据库的创建语句（看它的定义）
SHOW CREATE DATABASE mydb;
```

`SHOW CREATE DATABASE` 输出示例：
```
+----------+------------------------------------------------------------------+
| Database | Create Database                                                  |
+----------+------------------------------------------------------------------+
| mydb     | CREATE DATABASE `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+------------------------------------------------------------------+
```
这个输出就是当初创建这个数据库时"真正执行"的完整 SQL。

【为什么？】
这三个命令对应"查"的三个层次：
- `SHOW DATABASES`：宏观层——服务器上有哪些数据库？相当于 `ls /data/`
- `USE`：选择层——接下来所有操作在哪个库里执行？
- `SHOW CREATE DATABASE`：细节层——这个库当初是怎么建的？字符集是什么？

测试工程师最常用的场景：定位环境问题时，需要确认测试库的字符集和生产库是否一致。`SHOW CREATE DATABASE` 能直接告诉你答案，不用去翻半年前的建库脚本。

【必须掌握】
- `SHOW DATABASES;` → 列出所有库（包含系统库）
- `USE 库名;` → 切换当前工作库，后续 SQL 在此库执行
- `SHOW CREATE DATABASE 库名;` → 查看建库 SQL 和字符集
- `SELECT DATABASE();` → 查看当前在哪个库

【企业场景】

```sql
-- 典型的排查流程
-- 1. 我连的是哪个服务器？有哪些库？
SHOW DATABASES;

-- 2. 测试库的字符集对吗？
SHOW CREATE DATABASE myapp_test;
-- 输出中看 CHARACTER SET 是不是 utf8mb4

-- 3. 切到测试库开始干活
USE myapp_test;

-- 4. 确认切换成功
SELECT DATABASE();  -- 返回 myapp_test
```

【面试考察】
面试官："怎么查看当前数据库的字符集？"

参考回答框架：
1. `SHOW CREATE DATABASE 库名;` 直接看建库语句中的 CHARACTER SET
2. `SHOW VARIABLES LIKE 'character_set_database';` 看当前库的字符集变量
3. 这两个的区别：VARIABLES 显示的是当前会话的变量值，CREATE DATABASE 显示的是库定义

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 忘了 USE，SQL 在错误的库上执行 | 先 `SELECT DATABASE();` 确认，再执行 |
| `SHOW CREATE DATABASE` 输出不理解 | 看输出里的 `CHARACTER SET` 和 `COLLATE` 字段 |
| 不知道当前在哪个库，乱写表名 | 每次连数据库先 USE + SELECT DATABASE 确认 |

【我的理解】
> （在命令行中依次执行：`SHOW DATABASES;` → 你能认出哪几个是系统库？哪几个是你自己建的？
> 然后 `USE mysql;` → `SELECT DATABASE();` → 验证切换成功 → 再 `SHOW CREATE DATABASE mysql;` 看看系统库的字符集是什么。
> 最后切回你之前建的测试库。这个过程就是"数据库导航"，测试工作中每天都要做。）

---

### 知识点 3：ALTER DATABASE — 修改数据库

【课程原话/定义】
`ALTER DATABASE` 用于修改已存在数据库的属性，最常用的场景是修改字符集和排序规则。

```sql
-- 修改数据库字符集
ALTER DATABASE mydb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

注意：ALTER DATABASE 只能改库级别的属性（字符集、排序规则、加密等），不能改库名。MySQL 不支持 `RENAME DATABASE`。

【为什么？】
什么时候需要 ALTER DATABASE？
1. 老项目从 latin1 迁移到 utf8mb4
2. 测试环境当初用默认配置建的库，现在要和生产环境对齐
3. 从其他数据库导入数据后，发现排序规则不对导致查询结果不一致

ALTER DATABASE 只影响**之后新建的表**，已有表的字符集不会自动改——这是一个超级大坑。

```sql
-- 验证：改库字符集 ≠ 改已有表的字符集
ALTER DATABASE mydb CHARACTER SET utf8mb4;  -- 改库
CREATE TABLE new_table (id INT);             -- 新表继承 utf8mb4 ✓
-- 但 old_table 还是原来的字符集 ✗
ALTER TABLE old_table CONVERT TO CHARACTER SET utf8mb4;  -- 需要单独改表
```

【必须掌握】
- `ALTER DATABASE 库名 CHARACTER SET 字符集 COLLATE 排序规则;`
- 只能改字符集和排序规则，不能改库名
- 已有表的字符集不受影响，需单独 `ALTER TABLE ... CONVERT TO CHARACTER SET`
- 改之前先用 `SHOW CREATE DATABASE` 查看当前设置

【企业场景】

| 场景 | 操作 |
|------|------|
| 老项目字符集升级 | `ALTER DATABASE` + 逐表 `ALTER TABLE ... CONVERT TO` |
| 测试环境对齐生产 | 从生产导出建库语句，在测试环境用 ALTER DATABASE 对齐 |
| 排查排序问题 | 发现排序结果不对 → 查 COLLATE 是否一致 |

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 ALTER DATABASE 能改库名 | MySQL 不支持 RENAME DATABASE，只能导出 → 新建 → 导入 |
| 以为改了库字符集所有表就自动改了 | 已有表必须逐表 ALTER TABLE |
| 改了字符集不改 COLLATE | 字符集和排序规则是一对，同时修改 |

【扩展知识】
生产环境改字符集的标准操作流程（SOP）：
1. 备份数据库（`mysqldump`）
2. 修改库字符集（`ALTER DATABASE`）
3. 逐表修改字符集（`ALTER TABLE ... CONVERT TO CHARACTER SET`）
4. 验证数据完整性（抽查中文数据、emoji 数据）

【我的理解】
> （你已经创建了 `test_latin1` 库（latin1 字符集）。
> ① 执行 `ALTER DATABASE test_latin1 CHARACTER SET utf8mb4;`
> ② `SHOW CREATE DATABASE test_latin1;` → 确认字符集改了
> ③ 但是之前建的表呢？查一下：`SHOW CREATE TABLE 表名;` → 表的字符集变了吗？
> 这个实验能让你深刻理解"库级修改 ≠ 表级修改"。）

---

### 知识点 4：DROP DATABASE — 删除数据库 & 系统数据库

【课程原话/定义】
`DROP DATABASE` 删除整个数据库——包括里面的所有表、所有数据、所有视图、所有存储过程。删了就没了，没有回收站。

```sql
-- 安全删除
DROP DATABASE IF EXISTS mydb;

-- 危险删除（库不存在会报错）
DROP DATABASE mydb;
```

MySQL 安装后自带 4 个系统数据库，**绝对不能删**：

| 系统数据库 | 作用 | 删除后果 |
|-----------|------|---------|
| `mysql` | 存储用户账户、权限、时区等核心元数据 | MySQL 直接无法启动 |
| `information_schema` | 数据库元信息的只读视图（有哪些表、列、索引等） | 所有查询元信息的操作失败 |
| `performance_schema` | 性能监控数据（查询耗时、锁等待、内存使用等） | 性能分析功能失效 |
| `sys` | 基于 performance_schema 的易用视图集合 | DBA 常用诊断工具失效 |

【为什么？】
为什么 DROP DATABASE 需要极其谨慎？

1. **不可恢复**：MySQL 没有回收站功能，DROP 直接物理删除数据文件
2. **级联删除**：库里的所有表、所有数据、所有索引、所有视图……全部消失
3. **没有确认**：不像 Workbench 有 Apply → 确认弹窗，命令行直接执行

`IF EXISTS` 的价值：自动化脚本中如果没有它，第一次跑成功删除，第二次跑就报错（库已不存在），脚本中断。加了 `IF EXISTS`，无论库存不存在都正常执行。

【必须掌握】
- `DROP DATABASE [IF EXISTS] 库名;`
- 4 个系统数据库绝对不能删：mysql、information_schema、performance_schema、sys
- 没有确认提示，没有回收站，执行即删除
- 测试脚本中必须加 `IF EXISTS`

【企业场景】

| 场景 | 操作 |
|------|------|
| 自动化测试清理 | `DROP DATABASE IF EXISTS test_db;` + 重新 `CREATE DATABASE` |
| 本地环境重置 | 删掉开发库，重新导入生产备份重新测试 |
| 新人误操作 | "我把 mysql 库删了怎么办？"→ 只能重装 MySQL |
| CI/CD 隔离 | 每个测试任务创建独立库，跑完即删 |

```sql
-- 安全删除流程（先确认，再动手）
SHOW DATABASES;                           -- 1. 确认要删的库名
SELECT DATABASE();                        -- 2. 确认当前不在要删的库里
DROP DATABASE IF EXISTS test_old;         -- 3. 执行删除
SHOW DATABASES;                           -- 4. 确认已删除
```

【面试考察】
面试官："MySQL 有哪些系统数据库？哪些绝对不能删？"

参考回答框架：
1. 四个系统库：mysql（用户权限）、information_schema（元数据）、performance_schema（性能）、sys（诊断）
2. 最危险的是 mysql 库——删除后 MySQL 无法启动，只能重装
3. information_schema 是只读视图，存储了所有数据库和表的元信息
4. performance_schema 用于性能监控，sys 是对它的封装

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `DROP DATABASE` 不加 `IF EXISTS` | 自动化脚本必须加，否则不可重复执行 |
| 误删系统库 | 操作前 `SHOW DATABASES` 看清楚，避免在 mysql/performance_schema 上操作 |
| 删完发现删错了 | 没有办法恢复——唯一生路是从备份恢复 |
| 在要删的库里执行 DROP | 先 `USE` 到别的库，否则某些客户端会报错 |

【我的理解】
> （执行 `SHOW DATABASES;` 列出你电脑上所有的数据库。哪些是你自己建的？哪些是系统自带的？
> 对于每个系统库，尝试理解它的作用：
> - `mysql` 库里存了什么？→ `USE mysql; SHOW TABLES;` 看看有哪些表（user 表、db 表…）
> - `information_schema` 和 `performance_schema` 有什么区别？一个是"元数据"，一个是"运行数据"
> 记住一句话：**DROP 没有回头路，删库前先 SHOW DATABASES 三遍。**）

---

### 知识点 5：数据库命名规则

【课程原话/定义】
MySQL 对数据库的命名有一套规则和限制：

| 规则 | 说明 |
|------|------|
| 长度限制 | 最多 64 个字符 |
| 合法字符 | 字母、数字、下划线 `_`、美元符 `$` |
| 不能用的 | MySQL 关键字（CREATE、SELECT、TABLE 等）、纯数字、空格、特殊符号 |
| 大小写 | Windows 下不区分大小写，Linux 下区分大小写 |
| 反引号 | 如果非要用关键字作为库名/表名，用反引号包裹 `` ` `` |

```sql
-- 合法的库名
CREATE DATABASE my_database;
CREATE DATABASE test_db_2026;
CREATE DATABASE app_backend;

-- 不合法 / 不推荐的库名
CREATE DATABASE 123db;          -- 不能以数字开头
CREATE DATABASE my-database;    -- 包含连字符 -（虽然反引号可以但别用）
CREATE DATABASE SELECT;         -- 关键字（虽然反引号可以但别用）
CREATE DATABASE `SELECT`;       -- 反引号强行用关键字，但极度不推荐
```

【为什么？】
命名不规范是团队协作的第一大坑。假设你的同事建了个库叫 `MyDatabase`，你在 Linux 服务器上写 `SELECT * FROM mydatabase`——报错找不到。因为 Linux 区分大小写，`MyDatabase ≠ mydatabase`。

好的命名规则：
```
项目名_环境_功能
例如：myapp_test、myapp_dev、myapp_prod
```

【必须掌握】
- 库名最多 64 个字符
- 只能使用：字母、数字、下划线 `_`、`$`
- 不能用：关键字、纯数字开头、空格、特殊符号
- **统一用小写字母 + 下划线**（snake_case），避免跨平台大小写问题
- 库名要能"见名知意"——`mydb` 不如 `myapp_test`

【企业场景】

| 场景 | 命名约定 |
|------|---------|
| 开发环境 | `project_dev` |
| 测试环境 | `project_test` |
| 预发布 | `project_staging` |
| 生产环境 | `project_prod`（线上环境测试工程师通常只读） |

```sql
-- 测试工程师创建个人测试库（用名字区分，避免冲突）
CREATE DATABASE IF NOT EXISTS test_riley;   -- 个人测试库

-- 跑自动化测试的专用库
CREATE DATABASE IF NOT EXISTS myapp_autotest;
```

【面试考察】
面试官："数据库命名有什么规范？你在项目里怎么给测试库起名？"

参考回答框架：
1. 统一小写 + 下划线（snake_case），避免跨平台大小写问题
2. 不用关键字、不用特殊字符、不用纯数字开头
3. 命名要有语义：项目名_环境名，如 `myapp_test`
4. 测试工程师的测试库名字要能区分是谁的测试环境，避免多人共用污染

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 用大写字母命名 | 统一小写，避免 Linux 部署时大小写问题 |
| 用 `-` 连字符 | 用下划线 `_`，因为 `-` 在某些 SQL 客户端被当作减号 |
| 起名叫 `test` 或 `db1` | 起有意义的名称，三个月后你还能看懂 |
| 多人共用同一个测试库 | 每人/每个测试任务独立建库，数据不互相污染 |

【扩展知识】
其他数据库的命名差异：

| 数据库 | 命名规则差异 |
|--------|-------------|
| PostgreSQL | 默认转小写，大写需双引号 `"MyTable"` |
| Oracle | 对象名最长 30（老版本），自动转大写 |
| SQL Server | 可以用 `[方括号]` 包裹含特殊字符的名称 |

【我的理解】
> （试着创建以下数据库，看看哪些能成功哪些报错：
> ① `CREATE DATABASE 123abc;`
> ② `CREATE DATABASE my-db;`
> ③ `CREATE DATABASE SELECT;`
> ④ `CREATE DATABASE \`SELECT\`;`  — 注意这里的引号是反引号（键盘 ESC 下面的键）
> 成功创建后用 `DROP DATABASE IF EXISTS ...;` 清理。
> 你公司的代码库和数据库命名规范是什么？是 snake_case 还是 camelCase？思考为什么团队要有统一命名规范。）

---

## 二、MySQL 数据类型

### 知识点 6：MySQL 数据类型大全

【课程原话/定义】
数据类型定义了列中能存储什么值。MySQL 的数据类型分为四大类：数值、字符串、日期时间、二进制。

---

#### 6.1 整数类型

| 类型 | 字节数 | 有符号范围 | 无符号范围 | 用途 |
|------|--------|-----------|-----------|------|
| TINYINT | 1 | -128 ~ 127 | 0 ~ 255 | 年龄、状态码、布尔值 |
| SMALLINT | 2 | -32768 ~ 32767 | 0 ~ 65535 | 小计数器、年份 |
| MEDIUMINT | 3 | -8388608 ~ 8388607 | 0 ~ 16777215 | 中等数量 |
| INT / INTEGER | 4 | -2147483648 ~ 2147483647 | 0 ~ 4294967295 | 主键 ID、用户数 |
| BIGINT | 8 | -2^63 ~ 2^63-1 | 0 ~ 2^64-1 | 超大 ID、雪花算法 |

```sql
-- 整型使用示例
CREATE TABLE int_demo (
    id INT PRIMARY KEY AUTO_INCREMENT,      -- 主键，自增
    age TINYINT UNSIGNED,                   -- 年龄 0-255，无符号
    status TINYINT DEFAULT 0,               -- 状态码：0正常 -1禁用
    user_count INT UNSIGNED DEFAULT 0       -- 用户数，不能为负
);
```

【为什么？】
为什么要分这么多整数类型？**存储空间就是钱**。一个表有 1 亿行，每行省 3 个字节就是 300MB。该用 TINYINT 的字段用了 BIGINT，浪费 7 倍空间，查询和索引都变慢。

UNSIGNED（无符号）的作用：年龄、计数器这些永远不为负的值，用 UNSIGNED 范围翻倍。比如 TINYINT UNSIGNED 可以存 0-255，比有符号的 127 大一倍。

---

#### 6.2 浮点数与定点数类型

| 类型 | 字节数 | 说明 | 典型场景 |
|------|--------|------|---------|
| FLOAT | 4 | 单精度浮点，约 7 位有效数字 | 不精确的科学计算 |
| DOUBLE | 8 | 双精度浮点，约 15 位有效数字 | 不精确的大数计算 |
| DECIMAL(M,D) | 变长 | 定点数，M=总位数 D=小数位 | **金额、价格（精确）** |

```sql
-- 浮点 vs 定点：精度对比
CREATE TABLE money_demo (
    price_float FLOAT,               -- 存 99.99 → 可能变成 99.989997863...
    price_decimal DECIMAL(10,2)      -- 存 99.99 → 始终是 99.99
);

INSERT INTO money_demo VALUES (99.99, 99.99);
SELECT * FROM money_demo;
-- price_float:  99.98999786376953  ← 精度丢失！
-- price_decimal: 99.99             ← 精确
```

【为什么？】
金融系统敢用 FLOAT 存金额就等着审计被查。FLOAT/DOUBLE 是**近似值**（二进制无法精确表示十进制小数），DECIMAL 是**精确值**（以字符串形式存储，保证精度）。

一句话口诀：**价格金额用 DECIMAL，其他用 DOUBLE 够用，FLOAT 基本不用。**

---

#### 6.3 字符串类型

| 类型 | 最大长度 | 存储方式 | 典型场景 |
|------|---------|---------|---------|
| CHAR(M) | 255 字符 | 定长，未满补空格 | 手机号、身份证、MD5 |
| VARCHAR(M) | 65535 字节 | 变长，按实际长度 + 1/2 字节 | 用户名、邮箱、地址 |
| TINYTEXT | 255 字节 | 变长 | 短文本 |
| TEXT | 65535 字节 (~64KB) | 变长 | 文章内容、备注 |
| MEDIUMTEXT | 16777215 字节 (~16MB) | 变长 | 长文档 |
| LONGTEXT | 4294967295 字节 (~4GB) | 变长 | 超大文本（很少用） |

```sql
-- CHAR vs VARCHAR 对比
CREATE TABLE str_demo (
    name VARCHAR(50),            -- 存 'Tom' 只占 3 字节 + 1 长度字节
    phone CHAR(11),              -- 存 '13800138000' 固定占 11 字节
    bio TEXT                     -- 存长文本简介
);
```

【为什么？】
CHAR 和 VARCHAR 的区别是面试必考：

| 对比维度 | CHAR | VARCHAR |
|----------|------|---------|
| 存储方式 | 定长，不够补空格 | 变长，只存实际内容 |
| 速度 | 快（不用计算长度） | 略慢（需要额外字节记录长度） |
| 空间 | 浪费（固定长度） | 节省（按需） |
| 适用场景 | 固定长度的值（手机号、身份证） | 变长的值（用户名、地址、邮箱） |
| 最大长度 | 255 字符 | 65535 字节（注意是字节不是字符） |

记忆技巧：**CHAR = 定长快但浪费，身份证手机号用它。VARCHAR = 变长省空间，用户名地址用它。**

TEXT 系列不能有默认值，也不能直接建索引（需要指定前缀长度），这是重要的限制：

```sql
CREATE TABLE text_demo (
    content TEXT NOT NULL DEFAULT ''   -- 报错！TEXT 不能有 DEFAULT
);
```

---

#### 6.4 日期时间类型

| 类型 | 格式 | 范围 | 占用空间 | 典型场景 |
|------|------|------|---------|---------|
| DATE | YYYY-MM-DD | 1000-01-01 ~ 9999-12-31 | 3 字节 | 生日、入职日期 |
| TIME | HH:MM:SS | -838:59:59 ~ 838:59:59 | 3 字节 | 时长、每日提醒时间 |
| DATETIME | YYYY-MM-DD HH:MM:SS | 1000-01-01 00:00:00 ~ 9999-12-31 23:59:59 | 8 字节（MySQL 5.6+） | 创建时间、更新时间 |
| TIMESTAMP | YYYY-MM-DD HH:MM:SS | 1970-01-01 00:00:01 ~ 2038-01-19 03:14:07 | 4 字节 | 记录时间、自动更新 |
| YEAR | YYYY | 1901 ~ 2155 | 1 字节 | 年份 |

```sql
-- 日期类型使用示例
CREATE TABLE date_demo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    birthday DATE,                                  -- 生日，只有日期
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- 自动更新时间
);
```

【为什么？】
DATETIME vs TIMESTAMP —— 又是一道面试必考题：

| 对比维度 | DATETIME | TIMESTAMP |
|----------|----------|-----------|
| 范围 | 1000-9999 年 | 1970-2038 年（有 2038 问题） |
| 时区 | 不随时区变化 | 自动转换 UTC（存 UTC，读转本地） |
| 空间 | 8 字节（5.6+） | 4 字节 |
| 自动更新 | 需手动设置 | 支持 ON UPDATE CURRENT_TIMESTAMP |
| 适用场景 | 固定日期（生日、历史日期） | 记录时间（创建/更新时间） |

记忆技巧：**TIMESTAMP = 省空间 + 有时区 + 会溢出（2038）。DATETIME = 范围大 + 无时区。记录创建/更新时间用 TIMESTAMP，存固定日期用 DATETIME。**

【必须掌握】
- 主键 ID：INT 或 BIGINT + AUTO_INCREMENT
- 金额：DECIMAL，不能用 FLOAT/DOUBLE
- 固定长度字符串：CHAR（如手机号 CHAR(11)）
- 可变长字符串：VARCHAR
- 创建时间：DATETIME 或 TIMESTAMP
- 状态/标志：TINYINT

```sql
-- 测试工程师建表"最常用数据类型"速查
-- 用户表典型结构
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,          -- 主键（大整数 + 自增）
    username VARCHAR(50) NOT NULL,                  -- 用户名（可变长）
    phone CHAR(11) NOT NULL DEFAULT '',             -- 手机号（定长）
    age TINYINT UNSIGNED,                           -- 年龄（小整数无符号）
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,    -- 余额（定点数精确）
    status TINYINT NOT NULL DEFAULT 0,              -- 状态：0正常 1禁用
    birthday DATE,                                  -- 生日（只有日期）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP   -- 创建时间
);
```

【企业场景】
测试工程师选择数据类型的思维模型：

| 被测字段 | 推荐类型 | 边界值测试思路 |
|----------|---------|---------------|
| 用户名 | VARCHAR(50) | 测 0 字符、1 字符、50 字符、51 字符 |
| 年龄 | TINYINT UNSIGNED | 测 -1、0、127、128、255、256 |
| 金额 | DECIMAL(12,2) | 测 0.00、0.01、9999999999.99、负数 |
| 手机号 | CHAR(11) | 测 10 位、11 位、12 位、含字母 |

【面试考察】
面试官："CHAR 和 VARCHAR 的区别是什么？DATETIME 和 TIMESTAMP 的区别？金额用什么类型？"

参考回答框架：
1. CHAR 定长（快但浪费），适合固定长度如手机号；VARCHAR 变长（省空间），适合可变长如用户名
2. DATETIME 范围大（1000-9999）、无时区；TIMESTAMP 范围小（1970-2038）、有时区、支持自动更新
3. 金额用 DECIMAL，不能用 FLOAT/DOUBLE（精度丢失）
4. 选类型的原则：够用就好，不要浪费存储空间

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 金额用 FLOAT/DOUBLE | 必须用 DECIMAL(M,D)，保证精度 |
| VARCHAR(11) 存手机号 | 手机号固定 11 位，用 CHAR(11) 更快 |
| TEXT 列设置 DEFAULT '' | TEXT 不能有默认值 |
| TIMESTAMP 存 2039 年的日期 | TIMESTAMP 有 2038 溢出问题，用 DATETIME |
| INT UNSIGNED 存年龄 | 年龄可能为 0，别用 -1 表示未设置，用 NULL |
| VARCHAR(65535) | 行最大 65535 字节，VARCHAR 还要留空间给其他列和开销字节 |

【扩展知识】
BIT 和 BOOLEAN 类型：

| 类型 | 说明 | 实际存储 |
|------|------|---------|
| BOOLEAN / BOOL | 布尔值 | 其实是 TINYINT(1)，0=false 非0=true |
| BIT(M) | 位字段 | M 范围 1-64，存储二进制位 |

BLOB 类型（二进制大对象，存文件/图片）：

| 类型 | 最大大小 |
|------|---------|
| TINYBLOB | 255 字节 |
| BLOB | 64KB |
| MEDIUMBLOB | 16MB |
| LONGBLOB | 4GB |

```sql
-- 实际项目中文件通常不存数据库，存 OSS/文件服务器
-- 数据库中只存文件 URL
ALTER TABLE users ADD COLUMN avatar_url VARCHAR(500);
```

【我的理解】
> （打开你之前在 Ch01 中建的任意一张表，用 `SHOW CREATE TABLE 表名;` 看看每个字段的数据类型。
> 然后回答以下问题，不看笔记：
> ① 年龄字段用什么类型？为什么不用 INT？
> ② 手机号用什么类型？CHAR 还是 VARCHAR？长度多少？
> ③ 订单金额用什么类型？用 FLOAT 会有什么后果？
> ④ 创建时间用什么类型？如果业务需要"订单超过 30 天自动取消"，用 DATETIME 还是 TIMESTAMP？
> ⑤ 一个字段存"是否删除"（是/否），用什么类型最小？）

---

## 三、DDL 表操作

### 知识点 7：CREATE TABLE — 创建表

【课程原话/定义】
`CREATE TABLE` 是 DDL 中最核心的语句，定义了表的结构：表名、列名、数据类型、约束。

**完整语法：**
```sql
CREATE TABLE [IF NOT EXISTS] 表名 (
    列名1 数据类型 [NOT NULL] [DEFAULT 默认值] [AUTO_INCREMENT] [COMMENT '注释'],
    列名2 数据类型 [约束],
    ...
    [PRIMARY KEY (列名)],
    [INDEX 索引名 (列名)],
    [UNIQUE KEY 唯一键名 (列名)]
) [ENGINE=存储引擎] [CHARACTER SET=字符集] [COMMENT='表注释'];
```

**列属性详解：**

| 属性 | 语法 | 作用 |
|------|------|------|
| NOT NULL | `username VARCHAR(50) NOT NULL` | 该列不允许为 NULL，插入时必须给值 |
| DEFAULT | `status TINYINT DEFAULT 0` | 插入时如果不指定该列，使用默认值 |
| AUTO_INCREMENT | `id INT AUTO_INCREMENT` | 自动递增，每插入一行自动 +1 |
| PRIMARY KEY | `id INT PRIMARY KEY` | 主键约束：唯一 + 非空，一张表只能一个 |
| COMMENT | `age TINYINT COMMENT '用户年龄'` | 给列或表添加注释 |

```sql
-- 完整的建表示例（学生表）
CREATE TABLE IF NOT EXISTS student (
    id          INT PRIMARY KEY AUTO_INCREMENT COMMENT '学生ID，主键，自增',
    name        VARCHAR(50) NOT NULL COMMENT '姓名，不能为空',
    gender      CHAR(1) NOT NULL DEFAULT 'M' COMMENT '性别：M男 F女',
    age         TINYINT UNSIGNED COMMENT '年龄',
    phone       CHAR(11) NOT NULL DEFAULT '' COMMENT '手机号',
    score       DECIMAL(5,2) NOT NULL DEFAULT 0.00 COMMENT '成绩，精确到小数点后2位',
    status      TINYINT NOT NULL DEFAULT 1 COMMENT '状态：0禁用 1正常',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';
```

【为什么？】
列属性的存在是为了**数据完整性**——你不可能靠应用层代码保证每一条数据的质量。数据库层面的约束是最后一道防线：

```sql
-- 如果没有 NOT NULL 约束
INSERT INTO student (name, age) VALUES (NULL, 20);  -- 成功！但 name 是 NULL
-- 后来 SELECT * FROM student WHERE name IS NULL; 查出一堆脏数据

-- 有 NOT NULL 约束
-- 直接报错：Column 'name' cannot be null → 数据干净
```

**AUTO_INCREMENT 的精妙之处**：
- 不用手动分配 ID，数据库帮你搞定
- 即使并发插入，ID 也不会重复（内部用锁保证）
- 删除记录后，ID 不会回填（删了 id=5，下一条是 6，不是 5）

**DEFAULT 的企业价值**：
```sql
-- 没有 DEFAULT
INSERT INTO student (name, gender, phone) VALUES ('张三', 'M', '13800138000');
-- score 被插入 NULL —— 后续计算 AVG(score) 时 NULL 被忽略，结果不准！

-- 有 DEFAULT
INSERT INTO student (name, gender, phone) VALUES ('张三', 'M', '13800138000');
-- score 被插入 0.00 —— 查询计算一切正常
```

【必须掌握】
- 完整建表语法，特别是列属性的组合使用
- `NOT NULL`：保证关键字段不落空
- `DEFAULT`：给非必填字段提供合理默认值
- `AUTO_INCREMENT`：自增主键（必须配合 PRIMARY KEY 或 UNIQUE）
- `PRIMARY KEY`：唯一标识一行（= NOT NULL + UNIQUE）
- `COMMENT`：给列和表加注释（好习惯，DDL 也是文档）
- 表级选项：`ENGINE=InnoDB`（支持事务）、`CHARSET=utf8mb4`

【企业场景】

```sql
-- 测试工程师建表的实际场景

-- 场景1：建一张自动化测试用的临时表
CREATE TABLE IF NOT EXISTS auto_test_result (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    case_name   VARCHAR(200) NOT NULL COMMENT '用例名称',
    result      CHAR(4) NOT NULL DEFAULT 'PASS' COMMENT 'PASS/FAIL/SKIP',
    error_msg   TEXT COMMENT '失败原因',
    run_time    DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间'
);

-- 场景2：建一张模拟业务表用于接口测试
CREATE TABLE IF NOT EXISTS test_orders (
    id          BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_no    VARCHAR(32) NOT NULL COMMENT '订单号',
    user_id     BIGINT NOT NULL COMMENT '用户ID',
    amount      DECIMAL(12,2) NOT NULL COMMENT '订单金额',
    status      TINYINT NOT NULL DEFAULT 0 COMMENT '0待支付 1已支付 2已取消',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_order_no (order_no)
);
```

【面试考察】
面试官："建表时你会设置哪些列属性？NOT NULL 和 DEFAULT 分别解决什么问题？"

参考回答框架：
1. NOT NULL：保证数据完整性，防止关键字段出现 NULL 导致查询和计算异常
2. DEFAULT：给列提供合理默认值，让插入操作更简洁，避免未赋值的列出现 NULL
3. AUTO_INCREMENT：自动生成唯一递增 ID，配合主键使用
4. PRIMARY KEY：唯一标识每行记录，InnoDB 必须要有主键
5. COMMENT：给表和列加注释，提高代码可读性（自己三个月后也能看懂）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 主键不设 AUTO_INCREMENT | 主键推荐自增，少数场景用 UUID（分布式系统） |
| 所有字段都允许 NULL | 关键业务字段（姓名、金额、手机号）设 NOT NULL |
| 忘了设 DEFAULT | 非必填字段设 DEFAULT，避免 NULL |
| 用 VARCHAR(65535) 导致建表失败 | 行最大 65535 字节，要考虑所有列的总和 |
| 建表不写 COMMENT | 注释是给自己和团队看的，省这几秒不值得 |
| ENGINE 选 MyISAM | 现代项目默认 InnoDB（支持事务、行级锁、外键） |

【扩展知识】
InnoDB 的行格式与溢出：

```sql
-- 查看表的行格式
SHOW TABLE STATUS WHERE Name = 'student';

-- 当一行数据超过页大小的一半时，VARCHAR/TEXT/BLOB 会"溢出"到额外页
-- 这就是为什么 VARCHAR(65535) 实际上可能建表失败
-- 因为行的大小 = 所有列大小 + VARCHAR长度前缀 + NULL标志位 ≤ 页大小的约一半
```

【我的理解】
> （用命令行完成以下操作：
> ① 创建一个 `practice_user` 表，包含字段：id（主键自增）、username（非空）、email（默认空字符串）、age（无符号）、created_at（默认当前时间）
> ② 用 `DESC practice_user;` 查看表结构 → 确认每个列的约束
> ③ 插入一条只给 username 的数据：`INSERT INTO practice_user (username) VALUES ('test');`
> ④ 查询：`SELECT * FROM practice_user;` → 看看其他列被填了什么值（这就是 DEFAULT 的作用）
> ⑤ 再插入一条不给 username 的数据 → 看看会发生什么（这就是 NOT NULL 的作用）
> ⑥ 最后 `DROP TABLE IF EXISTS practice_user;` 清理）

---

### 知识点 8：复制表 — CREATE TABLE ... LIKE

【课程原话/定义】
`CREATE TABLE ... LIKE` 可以复制一张表的**结构**（列定义、数据类型、索引、约束），但不复制数据。

```sql
-- 复制表结构（不含数据）
CREATE TABLE new_table LIKE old_table;

-- 完整示例
CREATE TABLE student_backup LIKE student;
-- student_backup 和 student 结构完全一致，但没有任何数据
```

如果需要复制结构 + 数据：

```sql
-- 方式1：LIKE + INSERT ... SELECT
CREATE TABLE student_copy LIKE student;
INSERT INTO student_copy SELECT * FROM student;

-- 方式2：CREATE TABLE ... AS SELECT（会丢失索引和约束）
CREATE TABLE student_copy2 AS SELECT * FROM student;
-- 注意：AS SELECT 不会复制 PRIMARY KEY、AUTO_INCREMENT、索引！
```

| 复制方式 | 结构 | 数据 | 主键 | 索引 | AUTO_INCREMENT |
|----------|------|------|------|------|---------------|
| `LIKE` | ✅ | ❌ | ✅ | ✅ | ✅ |
| `AS SELECT` | ✅ | ✅ | ❌ | ❌ | ❌ |
| `LIKE` + `INSERT SELECT` | ✅ | ✅ | ✅ | ✅ | ✅ |

【为什么？】
测试工程师最常用的场景：**快速搭建测试表**。你要测试一个复杂 SQL，需要一张和生产结构一模一样的表，但只想操作测试数据。

```sql
-- 典型测试工作流
-- 1. 复制生产表结构
CREATE TABLE user_test LIKE users;

-- 2. 只导必要数据
INSERT INTO user_test SELECT * FROM users WHERE id < 100;

-- 3. 在副本上随便测（增删改都不影响原表）
-- ...测试...

-- 4. 测完删除
DROP TABLE user_test;
```

`AS SELECT` 的坑：面试常考——它不复制索引和主键。如果你用 `AS SELECT` 复制表然后做 JOIN 查询，性能可能从毫秒级变成秒级（因为没有索引）。

【必须掌握】
- `CREATE TABLE 新表 LIKE 原表;` → 复制完整表结构（含主键、索引、约束），无数据
- `CREATE TABLE 新表 AS SELECT ...` → 复制结构 + 数据，但不复制索引
- 完整复制 = `LIKE + INSERT INTO ... SELECT`
- 测试中最常用 `LIKE`（数据结构对齐，数据自己造）

【企业场景】

| 场景 | 操作 |
|------|------|
| 搭建测试环境 | `CREATE TABLE test_users LIKE prod_users;` |
| 表结构迁移 | `CREATE TABLE new_users LIKE old_users;` + 加新字段 |
| 安全操作演练 | 先在副本上试 ALTER TABLE，确认无误再上生产 |
| 多环境同步 | 用 LIKE 确保测试/预发布表结构和生产一致 |

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 `AS SELECT` 复制了索引 | `AS SELECT` 不复制索引，用 `LIKE` 再 `INSERT` |
| 用 `LIKE` 后直接测 JOIN 查询很慢 | `LIKE` 已复制了索引，慢的话可能是数据量太大或统计信息过期 |
| 忘了是"空表"就做 SELECT | `LIKE` 只复制结构，先 `SELECT COUNT(*)` 确认有没有数据 |

【我的理解】
> （用之前创建的 `student` 表做实验：
> ① `CREATE TABLE student_like LIKE student;` → `DESC student_like;` → 确认结构一致
> ② `CREATE TABLE student_as AS SELECT * FROM student;` → `DESC student_as;` → 对比两者的区别
> ③ 哪张表有 PRIMARY KEY？哪张表有 AUTO_INCREMENT？用 `SHOW CREATE TABLE 表名;` 确认
> ④ 现在你能说清楚 `LIKE` 和 `AS SELECT` 的核心区别了吗？测试场景用哪个更多？）

---

### 知识点 9：SHOW TABLES / DESCRIBE — 查看表信息

【课程原话/定义】
知道有哪些表、表长什么样，是写 SQL 的前提。

```sql
-- 查看当前库的所有表
SHOW TABLES;

-- 查看表结构（3 种等价方式）
DESCRIBE student;
DESC student;
SHOW COLUMNS FROM student;

-- 查看完整的建表语句（含索引、约束、字符集）
SHOW CREATE TABLE student;
```

三种查表结构的方式对比：

| 命令 | 显示内容 | 详细程度 |
|------|---------|---------|
| `DESCRIBE student` | Field, Type, Null, Key, Default, Extra | 简要 |
| `SHOW COLUMNS FROM student` | 同上，结果集完全一样 | 简要 |
| `SHOW CREATE TABLE student` | 完整的 CREATE TABLE 语句 | 详细（含所有细节） |

DESCRIBE 输出解读：

```
+-------------+-----------------+------+-----+---------+----------------+
| Field       | Type            | Null | Key | Default | Extra          |
+-------------+-----------------+------+-----+---------+----------------+
| id          | int             | NO   | PRI | NULL    | auto_increment |
| name        | varchar(50)     | NO   |     | NULL    |                |
| gender      | char(1)         | NO   |     | M       |                |
| age         | tinyint unsigned| YES  |     | NULL    |                |
| score       | decimal(5,2)    | NO   |     | 0.00    |                |
| create_time | datetime        | YES  |     | NULL    |                |
+-------------+-----------------+------+-----+---------+----------------+
```

| 列名 | 含义 | 面试要点 |
|------|------|---------|
| Field | 字段名 | — |
| Type | 数据类型 | — |
| Null | 是否允许 NULL | YES = 允许 NULL，NO = NOT NULL |
| Key | 键类型 | PRI = 主键，UNI = 唯一键，MUL = 非唯一索引 |
| Default | 默认值 | NULL 表示没有设默认值（注意：允许 NULL 时默认值为 NULL） |
| Extra | 额外信息 | auto_increment、on update CURRENT_TIMESTAMP 等 |

【为什么？】
`SHOW CREATE TABLE` 是最诚实的——它显示的是表的"真实定义"，不是你以为的定义。当你的 INSERT 失败、查询结果不符合预期时，第一步永远是 `SHOW CREATE TABLE`。

```sql
-- 典型排障流程
-- 问题：为什么插入 score 字段总是 NULL？
INSERT INTO student (name) VALUES ('test');
SELECT * FROM student WHERE name = 'test';  -- score 是 NULL！

-- 排查：
SHOW CREATE TABLE student;
-- 发现：`score` decimal(5,2) DEFAULT NULL  ← 没设 DEFAULT！
-- 修复：
ALTER TABLE student MODIFY score DECIMAL(5,2) NOT NULL DEFAULT 0.00;
```

【必须掌握】
- `SHOW TABLES;` → 列出当前库的所有表
- `DESC 表名;` → 查看表的列定义
- `SHOW CREATE TABLE 表名;` → 查看完整建表语句
- 能读懂 DESCRIBE 输出的每一列含义
- 能区分 Key 列的 PRI（主键）、UNI（唯一键）、MUL（索引）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 忘了 USE 就 SHOW TABLES | 先 `SELECT DATABASE();` 确认在哪个库 |
| DESCRIBE 看到 DEFAULT NULL 以为没设默认值 | 区分：没说默认值 vs 默认值为 NULL |
| 只看 DESC 不看 SHOW CREATE TABLE | DESC 看不到索引详情和表级选项，排障看 CREATE TABLE |

【我的理解】
> （在命令行中完成以下操作：
> ① `SHOW TABLES;` → 看看你的库里有几张表
> ② `DESC student;` → 逐列读懂 Field/Type/Null/Key/Default/Extra
> ③ `SHOW CREATE TABLE student\G`（注意结尾是 `\G` 不是 `;`）→ `\G` 能让输出纵向排列，更易读
> ④ 用 `SHOW CREATE TABLE` 输出中的信息，回答：student 表用的是什么存储引擎？什么字符集？有什么索引？
> ⑤ 你能不查笔记，解释 Key 列中 PRI、UNI、MUL 分别是什么意思吗？）

---

### 知识点 10：ALTER TABLE — 修改表结构

【课程原话/定义】
`ALTER TABLE` 是 DDL 中功能最强的命令——可以增加列、修改列、删除列、重命名列。表创建后结构的任何变化都靠它。

```sql
-- 四种核心操作
ALTER TABLE 表名 ADD 列名 数据类型 [约束] [FIRST|AFTER 列名];       -- 增加列
ALTER TABLE 表名 MODIFY 列名 新数据类型 [约束];                    -- 修改列定义
ALTER TABLE 表名 CHANGE 旧列名 新列名 新数据类型 [约束];             -- 重命名列 + 修改
ALTER TABLE 表名 DROP [COLUMN] 列名;                              -- 删除列
```

---

#### 10.1 ADD — 增加列

```sql
-- 在最后添加一列
ALTER TABLE student ADD email VARCHAR(100);

-- 添加到指定位置
ALTER TABLE student ADD phone CHAR(11) AFTER name;     -- 在 name 列之后
ALTER TABLE student ADD is_deleted TINYINT DEFAULT 0 FIRST;  -- 在最前面

-- 同时添加多列
ALTER TABLE student
    ADD address VARCHAR(200) COMMENT '地址',
    ADD remark TEXT COMMENT '备注';
```

【为什么？】
业务需求变化 → 表结构要跟着变。比如产品经理说"用户表要加个性别字段"，你不能删表重建（数据丢了），只能 ALTER TABLE ADD。`AFTER` 和 `FIRST` 控制列顺序——虽然 SQL 标准不关心列顺序，但人类看表时有序更可读。

---

#### 10.2 MODIFY — 修改列定义

```sql
-- 修改列的数据类型和约束
ALTER TABLE student MODIFY age SMALLINT UNSIGNED;
ALTER TABLE student MODIFY name VARCHAR(100) NOT NULL COMMENT '学生姓名';
ALTER TABLE student MODIFY score DECIMAL(6,2) DEFAULT 0.00;
```

注意：MODIFY 不能改列名，只能改类型和约束。改列名用 CHANGE。

---

#### 10.3 CHANGE — 重命名列 + 修改定义

```sql
-- CHANGE 同时改了列名和类型
ALTER TABLE student CHANGE name student_name VARCHAR(100) NOT NULL COMMENT '学生姓名';

-- CHANGE 只改列名（不改类型也要写完整类型定义）
ALTER TABLE student CHANGE score total_score DECIMAL(5,2) NOT NULL DEFAULT 0.00;
```

CHANGE 的坑：即使你只想改列名，也必须把数据类型、约束全部重写一遍。

```sql
-- 只想把 name 改成 student_name → 必须重写完整定义
ALTER TABLE student CHANGE name student_name VARCHAR(50) NOT NULL;
--                                     ↑ 即使不改类型也要写！
```

MySQL 8.0 引入了更友好的语法：

```sql
-- MySQL 8.0+：只改列名用 RENAME COLUMN（不需要重写类型）
ALTER TABLE student RENAME COLUMN name TO student_name;
```

---

#### 10.4 DROP — 删除列

```sql
-- 删除列（危险：数据一并删除！）
ALTER TABLE student DROP remark;
ALTER TABLE student DROP COLUMN address;   -- COLUMN 关键字可省略
```

删除列会丢失该列的所有数据，不可恢复。生产环境删列前必须备份。

---

#### MODIFY vs CHANGE 对比总结

| 操作 | MODIFY | CHANGE |
|------|--------|--------|
| 改列名 | ❌ 不支持 | ✅ 必须用 CHANGE |
| 改数据类型 | ✅ | ✅ |
| 改约束 | ✅ | ✅ |
| 改列名+类型 | ❌ | ✅ |
| 语法简洁度 | 简洁（只写要改的） | 繁琐（必须写完整定义） |

【为什么？】
ALTER TABLE 是生产环境最危险的操作之一。为什么？

1. **元数据锁（MDL）**：ALTER TABLE 会锁表，期间所有读写阻塞
2. **表重建**：改数据类型可能触发全表重建，大表可能跑几小时
3. **不可回滚**：ALTER TABLE 是隐式提交的 DDL，不能放在事务里回滚

```sql
-- 生产环境修改表结构的安全流程
-- 1. 在测试环境先验证
-- 2. 用 pt-online-schema-change 或 gh-ost（在线 DDL 工具，不锁表）
-- 3. 在业务低峰期执行
-- 4. 执行前备份
```

【必须掌握】
- `ADD 列名 类型 [AFTER 列名]` → 增加列
- `MODIFY 列名 新类型 [约束]` → 修改列定义（不改列名）
- `CHANGE 旧列名 新列名 新类型 [约束]` → 改列名 + 改定义
- `DROP [COLUMN] 列名` → 删除列
- MODIFY 不改列名，CHANGE 可以改列名（但必须重写完整定义）
- MySQL 8.0+ 推荐用 `RENAME COLUMN` 只改列名

【企业场景】

```sql
-- 测试工程师用 ALTER TABLE 的场景

-- 场景1：临时加一个测试标记列
ALTER TABLE users ADD test_flag TINYINT DEFAULT 0 COMMENT '测试标记';

-- 场景2：测试过程中发现 VARCHAR 长度不够
ALTER TABLE users MODIFY username VARCHAR(100);

-- 场景3：测试数据清理（删除临时加的列）
ALTER TABLE users DROP test_flag;
```

【面试考察】
面试官："ALTER TABLE 的 MODIFY 和 CHANGE 有什么区别？什么时候用哪个？"

参考回答框架：
1. MODIFY 用于修改列的数据类型和约束，不能改列名
2. CHANGE 可以改列名 + 改类型，但必须重写完整定义
3. 只改类型用 MODIFY（语法简洁），改列名用 CHANGE 或 MySQL 8.0 的 RENAME COLUMN
4. 注意生产环境 ALTER TABLE 会锁表，大表需要特殊处理

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| MODIFY 时忘了写约束（之前有 NOT NULL 新 MODIFY 没写） | MODIFY 会覆盖全部定义，必须把所有约束都重写 |
| CHANGE 只想改列名但忘了写类型 | 语法是 `CHANGE 旧名 新名 类型` 三要素缺一不可 |
| 生产环境直接 ALTER TABLE | 大表用 pt-osc 或 gh-ost 在线 DDL 工具 |
| DROP COLUMN 后数据没了才意识到 | 删列前 SELECT 一遍确认数据量，做好备份 |

【扩展知识】
在线 DDL（Online DDL）—— MySQL 5.6+ 对部分 ALTER TABLE 操作支持不锁表：

```sql
-- 指定在线 DDL 算法
ALTER TABLE student ADD email VARCHAR(100), ALGORITHM=INPLACE, LOCK=NONE;
-- ALGORITHM=INPLACE：原地修改，不重建表（快）
-- ALGORITHM=COPY：复制整表（慢但兼容性好）
-- LOCK=NONE：不锁表，允许并发读写
```

但并非所有 ALTER TABLE 都支持在线 DDL——改数据类型通常需要 COPY。

【我的理解】
> （用之前创建的 `student` 表完成以下练习：
> ① 添加一列 `email VARCHAR(100)` 在 `age` 之后
> ② 用 MODIFY 把 `score` 的类型改为 `DECIMAL(6,2)`
> ③ 用 CHANGE 把 `name` 重命名为 `stu_name`（保留原有的 VARCHAR(50) NOT NULL）
> ④ 删除 `email` 列
> ⑤ 每做完一步都用 `DESC student;` 验证结果
> ⑥ 最后回忆：MODIFY 和 CHANGE 的区别是什么？如果只是改列名，MySQL 8.0 提供了什么更方便的语法？）

---

### 知识点 11：RENAME TABLE — 重命名表

【课程原话/定义】
重命名表有两种语法：

```sql
-- 方式1：ALTER TABLE ... RENAME TO
ALTER TABLE student RENAME TO student_info;

-- 方式2：RENAME TABLE ... TO
RENAME TABLE student TO student_info;

-- 同时重命名多张表
RENAME TABLE
    student TO student_info,
    teacher TO teacher_info,
    course TO course_info;
```

| 对比维度 | ALTER TABLE ... RENAME | RENAME TABLE ... TO |
|----------|----------------------|---------------------|
| 单表重命名 | ✅ | ✅ |
| 多表重命名 | ❌（需要多条语句） | ✅（一条语句原子操作） |
| 跨库移动 | ❌ | ✅ `RENAME TABLE db1.t1 TO db2.t1` |
| 原子性 | 单表 | 多表原子 |

【为什么？】
RENAME TABLE 的杀手级特性：**多表原子重命名**。如果两张表需要同时改名，用 RENAME TABLE 要么全成功，要么全失败——不会出现改了一张另一张没改的中间状态。

```sql
-- 原子操作：两张表同时改名，不会出现中间状态
RENAME TABLE
    old_users TO new_users,
    old_orders TO new_orders;
-- 要么两张都改成功，要么两张都不改
```

跨库移动表是另一个强大功能：

```sql
-- 把表从 db_test 移动到 db_prod（同服务器内）
-- 相当于 mv，不是 cp + rm
RENAME TABLE db_test.users TO db_prod.users;
```

【必须掌握】
- `ALTER TABLE 旧名 RENAME TO 新名;` — 单表重命名
- `RENAME TABLE 旧名 TO 新名;` — 单表/多表/跨库重命名
- RENAME TABLE 多表操作是原子的
- 可以跨数据库移动表（同 MySQL 实例内）

【企业场景】

| 场景 | 操作 |
|------|------|
| 表名规范化 | `RENAME TABLE usr TO users;` |
| 表归档 | `RENAME TABLE orders TO orders_2026_backup;` |
| 蓝绿部署 | `RENAME TABLE users TO users_old, users_new TO users;` |
| 表数据对调 | RENAME 交替改名 |

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 以为 ALTER TABLE RENAME 支持多表 | 多表必须用 RENAME TABLE |
| RENAME 后视图/存储过程失效 | 视图引用了旧表名，改名后要同步更新 |
| 跨库 RENAME 以为能跨服务器 | RENAME TABLE 只能同 MySQL 实例，跨服务器用 mysqldump |

【我的理解】
> （用 `student` 表做实验：
> ① `ALTER TABLE student RENAME TO stu;` → `SHOW TABLES;` → 确认改名成功
> ② `RENAME TABLE stu TO student;` → 改回原名
> ③ 两种语法哪种更简洁？如果要同时改 3 张表的名字，你会用哪种？）

---

### 知识点 12：DROP TABLE — 删除表

【课程原话/定义】
`DROP TABLE` 删除整张表——表结构 + 所有数据 + 所有索引 + 所有触发器，统统没了。

```sql
-- 安全删除
DROP TABLE IF EXISTS student;

-- 危险删除（表不存在会报错）
DROP TABLE student;

-- 同时删除多张表
DROP TABLE IF EXISTS student, teacher, course;
```

和 DROP DATABASE 一样，DROP TABLE 没有确认、没有回收站、不可回滚。

【为什么？】
为什么需要谨慎？

1. **不可恢复**：数据文件直接被删除，不像 Windows 有回收站
2. **隐式提交**：DROP 是 DDL，不能放在事务里 ROLLBACK
3. **级联影响**：如果有外键引用，默认会阻止删除（除非用 CASCADE）

```sql
-- 外键保护的例子
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE users;
-- ERROR 1217: Cannot delete or update a parent row: a foreign key constraint fails
-- 如果要强制删除：
DROP TABLE orders, users;  -- 先删子表再删父表，或先删外键
```

DROP TABLE vs DELETE vs TRUNCATE（面试必考）：

| 操作 | 分类 | 删除内容 | 能否回滚 | 重置自增 | 速度 |
|------|------|---------|---------|---------|------|
| `DROP TABLE` | DDL | 表结构 + 全部数据 | ❌ | — | 最快 |
| `TRUNCATE TABLE` | DDL | 全部数据，保留结构 | ❌ | ✅ | 快 |
| `DELETE FROM` | DML | 按条件删数据 | ✅ | ❌ | 慢（逐行删） |

```sql
-- 三者的区别演示
-- DELETE：删数据，保留结构，可回滚
START TRANSACTION;
DELETE FROM student WHERE id = 1;
ROLLBACK;  -- 数据恢复！

-- TRUNCATE：清空数据，重置自增，不可回滚
TRUNCATE TABLE student;  -- 所有数据没了，AUTO_INCREMENT 回到 1

-- DROP TABLE：表都没了
DROP TABLE student;  -- 结构和数据全没
```

【必须掌握】
- `DROP TABLE [IF EXISTS] 表名;`
- 删除的是整张表（结构 + 数据 + 索引），不可恢复
- IF EXISTS 让脚本可重复执行
- DROP / TRUNCATE / DELETE 三者的区别是面试必考

【企业场景】

| 场景 | 操作 |
|------|------|
| 自动化测试清理 | `DROP TABLE IF EXISTS test_users;` |
| 临时表用完就删 | `DROP TABLE IF EXISTS tmp_result;` |
| 重置测试环境 | `DROP TABLE IF EXISTS ...;` + 重新 `CREATE TABLE` |
| 不希望保留历史数据 | 用 TRUNCATE（清空数据但保留表结构） |

```sql
-- 测试环境重置脚本
DROP TABLE IF EXISTS test_orders;
DROP TABLE IF EXISTS test_users;

CREATE TABLE test_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE test_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL
);
```

【面试考察】
面试官："DROP TABLE、TRUNCATE TABLE、DELETE FROM 有什么区别？"

参考回答框架：
1. DROP TABLE 是 DDL，删除整张表（结构+数据+索引），不可回滚，最快
2. TRUNCATE TABLE 是 DDL，清空表中所有数据但保留表结构，不可回滚，重置 AUTO_INCREMENT
3. DELETE FROM 是 DML，按条件删除数据，可回滚，不重置自增，最慢（逐行删+写日志）
4. 测试环境清理：用 DROP+CREATE 或 TRUNCATE；生产中删数据：用 DELETE（可回滚）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `DROP TABLE` 不加 `IF EXISTS` | 自动化脚本必须加 |
| 以为 TRUNCATE 能回滚 | TRUNCATE 是 DDL，隐式提交，不能 ROLLBACK |
| 用 DELETE 删全表数据 | 清空全表用 TRUNCATE，比 DELETE 快得多 |
| 忘记外键约束导致 DROP 失败 | 先 `SHOW CREATE TABLE` 看外键，或先删子表再删父表 |

【我的理解】
> （在你的测试库里完成以下实验：
> ① 用 `CREATE TABLE test_drop (id INT);` 建一张临时表
> ② 插入一行数据 `INSERT INTO test_drop VALUES (1);`
> ③ `DROP TABLE test_drop;` → `SHOW TABLES;` → 表还存在吗？
> ④ 重建表，插入数据 → 用 `DELETE FROM test_drop;` 删除数据 → `SHOW CREATE TABLE test_drop;` → 表还在吗？AUTO_INCREMENT 重置了吗？
> ⑤ 再插入数据 → 用 `TRUNCATE TABLE test_drop;` → 表还在吗？如果再插入，AUTO_INCREMENT 从头开始了吗？
> ⑥ 现在你能完整说出 DROP / TRUNCATE / DELETE 三者的区别了吗？）

---

## 今日课程总结

| 模块 | 知识点 | 核心内容 | 面试权重 |
|------|--------|---------|----------|
| 数据库操作 | CREATE DATABASE | 完整语法、IF NOT EXISTS、CHARACTER SET | ★★★★★ |
| 数据库操作 | SHOW / USE | 查看切换、SHOW CREATE DATABASE | ★★★☆☆ |
| 数据库操作 | ALTER DATABASE | 修改字符集、注意不影响已有表 | ★★★☆☆ |
| 数据库操作 | DROP DATABASE | IF EXISTS、4个系统库不能删 | ★★★★★ |
| 数据库操作 | 命名规则 | 64字符、小写+下划线、不用关键字 | ★★★★☆ |
| 数据类型 | 整数类型 | TINYINT~BIGINT、UNSIGNED、空间换选择 | ★★★★☆ |
| 数据类型 | 浮点/定点 | FLOAT/DOUBLE 近似、DECIMAL 精确（金额） | ★★★★★ |
| 数据类型 | 字符串类型 | CHAR vs VARCHAR、TEXT 系列限制 | ★★★★★ |
| 数据类型 | 日期时间 | DATETIME vs TIMESTAMP、自动更新 | ★★★★★ |
| 表操作 | CREATE TABLE | 所有列属性：NOT NULL/DEFAULT/AUTO_INCREMENT/PRIMARY KEY/COMMENT | ★★★★★ |
| 表操作 | LIKE 复制 | 复制结构不含数据、vs AS SELECT 的区别 | ★★★★☆ |
| 表操作 | SHOW/DESC | SHOW TABLES、DESCRIBE、SHOW CREATE TABLE | ★★★★☆ |
| 表操作 | ALTER TABLE | ADD/MODIFY/CHANGE/DROP、MODIFY vs CHANGE | ★★★★★ |
| 表操作 | RENAME TABLE | 单表/多表/跨库、原子性 | ★★★☆☆ |
| 表操作 | DROP TABLE | IF EXISTS、DROP vs TRUNCATE vs DELETE | ★★★★★ |

---

## 本章核心面试题速查

### Q1：CREATE DATABASE 写一条完整的建库语句，包含字符集设置。
```sql
CREATE DATABASE IF NOT EXISTS myapp
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

### Q2：CHAR 和 VARCHAR 的区别？
- CHAR：定长，未满补空格，快但浪费空间，适合固定长度字段（手机号 CHAR(11)）
- VARCHAR：变长，按实际存储，省空间但略慢，适合可变长字段（用户名）

### Q3：DATETIME 和 TIMESTAMP 的区别？
- DATETIME：范围 1000-9999，无时区，8字节，适合固定日期
- TIMESTAMP：范围 1970-2038，有时区（存UTC），4字节，支持自动更新，适合记录时间

### Q4：金额用什么数据类型？为什么？
- DECIMAL(M,D)，不能用 FLOAT/DOUBLE
- FLOAT/DOUBLE 是近似值，二进制无法精确表示十进制小数
- 99.99 存 FLOAT 可能变成 99.989997863...

### Q5：DROP / TRUNCATE / DELETE 三者的区别？
- DROP TABLE (DDL)：删表结构+数据，不可回滚，最快
- TRUNCATE TABLE (DDL)：清空数据保留结构，不可回滚，重置自增
- DELETE FROM (DML)：按条件删数据，可回滚，不重置自增，最慢

### Q6：ALTER TABLE 的 MODIFY 和 CHANGE 的区别？
- MODIFY：修改列的数据类型和约束，不能改列名
- CHANGE：修改列名+数据类型+约束，即使只改列名也必须重写完整类型定义

### Q7：CREATE TABLE ... LIKE 和 AS SELECT 的区别？
- LIKE：完整复制表结构（主键、索引、约束），不含数据
- AS SELECT：复制结构+数据，但不复制主键、索引、AUTO_INCREMENT

### Q8：MySQL 有哪些系统数据库？哪些绝对不能删？
- mysql（用户权限）、information_schema（元数据）、performance_schema（性能）、sys（诊断）
- 四个都不能删，尤其是 mysql（删了 MySQL 无法启动）

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-MySQL基础与SQL入门]] — SQL 四大分类 DDL/DML/DQL/DCL、Workbench 建表操作、SQL 通用语法
- [[../接口测试/Ch03-请求与响应处理]] — 接口测试后查数据库验证数据落库
