---
tags: [课程笔记, 性能测试, 性能监控, JMeter, InfluxDB, Grafana]
course: "性能测试"
chapter: "Ch43-jmeter实时压测结果收集"
created: 2026-10-11
status: draft
---

# Ch43 - jmeter实时压测结果收集

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L2-性能监控体系（站点：**性能监控** / `L2/tutorial`）
- 站点页：性能监控 / L2 → jmeter实时压测结果收集
- 前置：[[Ch41-搭建数据分析系统Grafana]]（Grafana 已就绪）、[[../L2-JMeter参数化与并发/Ch32-JMeter变量与引用|Ch32]]（JMeter 变量与断言）、[[../L1-JMeter常用组件/Ch19-JMeter监听器|L1 Ch19-JMeter监听器]]（Backend Listener 元件首次出现）
- 本章定位：本模块的**收口章**——把**压测结果**（业务指标）也变成时间序列，与 [[Ch42-Prometheus监控系统部署应用实战]] 的**机器指标**拼成同一块实时看板

> 📌 内容缺口提示：站点该页正文约 1 300 字 + **9 张截图**，"如何实时压测"步骤完整但**参数只给了"填什么"，没解释"为什么"**；`Backend Listener` 的几个参数（`summaryOnly`、`percentiles`、`testTitle`）与 InfluxDB 版本差异会直接影响能否出图。本笔记按原文整理，参数含义与 InfluxDB 1.x/2.x 差异依据 **JMeter 官方文档（Backend Listener / InfluxdbBackendListenerClient）** 补齐。

> ⚠️ 课程原文勘误（3 处，动手必踩）：
> 1. `docker exec –it JMeterdb bash` —— 正文用的是**中文破折号/en dash（–）**而非减号（-），照抄会报命令找不到。正确：`docker exec -it JMeterdb bash`。
> 2. 参数名原文写作 `influxdbURL` —— 官方参数名是 **`influxdbUrl`**（小写 url）。Backend Listener **按参数名精确读取**，写错可能同名参数不生效（URL 退回默认值），表现为"压测跑了但 InfluxDB 没数据"。
> 3. 原文未强调**版本匹配**：`InfluxdbBackendListenerClient` 面向 **InfluxDB 1.x**（原文用 `influxdb:1.8`，是正确选择）；若换成 InfluxDB 2.x，需要 token/org/bucket 且写入方式不同，直接照抄 1.x 的配置会写不进去。

---

### 知识点1：JMeter + InfluxDB + Grafana 实时压测体系

【课程原话/定义】
JMeter、Grafana 和 InfluxDB 结合成的实时压测体系是一个强大的性能监控和测试解决方案。这个体系能够**实时地收集、分析和展示性能测试数据**，帮助开发者和测试人员更好地理解系统的性能表现，及时发现潜在问题并进行优化。

课程给出的"结合 Grafana 进行实时压测的优点"（原文 4 条）：
1. **实时数据收集**：JMeter 在测试过程中实时生成性能数据，并将其发送到 InfluxDB 进行存储；
2. **数据分析和可视化**：InfluxDB 存储的数据可以通过 Grafana 高效查询和分析，并以图表和仪表板形式展示；
3. **性能监控和预警**：通过 Grafana 仪表板实时监控性能表现，出现异常时及时预警；
4. **问题定位和优化**：根据 Grafana 展示的性能数据，定位潜在性能问题并进行针对性优化。

【为什么？】
这套体系解决的是压测中一个非常具体的痛点：**"压测过程中你看不到结果"**。

传统做法是压完一轮、打开聚合报告（Aggregate Report）才知道 TPS/RT/错误率——**如果第 3 分钟就出现了拐点，你要等到 30 分钟压完才发现，白白浪费 27 分钟**（还要再压一轮）。实时体系把"结果"变成**流动的曲线**：

| 对比项 | 传统（聚合报告） | 实时体系（JMeter + InfluxDB + Grafana） |
|---|---|---|
| 数据可见时间 | 压测结束后 | **压测过程中秒级** |
| 数据形态 | 一张汇总表 | 时间序列曲线（可放大、可比对、可跨轮次） |
| 拐点发现 | 事后推算 | **现场看到 TPS 走平、RT 抬头** |
| 多轮对比 | 手动拼表 | 同一看板切 `testTitle` 变量对比 |
| 团队协作 | 截图传阅 | 大屏共享同一份实时事实 |

还有一层工程意义：**它让"压测"变成"可观测的实验"**——你能一边加压一边调整（例如发现 TPS 在并发 300 停止增长，就地把并发降到 250 做稳定性测试），而不是"盲压一轮 → 等报告 → 再来一轮"。这与 [[Ch40-搭建服务端性能监控系统Prometheus]] 那套机器监控是**互补的两侧**：

| 体系 | 数据 | 回答的问题 | 典型工具 |
|---|---|---|---|
| 机器监控（Ch42） | CPU/内存/IO/网络 | **系统哪里到极限了？** | Prometheus + Node Exporter |
| 压测结果收集（本章） | TPS/RT/错误率/吞吐量 | **业务表现怎么样？** | JMeter + InfluxDB |

**两块数据落在同一块 Grafana 看板上，才算完成闭环。**

【必须掌握】

| 优点（原文 4 条） | 对应的工程价值 |
|---|---|
| 实时数据收集 | 压测中即可见，避免盲压 |
| 数据分析与可视化 | 曲线比表格更能暴露拐点与趋势 |
| 性能监控与预警 | 阈值触发通知，不必全程盯屏 |
| 问题定位与优化 | 业务恶化点与机器指标对齐 → 定位瓶颈层 |

| 三个组件 | 角色 | 一句话 |
|---|---|---|
| JMeter（Backend Listener） | 数据**生产**方 | 每次采样把结果推给 InfluxDB |
| InfluxDB | 时序**存储** | 保存压测结果的"账本"（可被 Grafana 查询） |
| Grafana | **展示 + 告警** | 把 InfluxDB 里的数据画成实时看板 |

【企业场景】
压测现场的典型画面：会议室大屏上是 Grafana 实时看板，压测开始后 TPS 曲线爬升、RT 平稳；到第 8 分钟 RT 的 P95 从 200ms 抬到 600ms、错误率开始冒头——**当场就能判断"到拐点了"**，立即停止加压、记录该并发数作为本轮的容量结论，然后转做稳定性测试。**这比起"压完再优化脚本再压一轮"节省的是整轮时间和人力。** 面试讲"我用 JMeter + InfluxDB + Grafana 做实时压测看板，压测中现场定位拐点"——这是很具体的实战能力。

【面试考察】
面试官："压测过程中你怎么实时看结果？为什么不用聚合报告？"

参考回答框架：
1. 方案：JMeter Backend Listener → InfluxDB（时序存储）→ Grafana（实时看板 + 告警）；
2. 相比聚合报告的优势：秒级可见（不必压完才知道）、曲线暴露拐点与趋势、多轮可对比、团队共享同一份事实；
3. 与机器监控互补：业务指标（TPS/RT/错误率）与资源指标（CPU/IO/网络）同板对齐，才能定位瓶颈层；
4. 纪律：压测时间窗与看板时间范围对齐，压后归档数据。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 只靠聚合报告（压完才看） | 拐点出现后继续压是浪费；实时看板能现场止损与调整 |
| 以为实时看板能替代机器监控 | 业务指标回答"慢不慢"，机器指标回答"为什么慢"；两者互补 |
| 压测结束不做数据归档 | InfluxDB 有保留策略，历史数据会过期；重要数据要及时导出 |
| 用实时看板的数据直接当最终结论 | 看板用于**过程判断**；最终报告应基于完整数据（含机检、基线、断言结果） |
| 忽略"看板数据量"带来的开销 | `summaryOnly=false` 会写大量样本；长时压测要考虑 InfluxDB 容量 |

【我的理解】引导题（用自己的话回答）：
1. 用"盲压 30 分钟 vs 实时看到拐点"这个对比，说明实时体系省下的到底是什么。
2. 为什么本章的体系与 Ch42 的机器监控"必须同时上板"才能定位瓶颈？只用其一各自能得出什么结论？

---

### 知识点2：数据流与组件角色（谁生产、谁存储、谁展示）

【课程原话/定义】
课程步骤（原文）：环境准备（安装 JDK 并配置环境、安装 JMeter 并配置环境）→ 创建 InfluxDB 服务 → 创建数据库 → 打开 JMeter 设置数据传导并压测 → 结合 Grafana 服务展示压测结果。

【为什么？】
这条链的每一步都有"为什么这样做"的设计考量，理解了才不会配错：

1. **为什么用 InfluxDB 而不是 MySQL？** 压测结果天生是**时间序列**（每秒成千上万个采样点，带时间戳），InfluxDB 这类时序库针对"按时间写入 + 按时间区间聚合查询"做了专门优化（高写入吞吐、按时间自动分区、内置聚合函数）。用关系库硬扛会很快遇到写入瓶颈——**这正是"用对工具"的典型场景**。
2. **为什么是 JMeter 主动"推"（push），而 Prometheus 是"拉"（pull）？** 压测结果产生于瞬时、海量、短周期，推模型能让 JMeter 边压边写（Backend Listener 在每次采样后回调）；而 Prometheus 的拉模型适合长期稳定的指标目标（主机、服务）。**两种模型各有适用场景**，这也是面试常问的对比点。
3. **为什么 Grafana 能直接连 InfluxDB？** 因为它支持 InfluxDB 作为数据源（InfluxDB 1.x 用 InfluxQL 查询）——**Grafana 的"多数据源"特性让"机器指标 + 压测指标"能落到同一块看板**（见 [[Ch41-搭建数据分析系统Grafana]]）。

数据流全貌（记住这张图，配置时不会迷路）：
```
JMeter（Backend Listener，InfluxdbBackendListenerClient）
   │  ① 每次采样后 push 到 InfluxDB HTTP 接口（默认写库 jmeter，measurement 也是 jmeter）
   ▼
InfluxDB :8086（数据库 JMeter）
   │  ② Grafana 以 InfluxDB 为数据源查询（InfluxQL）
   ▼
Grafana :3000（实时看板 + 告警）
```

【必须掌握】

| 环节 | 组件/配置 | 要点 |
|---|---|---|
| 生产 | JMeter **Backend Listener** | 选择实现类 `InfluxdbBackendListenerClient`；JMeter 5.0+ 内置（旧版需装插件） |
| 传输 | HTTP 写入（默认 8086） | `influxdbUrl` 指向**能被 JMeter 访问到的** InfluxDB 地址 |
| 存储 | InfluxDB（**1.8**，原文选择正确） | 库名（原文 `JMeter`）、measurement（默认 `jmeter`）、保留策略 |
| 查询 | InfluxQL / Flux | Grafana 数据源配置时注意版本对应的查询语言 |
| 展示 | Grafana | 面板查询命中 measurement 与 field/tag（如 `testTitle`、`application`） |
| 对比 | Prometheus（pull） | 拉模型 vs 推模型：用途不同，不必二选一 |

【企业场景】
一次"参数化了但库是空的"事故复盘：JMeter 里 Backend Listener 配好了、URL 也填了，但 InfluxDB 里就是没数据。排查发现两点：① url 写的是 `http://localhost:8086`，而 JMeter 跑在**宿主机**、InfluxDB 跑在**容器**里（容器端口映射需用宿主 IP 访问，localhost 反而不通）；② 参数名写作 `influxdbURL` 而实现类按 `influxdbUrl` 读取。**两个小写字母级别的差异，导致整轮压测没有实时曲线。** 这类问题的排查思路是"按数据流逐跳验证"：JMeter 日志（有无写入报错）→ InfluxDB 里 `show measurements` → Grafana 数据源与查询。

【面试考察】
面试官："JMeter 的结果是怎么进到 Grafana 的？为什么中间要用 InfluxDB？"

参考回答框架：
1. 链路：JMeter Backend Listener（`InfluxdbBackendListenerClient`）→ push 到 InfluxDB → Grafana 以 InfluxDB 为数据源查询绘图；
2. 为什么用时序库：压测结果是海量带时间戳的采样点，时序库对"高写入 + 时间区间聚合"做了优化；
3. 推 vs 拉：JMeter 用推（push）适合短周期海量数据；Prometheus 用拉（pull）适合长期稳定目标；
4. 排查要点：地址要"生产端可达"、参数名精确、InfluxDB 版本匹配（1.x vs 2.x）。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 用关系库（MySQL）存压测原始采样 | 海量时间序列写入会成瓶颈；应使用时序库 |
| 认为 Prometheus 能替代 InfluxDB 做压测实时看板 | Prometheus 是拉模型 + 长期指标，压测结果更适合 push 到时序库 |
| `influxdbUrl` 填 `localhost` 却跨容器/跨机 | 地址必须"从 JMeter 侧可达"；容器场景要注意端口映射与宿主 IP |
| 忽略 InfluxDB 版本 | 1.x（InfluxQL + 端口 8086）与 2.x（token/org/bucket）配置完全不同 |
| 不检查 measurement/字段名 | Grafana 查询写错 measurement 就会 "No data" |

【我的理解】引导题（用自己的话回答）：
1. 请把 JMeter → InfluxDB → Grafana 这条链画成一句话流程，并标出每一步的验证方法。
2. 为什么"压测结果用推、主机指标用拉"？两种模型各自适合什么数据特征？

---

### 知识点3：环境准备与 InfluxDB 搭建（创建库）

【课程原话/定义】
课程步骤（原文）：
1. **环境准备**：安装 JDK 并配置环境（参考教程）；安装 JMeter 并配置环境（参考教程）；
2. **创建 influxdb 服务**：
   - 拉取镜像 `docker pull influxdb:1.8`；
   - 创建并启动容器 `sudo docker run -d -p 8086:8086 -p 8083:8083 --name JMeterdb influxdb:1.8`；
   - 检验容器是否启动：`docker ps`；
3. **创建数据库**：
   - 进入 JMeterdb 容器内部：`docker exec –it JMeterdb bash`（⚠️ 勘误：应为 `docker exec -it JMeterdb bash`）；
   - 进入容器命令行模式 `influx`；
   - 创建数据库 `create database JMeter;`；
   - 检查数据库是否创建成功 `show databases;`。

【为什么？】
这一步的关键不是"照抄命令"，而是搞清**三个"名字"之间的关系**，因为后面 JMeter 与 Grafana 都要引用它们：

| 名字 | 原文取值 | 用在哪 | 写错的后果 |
|---|---|---|---|
| 容器名 | `JMeterdb` | `docker exec/ps/rm` 时用 | 执行命令找不到容器 |
| 数据库名 | `JMeter` | JMeter 的 `influxdbUrl` 参数（`db=JMeter`）、Grafana 数据源配置 | 写入/查询落到不存在的库 |
| measurement | 默认 `jmeter` | Grafana 面板查询时用（`FROM jmeter`） | 面板 "No data" |

另外两点工程提醒：
1. **端口说明**：`8086` 是 InfluxDB 的 HTTP API（写入/查询都走它）；原文还映射了 `8083`（InfluxDB 1.x 的 Web 管理界面，1.8 已不推荐使用），现代做法是只留 8086，管理界面交给 Grafana。
2. **容器 vs 宿主的地址**：InfluxDB 在容器里，JMeter 在宿主机（或另台机器）——`influxdbUrl` 要写**宿主机 IP:8086**（不是 `localhost`，除非 JMeter 也在同一容器的网络命名空间里）。这与 [[Ch42-Prometheus监控系统部署应用实战]] 里的"容器内 localhost 陷阱"是**同一个坑的两次出现**。

【必须掌握】

| 步骤 | 命令 | 验收 |
|---|---|---|
| 拉镜像 | `docker pull influxdb:1.8` | 无报错（**1.8 而非 2.x**，与 JMeter 客户端匹配） |
| 起容器 | `docker run -d -p 8086:8086 --name JMeterdb influxdb:1.8` | `docker ps` 显示 Up |
| 进容器 | `docker exec -it JMeterdb bash`（**减号**） | 进入容器 shell |
| CLI 进去 | `influx` | 出现 `>` 提示符 |
| 建库 | `create database JMeter;` | 无报错 |
| 验证 | `show databases;` | 列表里有 `JMeter` |
| 预留（【扩展知识】） | 保留策略/数据卷 `-v <本地目录>:/var/lib/influxdb` | 容器重建后数据仍在 |

【企业场景】
压测环境的标准交付里，"数据库建好了"这句话必须能以证据形式给出：**贴上 `show databases;` 的输出**（或截图）。因为后面 JMeter 写不进去时的第一问就是"库存在吗、名字对得上吗"。同理，容器**挂数据卷**要在第一次起容器时就做（`-v ...:/var/lib/influxdb`），否则容器一删，整轮压测的历史数据全没了——**这类"事后无法补救"的配置，必须在开始时做对**。

【面试考察】
面试官："JMeter 的压测结果存在哪？怎么建库、怎么验证？"

参考回答框架：
1. 存储：时序库 InfluxDB（1.x 版本与 JMeter 的 `InfluxdbBackendListenerClient` 匹配）；
2. 建库：`docker run -d -p 8086:8086 --name JMeterdb influxdb:1.8` → `docker exec -it JMeterdb bash` → `influx` → `create database JMeter;` → `show databases;` 验证；
3. 名字要对齐：容器名 / 数据库名 / measurement 三者在 JMeter 与 Grafana 配置里必须一致；
4. 加分：挂数据卷持久化；只保留 8086 端口；注意 InfluxDB 1.x 与 2.x 的配置差异。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 拉 `influxdb:latest`（2.x）却用 1.x 的 JMeter 配置 | 版本必须匹配：JMeter 的 InfluxdbBackendListenerClient 面向 1.x |
| `docker exec –it`（en dash 抄错） | 要用减号 `-it`；复制课程命令时注意全角/半角 |
| 不挂数据卷 | 容器删除即丢数据（InfluxDB 数据在 `/var/lib/influxdb`） |
| 建完库不验证 | 必须 `show databases;` 确认库名（大小写敏感：`JMeter` ≠ `jmeter`） |
| 权限/端口未开放 | 压测机到 8086 不通 → 写不进去；先 `curl` 测连通 |

【我的理解】引导题（用自己的话回答）：
1. 请写出"容器名 / 数据库名 / measurement"分别在哪里被引用，以及写错各自的后果。
2. 为什么 InfluxDB 容器要挂数据卷？不挂会在什么时候吃亏？

---

### 知识点4：JMeter 侧配置 Backend Listener（参数逐个说清）

【课程原话/定义】
课程步骤（原文）：
- 创建线程组，线程组配置（截图）；
- 配置元件 Backend Listener implementation：
  - 在 JMeter 中添加 **Backend Listener** 组件，用于收集数据并发送给 InfluxDB；
  - 在 **Backend Listener implementation** 中选择 `InfluxdbBackendListenerClient`（**必须使用 JMeter 5.0 以上版本**，否则需要单独装插件才能看到这个组件）；
  - 在 `influxdbURL` 中填写实际的 influxdb hostname（⚠️ 勘误：官方参数名为 `influxdbUrl`）；
  - `application` 中填 `baidu`；
  - `testTitle` 中填 `Baidu Testing`；
  - `percentiles` 中填 `50;90;95;99`；
  - 将 `summaryOnly` 设置为 `false`；
  - 其余配置不变；
- 检查终端的 JMeterdb 容器内部的数据库是否新增了数据（截图）。

【为什么？】
这几个参数为什么这样填，决定了你后面能不能画出想要的图：

| 参数 | 原文取值 | 含义与影响 |
|---|---|---|
| `Backend Listener implementation` | `InfluxdbBackendListenerClient` | 决定"往哪写、怎么写"；**JMeter 5.0+ 内置**，旧版需装插件（这是官方组件，无需额外下载） |
| `influxdbUrl` | 实际 hostname | 写入地址，**形如 `http://<宿主IP>:8086/write?db=JMeter`**（`db` 就是第 3 步建的库名）；写成 `influxdbURL` 可能不生效（勘误 2） |
| `application` | `baidu` | 打标签（tag），用于在 Grafana 里按"被测应用"筛选/分组——**多项目共用一个库时靠它区分** |
| `testTitle` | `Baidu Testing` | 打标签（tag），用于区分**不同轮次/不同场景**的压测——看板上做"多轮对比"就靠它（对应看板变量 `$testTitle`，见 [[Ch41-搭建数据分析系统Grafana]]） |
| `percentiles` | `50;90;95;99` | 要计算并写入哪些**分位值**（分号分隔）——这些就是面板上 P95/P99 的来源；不写就没有分位数据 |
| `summaryOnly` | `false` | **false＝写入每个采样点的明细**（数据量大、可做精细曲线）；true＝只写汇总（数据少、粒度粗） |

**"为什么必须 ≤ 5.0 才有"与"为什么 summaryOnly 设 false"** 这两处是原文的隐含知识点：
- 前者说明**组件是新特性**：老版本要靠第三方插件（`jpgc` 插件包里也有 InfluxDB Backend Listener），企业里遇到老版本 JMeter 时不要慌，是插件问题不是配置问题；
- 后者说明**数据量与精度的权衡**：`summaryOnly=false` 能画出"每一秒"的曲线（**压测排错必须**），代价是 InfluxDB 写入量大（长时压测要注意容量与保留策略）；如果只是要一个总览，可设 true 降负载。

【必须掌握】

| 配置项 | 正确值/写法 | 说明 |
|---|---|---|
| 实现类 | `InfluxdbBackendListenerClient` | JMeter 5.0+ 内置；旧版需插件 |
| 写入地址 | `influxdbUrl = http://<可达IP>:8086/write?db=JMeter` | 参数名**小写 url**；`db` 与建库名一致 |
| 应用标签 | `application = <被测应用名>` | 多应用共库时区分 |
| 轮次标签 | `testTitle = <本轮压测名>` | 多轮对比的关键（看板变量） |
| 分位值 | `percentiles = 50;90;95;99` | 分号分隔；面板 P95/P99 的来源 |
| 明细开关 | `summaryOnly = false` | 写明细才能画细曲线；注意数据量 |
| 验证 | InfluxDB 里 `use JMeter; show measurements; select * from jmeter limit 5;` | 能查到数据才算通了 |

【企业场景】
多轮压测的命名纪律：`testTitle` 写成"**项目-场景-日期-轮次**"（如 `order-baseline-20261011-r1`），`application` 写服务名。这样在 Grafana 里用 `$testTitle` 变量一下就能**把"优化前"和"优化后"两轮数据叠在同一张图上**，直接量化优化收益（RT P95 从 650ms → 320ms）。**这个习惯让"调优收益"可被证明**，也是面试里讲性能调优故事时必须有的数据支撑。

【面试考察】
面试官："JMeter 怎么把结果写到 InfluxDB？关键参数有哪些？"

参考回答框架：
1. 元件：Backend Listener → 实现类选 `InfluxdbBackendListenerClient`（JMeter 5.0+ 内置，旧版需插件）；
2. 关键参数：`influxdbUrl`（含 `write?db=<库名>`，注意小写 url 与可达地址）、`application`（应用标签）、`testTitle`（轮次标签）、`percentiles=50;90;95;99`（分位值）、`summaryOnly=false`（写明细）；
3. 验证：进 InfluxDB 容器 `influx` → `use JMeter; show measurements;` 有 `jmeter` measurement 且有数据；
4. 加分：`testTitle`/`application` 用作 Grafana 变量做多轮与多应用对比。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 参数名写 `influxdbURL` | 官方为 `influxdbUrl`（小写），Backend Listener 按名精确读取 |
| `influxdbUrl` 里漏了 `db=JMeter` | 写入会落到默认库（或失败），Grafana 查不到 |
| 地址写 `localhost`（JMeter 与 InfluxDB 不同机/容器） | 必须"从 JMeter 侧可达"，通常写宿主 IP |
| 老版本 JMeter 看不到该实现类就以为配错了 | 5.0 以下需安装插件（如 jpgc 插件包） |
| `summaryOnly=true` 却想要细粒度曲线 | true 只写汇总；要明细必须 false（注意数据量） |
| 不设 `percentiles` | 没有 P95/P99 数据，无法评估用户体验长尾 |

【我的理解】引导题（用自己的话回答）：
1. 请解释 `summaryOnly` 与 `percentiles` 两个参数分别影响"数据量"和"能画什么图"。
2. 为什么 `testTitle` 要写成"项目-场景-日期-轮次"？它给后续分析带来什么便利？

---

### 知识点5：Grafana 展示、常用指标与坑清单

【课程原话/定义】
课程步骤（原文）：
- **结合 Grafana 服务进行压测结果展示**：拉取镜像 `docker pull grafana/grafana` → 创建并启动容器 `docker run -d -p 3000:3000 --name JMeterGrafana grafana/grafana` → 检验容器（`docker ps`、浏览器 `localhost:3000`）→ 配置数据源（截图多张）→ 创建面板（截图）→ 打开面板，查看数据（截图）。

课程给出的"常用指标"（原文 5 条）：
1. **TPS（Transactions Per Second）**：每秒事务数，性能测试中最重要的指标之一，衡量系统在单位时间内处理事务的能力（每个事务包含发送请求、服务端处理、返回结果的完整过程）；
2. **QPS（Queries Per Second）**：每秒查询率，衡量服务器每秒能响应的查询次数；**只有一个请求接口时 QPS 等价于 TPS**；一个事务可能产生多次请求，这些请求都计入 QPS；
3. **并发数（Concurrency Number）**：系统同时能处理的请求数量，反映负载能力；可通过分析机器 1 秒内的访问日志数量得到；
4. **吞吐量（Throughput）**：单位时间内系统处理请求的数量；TPS 和 QPS 都是吞吐量的常用量化指标；
5. **响应时间（Response Times）**：从客户端发出请求开始，到收到服务端响应结束的计时。

【为什么？】
这四个指标里最容易被问的是 **TPS 与 QPS 的关系**（原文也点明"只有一个请求接口时 QPS 等价于 TPS"）。用一句更工程化的话总结：**一个事务可能包含多次请求**——"登录+查询"是一个事务（1 TPS），但包含 2 次 HTTP 请求（2 QPS）。所以：
- 接口级压测（单接口）：TPS ≈ QPS；
- 业务级压测（多接口链路）：TPS < QPS，**报数时要说清是哪个口径**——这是报告被质疑的高频点。

另外要记住 Grafana 侧的三个"落地要点"（原文只有截图）：
1. **数据源**：新增 **InfluxDB** 数据源，URL 填**从 Grafana 侧可达**的地址（容器场景别写 `localhost`），Database 填 `JMeter`；
2. **查询**：面板里写 InfluxQL（如按 `testTitle` 过滤，对 `rt`/`count` 做时间聚合），**注意"速率 vs 累计"**——TPS 类曲线要用时间窗口聚合（对照 [[Ch41-搭建数据分析系统Grafana]] 知识点5 的口径纪律）；
3. **时间与刷新**：看板时间范围对齐压测窗口；刷新间隔设 5s~10s，否则看到的"实时"其实是几十秒前的。

【必须掌握】

| 指标（原文） | 口径要点 | 在 Grafana 上怎么看 |
|---|---|---|
| TPS | 每秒完成的事务数（完整业务过程） | 按时间窗口聚合的折线（看拐点） |
| QPS | 每秒查询/请求数；单接口时 ≈ TPS | 同上；多接口链路时与 TPS 不等 |
| 并发数 | 同时处理的请求数；**≈ QPS × RT** | 折线与 TPS/RT 对照，判断是否达到设定并发 |
| 吞吐量 | 单位时间处理量（TPS/QPS 是常用量化） | 与 TPS 曲线同看 |
| 响应时间 | 请求发出到收到响应；**要看分位值** | 平均 + P90/P95/P99 多线并列 |

| 落地检查 | 正确做法 |
|---|---|
| Grafana 数据源 | InfluxDB，URL 从 Grafana 侧可达，Database = `JMeter` |
| 面板查询 | InfluxQL 命中 measurement `jmeter` + tag `testTitle`/`application` |
| 口径 | 速率用时间窗口聚合；避免把累计值画成速率 |
| 时间 | 时间范围＝压测窗口；刷新 5s/10s |
| 归档 | 压测后导出看板截图与关键数据（进报告） |

【企业场景】
交付一轮压测的完整证据包（可直接照抄）：① Grafana 看板截图（TPS/RT/错误率 + 机器指标）；② `testTitle` 命名让多轮数据可叠加对比；③ InfluxDB 内数据导出（CSV）；④ 报告里写清"本轮 TPS 口径是业务事务（含登录），QPS 约为 TPS 的 1.8 倍"。**第 ④ 条特别能体现专业度**——大多数人的报告里从不写口径，导致数据一出会议室就产生分歧。

【面试考察】
面试官："TPS 和 QPS 有什么区别？压测结果你会怎么展示？"

参考回答框架：
1. 口径：TPS＝每秒事务数（一个事务可含多次请求）；QPS＝每秒请求数；**单接口压测时两者近似相等，链路压测时 TPS < QPS**，报数必须说明口径；
2. 并发数与两者关系：并发数 ≈ QPS × RT（利特尔法则）；
3. 展示：JMeter → InfluxDB → Grafana 实时看板，看平均与分位值（P90/P95/P99），把业务曲线与机器指标放在同一时间轴；
4. 纪律：看板时间范围对齐压测窗口、刷新 5~10s、压后归档数据与口径说明。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 报告只写"TPS 5000"，不写口径 | 单接口还是业务链路差别巨大；必须注明 |
| 用平均值代表响应时间 | 平均值会掩盖长尾；必须看 P90/P95/P99（原文的 `percentiles` 就是为它服务的） |
| Grafana 数据源填 `localhost:8086`（跨容器） | 要用 Grafana 侧可达地址（宿主 IP / 容器名） |
| 面板把累计计数当速率画 | 曲线一直涨＝口径错了；要用时间窗口聚合 |
| 看板刷新太慢（默认）导致"看的是历史" | 压测期刷新设 5s/10s；时间范围对齐压测窗口 |
| 压完不导出数据 | InfluxDB 保留策略可能清理历史；先导出再清理环境 |

【我的理解】引导题（用自己的话回答）：
1. 请举例说明"一个事务包含 3 次请求"时 TPS 与 QPS 的关系，并说明报告里该怎么写。
2. 为什么响应时间必须看分位值？请用"平均值 200ms 但 P99 是 3s"这个例子解释它对用户体验意味着什么。

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 实时压测体系 | JMeter + InfluxDB + Grafana；4 条优点（实时收集/可视化/预警/定位）；相比聚合报告的价值：压测中当场发现拐点 | ★★★★★ |
| 数据流与选型 | JMeter 推（push 到 InfluxDB，时序库）→ Grafana 查询展示；与 Prometheus 拉模型互补 | ★★★★★ |
| InfluxDB 搭建 | `influxdb:1.8`，端口 8086（+8083 已不推荐）；`docker exec -it` 进容器 → `influx` → `create database JMeter;` → `show databases;` | ★★★★★ |
| JMeter 配置 | `InfluxdbBackendListenerClient`（5.0+ 内置）→ `influxdbUrl`（小写 url + `write?db=JMeter`）、`application`、`testTitle`、`percentiles=50;90;95;99`、`summaryOnly=false` | ★★★★★ |
| Grafana 展示与指标 | InfluxDB 数据源（可达地址 + Database）；TPS/QPS/并发数/吞吐量/响应时间；**口径必须写清**（TPS vs QPS）、分位值必看 | ★★★★★ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】创建并启动 InfluxDB 容器后的状态（原文 1 张）
> 📷 【截图占位】线程组配置（原文 1 张）
> 📷 【截图占位】Backend Listener 参数配置（原文 1 张）
> 📷 【截图占位】检查 JMeterdb 容器内数据库是否新增数据（原文 2 张）
> 📷 【截图占位】`localhost:3000` 进入 Grafana 管理页面（原文 1 张）
> 📷 【截图占位】配置 Grafana 数据源（原文 5 张）
> 📷 【截图占位】创建面板（原文 3 张）
> 📷 【截图占位】打开面板查看数据（原文 1 张）

## 关联笔记

- [[Ch41-搭建数据分析系统Grafana]]（Grafana 数据源与看板配置；看板变量 `$testTitle`）
- [[Ch42-Prometheus监控系统部署应用实战]]（机器指标侧：Node Exporter + Prometheus；与本章业务指标同板）
- [[Ch39-性能监控系统价值]]（体系选型与场景）
- [[Ch40-搭建服务端性能监控系统Prometheus]]（另一条采集链路：拉模型）
- [[../L1-JMeter常用组件/Ch19-JMeter监听器|L1 Ch19-JMeter监听器]]（Backend Listener 首次出现；聚合报告与实时写入的差异）
- [[../L1-JMeter常用组件/Ch31-监听器与测试结果|L1 Ch31-监听器与测试结果]]（View Results Tree / Graph Results 的字段口径）
- [[../L1-性能测试体系/Ch02-性能测试概念与指标体系|L1 Ch02-性能测试概念与指标体系]]（TPS/QPS/并发数/RT 的口径与"并发数 = QPS × RT"）
- [[../L1-性能测试体系/Ch09-性能测试报告|L1 Ch09-性能测试报告]]（把看板数据写进报告）
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
