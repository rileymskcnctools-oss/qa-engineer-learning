---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch10-Postman实战练习"
created: 2026-09-15
status: draft
---

# Ch10 - Postman 实战练习

## 课程来源
- 学习日期：

---

## 一、接口文档分析（Swagger）

### 知识点 1：Swagger 接口文档

【课程原话/定义】
宠物商店接口文档：https://petstore.swagger.io
Swagger 是一个用于**生成、描述和调用 RESTful 接口**的 Web 服务。通俗讲：Swagger 把项目中所有想暴露的接口展现在页面上，并且可以进行接口调用和测试。

现在大部分项目都使用 Swagger，因为后端开发不需要专门为接口使用者编写接口文档——接口更新后，只需修改代码中的 Swagger 描述即可实时生成新文档，避免接口文档老旧不能使用的问题。通过 Swagger 页面可以直接调用接口，降低调试成本。

【为什么？】
为什么 Swagger 取代了手写接口文档？因为传统接口文档是"人写的"，代码一改文档就过期，前后端经常因为"文档和实际不一致"扯皮。Swagger 的文档是"代码生成的"——后端在代码里加注解（如 @ApiOperation），Swagger 自动扫描生成页面，代码改了文档自动更新，**文档永远和代码一致**。这解决了接口文档最大的痛点：失真。

【必须掌握】
- Swagger 是 RESTful 接口的"文档生成 + 在线调试"工具
- 文档由代码注解自动生成，代码更新文档实时同步
- 页面可直接"Try it out"调用接口，无需额外工具
- 接口文档页面能看到：请求方法、参数、响应格式、Curl 命令

【企业场景】
你在公司要测一个新接口，第一件事是找它的 Swagger 地址（一般是 `/swagger-ui.html` 或 `/doc.html`）。打开后能看到这个服务的所有接口、每个接口的参数说明和返回示例，还能直接点"Try it out"在线调一下，快速搞清楚接口的输入输出，再据此设计用例。有了 Swagger，你不再依赖开发"口头描述接口"。

【面试考察】
面试官："你们项目用什么管理接口文档？Swagger 有什么好处？"

参考回答框架：
1. 用 Swagger（或 Knife4j/Postman 文档）管理接口文档
2. 好处一：文档由代码注解自动生成，不会和实现脱节
3. 好处二：页面可在线调试接口，降低前后端联调成本
4. 好处三：接口变更实时同步，避免文档过期

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Swagger 是"测试工具" | 它是文档生成 + 在线调试工具，不是专门的测试工具 |
| 手写接口文档和 Swagger 一样 | Swagger 文档由代码生成，永远和代码一致；手写文档会过期 |
| 有 Swagger 就不用测试了 | Swagger 只方便调试，不能替代系统性的接口测试 |

【我的理解】
> （为什么"代码生成的文档"比"手写的文档"更可靠？手写接口文档最常见的坑是什么？）

---

### 知识点 2：Swagger 页面调试接口（Try it out）

【课程原话/定义】
以查询宠物接口为例，在 Swagger 页面上调试：
- 点击 **Try it out**
- 请求参数 status 选择 available
- 点击 **Execute** 发出请求
- 下方展示：当前请求的 **Curl 命令**、完整 **URL**、**响应状态码和响应体**

有了 Swagger，就能方便地获取接口信息，据此设计测试用例。

【为什么？】
为什么要会"在 Swagger 上调试"？因为它是你"读懂接口"最快的方式：Try it out 让你不用写代码、不用开 Postman 就能发请求看结果，而且它直接给出**等价的 Curl 命令**——你可以把 Curl 复制到 Postman（Import）或命令行，快速复现。掌握这个流程，你就打通了"看文档 → 调接口 → 设计用例"的完整链路。

【必须掌握】
- Try it out → 填参数 → Execute → 看响应
- Swagger 会展示：Curl 命令、完整 URL、响应状态码、响应体
- Curl 命令可导入 Postman（Import），快速还原请求
- 调试得到的信息（方法/参数/返回结构）是设计用例的依据

【企业场景】
你拿到宠物商店的 Swagger 地址，先找到"查询宠物"接口（GET /pet/findByStatus），点 Try it out，选 status=available，Execute，看到返回一堆宠物 JSON。你把返回结构记下来（每个宠物有 id、name、status 等字段），再据此设计断言：断言返回的 status 都是 available、返回是数组且非空。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 只会看文档，不会点 Try it out 调试 | Try it out 能快速验证接口真实行为，比只看描述可靠 |
| 忽略 Swagger 给的 Curl 命令 | Curl 可导入 Postman 复用，是"从文档到工具"的桥 |
| 不记录返回结构就设计用例 | 返回结构（字段/类型）是写断言的前提 |

【我的理解】
> （Swagger 页面上的"Try it out"和你在 Postman 里发请求，本质是不是一回事？Swagger 给出的 Curl 命令有什么用？）

---

## 二、接口测试用例设计

### 知识点 3：宠物增删改查冒烟测试用例设计

【课程原话/定义】
宠物商店接口的增删改查冒烟测试用例：
- **查询宠物**：GET /pet/findByStatus，参数 status（available/pending/sold）
- **新增宠物**：POST /pet，body 传 JSON（含 id、category、name、photoUrls、tags、status），id 具有唯一性需要修改
- **更新宠物**：PUT /pet，body 传 JSON（改 name 等字段）
- **删除宠物**：DELETE /pet/{petId}，id 跟在 URL 中

新增宠物请求体示例：
```json
{
  "id": 9223372000001083222,
  "category": {"id": 1, "name": "cat"},
  "name": "miao",
  "photoUrls": ["string"],
  "tags": [{"id": 5, "name": "cute"}],
  "status": "available"
}
```

【为什么？】
为什么冒烟用例是"增删改查"四条？因为这四个操作覆盖了 RESTful 的四个核心动词（POST=增、GET=查、PUT=改、DELETE=删），是最小完备的冒烟集。跑通它们，就证明这个服务的 CRUD 基本能力正常，可以进入详细测试。注意"新增宠物 id 要改"——因为 id 唯一，重复提交会冲突，这是排重逻辑的体现（对应 [[Ch08-接口测试用例设计]] 知识点 5）。

【必须掌握】
- 冒烟四用例：查（GET findByStatus）、增（POST）、改（PUT）、删（DELETE）
- 新增/更新的 body 是 JSON，放 raw
- 删除的 id 直接拼在 URL（路径参数），如 /pet/{petId}
- 新增宠物的 id 要保证唯一，否则冲突

【企业场景】
你在公司对一个新服务做冒烟：先查（能不能查到数据）→ 增（能不能创建）→ 改（能不能更新刚创建的）→ 删（能不能删掉）。这条"增-改-删"的链路是有依赖的——删的 id 来自增返回的 id。设计冒烟用例时，要保证用例之间的数据依赖能串起来（这正是后面"变量关联"要解决的）。

【面试考察】
面试官："给你一个宠物商店接口，怎么设计冒烟测试用例？"

参考回答框架：
1. 覆盖 CRUD 四个核心操作
2. 查：GET findByStatus + status 参数
3. 增：POST + JSON body（id 唯一）
4. 改：PUT + JSON body（改 name）
5. 删：DELETE + 路径参数 id
6. 注意数据依赖：删的 id 来自增返回的 id

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 新增宠物 id 用固定值重复提交 | id 唯一，重复提交会冲突，需每次修改 |
| 删除接口把 id 放 body 里 | 该接口 id 是路径参数（/pet/{id}），不是 body |
| 冒烟只测查询不测增改删 | 冒烟要覆盖 CRUD 全链路，才能证明服务基本可用 |

【我的理解】
> （为什么"新增宠物"的 id 需要每次修改？如果两次新增用同一个 id，会发生什么？这和 Ch08 的"排重逻辑"有什么关系？）

---

## 三、编写断言与运行测试集

### 知识点 4：编写断言（Tests）

【课程原话/定义】
Tests 主要做断言：断言就是**结果和预期对比**——一致则用例通过（PASS），不一致则失败（FAIL）。Tests 里用 JavaScript 脚本写断言，Postman 预置了常用断言模板。

常用断言：
1. **验证响应状态码**：`pm.test("响应状态码为 200", function () { pm.response.to.have.status(200); });`
2. **检查响应体含某字符串**：`pm.expect(pm.response.text()).to.include("doggie");`
3. **JSON 某值等于预期**：`var jsonData = pm.response.json(); pm.expect(jsonData[0].name).to.eql("doggie");`
4. **响应体与某字符串完全相同**：`pm.response.to.have.body("response_body_string");`
5. **响应头存在某字段**：`pm.response.to.have.header("Content-Type");`
6. **响应时间小于某值**：`pm.expect(pm.response.responseTime).to.be.below(200);`

【为什么？】
为什么要用断言而不是"肉眼看响应"？因为肉眼看只能判断一两次，断言让判断**自动化、可重复、可批量**。Postman 的断言基于 `pm`（Postman API）对象，`pm.test(名称, 函数)` 定义一个测试，`pm.response` 提供响应数据，`pm.expect(...).to.xxx()` 是断言语法（Chai 风格）。理解了 `pm` 这几个核心对象，就能自己写断言。

【必须掌握】
- 断言 = 预期 vs 实际，一致 PASS、不一致 FAIL
- `pm.test(name, fn)` 定义一条断言；`pm.response` 访问响应
- 状态码断言：`pm.response.to.have.status(200)`
- 字符串包含：`pm.expect(pm.response.text()).to.include("x")`
- JSON 取值：`pm.response.json()` 后取字段，`.to.eql(期望值)`
- 响应头断言：`pm.response.to.have.header("Content-Type")`
- 响应时间断言：`pm.expect(pm.response.responseTime).to.be.below(200)`

【企业场景】
你在公司写接口用例，每一条都配断言，而不是手动看结果：状态码 200、业务 code==0、返回的 name 字段等于预期值、关键字段存在。断言写好保存进 Collection，以后回归点 Run，几秒钟就能看到哪些接口 PASS、哪些 FAIL，不用再逐个人工核对响应体。

【面试考察】
面试官："Postman 的断言怎么写？常用的有哪几种？"

参考回答框架：
1. 在 Tests 里用 JavaScript 写，基于 pm 对象
2. `pm.test(name, function)` 定义测试用例
3. 常用：状态码（status）、响应体包含字符串（include）、JSON 字段值（eql）、响应头存在（header）、响应时间（below）
4. 断言本质是"预期 vs 实际"的自动化比较

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 断言写在 Pre-request Script 里 | 断言应写在 Tests 里（请求后执行），Pre-request 是请求前脚本 |
| `jsonData[0].name` 取不到 | 先确认返回是数组还是对象，索引/字段要对应 |
| 全量断言用 have.body 太脆 | 响应体有动态字段（时间戳等）时，全量断言会误报，宜用字段断言 |

【我的理解】
> （`pm.response.text()` 和 `pm.response.json()` 有什么区别？为什么断言 JSON 字段要用 `.json()` 而不是 `.text()`？）

---

### 知识点 5：创建测试集并运行

【课程原话/定义】
创建测试集（Collection）：左侧 Collections 点 `+` 新建 collection（命名"宠物商店"），可在 collection 内再建 folder（命名"宠物"）分层管理。

把接口请求存到 collection：命名（查询宠物/新增宠物/更新宠物/删除宠物）、设置方法、URL、参数、body、Tests 断言。

运行测试集：点击 folder 或 collection 的 **Run** → 进入执行页面 → 选择集合、环境变量、执行次数、延迟时间、测试数据 → 点 Run 执行 → 进入结果页查看通过/失败。

【为什么？】
为什么要把接口存进 Collection 再 Run，而不是一个个点 Send？因为 Collection 是"可批量、可回归、可复用的测试资产"。单个 Send 是"调试"，Collection Run 是"测试执行"——它能一次性跑完所有用例、统计通过率、支持数据驱动（导入 CSV）。这就是"手动调试"和"自动化回归"的分水岭。

【必须掌握】
- Collection 可分层（folder 分组），如"宠物商店/宠物"
- 每个请求存：命名 + 方法 + URL + 参数/body + Tests
- Run：选集合、环境、执行次数、延迟、测试数据（CSV）
- 结果页：查看每个请求的 PASS/FAIL + 统计

【企业场景】
你在公司把接口用例按模块存成 Collection（用户模块、订单模块...），跑回归时选对应 Collection 点 Run，几十条用例一次跑完，结果页直接看出哪条挂了、为什么挂（响应内容）。新版本发版前，这一套 Collection Run 就是你的接口回归手段。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 请求存在 History 不存 Collection | 存 Collection 才能批量运行、回归、分享 |
| Run 时选错环境 | 环境选错会请求到错误的后端（甚至生产） |
| 不写断言就 Run | 没有断言，Run 结果全是"发送成功"，测不出正确性 |

【我的理解】
> （"单个 Send"和"Collection Run"的本质区别是什么？为什么说 Collection Run 才算是"接口自动化回归"？）

---

### 知识点 6：Postman 变量（作用域与优先级）

【课程原话/定义】
Postman 变量主要用于**参数化和关联**，按作用域分为：
- **Local**：脚本中定义的变量，只在当前脚本生效
- **Global**：全局变量，所有接口可调用
- **Collection**：测试集变量，该集合内接口使用
- **Environment**：环境变量，用于切换不同环境（如 test/stage）
- **Data**：测试集导入的外部数据（数据驱动）

变量优先级（重名时从高到低）：**Data → Environment → Collection → Global → Local**。

使用方式：`{{变量名}}`，Postman 解析时替换为对应值。

【为什么？】
为什么要分这么多作用域？因为不同变量服务于不同目的：
- Global 存"到处都要用的"（如 token）
- Collection 存"这个集合专用的"（如 petId）
- Environment 存"随环境变的"（如 baseURL）
- Data 存"每次执行要变的测试数据"（数据驱动）

优先级保证"局部覆盖全局"——比如同名的 `status`，Data 里传的值优先于 Environment。理解优先级，才能在变量重名时搞清楚"到底用的哪个值"。

【必须掌握】
- 变量用途：参数化（复用值）+ 关联（接口间传值，如增返回 id 给删用）
- 五种作用域：Local / Global / Collection / Environment / Data
- 优先级（高→低）：Data → Environment → Collection → Global → Local
- 引用：`{{变量名}}`
- 脚本设置/获取：`pm.globals.set/get`、`pm.environment.set/get`、`pm.collectionVariables.get`

【企业场景】
你在公司测宠物商店：baseURL 放 Environment（切 test/stage 环境）；petId 放 Collection 变量（新增接口返回后 set，删改接口 get 复用）；token 放 Global（所有接口都要）。关联场景：新增宠物返回的 id 存进 Collection 变量，删除接口的 URL 用 `{{petId}}` 引用，实现"增-删"数据联动。

【面试考察】
面试官："Postman 变量有哪几种作用域？优先级是怎样的？"

参考回答框架：
1. 五种：Local、Global、Collection、Environment、Data
2. 优先级（高→低）：Data → Environment → Collection → Global → Local
3. 用途：Environment 切环境、Global 存通用值、Collection 存集合专用值、Data 做数据驱动
4. 参数化和关联：`{{变量}}` 引用；接口间通过 set/get 传值

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 把"优先级"记反 | 是 Data 最高、Local 最低（局部覆盖全局） |
| 环境变量和集合变量混用 | Environment 跨集合、随环境切；Collection 只在该集合内生效 |
| 变量赋值只在 Tests 里做 | Pre-request Script 里也能 set 变量（请求前设置） |

【扩展知识】
Environment 的典型用法：创建 test 和 stage 两个环境，都定义 `baseURL` 但值不同（`https://petstore.swagger.io/v2` vs 测试环境地址）。请求 URL 用 `{{baseURL}}/pet`，只需在右上角切换环境，同一套用例就能测不同后端。这是"一套用例、多环境复用"的核心实践。

【我的理解】
> （如果 Global 里 `status=sold`，Environment 里 `status=available`，请求里用 `{{status}}`，最终发出去的是哪个值？为什么？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Swagger 文档 | 代码生成文档，Try it out 在线调试，可复制 Curl | ★★★☆☆ |
| 冒烟用例设计 | 宠物 CRUD 四用例，id 唯一、数据依赖 | ★★★★☆ |
| 断言编写 | pm.test + 状态码/字符串/JSON/header/响应时间 | ★★★★★ |
| 测试集运行 | Collection 分层 + Run 批量执行 + 结果统计 | ★★★☆☆ |
| 变量与作用域 | 五种作用域 + 优先级 + 参数化关联 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch08-接口测试用例设计]]
- [[Ch09-Postman基础使用]]
