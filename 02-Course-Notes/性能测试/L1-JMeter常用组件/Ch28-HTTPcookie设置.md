---
tags: [课程笔记, 性能测试]
course: "性能测试"
chapter: "Ch28-HTTPcookie设置"
created: 2026-09-23
status: draft
---

# Ch28 - HTTPcookie设置

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L1-JMeter常用组件（站点：性能测试工具 / L1.JMeter 常用组件）
- 站点页：性能测试工具 / L1.JMeter 常用组件 → HTTPcookie设置
- 前置：[[../L1-性能测试体系/Ch01-性能测试介绍与压力曲线模型|L1 Ch01-性能测试介绍与压力曲线模型]]

> 本章对应课程站点「HTTPcookie设置」页：HTTP Cookie Manager 参数、Cookie 格式（Cookie Policy）、自定义 Cookie 实战。本章属于配置元件，其**作用范围**与**执行顺序**见 [[Ch22-JMeter常用配置元件剖析]]。

---

### 知识点1：HTTP Cookie Manager 与 Cookie 设置

【课程原话/定义】
在 JMeter 中，HTTP Cookie Manager 是一个非常常用的元件，用于管理 HTTP 请求中的 Cookie，模拟浏览器行为，使用户会话得以保持。它能够处理服务器发送的 Cookie，并在后续请求中自动携带这些 Cookie；在实际的 Web 测试中，Cookie 是用于跟踪用户会话和存储用户信息的一种重要机制，因此正确管理 Cookie 对于模拟真实用户行为至关重要。

**参数配置（课程原文）**：

| 选项 | 含义（课程原文） |
|------|------------------|
| 每次反复清除 Cookies？（Clear cookies each iteration?） | 每次迭代时，都将 Cookies 清空 |
| Use Thread Group configuration to control cookie clearing | 用户线程组去配置清空 Cookie |
| Cookie 格式 standard | 标准格式 |
| Cookie 格式 standard-strict | 严格格式 |
| Cookie 格式 ignoreCookies | 此规格忽略所有 Cookie。被用来防止 HttpClient 接受和发送的 Cookie |
| Cookie 格式 netscape | 最原始的 Cookies 规范，同时也是 RFC2109 的基础；仍与 RFC2109 有很多重要差异，可能需要特定服务器才兼容 |
| Cookie 格式 default | 默认 |
| Cookie 格式 rfc2109 | HttpClient 使用的默认 Cookies 协议 |
| Cookie 格式 rfc2965 | 定义版本 2，尝试弥补版本 1 中 rfc2109 标准的缺点 |
| Cookie 格式 compatibility | **推荐选择**：兼容性设计，适应尽可能多的不同服务器；不是完全按标准实现；遇到解析 Cookie 的问题时可能就要用到这个规范 |
| 存储在 Cookie 管理器中的 Cookie（User-Defined Cookies） | 自定义 Cookie，可以手动添加 |

**课程案例**：以给百度首页请求添加 cookie 信息为例。
1. 步骤一：测试计划中添加线程组，线程组中添加 HTTP Request、HTTP Cookie Manager 和 View Results Tree
2. 步骤二：在 HTTP Cookie Manager 中配置添加自定义的 cookie
3. 步骤三：View Results Tree 中查看——自定义的 cookie 被添加在请求的 **Cookie Data** 中

【为什么？】
Cookie 是**会话的物理载体**：服务端在响应里 `Set-Cookie`，客户端下次请求带 `Cookie` 回来，服务端才知道"你是刚才登录的那个人"。JMeter 不启用 Cookie Manager 时不做这件事，于是会出现压测里最隐蔽的一类失真：
1. **链路断裂**：登录接口拿到会话，但后续请求不带会话 → 每个请求都在"未登录"分支被拒 → RT 极短、TPS 极高；
2. **服务端压力性质变化**：没有会话复用，服务端要为每个请求创建新会话，会话存储（Redis/内存）压力被无限放大，压出来的瓶颈在"会话创建"上，而线上真实瓶颈可能在业务逻辑上。

"Cookie 格式（Cookie Policy）"这一组选项存在的意义是**兼容性**：不同服务端发 Cookie 时遵循的规范不同（老的 netscape 规范、RFC2109、RFC2965），严格实现有时反而解析不了；所以课程与官方都推荐用最"宽容"的 `compatibility`。而"每次迭代清空 Cookie"则用来区分两种用户模型：**每次迭代清空 = 每次都是新访客（测冷启动/缓存未命中）；不清空 = 同一用户连续操作（测真实会话链路）**。

【必须掌握】

| 场景 | Clear cookies each iteration | Cookie 格式 | 说明 |
|------|------------------------------|-------------|------|
| 模拟"新用户"访问（缓存冷启动、注册/首访流程） | 勾选 | compatibility | 每次迭代重置会话 |
| 模拟"同一用户连续操作"（登录→下单） | 不勾选 | compatibility | 会话在迭代间保持（默认） |
| 由线程组统一控制 | 勾选 Use Thread Group configuration to control cookie clearing | compatibility | 交给线程组配置决定（【扩展知识】：与线程组的"每次迭代使用同一用户"语义对应） |
| 排查 Cookie 解析问题 | 保持默认 | 从 compatibility 逐步尝试 standard / rfc2109 | 解析不到 Cookie 时优先怀疑 policy 与格式 |
| 需要固定 Cookie 值 | — | compatibility | 用 User-Defined Cookies 手动添加键值对 |

【企业场景】
你在压一个"多步业务流程"：登录 → 查商品 → 加购物车 → 下单。企业做法是：**线程组下挂一个 HTTP Cookie Manager，Cookie 格式选 compatibility，不勾"每次迭代清空"**，让同一个线程在多次迭代中保持同一会话（模拟真实用户连续操作）；同时用 CSV 让每个线程用不同账号，这样"线程数 = 并发用户数"才成立。如果压的是"详情页缓存效果"，你反而要勾上"每次迭代清空 Cookie"，让请求更像首次访问（无 Cookie 时缓存与登录态处理的路径不同）。**同一个脚本因为这一个勾选，测的是两件完全不同的事——这就是它必须写进测试计划评审的原因。**

【面试考察】
面试官："JMeter 里怎么保持登录态？Cookie Manager 的 Cookie 格式怎么选？"

参考回答框架：
1. 保持登录态的两种方式：HTTP Cookie Manager 自动管理（推荐）；或后置处理器提取 token/Cookie 再手动加到 Header Manager
2. Cookie Manager 的机制：接收 `Set-Cookie` → 保存 → 后续同作用域请求自动带 `Cookie` 头（可在 View Results Tree 的 Cookie Data 里验证）
3. Cookie Policy 选 compatibility（推荐）：兼容性最好，遇到解析问题再尝试其他规范
4. "每次迭代清空 Cookie"决定用户模型：清空 = 每次新用户；不清空 = 同一用户连续操作；也可交给线程组统一控制

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 以为加了 Cookie Manager 就一定保持登录 | 只有当登录响应确实 `Set-Cookie` 且后续请求在**同一作用域**内时才自动带出；用 View Results Tree 的 Cookie Data 验证，不要假设 |
| Cookie 格式选得过严（standard-strict） | 严格模式在真实服务端上常解析失败，课程与官方都推荐 compatibility |
| 混淆"清空 Cookie"与"清空变量" | Clear cookies each iteration 只清 Cookie；变量（如 CSV 读到的用户名）不受它影响 |
| 把自定义 Cookie 用来做鉴权主通道 | User-Defined Cookies 是固定键值，适合稳定的会话标识/测试标记；真正的登录态应交给自动管理或提取后动态传递 |
| 全链路脚本忘了 Cookie Manager，靠"看起来对"交付 | 错误率可能仍是 0（因为服务端返回 200 + 未登录提示），错误率指标会掩盖整段数据作废 |

【我的理解】引导题（用自己的话回答）：
1. "每次迭代清空 Cookie"这个勾选，会让同一份脚本分别测试哪两类完全不同的场景？各举一个业务例子。
2. 为什么课程推荐 `compatibility` 而不是"最严格、最标准"的那个选项？这背后的工程取舍是什么？

> 本章属于配置元件：作用范围（层级决定生效范围）与执行顺序（作用域开始处、取样器之前生效）见 [[Ch22-JMeter常用配置元件剖析]]。

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| HTTP Cookie Manager | 会话保持机制：接收 `Set-Cookie` → 保存 → 后续请求自动带出 | ★★★★★ |
| Cookie 格式（Cookie Policy） | standard / standard-strict / ignoreCookies / netscape / default / rfc2109 / rfc2965 / **compatibility（推荐）** | ★★★★☆ |
| 每次迭代清空 Cookie | 决定用户模型：清空＝每次新用户；不清空＝同一用户连续操作 | ★★★★★ |
| 自定义 Cookie（User-Defined Cookies） | 手动添加固定键值对；课程案例以百度首页请求为例 | ★★★★☆ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】HTTP cookie 设置：添加元件步骤 + Cookie Manager 参数面板 + 自定义 Cookie 配置 + Cookie Data 结果（原文共 5 张）

## 关联笔记

- [[Ch22-JMeter常用配置元件剖析]]（作用范围与执行顺序、Cache Manager、CSV Data Set Config）
- [[Ch29-HTTP信息头管理器]]（同页拆出的另一章：自定义请求头与变量）
- [[Ch21-JMeter断言元件的使用]]
- [[Ch24-JMeter后置处理器]]（提取器取到的 token/Cookie 可回填给后续请求）
- [[../L1-性能测试体系/Ch02-性能测试概念与指标体系|L1 Ch02-性能测试概念与指标体系]]
- [[../L1-性能测试体系/Ch04-行业流行性能压测工具介绍|L1 Ch04-行业流行性能压测工具介绍]]
- [[../../接口自动化测试/L2-接口请求构造与响应断言/Ch13-cookie处理|接口自动化 Ch13-cookie处理]]
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
