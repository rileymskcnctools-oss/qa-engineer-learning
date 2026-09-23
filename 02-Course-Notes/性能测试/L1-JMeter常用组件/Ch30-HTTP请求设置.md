---
tags: [课程笔记, 性能测试]
course: "性能测试"
chapter: "Ch30-HTTP请求设置"
created: 2026-09-23
status: draft
---

# Ch30 - HTTP请求设置

## 课程来源

- 学习日期：2026-09-23
- 课程模块：性能测试 / L1-JMeter常用组件（站点：性能测试工具 / L1.JMeter 常用组件）
- 站点页：性能测试工具 / L1.JMeter 常用组件 → HTTP请求设置
- 前置：[[../L1-性能测试体系/Ch01-性能测试介绍与压力曲线模型|L1 Ch01-性能测试介绍与压力曲线模型]]

> 本章对应课程站点「HTTP请求设置」页：HTTP 请求的**高级参数**（Implementation、连接/响应超时、Embedded Resources from HTML Files、Source address、Proxy Server、Save response as MD5 hash）。基础字段（协议/服务器/端口/方法/路径/内容编码）与采样器概念见 [[Ch17-JMeter采样器]]，重定向 / KeepAlive / multipart 与三种参数类型见 [[Ch27-HTTP请求属性设置]]。

---

### 知识点1：HTTP 请求高级参数（高级界面详解）

【课程原话/定义】

| 分组 | 选项 | 课程原文说明 |
|---|---|---|
| Client implementation | Implementation | 发送 http 请求的方式，可选项为 java 和 HttpClient4，默认为 HttpClient4 |
| Client implementation | Connect | 连接超时时间设置，单位为毫秒 |
| Client implementation | Response | 响应等待超时时间设置，单位为毫秒 |
| Embedded Resources from HTML Files | Retrieve All Embedded Resources | 当该选项被选中时，jmeter 在发出 HTTP 请求并获得响应的 HTML 文件内容后，还对该 HTML 进行解析，并获取 HTML 中包含的所有资源（图片、flash 等） |
| Embedded Resources from HTML Files | Parallel downloads | 设置是否使用自设资源池，勾选后可设置大小 |
| Embedded Resources from HTML Files | Number | 资源池大小，默认为 6 |
| Embedded Resources from HTML Files | URLs must match | URL 匹配过滤，填写此项则只会下载与此内容项匹配的 url 的资源 |
| Source address | Source address | 只用于 http 协议且 Implementation 为 HttpClient4 的情况，此属性用于启用 IP 欺骗。会重写了这个 http 请求使用的默认本地 IP 地址。用于 Jmeter 主机具有多个 IP 地址（即 IP 别名、网络接口、设备）的情况。该值可以是主机名、IP 地址或网络接口设备 |
| Proxy Server | 代理配置 | 代理服务器的相关配置信息 |
| Optional Tasks | Save response as MD5 hash? | 选中该项，在执行时仅记录服务端响应数据的 MD5 值，而不记录完整的响应数据。在需要进行数据量非常大的测试时，建议选中该项以减少取样器记录响应数据的开销 |

课程的实操验证：以访问百度首页为例，勾选 `Save response as MD5 hash?`，对比勾选前后的响应结果区别。

【为什么？】
「高级参数」这一页是区分「会用 JMeter」和「会做压测」的分水岭，因为它全部回答同一个问题：**压测数字准不准、加压机扛不扛得住**。

- **Connect / Response 超时**：不设超时，一个卡住的连接会把线程一直占着，导致「并发上不去」但看起来又不是失败——这是最典型的数据失真来源。
- **Retrieve All Embedded Resources**：真实浏览器会下载 HTML 里引用的所有静态资源。只压 HTML 不压资源，测出来的压力可能只有真实的三分之一。而并发下载（资源池大小默认 6）正是浏览器的行为特征。
- **Save response as MD5 hash**：JMeter 要把每个响应体都存在内存/文件里，大响应体（视频流、大 JSON）会迅速吃满加压机内存并拖慢 GC。只存 MD5 就把「内容校验」和「数据存储」两个需求解耦了——你依然能判断响应是否变化，但不再存储全文。

【必须掌握】

| 参数 | 默认值 | 什么时候必须改 |
|---|---|---|
| Implementation | HttpClient4 | 无特殊需求保持默认；老版本插件生态可能需要 java 实现 |
| Connect 超时 | 未设 | 压测必设（如 5000ms），否则线程可能被不响应的连接占死 |
| Response 超时 | 未设 | 压测必设（如 30000ms），业务 SLA 之外的等待没有统计意义 |
| Retrieve All Embedded Resources | 未勾选 | 压测「网页」时必勾；压测纯接口（JSON/XML API）时不勾 |
| Parallel downloads | — | 模拟浏览器并发下载时勾选，配合 Number 设置池大小 |
| Number | 6 | 与真实浏览器连接数对齐；数值越高对本机网络压力越大 |
| URLs must match | 空 | 只想压自家域名、排除第三方 CDN 时填写匹配规则 |
| Save response as MD5 hash | 未勾选 | 响应体很大、只需校验一致性时勾选 |

【企业场景】
你要压测一个商品搜索接口，返回的 JSON 里带 300 条结果、单次响应 800KB。第一轮跑 200 并发时，加压机 CPU 和内存双双飙红，报告的 TPS 低得离谱——因为你在测自己的机器而不是被测系统。你的处理是：勾选 `Save response as MD5 hash?`，监听器改用只统计指标的方式（禁用查看结果树），同时显式设置 Connect/Response 超时。第二轮数据就稳定了。相反，如果你压的是「首页渲染」这类含大量图片的页面，就必须勾上 `Retrieve All Embedded Resources` 并设 Number=6，否则测出的压力会明显低于真实用户访问。

【面试考察】
1. **面试官怎么问**：「压测时加压机压力很大，怎么办？」
   **回答框架**：分辨瓶颈在加压机还是被测系统——关掉明细监听、用 MD5 存响应、提高加压机规格、分布式压测、减小响应体采样量。
2. **面试官怎么问**：「超时参数要不要设置？不设会怎样？」
   **回答框架**：必须设置；不设时慢连接会长期占用线程，导致并发达不到、耗时统计失真，还可能掩盖真正的服务端问题。
3. **面试官怎么问**：「压网页和压接口在配置上有什么差别？」
   **回答框架**：压网页要勾 Retrieve All Embedded Resources 并配置并发下载与资源过滤；压接口不需要，且更关注响应体处理和编码。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 压测时不设 Connect/Response 超时 | 慢连接会占死线程，结果是「并发虚高、TPS 虚低」，必须显式设超时 |
| 压接口时也勾上 Retrieve All Embedded Resources | 只会增加无效请求，接口场景不解析 HTML，勾了纯属浪费加压机资源 |
| 以为勾了保存 MD5 就不能校验响应内容了 | MD5 本身就是内容一致性凭据，只是看不到明文；要断言内容细节就不能勾 |
| 大响应体压测时仍开着查看结果树 | 监听器会缓存全部响应，是加压机内存爆掉的头号原因 |

【我的理解】
1. 「只存 MD5」和「存完整响应」这两者的取舍，本质上是把哪两个测试目标解耦了？请你自己说清楚：什么情况下必须先存全文，什么情况下只存 MD5 就够。
2. 如果你压的是含 50 张图片的首页，Number 设为 6 和设为 60 分别会发生什么？请从「浏览器真实行为」和「加压机网络开销」两个角度分析。

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| HTTP 高级参数 | Implementation / Connect 与 Response 超时 / 静态资源下载 / Source address / Proxy / MD5 | ★★★★☆ |
| 压测准确性 | 超时必设、静态资源按场景勾选、大响应体用 MD5 降低加压机开销 | ★★★★★ |
| 加压机不是瓶颈 | 高级参数的落脚点都是"数字准不准、加压机扛不扛得住" | ★★★★★ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】HTTP Request 高级选项配置（Implementation / Embedded Resources / Save response as MD5 hash）（原文共 1 张）
> 📷 【截图占位】勾选 Save response as MD5 hash 前后的响应结果对比（原文共 1 张）

## 关联笔记

- [[Ch17-JMeter采样器]]（采样器概念与 HTTP Request 基础字段）
- [[Ch27-HTTP请求属性设置]]（重定向 / KeepAlive / multipart、三种参数类型）
- [[Ch29-HTTP信息头管理器]]
- [[Ch31-监听器与测试结果]]（大响应体场景要先精简监听器）
- [[../L1-性能测试体系/Ch02-性能测试概念与指标体系|L1 Ch02-性能测试概念与指标体系]]
- [[../L1-性能测试体系/Ch07-性能测试流程与方法|L1 Ch07-性能测试流程与方法]]
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺]]
