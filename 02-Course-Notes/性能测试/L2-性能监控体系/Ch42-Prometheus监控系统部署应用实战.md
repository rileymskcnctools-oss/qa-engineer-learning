---
tags: [课程笔记, 性能测试, 性能监控, Prometheus, Node Exporter]
course: "性能测试"
chapter: "Ch42-Prometheus监控系统部署应用实战"
created: 2026-10-11
status: draft
---

# Ch42 - Prometheus监控系统部署应用实战

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L2-性能监控体系（站点：**性能监控** / `L2/tutorial`）
- 站点页：性能监控 / L2 → Prometheus监控系统部署应用实战
- 前置：[[Ch40-搭建服务端性能监控系统Prometheus]]（Prometheus 本体）、[[Ch41-搭建数据分析系统Grafana]]（可视化）
- 本章定位：把三者**接成一条可用的闭环**——**Prometheus（存）+ Node Exporter（采）+ Grafana（看）**，这是"主机/容器监控"的标准最小体系

> 📌 内容缺口提示：站点该页正文约 1 100 字 + **11 张截图**（大多在"配置 grafana 数据源"那一步），"搭建"部分三步命令清楚但**没有讲 Node Exporter 到底暴露了什么指标、怎么验证、指标名是什么**。本笔记按原文整理，**Node Exporter 指标名与验证方法**依据 Prometheus 官方文档（`node_exporter` 标准指标）补齐。

> ⚠️ 原文小坑（2 处，动手时会卡）：
> 1. `docker exec –it JMeterdb bash` 之类的命令里，课程正文用了**中文破折号/en dash（–）**而不是减号（-）；照抄会报 `executable file not found`。
> 2. `docker run ... -v <your local folder>:/var/lib/grafana` 中的 `<your local folder>` 是占位符，**必须换成真实路径**（Windows 下形如 `D:/grafana-data`），直接复制会报错。

---

### 知识点1：三件套的分工（Prometheus / Node Exporter / Grafana）

【课程原话/定义】
Prometheus、Grafana 和 Node Exporter 三者结合，构建了一个强大的监控体系，专门用于 Linux 主机和容器的监控。这个体系能够实时收集、分析和可视化各种系统指标，帮助运维人员快速定位问题，确保系统的稳定性和性能。

- **Prometheus** 是这个监控体系的核心，负责**收集和存储**来自各个目标的指标数据；
- **Node Exporter** 是一个部署在被监控服务器上的轻量级程序，负责**收集服务器的各种指标数据**（CPU 使用率、内存占用、磁盘空间等），并将这些数据暴露为 Prometheus 可以抓取的 **HTTP 端点**（以便 Prometheus 定期拉取并存储）；
- **Grafana** 是一个开源的数据可视化工具，它可以从 Prometheus 等数据源中读取数据，并将其展示为各种图表和仪表盘。

【为什么？】
这三者的关系是一条**标准的数据流**，理解了这条流，你就能把任何一个新对象接进体系：

```
被监控对象（Linux 主机）
    │  ① 采集并暴露
    ▼
Node Exporter  :9100/metrics   ← 一个 HTTP 端点（文本格式的指标）
    │  ② 定时拉取（scrape）
    ▼
Prometheus     :9090           ← 存时序 + PromQL 查询
    │  ③ 作为数据源查询
    ▼
Grafana        :3000           ← 画面板/看板 + 告警
```

关键认知有两条：
1. **"Exporter 模式"是 Prometheus 生态的核心思想**：任何想被监控的东西，只要有一个能输出 `/metrics` 文本的组件（官方 Exporter、中间件自带、自研脚本），就能进体系。Node Exporter 就是把 Linux 主机的 `/proc`、`/sys` 里的系统指标"翻译"成 `/metrics` 的那个翻译官——**它做的正是 [[Ch38-系统性能数据收集（cpu、mem、net、io）]] 那些命令自动化、结构化之后的版本**；
2. **分层失败可以分层排查**：9100 不通 → 采集层问题；9090 里查不到数据 → 拉取/存储问题；Grafana 空 → 数据源或查询问题。**不要一上来就怀疑 Grafana**（它只是最末端）。

【必须掌握】

| 组件 | 端口 | 角色 | 一句话职责 | 失败时的现象 |
|---|---|---|---|---|
| Node Exporter | 9100 | 采集/暴露主机指标 | 把主机指标变成 `/metrics` | `/targets` 该 job DOWN → 无主机数据 |
| Prometheus | 9090 | 采集/存储/查询/告警规则 | 定时拉取 + 时序存储 + PromQL | `/targets` 能开但无数据；查询为空 |
| Grafana | 3000 | 可视化与告警 | 连数据源、画看板、配阈值告警 | 面板 "No data"（先查它连的数据源） |

| 数据流三步 | 动作 | 验证点 |
|---|---|---|
| 采集 | Node Exporter 启动并暴露 9100 | 浏览器 `主机IP:9100/metrics` 有大量 `node_*` 指标文本 |
| 拉取 | Prometheus 的 job `linux` 抓 `IP:9100` | `/targets` 中该 target 为 **UP** |
| 展示 | Grafana 加 Prometheus 数据源并画图 | 面板能查出 `node_cpu_seconds_total` 等指标 |

【企业场景】
你要给"3 台应用机 + 1 台 DB"建监控。做法：每台机器起一个 Node Exporter（9100），Prometheus 配置一个 `job_name: linux` 列出 4 个 `${IP}:9100`，Grafana 导入一张 Node Exporter 社区看板。**20 分钟就能拿到"4 台机器的 CPU/内存/磁盘/网络"全景**——如果不用 Node Exporter 而用脚本采集，你需要自己写 4 类命令 × 4 台机器的采集、存储、画图，维护成本高一个量级。**"Exporter 模式"省的是长期维护成本。**

【面试考察】
面试官："Prometheus + Node Exporter + Grafana 三者的关系是什么？"

参考回答框架：
1. 三层分工：Node Exporter **采集并暴露**（`/metrics`，9100）→ Prometheus **拉取、存储、查询**（9090，pull + TSDB + PromQL）→ Grafana **可视化与告警**（3000，数据源消费）；
2. 思想：Exporter 模式让任何对象只要暴露 `/metrics` 就能进体系（官方/中间件/自研都行）；
3. 排查：分层定位（9100 采集 → 9090 拉取 → 3000 展示），不要一上来怀疑 Grafana；
4. 落地：主机监控最小体系=三者；K8s 场景再加 cAdvisor/kube-state-metrics。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 以为 Grafana 没数据＝Grafana 有问题 | 按数据流反向排查：先 9100（采集）→ 再 9090（拉取）→ 最后 3000（展示） |
| 把 Node Exporter 当"监控系统" | 它只是**采集器**（暴露端点），没有存储与展示 |
| 在每台机器上都装一个 Prometheus | Prometheus 是中心（一个即可服务多机）；被监控机只装 Exporter |
| 忽略端口与防火墙 | 9100/9090/3000 任一不通，链路就断；容器场景还要注意端口映射 |
| 忘记"主机与容器"的视角差异 | 容器内 Exporter 看到的是容器命名空间，与宿主指标不同 |

【我的理解】引导题（用自己的话回答）：
1. 请把"采集 → 拉取 → 展示"三步各写一条验证命令/页面，并说明哪一步出问题会看到什么现象。
2. 为什么说 Node Exporter 是 [[Ch38-系统性能数据收集（cpu、mem、net、io）]] 那套命令的"自动化、结构化版本"？

---

### 知识点2：应用场景与体系优点

【课程原话/定义】
课程给出的"应用场景"（原文 5 条）：
1. **云原生和容器化环境监控**：实时收集容器的 CPU/内存等指标，Grafana 可视化，Node Exporter 部署在容器所在节点上采集节点指标；
2. **微服务架构监控**：Prometheus 监控每个服务的性能指标，Grafana 展示调用关系与性能瓶颈，Node Exporter 监控服务所在节点状态；
3. **基础设施监控**：服务器、网络设备、数据库等，收集性能指标与状态信息；
4. **业务应用监控**：用户访问量、响应时间、错误率等，Grafana 图表展示助业务团队决策；
5. **告警和通知**：基于 Prometheus 告警规则与 Grafana 告警通知，指标超阈值时及时通知。

原文"性能监控体系的优点"：三者适用于各种需要实时监控和管理的场景，无论云原生、微服务还是传统基础设施与业务应用，都能实现高效、灵活的监控。

【为什么？】
把 5 个场景放在一起看，会发现这套体系真正的优点是**"同一个模型覆盖从主机到业务的全栈"**：

| 场景 | 监控对象 | 指标来源 | 谁来看 |
|---|---|---|---|
| 云原生/容器 | 节点 + 容器 | Node Exporter（节点）+ cAdvisor（容器） | 运维 OnCall |
| 微服务 | 服务实例 | 应用 `/metrics`（如 Actuator/微服务框架）+ Exporter | 开发/测试/运维 |
| 基础设施 | 服务器/网络/DB | Node Exporter + 各类中间件 Exporter | 运维 |
| 业务应用 | 业务指标 | 应用自定义指标（QPS、下单成功数…） | 业务/产品/测试 |
| 告警通知 | — | 规则（PromQL）+ 通知渠道 | 全员 |

对测试开发岗来说，重点是第 3 条与第 4 条的组合：**压测时你要同时看"基础设施指标"（CPU/IO/网络）和"业务指标"（RT/TPS/错误率）**，而这两类恰好就是这套体系的两侧。换句话说，**学这套体系不是为了当运维，而是为了让自己的压测结论有据可依**——这正是本模块放在"性能测试"课程里的原因。

【必须掌握】

| 场景（原文 5 条） | 对压测的用法 |
|---|---|
| 云原生/容器监控 | 压测容器化服务时，看容器与节点的双层指标（注意 cgroup 限制） |
| 微服务监控 | 压测单服务时，看它的实例指标；多服务时看调用链（[[Ch39-性能监控系统价值]]） |
| 基础设施监控 | 压测前确认环境基线；压测中找资源瓶颈 |
| 业务应用监控 | 压测的业务指标（RT/TPS/错误率）与 SLA 对照 |
| 告警和通知 | 压测中阈值告警（如错误率 > 1%）——不必全程盯屏 |

| 优点 | 体现 |
|---|---|
| 覆盖面广 | 主机 / 容器 / 中间件 / 业务，一套模型通吃 |
| 可扩展 | 新的监控对象＝新 Exporter（或自研 `/metrics`） |
| 时间序列能力 | 历史对比、趋势分析、跨实例聚合（PromQL） |
| 可视化与告警 | Grafana 看板 + 阈值通知，团队共享同一份事实 |

【企业场景】
一次"上线前压测"的完整用法：压测前用这套体系看**过去两周**的 CPU/内存趋势（确定基线是否异常）；压测中看**实时**的 CPU/IO + JMeter 指标（找拐点）；压测后看**压测窗口**的曲线（写报告）。**同一份数据三个时段三种用法**——这就是"时间序列 + 看板"相比"手工敲命令"的根本优势。

【面试考察】
面试官："这套监控体系能用在哪些场景？对测试工作有什么帮助？"

参考回答框架：
1. 场景：容器/云原生、微服务、基础设施、业务应用、告警通知（一套模型覆盖全栈）；
2. 优点：覆盖面广（Exporter 模式可扩展）、时间序列能力（趋势/对比/聚合）、可视化与告警；
3. 对测试的用法：压测前采基线、压测中实时找拐点与瓶颈层、压测后留证据写报告；
4. 加分：容器场景要注意 cgroup 视角；告警阈值要有依据（SLA/历史数据）。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 认为监控体系只服务运维 | 测开用它是为了压测的数据可信与结论可交付 |
| 压测只看实时曲线 | 还要看历史（基线是否异常）与压测窗口（归档与对比） |
| 用一套阈值套所有环境 | 阈值应基于环境/SLA/历史基线，不能照抄 |
| 忽略 cgroup/虚拟化视角 | 容器与虚拟机的指标与宿主不同层，结论要说明视角 |
| 只监控被测服务，不监控下游依赖 | 链路下游（DB/缓存/第三方）的指标缺失会导致误判 |

【我的理解】引导题（用自己的话回答）：
1. 请把"压测前 / 压测中 / 压测后"三个阶段各自要看的指标列一下，并说明数据来自哪个组件。
2. 为什么说这套体系对测试岗的价值是"让压测结论可交付"，而不是"学会当运维"？

---

### 知识点3：搭建四步（Prometheus → Node Exporter → Grafana → 数据源）

【课程原话/定义】
课程给出的搭建步骤（原文）：
1. 创建 Prometheus 服务（见前面章节，已有部署 Prometheus 的完整教程）；
2. 创建并启动 Node Exporter 服务：
   - 下载镜像 `docker pull prom/node-exporter`；
   - 生成容器 `docker run -d --name node_exporter -p 9100:9100 prom/node-exporter`；
   - 检验容器是否启动成功：`docker ps`；打开浏览器输入 `localhost:9100` 查看是否有数据；
3. 创建 Grafana 服务：
   - 下载镜像 `docker pull grafana/grafana`；
   - 创建容器 `docker run -d -p 3000:3000 --name=<docker name> -v <your local folder>:/var/lib/grafana grafana/grafana`；
   - 检验容器：`docker ps`；浏览器输入 `localhost:3000` 判断能否进入 Grafana 管理页面；
4. 配置 Grafana 数据源（原文此处有多张截图）。

【为什么？】
四步的顺序**不能颠倒**，因为每一步都为下一步提供依赖：Prometheus 提供存储与查询 → Node Exporter 提供数据源 → Grafana 提供展示 → 数据源配置把两端接上。把每一步的"验收点"补齐，才是可交付的搭建：

| 步 | 命令 | 验收点（缺一不可） |
|---|---|---|
| 1 Prometheus | 见 [[Ch40-搭建服务端性能监控系统Prometheus]] | `/targets` 能打开（即使暂时只有自己一个 target） |
| 2 Node Exporter | `docker pull prom/node-exporter`；`docker run -d --name node_exporter -p 9100:9100 prom/node-exporter` | 浏览器 `主机IP:9100/metrics` 出现大量 `node_*` 指标文本 |
| 3 Grafana | `docker pull grafana/grafana`；`docker run -d -p 3000:3000 --name grafana -v <本地目录>:/var/lib/grafana grafana/grafana` | `主机IP:3000` 能进登录页（默认 admin/admin） |
| 4 接数据源 | Grafana → Data Sources → Prometheus → 填 URL → Save & Test | 页面提示数据源可用 |
| 5（补）加 job | 在 `prometheus.yml` 里加 `job_name: linux` + `targets: ['<Node Exporter地址>:9100']` | Prometheus `/targets` 出现该 target 且为 **UP** |

**关键细节（最容易卡住人的地方）**：
1. **地址要用"容器可达"的地址**：Grafana 容器里填 `http://localhost:9090` 会失败（那是容器自己）；Prometheus 容器里填 `localhost:9100` 也会失败（同理）。用**宿主机 IP**，或把几个容器放进同一个自定义 `docker network` 用**容器名**互访，或加 `--add-host=host.docker.internal:host-gateway`；
2. **`9100` 要能看到指标文本才算成功**：只显示"网页打不开/空白"通常意味着端口没映射或容器没起；
3. **Grafana 卷必须挂**（原文已有 `-v`）：否则看板与数据源配置会随容器消失。

【必须掌握】

| 组件 | 镜像（小写！） | 端口 | 关键参数/挂载 | 验证 |
|---|---|---|---|---|
| Prometheus | `prom/prometheus` | 9090 | `-v <配置目录>:/etc/prometheus`，`-v <数据目录>:/prometheus` | `/targets`、`/graph` |
| Node Exporter | `prom/node-exporter` | 9100 | 一般无需挂载 | `主机IP:9100/metrics` 有 `node_*` 文本 |
| Grafana | `grafana/grafana` | 3000 | `-v <本地目录>:/var/lib/grafana` | `主机IP:3000` 登录页 |
| Grafana 数据源 | — | — | URL 必须是**容器可达**的 Prometheus 地址 | Save & Test 通过 |

【企业场景】
把这三步写成一个 `docker-compose.yml`（企业标准做法）后，整个监控栈"一条命令拉起"，配置进 Git，换机器 5 分钟重建。压测环境尤其需要这种可复制性：**每次压测前用它一键恢复监控环境，压完删除**，既不污染环境又能保证每轮压测的监控口径一致（口径一致才能跨轮次对比）。

【面试考察】
面试官："主机监控体系怎么搭？有哪些坑？"

参考回答框架：
1. 四步：Prometheus（9090）→ Node Exporter（9100，暴露主机指标）→ Grafana（3000，挂载 `/var/lib/grafana`）→ Grafana 配 Prometheus 数据源（Save & Test）；
2. 关键坑：容器内地址要"容器可达"（不能写 localhost）；镜像名小写；Grafana 必须挂卷；9100 要能输出指标文本才算采集成功；
3. 实践：用 docker-compose 固化 + 配置入 Git，保证可复现与口径一致；
4. 收口：分层验证（9100 → 9090 → 3000），每一步都有明确的验收点。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| Grafana 数据源填 `http://localhost:9090` | 容器内 localhost＝容器自身；要用宿主 IP / 容器名 / host.docker.internal |
| Prometheus 的 targets 填 `localhost:9100` | 同样的道理；Node Exporter 在另一个容器里 |
| 只看 `docker ps` 就认为组件可用 | 要按验收点验证（9100 出指标文本、9090 targets UP、3000 能登录） |
| 镜像名写大写（`prom/Prometheus`） | Docker 仓库名必须小写，否则拉取直接失败 |
| 不挂 Grafana 数据卷 | 容器重建即丢看板与数据源配置 |

【我的理解】引导题（用自己的话回答）：
1. 请写出"9100 → 9090 → 3000"这条链上每一步的验证方式，并说明哪一步失败分别意味着什么。
2. 为什么在容器里"localhost"经常是错的？说出三种正确的写法。

---

### 知识点4：常见指标（9 类）与 Node Exporter 指标名对照

【课程原话/定义】
课程给出的"常见指标"（原文 9 条）：
1. **CPU 使用率（CPU Usage）**：反映 CPU 的繁忙程度，是评估系统性能的重要指标之一；
2. **内存使用率（Memory Usage）**：显示系统内存的使用情况，高内存使用率可能导致性能下降；
3. **磁盘 I/O（Disk I/O）**：衡量磁盘读写操作的效率，对于存储密集型应用至关重要；
4. **网络带宽（Network Bandwidth）**：反映网络传输数据的能力，是网络应用的关键指标；
5. **响应时间（Response Time）**：衡量系统或应用对请求的处理速度，直接影响用户体验；
6. **并发连接数（Concurrent Connections）**：同时与服务器建立连接的客户端数量，对评估服务器负载很重要；
7. **错误率（Error Rate）**：运行过程中发生的错误数量或比例，帮助识别潜在问题；
8. **吞吐量（Throughput）**：单位时间内处理的事务数量或数据传输量，反映系统的处理能力；
9. **资源利用率（Resource Utilization）**：综合评估 CPU、内存、磁盘、网络的使用情况，判断系统是否得到有效利用。

【为什么？】
这 9 类指标其实就是"**机器指标（1~4、9）+ 业务指标（5~8）**"两组。它们要**成对出现**才有意义：
- 业务指标告诉你"**用户感受到什么**"（RT、错误率、吞吐量、并发连接）；
- 机器指标告诉你"**为什么**"（CPU、内存、磁盘、网络、资源利用率）。

把机器指标翻译成 Prometheus 里真实的指标名（这是原文没有、但你动手必须要的东西，官方 Node Exporter 标准指标）：

| 指标类（原文） | Node Exporter 指标名（示例） | 常用 PromQL 思路 |
|---|---|---|
| CPU 使用率 | `node_cpu_seconds_total{mode=...}` | `1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))` |
| 内存使用率 | `node_memory_MemAvailable_bytes`、`node_memory_MemTotal_bytes` | `1 - MemAvailable / MemTotal` |
| 磁盘 IO | `node_disk_io_time_seconds_total`、`node_disk_read/write_bytes_total` | 用 `rate()` 求 %util 近似与吞吐 |
| 磁盘空间 | `node_filesystem_avail_bytes`、`size_bytes` | `1 - avail/size`（按 mountpoint 过滤） |
| 网络带宽 | `node_network_receive_bytes_total`、`node_network_transmit_bytes_total` | `rate(...)` 得字节/秒 |
| 负载 | `node_load1` / `node_load5` / `node_load15` | 与 `count(node_cpu_seconds_total{mode="idle"})` 比 |
| 目标存活 | `up` | `up{job="linux"}` 为 1 表示采集正常 |

**两个必须提醒的点**：① 这些 `*_total` 指标都是**累计计数器**，画图要用 `rate()`/`irate()` 求"速率"，直接画累计值会得到一条一直上涨的曲线（这是"看板数字不对"的头号原因，见 [[Ch41-搭建数据分析系统Grafana]] 知识点5）；② 压测时"响应时间/吞吐量/错误率"这些**业务指标不来自 Node Exporter**，而来自 JMeter（见 [[Ch43-jmeter实时压测结果收集]]）——**两类指标必须同时上板**。

【必须掌握】

| 组 | 指标（原文 9 类） | 数据来源 | 用途 |
|---|---|---|---|
| 机器 | CPU 使用率 / 内存使用率 / 磁盘 IO / 网络带宽 / 资源利用率 | Node Exporter → Prometheus | 找瓶颈层、判断是否饱和 |
| 业务 | 响应时间 / 并发连接数 / 错误率 / 吞吐量 | JMeter → InfluxDB（或应用 `/metrics`） | 判断用户体验与 SLA |
| 采集健康 | `up`、target 状态 | Prometheus 自身 | 确认"数据可信"的第一道检查 |

【企业场景】
压测看板上的经典布局就是按这两组分的：上半屏业务（TPS、RT P95/P99、错误率），下半屏机器（CPU us/sy/wa、内存 available、%util、网卡收发）。**看图表时先看业务（用户是否受影响），再看机器（瓶颈在哪一层）**——这个顺序能避免"盯着 CPU 看半天却没意识到用户已经报错了"。

【面试考察】
面试官："压测监控里你会看哪些指标？它们分别来自哪里？"

参考回答框架：
1. 分两组：机器指标（CPU/内存/磁盘/网络/利用率，来自 Node Exporter → Prometheus）与业务指标（RT/吞吐量/错误率/并发连接，来自 JMeter 或应用 `/metrics`）；
2. 关键要点：`*_total` 是累计值，必须用 `rate()`；CPU 使用率通常用 `1 - idle` 计算；内存看 `MemAvailable`；
3. 用法：先看业务恶化时间点，再对齐机器指标定位瓶颈层；用 `up` 确认采集健康；
4. 收口：两类指标必须在同一时间轴、同一看板，否则结论不可靠。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 直接画 `node_cpu_seconds_total` 或 `*_total` | 那是累计计数器；CPU 使用率要用 `rate()` + `idle` 反算 |
| 只看机器指标 | 业务指标（尤其是**分位值** RT 与错误率）才代表用户体验 |
| 只看业务指标 | 无法定位瓶颈层（CPU？IO？还是施压机？） |
| 用 `node_memory_MemFree_bytes` 判断内存 | 应看 `MemAvailable`（含可回收缓存，与 `free` 命令同一口径） |
| 忘记看 `up` / targets 状态 | 数据缺失会让曲线"看起来正常"（其实是断的） |

【我的理解】引导题（用自己的话回答）：
1. 请写出"CPU 使用率"的 PromQL 思路，并解释为什么要用 `1 - idle`。
2. 为什么"响应时间、吞吐量、错误率"不能从 Node Exporter 拿？它们该从哪里来？

---

### 知识点5：验证、压测落地与常见坑

【课程原话/定义】
课程总结（原文）：三者适用于各种需要实时监控和管理的场景，无论云原生、微服务还是传统基础设施和业务应用，都能通过这个体系实现高效、灵活的监控。

【为什么？】
本章的成果必须落到"压测时我能不能用它"，因此需要一份**压测前中后检查清单**。这份清单把本章所有知识点串起来，也是你交付监控环境的验收标准：

| 阶段 | 检查项 | 标准 |
|---|---|---|
| 压测前 | 三个组件容器均 Up | `docker ps` 三个 Up |
| 压测前 | 9100 出指标文本 | `主机IP:9100/metrics` 有 `node_*` |
| 压测前 | Prometheus `/targets` 全 UP | 无 DOWN、Last Scrape 在刷新 |
| 压测前 | 抓取间隔按需调细 | 压测期建议 5s（默认为 15s） |
| 压测前 | Grafana 数据源 Save & Test 通过、看板可出图 | 面板有数据、刷新间隔设 5s/10s |
| 压测前 | 采基线 | 空载 CPU/内存/连接数，记录机器规格 |
| 压测中 | 业务 + 机器指标同屏观测 | 找拐点、按需告警 |
| 压测后 | 归档看板截图与数据 | 进报告，可复核 |
| 压测后 | 环境清理（可选） | 容器/数据卷按需清理（注意别删了要留的数据） |

**另外提醒一个"体系自身"的取舍**：Node Exporter + Prometheus 的组合会有**自身的资源开销**（Prometheus 的 TSDB 写入、Exporter 的采集）。被测机装 Node Exporter 属于标准做法（开销很小），但 **Prometheus 本体不要部署在被压机器上**，否则它的写入与查询会和被测服务抢资源，污染指标。

【必须掌握】

| 类别 | 检查/动作 | 说明 |
|---|---|---|
| 采集健康 | `9100/metrics`、`/targets` 全 UP、`up` 指标 | 数据可信的第一道关 |
| 展示健康 | 数据源 Save & Test、面板有数、刷新间隔 | 避免"看图却看不到实时" |
| 口径正确 | `rate()` 求速率、`MemAvailable` 看内存、分位值看 RT | 避免"数字看着不对" |
| 部署纪律 | Prometheus 不与被测服务同机 | 避免监控自身污染指标 |
| 归档 | 截图 + 数据导出 | 报告的复核依据 |

【企业场景】
面试时如果被问"你怎么保证压测数据可信"，可以给出一份完整回答：**"① 监控链路三层验证（9100 → 9090 → 3000）；② 采集间隔按压测需要设置为 5s；③ 业务指标（JMeter→InfluxDB）与机器指标（Node Exporter→Prometheus）在同一块 Grafana 看板上对齐时间轴；④ 采前基线、压中实时、压后归档；⑤ Prometheus 不部署在被测机上。"** ——这段回答覆盖了工具、数据、纪律三个层面，是很有说服力的工程化表达。

【面试考察】
面试官："监控环境搭好后，你怎么确认它真的可用于压测？"

参考回答框架：
1. 三层验证：采集（9100 出指标）→ 拉取（`/targets` 全 UP、`up`=1）→ 展示（数据源通、面板有数）；
2. 配置适配：抓取间隔调细（5s）、刷新间隔调快（5s/10s）、时间范围与压测窗口对齐；
3. 口径检查：`rate()`、`MemAvailable`、分位值 RT；
4. 部署纪律：Prometheus 不与被测服务同机；采基线；压后归档；
5. 收口：把上述写成压测执行清单，形成团队标准动作。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 把 Prometheus 装在被压机器上 | 监控自身开销会污染被测指标；应分离部署 |
| 压测前不检查 targets | 数据缺失到最后才发现，只能重压 |
| 抓取间隔沿用默认 15s | 30 分钟压测只有 120 个点，毛刺被抹平 |
| 压测结束就把容器删掉 | 数据（尤其 InfluxDB/Prometheus 卷里的历史）可能还需要；先导出归档 |
| 认为"能看图"就万事大吉 | 还要确认口径、间隔、时间对齐与基线，否则图会误导决策 |

【我的理解】引导题（用自己的话回答）：
1. 请设计一份"压测前监控环境检查清单"（不少于 6 条），并说明每条防止什么事故。
2. 为什么"Prometheus 不与被测服务同机"是一条纪律？同机会造成什么后果？

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 三件套分工 | Node Exporter（9100 采集暴露）→ Prometheus（9090 拉取存储查询）→ Grafana（3000 可视化告警）；Exporter 模式可扩展 | ★★★★★ |
| 应用场景与优点 | 容器/微服务/基础设施/业务/告警；一套模型覆盖全栈、时间序列能力 | ★★★★☆ |
| 搭建四步 | Prometheus → Node Exporter（`prom/node-exporter`，9100）→ Grafana（挂 `/var/lib/grafana`）→ 配置数据源（地址要容器可达） | ★★★★★ |
| 常见指标 | 9 类（机器 5 + 业务 4）；Node Exporter 指标名（`node_cpu_seconds_total` 需 `rate()`、`MemAvailable`、`node_load1`、`up`） | ★★★★★ |
| 验证与落地 | 三层验证（9100 → 9090 → 3000）+ 压测前中后清单 + 部署纪律（Prometheus 不与被测同机） | ★★★★★ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】`localhost:9100` 查看 Node Exporter 是否有数据（原文 1 张）
> 📷 【截图占位】`localhost:3000` 进入 Grafana 管理页面（原文 1 张）
> 📷 【截图占位】配置 Grafana 数据源（原文 9 张）

## 关联笔记

- [[Ch40-搭建服务端性能监控系统Prometheus]]（Prometheus 本体的部署与配置）
- [[Ch41-搭建数据分析系统Grafana]]（Grafana 的部署、数据源与看板）
- [[Ch39-性能监控系统价值]]（为什么需要监控体系、选型逻辑）
- [[Ch38-系统性能数据收集（cpu、mem、net、io）]]（Node Exporter 采集的指标与手工命令的对应关系）
- [[Ch43-jmeter实时压测结果收集]]（业务指标侧：JMeter + InfluxDB + Grafana）
- [[../L1-服务端统计工具/Ch35-性能分析系统级别指标io cpu mem net|L1 Ch35-性能分析系统级别指标io cpu mem net]]（指标口径与判读）
- [[../L1-性能测试体系/Ch05-行业流行性能监控工具介绍|L1 Ch05-行业流行性能监控工具介绍]]（Prometheus + Grafana 在工具全景中的位置）
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
