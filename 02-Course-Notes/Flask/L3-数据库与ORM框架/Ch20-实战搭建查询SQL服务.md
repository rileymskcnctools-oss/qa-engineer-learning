---
tags: [课程笔记, Flask, ORM, 实战]
course: "Flask"
chapter: "Ch20-实战搭建查询SQL服务"
created: 2026-09-17
status: in_progress
---

# Ch19 - 【实战】搭建查询 SQL 服务

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 test_platform_backend/flask/L3

---

## 一、为测试解决数据库权限问题

### 知识点 1：SQL 解析 + 接口封装的查询服务

【课程原话/定义】
测试过程中，很多测试没有直接查询数据库的权限（公司权限管理严格）。这是"可测性不足"，需要提供测试钩子（testing hook，为测试增加的接口，显示系统内部状态）。

解决思路：通过接口封装，既解决权限问题，又满足测试需求。

实现思路：
1. **解析 SQL 语句**：解析 SQL 字符串，提取表名和 WHERE 条件
2. **执行 SQL 操作**：判断表是否支持查询，执行查询
3. **路由层**：提供 /query 接口，接收 SQL，返回结果

```python
def parse_query(sql_query):
    parsed = sqlparse.parse(sql_query)[0]
    if parsed.get_type() == "SELECT":       # 只允许 SELECT
        table_name = token_list[6].value    # 提取表名
        conditions = ...                    # 提取 WHERE 条件
        return table_name, conditions
    else:
        raise ValueError("只支持查询操作！！！")

@app.route('/query', methods=['POST'])
def sql_query():
    data = request.json
    sql_query = data.get('sql')
    table_name, conditions = parse_query(sql_query)
    results = execute_sqlalchemy_query(session, table_name, conditions)
    return jsonify(result_list)
```

安全限制的核心：只允许 SELECT、只允许查询白名单表（supported_tables）、解析 SQL 判断是否执行，避免恶意注入/删除。

【为什么？】
为什么测试要"搭查询 SQL 服务"？因为测试查库是高频需求（验证数据落库），但公司不给测试直接连库的权限。这个服务的本质是"用接口包装数据库查询"——测试通过 /query 接口提交 SQL，服务端解析、校验、执行，返回结果。这引用了《Google 测试之道》的"可测性"思想：系统可测性不足时，要新增"测试钩子"（testing hook）来暴露内部状态。而"只允许 SELECT + 白名单表"的安全限制，是为了在"开放查询能力"和"保护数据安全"之间取得平衡——既让测试能查，又防止误删/注入。

【必须掌握】
- 可测性不足 → 提供测试钩子（查询接口）
- SQL 解析：sqlparse 库解析 SQL，判断 SELECT、提取表名/条件
- 安全限制：只允许 SELECT、白名单表、防注入
- 接口封装：/query 接收 SQL，返回结果
- 本质：用接口包装数据库查询，解决权限问题

【企业场景】
你在公司测试环境，没有数据库查询权限，但验证"新增用户是否落库"需要查库。于是搭一个查询 SQL 服务：你 POST 一个 SELECT 到 /query，服务端解析后只查白名单表，返回结果。既让你能查数据，又通过"只读 + 白名单"保护了数据库安全。

【面试考察】
面试官：「测试没有数据库权限怎么办？什么是测试钩子？」

参考回答框架：
1. 这是可测性不足，需提供测试钩子（testing hook）
2. 搭查询 SQL 服务：接口封装数据库查询
3. 安全限制：只允许 SELECT + 白名单表
4. 既解决权限，又保护数据安全

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 接口不限制 SQL 类型 | 要只允许 SELECT，防 DELETE/注入 |
| 不设白名单表 | 要限制只能查指定表，防查敏感表 |
| 直接给测试数据库权限 | 公司安全不允许，用接口包装更安全 |

【扩展知识】
《Google 测试之道》的"可测性"是测试工程师的进阶概念：一个系统"好不好测"是设计出来的，不是测出来的。当系统缺少可测试接口时，测试要推动开发"新增测试钩子"。查询 SQL 服务就是"测试钩子"的一个实例——它不是为了业务，而是为了测试而增加的接口。

【我的理解】
> （为什么"用接口包装查询"比"直接给测试数据库权限"更安全？接口这一层能加哪些安全控制，是直接连库做不到的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 查询 SQL 服务 | SQL 解析 + 接口封装 + 安全限制 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch18-实战课程管理平台后端开发]]
- [[Ch15-数据CRUD]]
