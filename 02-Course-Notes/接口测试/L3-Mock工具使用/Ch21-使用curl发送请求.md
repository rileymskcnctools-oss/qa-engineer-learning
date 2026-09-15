---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch21-使用curl发送请求"
created: 2026-09-15
status: draft
---

# Ch21 - 使用 curl 发送请求

## 课程来源
- 学习日期：

---

## 一、cURL 与 Chrome DevTools

### 知识点 1：cURL 简介与 Chrome DevTools

【课程原话/定义】
cURL 是一个通过 URL 传输数据的、功能强大的命令行工具。它可以与 Chrome DevTools 配合，把浏览器发送的真实请求还原出来（附带认证信息），脱离浏览器执行，方便重放请求、修改参数调试、编写脚本。也可单独使用，根据自己的需求构造请求、调整参数，构造多种接口测试场景。

Chrome DevTools 是内嵌在 Chrome 里的网页调试工具，测试中常作为简单抓包工具（Network 面板查看请求详情）。

【为什么？**
为什么要用 curl？因为它是"命令行里的 Postman"——不依赖 GUI，可以写进脚本、进 CI、在服务器上跑（服务器没有浏览器和 Postman）。而"浏览器 Copy as cURL"是它的杀手锏：你在浏览器里看到一个请求，右键 Copy as cURL，就能得到一个"带完整认证信息（cookie/token/header）"的等价命令，直接在命令行重放，这是排查"为什么接口调不通"的最快手段。

【必须掌握】
- cURL 是命令行 URL 传输工具，可构造请求、重放、调试
- 配合 Chrome DevTools：右键请求 → Copy → Copy as cURL，还原真实请求
- 价值：脱离浏览器/Postman，可在服务器、脚本、CI 中执行
- Network 面板是简单抓包工具，看请求 URL/头/参数/响应

【企业场景】
你在公司服务器上（无浏览器）排查一个接口问题，或者写自动化脚本要重放某个请求，用 curl 就行。最常用的是：浏览器 F12 找到请求 → Copy as cURL → 粘到服务器命令行跑，得到一个带完整认证头的可复现命令。这比手动拼请求快得多、也准得多。

【面试考察】
面试官："怎么把一个浏览器里的请求快速变成命令行可复现的命令？"

参考回答框架：
1. 浏览器 F12 → Network → 右键请求 → Copy → Copy as cURL
2. 得到带完整 header/cookie/token 的 curl 命令
3. 在命令行/bash 里粘贴执行即可重放
4. 可加 -v 看详细日志，或改参数做调试

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 手动拼请求漏了认证头 | Copy as cURL 自动带全认证信息 |
| curl 只能在本地跑 | 服务器、脚本、CI 都能跑，这是它比 GUI 工具强的地方 |
| Copy as cURL 得到的是"另一种语言" | 就是标准 curl 命令，可直接在 bash 执行 |

【我的理解】
> （为什么说 curl 是"命令行里的 Postman"？它在服务器/CI 场景下相比 Postman 有什么不可替代的优势？）

---

## 二、cURL 常用命令与参数

### 知识点 2：cURL 常用命令与参数

【课程原话/定义】
常用命令：
- GET：`curl "https://httpbin.testing-studio.com/get" -H "accept: application/json"`
- POST：`curl -X POST "https://httpbin.testing-studio.com/post" -H "accept: application/json"`
- 代理：`curl -x 'http://127.0.0.1:8080' "https://httpbin.testing-studio.com/get"`

常用参数：
| 参数 | 含义 |
|------|------|
| -H | 消息头设置 |
| -u | 用户认证 |
| -d | 请求体数据 |
| --data-urlencode | 对内容进行 url 编码 |
| -G | 把 data 数据当成 get |
| -o | 写文件 |
| -x | http 代理、socks5 代理 |
| -v | 打印更详细日志 |
| -s | 关闭提示输出 |
| --help | 查看帮助 |

【为什么？**
为什么 curl 的参数要记？因为 curl 是"拼装 HTTP 请求的命令行"——每个参数对应 HTTP 请求的一个组成：`-H` 是 header、`-d` 是 body、`-u` 是认证、`-x` 是代理、`-X` 是 method。理解参数 = 理解 HTTP 请求结构在命令行的映射。尤其 `-v`（详细日志，能看请求头/响应头/三次握手）和 `-x`（代理，配合 Charles 抓包）是测试最常用的两个。

【必须掌握】
- `-H` 设置请求头，`-d` 传 body，`-X` 指定 method，`-u` 认证
- `-x` 走代理（配合 Charles 抓包），`-v` 打印详细日志
- `-G` 把 data 当 GET 参数，`-o` 写文件
- GET/POST 基本语法 + 走代理抓包

【企业场景】
你在公司用 curl 调试接口：`curl -v -x http://127.0.0.1:8888 https://api.xxx.com/get` 走 Charles 代理抓包并看详细日志；`curl -H "Content-Type: application/json" -d '{"a":1}' -X POST ...` 发 JSON POST；`curl -u user:pass ...` 带认证。这些组合覆盖了日常 90% 的接口调试场景。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| -d 和 -G 搞混 | -d 是 body（POST），-G 把 data 当 GET 参数 |
| 发 JSON 不加 Content-Type 头 | 服务端按默认格式解析，可能 415 |
| 忘了 -v 就不知道问题在哪 | -v 打印请求/响应详情，是排错关键 |

【我的理解】
> （`-H`、`-d`、`-X`、`-u`、`-x` 分别对应 HTTP 请求的哪一部分？用 curl 拼一个"带 JSON body + 认证 + 走代理"的 POST 请求。）

---

### 知识点 3：cURL 实战演练

【课程原话/定义】
实战演练：
1. **篡改请求头**：`curl -H "User-Agent:testing-studio" "http://www.baidu.com" -v`（把 UA 改为 testing-studio）
2. **企业微信创建标签（POST）**：`curl -H "Content-Type: application/json" -X POST --data '{"tagname":"hogwarts","tagid":13}' https://qyapi.weixin.qq.com/cgi-bin/tag/create?access_token=$token`
3. **认证上传（PUT）**：`curl -X PUT "$ES_HOST/$index/_doc/$id?pretty" --user username:password -H 'Content-Type: application/json' -d "$content"`

【为什么？**
这三个实战覆盖了 curl 的三大典型用法：① 篡改请求头（模拟不同客户端，测试 UA 相关逻辑）；② 发 POST 带 JSON body + token（企业微信这类开放平台 API 的典型调用）；③ 带认证的 PUT（ElasticSearch 这类需要 basic auth 的服务）。理解这三个场景，你就掌握了 curl 在"构造请求 + 带认证 + 改头"上的完整能力，能应付绝大多数接口调试。

【必须掌握】
- 改 UA：`-H "User-Agent:xxx"` 模拟不同客户端
- 发 JSON POST：`-H "Content-Type: application/json" -X POST -d '...'`
- 带 token：URL 里 `?access_token=$token` 或 `-H "Authorization: ..."`
- 认证：`--user username:password`（basic auth）
- 上传/写：`-X PUT` + `-d "$content"`

【企业场景】
你在公司测开放平台接口（企业微信/ES 等），用 curl 快速验证：改 UA 测兼容性、带 token 调企业微信 API、带 basic auth 写 ES。这些都不用开 Postman，直接命令行一条命令搞定，还能写进脚本批量跑。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| JSON body 里的引号不转义 | shell 里要用单引号包 JSON，避免引号冲突 |
| token 写死在命令里 | 用变量 `$token` 引用，避免泄露/过期 |
| basic auth 用 -H 手拼 | 直接用 `--user user:pass` 更简洁 |

【我的理解】
> （这三个实战分别演示了 curl 的哪些能力？如果让你"带 token 调一个 POST 接口并走代理抓包"，命令怎么拼？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| cURL 简介 | 命令行 URL 工具 + Copy as cURL | ★★★☆☆ |
| 常用参数 | -H/-d/-X/-u/-x/-v | ★★★★☆ |
| 实战 | 改 UA/JSON POST/认证 PUT | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch16-常用代理工具与代理模式]]
- [[Ch22-抓包分析TCP协议]]
