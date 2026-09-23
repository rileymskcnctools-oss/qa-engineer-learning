---
tags: [课程笔记, 性能测试]
course: "性能测试"
chapter: "Ch29-HTTP信息头管理器"
created: 2026-09-23
status: draft
---

# Ch29 - HTTP信息头管理器

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L1-JMeter常用组件（站点：性能测试工具 / L1.JMeter 常用组件）
- 站点页：性能测试工具 / L1.JMeter 常用组件 → HTTP信息头管理器
- 前置：[[../L1-性能测试体系/Ch01-性能测试介绍与压力曲线模型|L1 Ch01-性能测试介绍与压力曲线模型]]

> 本章对应课程站点「HTTP信息头管理器」页：自定义请求头、用用户定义变量做 token、View Results Tree 验证。本章属于配置元件，其**作用范围**与**执行顺序**见 [[Ch22-JMeter常用配置元件剖析]]。

---

### 知识点1：HTTP Header Manager（HTTP 信息头管理器）

【课程原话/定义】
HTTP Header Manager 是 JMeter 中的一个组件，用于管理 HTTP 请求的头部信息。在使用 JMeter 进行性能测试时，经常需要模拟不同的请求头，以便测试服务器的响应。通过 HTTP Header Manager，可以自定义 HTTP 请求的头部信息，例如 `User-Agent`、`Content-Type`、`Accept`、`Token` 等。这样可以模拟不同类型的请求，比如模拟浏览器的请求、模拟移动应用的请求等，以更好地模拟实际用户的行为。

课程案例（加分演示"用用户定义变量做请求头"）：
- 前提：在 **Test plan** 中添加用户定义的变量 `token=123456`
- 步骤一：在测试计划中添加线程组，在线程组中添加 HTTP Request、HTTP Header Manager 和 View Results Tree（以请求百度首页为例）
- 步骤二：在 HTTP Header Manager 中添加 token 字段，使用用户定义的变量（引用形式 `${token}`）
- 步骤三：在 View Results Tree 中查看结果——设置的 token 被添加在请求头中

【为什么？】
请求头是服务端**识别调用方**的依据，它决定了你压到的到底是哪一条链路：
1. `Content-Type` 决定服务端用什么解析器读你的请求体——`application/json` 与 `application/x-www-form-urlencoded` 会走完全不同的代码分支；
2. `User-Agent` 常被网关/WAF 用来做风控与限流策略（模拟 App 与模拟浏览器，遇到的限流阈值可能不同）；
3. `Token`/鉴权头决定"这条请求是否有权限执行业务"——**不带鉴权头的压测，压的是 401 分支，不是业务分支**。

用"用户定义的变量 + `${token}`"而不是写死值，是为了让同一个 Header Manager 能被参数化替换（切环境、切账号、配合 CSV 多用户）——这是配置元件与变量机制配合的典型用法。

【必须掌握】

| 配置项 | 说明 |
|--------|------|
| 名称 / 值 | 逐行添加请求头；值支持变量引用（`${token}`、`${__threadNum}` 等） |
| 与请求同名头的关系 | 若某个 HTTP Request 自己写了同名请求头，以请求内的为准（元件粒度更细的生效）——建议统一在 Manager 里维护，避免两处打架（【扩展知识】） |
| 常见必备头 | `Content-Type`（JSON/表单）、`Accept`、`User-Agent`、鉴权头（`token`/`Authorization`） |
| 变量来源 | Test Plan 的"用户定义的变量"、CSV Data Set Config、前置处理器/后置处理器生成的变量 |
| 变量名大小写 | 变量名大小写敏感（`${token}` 与 `${Token}` 是两个变量）（【扩展知识】） |

【企业场景】
你压的是移动端接口，服务端网关对 `User-Agent` 做了灰度策略：只有携带 `App/8.2.0` 的请求才会路由到新服务。如果你用 JMeter 默认的 `Apache-HttpClient` UA 直接压，请求全被路由到老服务——**你花一天压出来的曲线是上一代系统的容量**。所以企业里的标准动作是：抓一次真机请求（Charles/Fiddler 或浏览器 F12），把关键请求头拷进 HTTP Header Manager，再加鉴权头变量，确保 JMeter 发出去的请求和真实客户端"长得一样"。

【面试考察】
面试官："JMeter 里怎么统一给所有请求加请求头？值要动态变化怎么办？"

参考回答框架：
1. 元件：HTTP Header Manager 放在需要生效的层级（线程组下 = 组内所有请求生效）
2. 逐行添加键值对；值支持变量与函数引用
3. 动态化：Test Plan 里定义用户定义的变量（课程案例：`token=123456`），Manager 里写 `${token}`；更动态的场景用 CSV Data Set Config 或后置处理器提取（如登录后提取 token）
4. 排查：用 View Results Tree 的 Request 面板确认头部真的带上了，不要凭配置界面猜

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 变量名写错 / 大小写不一致 | `${token}` 引用了未定义或名字不同的变量时，JMeter 会**原样发送字符串**（如发出去的就是 `token: ${token}`），不报错，极易漏过；必须看 View Results Tree 的 Request 头 |
| 请求内又写了一遍同名头 | 两处都配时容易互相覆盖，排查时先确认哪一处生效；统一在一处维护最省事 |
| 忘记 Content-Type | 服务端按表单解析 JSON 请求体 → 参数全为空 → 业务失败但 HTTP 200，属于典型的"假成功" |
| 所有线程共用一个写死的 token | 前端场景里 token 与用户绑定；多用户压测要靠 CSV 或登录后提取动态生成（配合后置处理器） |
| 只在 Test Plan 层配了变量却不检查是否被覆盖 | 同名变量在更细作用域（如线程组）定义时会覆盖上层；变量是"就近覆盖"语义（【扩展知识】） |

【我的理解】引导题（用自己的话回答）：
1. 课程案例里为什么要在 Test Plan 里定义变量 `token=123456`，而不是直接在 Header Manager 里写 `123456`？
2. 如果压测跑了 10 分钟，第 3 分钟开始请求头里的 token 因为过期而失效，你的报告里会看到什么现象？怎么才能尽早发现？

> 本章属于配置元件：作用范围（层级决定生效范围）与执行顺序（作用域开始处、取样器之前生效）见 [[Ch22-JMeter常用配置元件剖析]]。

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| HTTP Header Manager 作用 | 统一管理请求头（`Content-Type` / `Accept` / `User-Agent` / 鉴权头） | ★★★★★ |
| 用用户定义变量做 token | Test Plan 定义 `token=123456` → Manager 里写 `${token}`（课程案例） | ★★★★★ |
| View Results Tree 验证 | 在结果树的 Request 面板确认请求头真的带上了 | ★★★★☆ |
| 变量与同名头冲突 | 变量名大小写敏感；请求内同名头与 Manager 冲突时以更细粒度为准 | ★★★★☆ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】HTTP 信息头管理器：添加元件步骤 + token 变量请求头配置 + 请求头结果（原文共 5 张）

## 关联笔记

- [[Ch22-JMeter常用配置元件剖析]]（作用范围与执行顺序、Cache Manager、CSV Data Set Config）
- [[Ch28-HTTPcookie设置]]（同页拆出的另一章：Cookie Manager 与自定义 Cookie）
- [[Ch21-JMeter断言元件的使用]]
- [[Ch27-HTTP请求属性设置]]（POST JSON 必须显式声明 `Content-Type`）
- [[Ch31-监听器与测试结果]]（用 Request 面板验证头部是否真的带上）
- [[../L1-性能测试体系/Ch04-行业流行性能压测工具介绍|L1 Ch04-行业流行性能压测工具介绍]]
- [[../../接口自动化测试/L2-接口请求构造与响应断言/Ch13-cookie处理|接口自动化 Ch13-cookie处理]]
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
