---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch09-Postman基础使用"
created: 2026-09-15
status: draft
---

# Ch09 - Postman 基础使用

## 课程来源
- 学习日期：

---

## 一、Postman 是什么

### 知识点 1：Postman 简介与优势

【课程原话/定义】
Postman 是一款流行的 API 测试工具和开发环境，旨在简化 API 开发过程、测试和文档编制。它提供一套功能强大的工具，帮助开发人员更轻松地构建、测试和调试 Web 服务。

Postman 的优势：
- 可以快速构建请求、保存以后再使用
- 提供响应结果的**比较功能**（断言），可以写测试用例，根据 pass/fail 判断是否通过
- 可以把测试用例放在**测试集中批量运行**，方便业务场景测试和回归
- 通过**环境变量**，同一套用例切换不同环境（生产/测试/正式）即可测试

【为什么？】
为什么 Postman 能成为接口测试的"标配工具"？因为它把接口测试的完整流程——构建请求、保存、断言、批量回归、多环境切换——都集成在了一个图形界面里。你不用写代码就能完成"发请求→看响应→写断言→批量跑"，这对测试人员（尤其不熟编程的）极其友好。而"集合（Collection）+ 环境变量"又让它能沉淀成可复用的测试资产。

【必须掌握】
- Postman 是 API 测试 + 开发辅助工具
- 四大优势：快速构建/保存请求、断言（pass/fail）、集合批量运行、环境变量切环境
- 核心概念：Request（请求）、Collection（测试集）、Environment（环境）、Test（断言脚本）

【企业场景】
你在公司日常接口调试：拿到一个接口，先在 Postman 里构建好请求（方法、URL、参数、header）并保存到 Collection，写好断言（断言状态码 200、字段正确），以后每次回归点一下 Run 就跑完。换测试环境时，只改环境变量的 `baseURL`，同一套用例直接复用。这就是 Postman 在工作中的典型用法。

【面试考察】
面试官："你用 Postman 做接口测试的流程是怎样的？"

参考回答框架：
1. 构建请求（方法/URL/参数/header/body）
2. 发送并查看响应（状态码/响应头/响应体）
3. 写断言（Tests 脚本）校验预期
4. 保存到 Collection，多接口组成测试集
5. 用环境变量管理多环境，切换后批量运行

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Postman 只能用来"手动调接口" | 还能写断言、批量运行、数据驱动、做 mock、做监控 |
| Postman 的断言是"自动生成的" | 断言需要自己在 Tests 里写（或用预置模板），不是点一下就有的 |
| Collection 只是"接口的文件夹" | Collection 支持变量、鉴权、前置/断言脚本，是测试资产单位 |

【我的理解】
> （Postman 的"集合 + 环境变量"为什么能让接口测试"一次编写、多环境复用"？如果不分离环境变量，切换环境会遇到什么麻烦？）

---

### 知识点 2：Postman 应用场景

【课程原话/定义】
应用场景：API 测试、自动化测试、性能测试、监控和断言、集成测试、协作与分享、Mock 服务器、环境管理、数据驱动测试。

【为什么？】
为什么要了解 Postman 的"应用场景边界"？因为 Postman 不是万能的——它适合快速调试、接口自动化、轻量回归和团队协作，但不适合做重度性能压测（那是 JMeter/Locust 的活）。知道它"能干什么、不能干什么"，才能选对工具，也不会在面试里把 Postman 吹过头。

【必须掌握】
- 核心场景：API 测试、接口自动化、集成测试、数据驱动
- 辅助场景：Mock 服务器、环境管理、监控断言、团队协作分享
- Postman 能做"轻量性能测试"（Runner 循环），但重度压测建议 JMeter/Locust
- 数据驱动：通过 CSV/JSON 文件批量注入测试数据

【企业场景】
你在公司的分工里：日常接口调试用 Postman，接口自动化用 pytest（代码更灵活、能进 CI），但 Postman 的 Collection 会导出给开发做联调参考；需要模拟还没开发好的第三方接口时，用 Postman 的 Mock Server 顶替。这就是"Postman 和代码自动化各有分工"的现实。

【面试考察】
面试官："Postman 和 pytest/requests 做接口自动化，你选哪个？"

参考回答框架：
1. Postman：上手快、可视化、适合快速调试和轻量回归
2. pytest/requests：可编程、易维护、易集成 CI、适合长期自动化
3. 结论：调试用 Postman，长期自动化用代码（pytest），两者配合使用

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 用 Postman 做大规模压测 | Postman 只能轻量循环，压测用 JMeter/Locust |
| Postman 自动化能完全替代代码 | 代码自动化更灵活（循环/断言/数据构造/CI），Postman 适合轻量场景 |
| Mock Server 是"造假接口返回" | 是模拟外部依赖的接口，用于前后端解耦并行开发 |

【我的理解】
> （为什么说"调试用 Postman、长期自动化用 pytest"？代码自动化比 Postman 多了哪些 Postman 做不到的事？）

---

## 二、Postman 安装与界面

### 知识点 3：Postman 安装与页面介绍

【课程原话/定义】
Postman 安装：进入官网 https://www.postman.com/ 选择系统下载安装。

页面介绍：
- **顶部栏**：Home（登录注册）、Workspaces（工作区，会员功能）、Reports（报告，付费）、Explore、搜索框、系统设置
- **左侧栏**：Collections（测试集）、APIs（创建 API）、Environments（环境管理）、Mock Servers、Monitors、History（历史）
- **右侧栏**：顶部环境信息、请求配置区域、响应查看区域

【为什么？】
为什么要熟悉界面布局？因为 Postman 的三大区域（请求配置、环境、响应查看）对应接口测试的"输入→环境→输出"三段。左侧栏的 Collections/Environments 是"资产区"（保存的用例和环境），右侧是"工作区"（当前正在操作的请求）。分清这两个区域，就不会在"哪里保存用例、哪里切环境"上迷路。

【必须掌握】
- 左侧 Collections：管理测试集（保存的接口用例）
- 左侧 Environments：管理环境变量
- 右侧：当前请求的配置区（方法/URL/参数/header/body）+ 响应区
- History：历史请求记录，可快速找回之前的请求
- 顶部搜索框：快速检索集合/请求

【企业场景】
你打开 Postman 的第一件事是：确认右上角选对了环境（开发/测试/生产），然后在左侧 Collections 找到对应模块的接口，右侧改参数、发请求、看响应。熟记这三个区域，能让你的操作不迷路、不发错环境（发错生产环境是事故）。

【面试考察】
面试官："Postman 里 Collection 和 Environment 分别是干什么的？"

参考回答框架：
1. Collection：测试集，存放一组接口请求（可加变量、脚本、鉴权）
2. Environment：环境，存放环境变量（如 baseURL、token）
3. 配合：Collection 里的请求用 `{{变量}}` 引用环境变量，切环境即切值
4. 用途：同一套用例多环境复用

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 把请求保存在 History 里 | History 只是历史记录，应保存到 Collection |
| 环境变量和集合变量混淆 | Environment 是跨集合的环境配置，Collection 变量只在该集合生效 |
| 忘记切环境直接发请求 | 可能把测试请求打到生产环境，是严重事故 |

【我的理解】
> （为什么"发请求前先确认环境"这么重要？如果你在 Postman 里选错环境，把一条删除请求发到了生产环境，会发生什么？）

---

## 三、Postman 基本使用

### 知识点 4：发送 GET 请求

【课程原话/定义】
发送 GET 请求的步骤（以 httpbin.ceshiren.com 为例）：
1. 选择 GET 请求方式
2. URL 填写 `https://httpbin.ceshiren.com/get`
3. 点击 Header，key 填 `accept`，value 填 `application/json`
4. 点击 Send，查看返回内容

【为什么？】
GET 请求的参数放在 URL 里（Params），Postman 的 Params 和 URL 是**双向同步**的——你在 Params 里填参数，会自动拼到 URL；你在 URL 里写带参数的地址，也会自动拆到 Params。理解这一点，能让你快速构造带参请求而不出错。

【必须掌握】
- GET 请求：方法选 GET，参数在 Params（对应 URL 的查询字符串）
- Params 与 URL 双向同步
- Header 用于添加请求头（如 accept: application/json）
- 发送后下方展示响应（状态码/响应头/响应体）

【企业场景】
你测试一个查询接口，在 Postman 里选 GET，URL 填接口地址，在 Params 里加 `status=available`，Send 后看返回的列表。要改查询条件时，直接在 Params 里改 value 再 Send。这比每次手拼 URL 高效得多，也少出错（特殊字符会被自动转义）。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| GET 参数写在 Body 里 | GET 参数应放 Params（URL 查询串），放 Body 无效 |
| 手动拼 URL 而不填 Params | 特殊字符（中文、空格）需转义，用 Params 可自动处理 |
| 忘记加必要的请求头 | 有些接口要求 accept/Content-Type，缺失会返回 406/415 |

【我的理解】
> （在 Postman 里往 Params 加一个参数，URL 会发生什么变化？反过来在 URL 里加参数，Params 又怎么变？这说明了什么？）

---

### 知识点 5：发送 POST 请求（form / JSON / 文件）

【课程原话/定义】
发送 POST 请求，请求体（Body）有四种设置方式：form-data、x-www-form-urlencoded、raw、binary。
- **form-data**：既可以上传键值对，也可以上传文件
- **x-www-form-urlencoded**：表单数据转换为键值对
- **raw**：上传任意格式文本（Text、JSON、XML、HTML 等）
- **binary**：只上传二进制数据，通常用于上传文件

POST 实战（httpbin.ceshiren.com/post）：
- FORM 格式：Body → form-data，key/value 键值对
- JSON 格式：Body → raw → JSON，如 `{"json_key1":"json_value1",...}`
- 文件格式：Body → form-data → File，选择本地文件上传

【为什么？】
为什么 POST 有四种 body 格式？因为它们对应不同的 Content-Type，服务端按 Content-Type 来解析请求体。form-data 用于"表单 + 文件上传"（multipart/form-data），x-www-form-urlencoded 用于纯表单（application/x-www-form-urlencoded），raw 用于 JSON/XML/文本（application/json 等），binary 用于纯二进制。**选错 body 格式，服务端就解析不出你的参数**，这是 Postman 新手最常见的坑。

【必须掌握】
- form-data：键值对 + 文件上传（multipart/form-data）
- x-www-form-urlencoded：纯表单键值对（application/x-www-form-urlencoded）
- raw：任意文本，JSON 最常用（需手动选 JSON 类型）
- binary：纯二进制文件
- JSON 请求要在 raw 里写合法的 JSON，并选 JSON 类型

【企业场景】
你在公司发 POST 请求时先看接口文档要求什么 Content-Type：登录接口要求 `application/json`，就在 raw 里写 JSON；上传头像的接口要求 `multipart/form-data`，就用 form-data 选 File。如果 body 格式和 Content-Type 对不上，服务端会返回 400/415，这是你排查"为什么参数没传过去"的第一方向。

【面试考察】
面试官："form-data 和 x-www-form-urlencoded 有什么区别？"

参考回答框架：
1. form-data：multipart/form-data，可传文件 + 键值对，每个字段独立分隔
2. x-www-form-urlencoded：application/x-www-form-urlencoded，纯键值对，`&` 连接、URL 编码
3. 上传文件用 form-data；纯文本表单可用 urlencoded
4. raw + JSON 用于 RESTful 接口（application/json）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 传 JSON 却选 form-data | 服务端按 form 解析，JSON 字符串变成乱码/字段丢失 |
| raw 里写 JSON 但没选 JSON 类型 | Content-Type 不对，服务端可能解析失败 |
| 上传文件用 x-www-form-urlencoded | 该格式不能传文件，必须用 form-data（或 binary） |

【我的理解】
> （为什么"body 格式"和"Content-Type"必须匹配？如果你用 form-data 发 JSON 字符串，服务端实际收到的是什么？）

---

### 知识点 6：接口响应解析

【课程原话/定义】
接口响应由三部分组成：状态行（协议版本 + 状态码 + 状态解释）、响应头、响应报文（服务端返回的业务数据）。

Postman 响应区的查看方式：
- **Body**：Pretty（按类型高亮 + 自动换行）、Raw（无高亮）、Preview（预览）、Visualize（脚本图形化）
- **Cookies**：服务端返回的 cookie 单独展示
- **Headers**：以 key-value 展示响应头，鼠标停留显示说明
- **Tests**：Tests 中断言脚本的执行结果
- **Status**：响应状态码 + 状态说明（如 200 OK）
- **Time**：服务端响应耗时
- **Size**：响应数据大小（拆分为 body 和 headers）
- **Save Response**：下载响应 body 到本地文件

【为什么？】
为什么要学会"读懂响应"？因为接口测试的本质就是"校验响应"。状态码告诉你请求成没成功，响应头告诉你数据格式和大小，响应体告诉你业务数据对不对。Postman 把这些信息分栏展示，就是让你能快速定位"问题出在哪一层"——是状态码不对（4xx/5xx）、还是数据字段不对（响应体）。

【必须掌握】
- 状态行：协议版本 + 状态码 + 状态描述
- 响应头：Content-Type、Content-Length 等元信息
- 响应体：业务数据（JSON/HTML/XML）
- Pretty 适合读 JSON（高亮 + 换行），Raw 看原始格式
- Time 看耗时，Size 看大小（可用于轻量性能观察）

【企业场景】
你发完请求，先看 Status 是不是 200，再看 Body（Pretty 模式）里的 JSON 字段对不对，需要时点 Headers 看 Content-Type 是不是 application/json。排查接口慢时，看 Time 字段是不是异常（比如某个接口从 50ms 变成 2s），排查返回体积大时看 Size。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 只看状态码 200 就认为接口正常 | 还要看响应体字段是否正确（业务可能返回 code!=0） |
| Pretty/Raw 内容"不一样"以为出 bug | 两者是同一数据的不同展示方式，Pretty 只做了格式化 |
| 分不清响应头和响应体 | 头是元信息（描述数据），体是实际业务数据 |

【我的理解】
> （一个接口返回 200，但 Body 里 JSON 的 `code` 字段是 500，这代表什么？为什么"状态码 200"不等于"业务成功"？）

---

### 知识点 7：HTTP 头信息（请求头）

【课程原话/定义】
添加请求头：手动添加 `My-Header: Harry`，Send 后可在响应中看到。
修改请求头：把 User-Agent 默认值改掉（如改为 `hogwarts`），需要先取消勾选默认头，再自定义 key。

【为什么？】
为什么要会改请求头？因为很多接口行为由请求头决定：User-Agent（服务端据此判断客户端类型，做兼容或反爬）、Cookie（登录态）、Content-Type（请求体格式）、Authorization（鉴权 token）。测试时经常需要伪造或修改这些头，来模拟不同客户端、切换登录态、绕过某些限制。

【必须掌握】
- 添加请求头：Headers 里加 key-value
- 修改默认头（如 User-Agent）：取消勾选原值，重新定义
- 常用请求头：User-Agent、Cookie、Content-Type、Authorization、Accept
- 修改 User-Agent 可模拟不同客户端（浏览器/App/爬虫）

【企业场景】
你在公司测一个"只允许 App 访问"的接口，直接发请求可能被拒，这时把 User-Agent 改成 App 的值就能通过；测"需要登录"的接口，把登录后拿到的 token/Cookie 填到请求头里就能访问。改请求头是你做"前置鉴权 + 客户端模拟"的基本功。

【面试考察】
面试官："接口测试中，请求头里的 Cookie 和 Token 分别干什么用？"

参考回答框架：
1. Cookie：服务端下发的会话标识，浏览器自动携带，用于维持登录态
2. Token：鉴权凭证，通常放 Authorization 头，无状态验证
3. 测试时：手动获取 token/Cookie 填入请求头，才能访问受保护接口
4. 区别：Cookie 依赖浏览器/会话，Token 更适合无状态 API

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 改 User-Agent 但没取消勾选默认值 | 默认值仍生效，自定义值不生效 |
| 把 token 放错位置 | token 通常在 Authorization 头（Bearer xxx），不是随便一个头 |
| 混淆 Cookie 和 Token | Cookie 是会话标识（有状态），Token 是无状态鉴权凭证 |

【我的理解】
> （为什么"模拟不同客户端"要改 User-Agent？服务端是怎么根据 User-Agent 判断"你是谁"的？这样做在测试里有什么用？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Postman 简介 | API 测试工具；构建/断言/集合/环境变量四大优势 | ★★★☆☆ |
| 应用场景 | API 测试/自动化/数据驱动/Mock/协作；压测不擅长 | ★★★☆☆ |
| 界面布局 | 左侧资产区（Collections/Environments）+ 右侧工作区 | ★★☆☆☆ |
| GET 请求 | 参数在 Params，与 URL 双向同步 | ★★★☆☆ |
| POST 请求 | 四种 body：form-data/urlencoded/raw/binary | ★★★★★ |
| 响应解析 | 状态行/响应头/响应体；Pretty/Raw/Status/Time/Size | ★★★☆☆ |
| 请求头 | 添加/修改头；User-Agent/Cookie/Token | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch08-接口测试用例设计]]
- [[Ch10-Postman实战练习]]
