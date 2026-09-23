---
tags: [课程笔记, 性能测试, MOC, JMeter]
created: 2026-09-23
status: in_progress
---

# L1 · JMeter 常用组件

> 复习优先级：⭐⭐⭐ 投简历必掌握 · ⭐⭐ 重要加分 · ⭐ 了解即可
> 课程站点：`performance.tutorial.hogwarts.ceshiren.com` → `performance/性能测试工具/L1/tutorial/...`（站点标题：`L1.JMeter 常用组件`）
> 编号说明：**章节编号按站点** —— 站点这一层的 21 个 tutorial 页，一页一章，全仓库连续编号 Ch11~Ch31（Ch01~Ch10 = [[../L1-性能测试体系-重点梳理|L1 性能测试体系]]）。

## 一句话定位

L1 讲性能测试的"语言和体系"，本模块讲**干活的工具**：用 JMeter 把"目标并发 / 目标吞吐"变成可执行的脚本 —— **测试计划 → 线程组 → 控制器 → 取样器 → 断言 → 定时器 → 前置/后置处理器 → 配置元件 → 监听器**，并搞清它们的**作用域与执行顺序**（本模块最容易被问倒的地方）。

## 章节清单（21 章 = 站点 21 页）

| 章节 | 站点页 | 重要性 | 状态 | 学习日期 | 内容概要 |
|------|--------|--------|------|---------|----------|
| [[Ch11-JMeter介绍与安装]] | JMeter介绍与安装 | ⭐⭐⭐ | 📝 | 2026-09-23 | JMeter 是什么、七大优点、安装 Java 8+ 与 JMeter、把 bin 配进环境变量 |
| [[Ch12-JMeter的运行]] | JMeter的运行 | ⭐⭐ | 📝 | 2026-09-23 | 运行环境要求（Java/系统/内存）、GUI 与命令行两种启动方式、主界面四部分与菜单（Run/Options/Help） |
| [[Ch13-使用代理服务器录制请求]] | 使用代理服务器录制请求 | ⭐⭐ | 📝 | 2026-09-23 | 代理录制原理与优点；HTTP(S) Test Script Recorder + 线程组 + 录制控制器、Port 8888、Include/Exclude 正则、浏览器代理、证书安装（含原文勘误） |
| [[Ch14-测试计划]] | 测试计划 | ⭐⭐⭐ | 📝 | 2026-09-23 | 测试计划 = 脚本与场景设计的基本运行单元；三部分设置（名称注释 / 用户定义变量 / 独立运行每个线程组、tearDown、函数测试模式、添加 jar） |
| [[Ch15-线程组]] | 线程组 | ⭐⭐⭐ | 📝 | 2026-09-23 | 线程组是测试计划的开始点；取样器错误后五种动作；线程属性（线程数 / Ramp-up / 循环次数 / 迭代执行方式 / 延迟创建 / 线程调度 Duration 与 Startup delay） |
| [[Ch16-控制器]] | 控制器 | ⭐⭐⭐ | 📝 | 2026-09-23 | 逻辑控制器的作用；事务控制器（Generate Parent Sample / Include duration of timer…）、If 控制器（Interpret Condition… / Evaluate for all children）、循环控制器、随机控制器；四者对比选用 |
| [[Ch17-JMeter采样器]] | JMeter采样器_取样器 | ⭐⭐⭐ | 📝 | 2026-09-23 | 采样器在元件体系中的位置；HTTP Request Sampler、Debug Sampler、BeanShell Sampler |
| [[Ch18-JMeter场景逻辑控制技术]] | JMeter场景逻辑控制技术 | ⭐⭐ | 📝 | 2026-09-23 | 用逻辑控制器编排真实业务流程：If / 循环类（Loop·While·ForEach）/ Switch / 事务控制器 + 商城购买三分支实战 |
| [[Ch19-JMeter监听器]] | JMeter监听器 | ⭐⭐⭐ | 📝 | 2026-09-23 | 监听器在报告链条里的位置；聚合报告（Aggregate Report 字段含义）、Backend Listener（InfluxDB/Graphite）、监听器使用规范 |
| [[Ch20-JMeter定时器]] | JMeter定时器 | ⭐⭐⭐ | 📝 | 2026-09-23 | 定时器在取样器之前执行；固定定时器、高斯随机定时器、吞吐量定时器（Target throughput **每分钟** + 五种 Calculate Throughput 模式）、并发定时器（集合点） |
| [[Ch21-JMeter断言元件的使用]] | JMeter断言元件的使用 | ⭐⭐⭐ | 📝 | 2026-09-23 | 响应断言（测试字段 + 模式匹配规则）、大小断言、XPath 断言、JSON 断言及四种选用 |
| [[Ch22-JMeter常用配置元件剖析]] | JMeter常用配置元件剖析 | ⭐⭐⭐ | 📝 | 2026-09-23 | 配置元件的作用；HTTP Cache Manager、CSV Data Set Config；**配置元件的作用范围与执行顺序**（原文表述勘误与准确说法） |
| [[Ch23-JMeter前置处理器]] | JMeter前置处理器 | ⭐⭐ | 📝 | 2026-09-23 | 前置处理器的定位；Sample Timeout（超时控制，非断言）、BeanShell PreProcessor（脚本造数据） |
| [[Ch24-JMeter后置处理器]] | JMeter后置处理器 | ⭐⭐⭐ | 📝 | 2026-09-23 | 关联取参三件套：JSON Extractor、正则表达式提取器（模板 $1$ / 匹配数字）、XPath Extractor + 变量机制与调试 |
| [[Ch25-JMeter执行顺序]] | JMeter执行顺序 | ⭐⭐⭐ | 📝 | 2026-09-23 | **八大组件**与同作用域执行顺序：配置元件 → 前置处理器 → 定时器 → 取样器 → 后置处理器 → 断言 → 监听器；同级从上到下；作用域含义与排错清单 |
| [[Ch26-JMeter虚拟用户管理]] | JMeter虚拟用户管理 | ⭐⭐ | 📝 | 2026-09-23 | 虚拟用户概念；三类线程组（setUp / Thread Group / tearDown）与各自适用场景；实操（python -m http.server 起被压服务）；三类线程组执行顺序 |
| [[Ch27-HTTP请求属性设置]] | HTTP请求属性设置 | ⭐⭐ | 📝 | 2026-09-23 | HTTP 请求基本属性 + **Redirect Automatically vs Follow Redirects**、Use KeepAlive、multipart/form-data；三种参数类型（参数 / 消息体数据 / 文件上传） |
| [[Ch28-HTTPcookie设置]] | HTTPcookie设置 | ⭐⭐ | 📝 | 2026-09-23 | HTTP Cookie Manager：参数（Clear cookies each iteration）、Cookie 格式（compatibility 推荐）、自定义 Cookie 实战 |
| [[Ch29-HTTP信息头管理器]] | HTTP信息头管理器 | ⭐⭐ | 📝 | 2026-09-23 | 用 HTTP Header Manager 自定义请求头（User-Agent / Content-Type / Token），配合用户定义变量 + View Results Tree 验证 |
| [[Ch30-HTTP请求设置]] | HTTP请求设置 | ⭐⭐ | 📝 | 2026-09-23 | HTTP Request 高级参数：客户端实现与超时、Embedded Resources（并行下载 / 资源池 / URL 过滤）、Source address、Proxy Server、Save response as MD5 hash |
| [[Ch31-监听器与测试结果]] | 监听器与测试结果 | ⭐⭐ | 📝 | 2026-09-23 | View Results Tree 三种查看模式（Sampler result / Request / Response data）；Graph Results 参数与底部统计含义（No of Samples / Latest Sample / Average / Deviation / Throughput / Median） |

## 学习进度

- 21 / 21 章已建笔记（站点「性能测试工具 / L1.JMeter 常用组件」21 个 tutorial 页全覆盖）
- 全模块约 25.7 万字符；每章七个内容标记齐全（按知识点逐项校验），无空表格、无悬空链接

## 建议学习顺序（不要按 Ch11→Ch31 硬刷）

| 轮次 | 章节 | 目标 |
|------|------|------|
| 第 1 轮 跑起来 | Ch11 → Ch12 → Ch14 → Ch15 | 装上 JMeter，看懂测试计划/线程组/线程属性，能把一条请求跑起来 |
| 第 2 轮 控并发 | Ch26 → Ch16 → Ch19 → Ch20 | 三类线程组、控制器、监听器与定时器 → 能设计"多少用户、什么节奏、怎么出结果" |
| 第 3 轮 造请求与校验 | Ch17 → Ch27 → Ch30 → Ch29 → Ch28 → Ch21 | HTTP 采样器与参数、请求头/cookie、四种断言 → 脚本"发得对、判得准" |
| 第 4 轮 取参与收口 | Ch24 → Ch23 → Ch22 → Ch25 → Ch13 → Ch18 | 关联取参、前置处理、配置元件、执行顺序 → 串起完整业务流程；录制脚本作为提速手段 |
| 面试前必背 | **Ch25（执行顺序）** + **Ch15（线程属性）** + **Ch19（聚合报告字段）** + **Ch21（断言）** | 面试高频三连：一个压测脚本必须有哪些组件 / 并发怎么设 / 结果怎么看 |

## 本模块必须能"背下来"的三件事

1. **八大组件 + 执行顺序**：配置元件 → 前置处理器 → 定时器 → 取样器 → 后置处理器 → 断言 → 监听器（同级从上到下）。
2. **线程属性三件套**：线程数（并发用户数）/ Ramp-up（多久达到并发）/ 循环次数（每轮做什么），以及"同一迭代内 Same user on each iteration 到底指什么"这个原文写错、面试爱问的点。
3. **关联取参链路**：前一个请求的响应 → 后置处理器提取（JSON / 正则 / XPath）→ 存为变量 → 后续请求用 `${变量}` 引用。

## 关联

- [[../L1-性能测试体系-重点梳理|L1-性能测试体系-重点梳理（跟着学版）]]
- [[../L1-性能测试体系/Ch04-行业流行性能压测工具介绍|L1 Ch04-行业流行性能压测工具介绍]]（为什么选 JMeter：六大优点与选型对比）
- [[../L1-性能测试体系/Ch07-性能测试流程与方法|L1 Ch07-性能测试流程与方法]]（并发模式 vs RPS 模式 → 对应线程组与吞吐量定时器的用法）
- [[../L1-性能测试体系/Ch08-性能测试计划|L1 Ch08-性能测试计划]]（发压工具配置与脚本编写阶段；注意区分"JMeter 的测试计划"与"性能测试计划文档"）
- [[../README|性能测试（课程 MOC）]]
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
