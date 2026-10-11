---
tags: [课程笔记, 性能测试, 性能监控, Prometheus]
course: "性能测试"
chapter: "Ch40-搭建服务端性能监控系统Prometheus"
created: 2026-10-11
status: draft
---

# Ch40 - 搭建服务端性能监控系统Prometheus

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L2-性能监控体系（站点：**性能监控** / `L2/tutorial`）
- 站点页：性能监控 / L2 → 搭建服务端性能监控系统Prometheus
- 前置：[[Ch39-性能监控系统价值]]（选型：为什么是 Prometheus）、[[Ch38-系统性能数据收集（cpu、mem、net、io）]]（要采集哪些指标）
- 后续：[[Ch41-搭建数据分析系统Grafana]]（把它画成看板）、[[Ch42-Prometheus监控系统部署应用实战]]（加 Node Exporter 采主机指标）

> 📌 内容缺口提示：站点该页正文约 1 100 字 + **1 张截图**，"如何搭建"只有 4 条命令 + 一段 YAML，**没有解释 YAML 每个字段的含义，也没有讲 Prometheus 的工作模型（pull / exporter / 时序库）、验证页面、数据持久化**。本笔记按原文整理，机制与验证部分依据 **Prometheus 官方文档**（`prometheus.io/docs`）的标准语义补齐。

> ⚠️ 课程原文勘误（3 处，本页最值得带走的部分）：
> 1. `docker pull prom/Prometheus` —— **大写 P 会导致拉取失败**（Docker 仓库名必须小写，会报 `invalid reference format: repository name must be lowercase`）。正确写法：**`docker pull prom/prometheus`**。
> 2. YAML 里 `scrape_interval:60s` / `evaluation_interval: 60s` —— **冒号后必须留空格**（YAML 语法要求 `键: 值`），写成 `scrape_interval:60s` 会导致配置解析失败。正确写法：`scrape_interval: 60s`。
> 3. `docker run ... -v <local folder>:/etc/Prometheus prom/Prometheus` —— **容器内配置目录是小写 `/etc/prometheus`**（配置文件为 `/etc/prometheus/prometheus.yml`）；写 `/etc/Prometheus` 挂载点对不上，容器会用默认配置（表现为"改了配置却不生效"）。

---

### 知识点1：Prometheus 是什么，解决什么问题

【课程原话/定义】
Prometheus 是一套开源的系统监控和报警框架，它受启发于 Google 的 **Brogmon** 监控系统。凭借其高性能、可扩展性和灵活性等特点，在各种监控场景中都能发挥出色的作用，帮助用户更好地管理和维护他们的系统和应用。

课程给出的"应用场景"（原文 7 条）：
1. **云原生和容器化环境监控**：CNCF 成员，与 Kubernetes 等容器编排系统天然集成，可监控 Pods/Services/Nodes；
2. **微服务架构监控**：多维数据模型 + 灵活查询语言，快速定位性能瓶颈与故障点；
3. **基础设施监控**：服务器、数据库、网络设备等，收集 CPU/内存/磁盘等指标并提供可视化界面；
4. **业务应用监控**：请求响应时间、吞吐量、错误率等关键指标；
5. **告警和通知**：内置告警功能，按规则触发并通过多种方式通知；
6. **混合云和多云环境监控**：通过 Exporter 与集成工具收集不同云平台的资源数据，提供统一视图；
7. **自定义监控需求**：丰富的 Exporter 组件与 API，支持定制监控方案（特定应用、中间件、自定义指标）。

【为什么？】
这 7 条场景背后是同一个设计选择：**Prometheus 用"指标 + 标签"的模型把所有监控对象拉平**。

传统监控（如老的 Zabbix 式主机监控）里，"我的机器的 CPU"和"你的机器的 CPU"是两条独立的、结构不同的记录；而 Prometheus 里它们是**同一条指标名 `node_cpu_seconds_total` 的两个时间序列**，靠标签区分：

```
node_cpu_seconds_total{instance="10.0.0.11:9100", mode="user"}
node_cpu_seconds_total{instance="10.0.0.12:9100", mode="user"}
```

这就是课程反复强调的"**多维数据模型**"（由指标名称和键/值对标签标识的时间序列数据组成）。它带来的直接好处是：**同一条查询语句可以跨机器/跨实例聚合、对比、下钻**（例如"所有实例的 CPU 使用率 Top 5"），而不必为每台机器写一条规则。你压测时想要"横向对比 3 台应用机的 CPU"，或"看压测窗口内所有实例的 P99 变化"，靠的就是这个模型。

"受启发于 Google Brogmon"这句也值得记：它决定了 Prometheus 的两条基本性格——**服务发现 + 拉取（pull）**，以及**适合记录"数字化的时间序列"而不是日志文本**（日志归 ELK/Loki，链路归 SkyWalking/Zipkin，见 [[Ch39-性能监控系统价值]]）。

【必须掌握】

| 场景（原文 7 条） | Prometheus 里的对应机制 |
|---|---|
| 云原生/容器监控 | Kubernetes 服务发现 + 各类 Exporter（cAdvisor 等） |
| 微服务监控 | 多维数据模型 + PromQL（按服务/实例/接口标签聚合） |
| 基础设施监控 | Node Exporter（主机）、各类中间件 Exporter |
| 业务应用监控 | 应用暴露 `/metrics` 端点（如 Spring Boot Actuator） |
| 告警通知 | 告警规则（rules）+ Alertmanager（分组、抑制、静默、路由） |
| 混合云/多云 | 各云厂商 Exporter，统一拉取视图 |
| 自定义监控 | 自研 Exporter / Pushgateway（批处理任务） |

| 记住这四条"性格" | 含义 |
|---|---|
| 拉取（pull） | Prometheus 主动去目标的 `/metrics` 抓数据（而不是被推送） |
| Exporter | 把各种被监控对象的指标"翻译"成 Prometheus 能拉的 HTTP 端点 |
| 时序数据库（TSDB） | 自带存储，按时间序列保存；有保留期（默认 15 天） |
| PromQL + Alertmanager | 查询语言用于分析与告警规则；Alertmanager 负责通知与降噪 |

【企业场景】
你在压测环境有 3 台应用机 + 1 台 DB。传统做法是每台机器 ssh 上去 `top`（低效且无法回溯）；Prometheus 做法：每台装 Node Exporter（9100），Prometheus 配置一个 `job_name: linux`、targets 列出 4 个地址，于是"4 台机器的 CPU/内存/磁盘"变成同一条指标的不同标签——在 Grafana 上一个面板能画 4 条线，加一个变量就能按机器筛选。**"部署一次、横向对比所有机器"正是多维模型的工程价值。**

【面试考察】
面试官："Prometheus 是什么？它的数据模型有什么特点？"

参考回答框架：
1. 定位：开源系统监控与报警框架，源自 Google Borgmon，CNCF 项目，K8s 生态亲和；
2. 数据模型：**指标名 + 键值对标签**组成的多维时间序列，同一指标可跨实例聚合/对比/下钻；
3. 工作方式：**pull（主动拉取）** 目标的 `/metrics`，靠各类 Exporter 暴露指标；自带 TSDB 存储；PromQL 查询；Alertmanager 告警；
4. 适用边界：适合指标（Metrics）；日志与链路要用 ELK/Loki 与 SkyWalking/Zipkin（见 [[Ch39-性能监控系统价值]]）。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 把 Prometheus 当"日志系统" | 它存的是**数值型时间序列**；日志与链路是另一层（Logs / Traces） |
| 认为 Prometheus 是 push 模型（像 Zabbix 主动上报） | 默认是 **pull**：Prometheus 主动抓 `/metrics`；批处理任务才用 Pushgateway |
| 忽略"标签"的重要性 | 多维模型的价值全在标签（instance/job/自定义标签）；标签乱起会让查询无法聚合 |
| 认为装了 Prometheus 就有数据 | 还得有 **Exporter 或 `/metrics` 端点**可供拉取，否则 targets 全是 DOWN |
| 忽略数据保留期 | TSDB 默认保留期有限，压测历史数据会过期，重要数据需导出或延长保留 |

【我的理解】引导题（用自己的话回答）：
1. 用"多条时间序列 + 标签"解释：为什么 Prometheus 能做到"一条查询跨 4 台机器"？
2. 为什么说"指标 / 日志 / 链路"是三件事？把 Prometheus 放错位置会有什么后果？

---

### 知识点2：核心概念与工作模型（job / target / 拉取 / PromQL）

【课程原话/定义】
（原文未系统讲机制，本节按官方语义补齐，用于解释下一节的 YAML。）

【为什么？】
要读懂 `prometheus.yml`，只需要搞清 5 个概念，它们是**层层包含**的关系：

1. **Target（目标）**：一个可被拉取的地址，如 `localhost:9090`（Prometheus 自己）或 `10.0.0.11:9100`（Node Exporter）；
2. **Job（作业）**：一组同类 target 的名字（如 `job_name: 'prometheus'`、`job_name: linux`）——**job 是"我按什么用途分组"**，查询时常用它过滤；
3. **Instance（实例）**：每个被拉取的具体目标标识（默认是 `host:port`），对应标签 `instance`；
4. **Scrape（抓取）**：Prometheus 按 `scrape_interval`（默认 15s）去每个 target 的 `/metrics` 拉一次数据；
5. **Rule Evaluation（规则求值）**：按 `evaluation_interval` 计算告警规则与记录规则——**注意这两个间隔是独立的**：抓取间隔决定数据密度，求值间隔决定告警灵敏度。

另外两个必知的组件：
- **PromQL**：查询语言（`rate(node_cpu_seconds_total{mode="user"}[5m])` 之类），Grafana 面板与告警规则都写它；
- **Alertmanager**：独立组件，负责告警的**分组/抑制/静默/路由**（不是 Prometheus 自己发通知）。

【必须掌握】

| 概念 | 含义 | 在 YAML / 界面里的位置 |
|---|---|---|
| Target | 一个可拉取的地址 | `static_configs.targets` |
| Job | 一组同类 target 的用途分组 | `job_name` |
| Instance | 具体目标标识（默认 host:port） | 自动生成标签 `instance`，也可用 `labels` 覆盖 |
| Labels | 键值对标签（多维模型的维度） | `labels:` 段，或在规则/relabel 中生成 |
| scrape_interval | 抓取间隔（默认 15s） | `global.scrape_interval`（可被 job 覆盖） |
| evaluation_interval | 规则求值间隔 | `global.evaluation_interval` |
| PromQL | 查询语言 | 界面 `/graph`、Grafana 面板、告警规则 |
| Alertmanager | 告警路由与降噪 | 独立部署，由 Prometheus 配置 `alerting` 指向 |
| 验证入口 | `/targets`（目标状态 UP/DOWN）、`/graph`（查询）、`/metrics`（自身指标） | 浏览器访问 9090 端口 |

【企业场景】
压测时你会用 `/targets` 页面做一次"体检"：确认所有 target 都是 **UP**（绿色）。如果某个应用机是 DOWN，那台机器的曲线在压测中会**断掉**——等你压完复盘才发现"数据缺了一段"，只能重压。**"压测前检查 targets 全 UP"和"压测前采集基线"是同一条纪律。** 另外，压测用的抓取间隔要提前调小（如 5s）——默认 15s 对 30 分钟的压测来说，很多瞬时尖刺会被平均掉（对照 [[Ch38-系统性能数据收集（cpu、mem、net、io）]] 里"采集间隔由现象尺度决定"）。

【面试考察】
面试官："Prometheus 是怎么采集数据的？scrape_interval 和 evaluation_interval 有什么区别？"

参考回答框架：
1. 模型：pull 模型，Prometheus 按 `scrape_interval` 周期性抓取各 target 的 `/metrics`；
2. 层级：target（地址）→ job（用途分组）→ instance（具体实例），标签构成多维模型；
3. 两个间隔：`scrape_interval` 决定**数据密度**（影响曲线精细度）；`evaluation_interval` 决定**告警/记录规则的求值频率**（影响告警灵敏度）；
4. 验证：`/targets` 看 UP/DOWN；`/graph` 用 PromQL 查询；datasource 给 Grafana；告警交给 Alertmanager。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 把两个 interval 当成一个 | `scrape_interval`（抓数据）≠ `evaluation_interval`（算规则），作用完全不同 |
| 压测用默认 15s 抓取间隔 | 30 分钟压测 + 15s 间隔 = 只有 120 个点，秒级毛刺会被抹掉；按现象尺度调小 |
| 只把 job 当"名字"随便起 | job 是查询与告警的常用过滤维度；命名要能表达"用途/环境" |
| 认为 Prometheus 自己会发通知 | 通知由 **Alertmanager** 负责（分组、抑制、静默、路由） |
| 装了 Prometheus 就以为有主机指标 | 主机指标要靠 **Node Exporter**（9100）暴露（见 [[Ch42-Prometheus监控系统部署应用实战]]） |

【我的理解】引导题（用自己的话回答）：
1. 用"job / target / instance / label"四个词解释：为什么同一条 PromQL 能查所有机器的 CPU？
2. 如果压测时 `/targets` 里有一台机器是 DOWN，你的报告会遇到什么问题？

---

### 知识点3：搭建步骤（原文 4 步 + YAML 逐行解读）

【课程原话/定义】
课程给出的 4 步（原文）：
1. 拉取 Prometheus 镜像 `docker pull prom/Prometheus`（⚠️ 勘误：应为小写 `prom/prometheus`）；
2. 创建一个 `Prometheus.yml` 配置文件：

```yaml
global:
  scrape_interval:60s
  evaluation_interval: 60s

scrape_configs:
  - job_name: 'Prometheus'
    static_configs:
      - targets: ['localhost:9090']
        labels:
          instance: 'Prometheus'

  - job_name: linux
    static_configs:
      - targets: ['IP地址:9100']
        labels:
          instance: localhost

    #此处的ip地址是后面创建node_exporter容器的容器ip地址
    #查看容器ip的命令为docker network inspect bridge
```

3. 创建 Prometheus 容器：`docker run -d --name Prometheus -p 9090:9090 -v <local folder>:/etc/Prometheus prom/Prometheus`（⚠️ 勘误：容器内应为 `/etc/prometheus`）；
4. 检验容器是否创建成功且在运行：`sudo docker ps` 检测运行状态；打开浏览器输入 `localhost:9090` 查看是否存在数据。

【为什么？】
把这份 YAML 逐行读懂，比背 4 条命令重要得多（下面已修正冒号后的空格问题）：

| 位置 | 含义 | 注意点 |
|---|---|---|
| `global.scrape_interval: 60s` | 全局抓取间隔 | **压测前建议调到 5s**；YAML 冒号后必须有空格 |
| `global.evaluation_interval: 60s` | 告警/记录规则求值间隔 | 与抓取间隔独立 |
| `scrape_configs:` | 抓取任务列表 | 每个 `-` 是一个 job |
| `job_name: 'Prometheus'` | 监控自己 | Prometheus 自身也暴露 `/metrics`，默认抓 `localhost:9090` |
| `targets: ['localhost:9090']` | 目标地址列表 | 单元素列表也要用 `[]`；多目标用逗号分隔 |
| `labels: instance: 'Prometheus'` | 覆盖默认 instance 标签 | 让 Grafana 里的名字更可读（否则显示为 `host:port`） |
| `job_name: linux` + `targets: ['IP地址:9100']` | 主机指标任务 | **这里的 IP 是 Node Exporter 容器的地址**（原文注释说的） |
| `-v <local folder>:/etc/prometheus` | 挂载配置目录 | 目录挂载时，`prometheus.yml` 要放在该目录里；也可直接挂单个文件 |
| `-p 9090:9090` | 端口映射 | 宿主 9090 → 容器 9090（Prometheus Web 界面/接口） |

**一个必须提醒的工程习惯**：容器 IP 是**动态**的（容器重建就变），把 `targets` 写死成容器 IP，重启后就会 DOWN。企业做法有三选：① 用宿主机 IP + 端口映射；② 把 Prometheus 与 Exporter 放进同一个自定义 `docker network`，用**容器名**当 DNS；③ 用服务发现（K8s / 文件 SD）。这也是原文注释"查看容器 IP 的命令为 `docker network inspect bridge`"背后的**脆弱点**。

【必须掌握】

| 步骤 | 命令/动作 | 验证方式 |
|---|---|---|
| 1 拉镜像 | `docker pull prom/prometheus`（小写！） | 无报错即成功 |
| 2 写配置 | `prometheus.yml`（`scrape_interval: 5s` 压测期更细） | 用 YAML 校验（缩进/冒号空格）避免启动失败 |
| 3 起容器 | `docker run -d --name prometheus -p 9090:9090 -v <本地目录>:/etc/prometheus prom/prometheus` | `docker ps` 显示 Up |
| 4 验证 | 浏览器 `http://localhost:9090` → `/targets` 看 **UP**、`/graph` 试查询 | `/targets` 全 UP；/graph 能查到 `up` 指标 |
| 5 持久化（【扩展知识】） | `-v <数据目录>:/prometheus`，可加 `--storage.tsdb.retention.time=30d` | 容器重建后历史数据仍在 |
| 6 热加载（【扩展知识】） | 加 `--web.enable-lifecycle` 后 `curl -X POST localhost:9090/-/reload` | 改配置不必重启容器 |

【企业场景】
团队要把 Prometheus 接入压测流程，交付物不该只是"我起了一个容器"，而应包括：① `prometheus.yml` 纳入 Git（可评审、可复制）；② 一条可复现的 `docker run`（含卷与保留期参数）；③ 验证截图或 `/targets` 输出；④ 一份说明"抓取间隔为什么设 5s、数据保留 30 天"。**换一台机器按这四样东西 10 分钟能重建**，这才是"会搭建"的标准，也是面试里最容易被追问"你怎么保证可复现"的答案。

【面试考察】
面试官："Prometheus 怎么部署？配置文件里有哪些关键字段？"

参考回答框架：
1. 部署：Docker 拉取官方镜像 `prom/prometheus`（小写）→ 准备 `prometheus.yml` → `docker run -d -p 9090:9090 -v <dir>:/etc/prometheus` → 浏览器验证 `/targets`；
2. 配置关键字段：`global.scrape_interval`（抓取间隔）、`evaluation_interval`（规则求值）、`scrape_configs`（job → targets → labels）；
3. 实践要点：抓取间隔按现象尺度设置（压测 5s）；挂载 `/etc/prometheus` 保证配置生效；数据卷 `/prometheus` 持久化 + 保留期；
4. 注意：targets 里的容器 IP 会变（重建即失效），生产用容器名/服务发现/宿主机地址。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| `docker pull prom/Prometheus`（大写 P） | 仓库名必须小写 → `prom/prometheus`，否则拉取报错 |
| YAML 写成 `scrape_interval:60s` | 冒号后必须空格（`scrape_interval: 60s`），否则配置解析失败 |
| 挂载到 `/etc/Prometheus`（大写） | 容器内路径是小写 `/etc/prometheus`；挂错则配置不生效 |
| 把 targets 写成容器 IP 就完事 | 容器 IP 会变（重启/重建即失效）；用容器名 + 同一网络、宿主机 IP 或服务发现 |
| 不挂数据卷 | 容器删掉后历史数据丢失；压测历史数据无法复盘 |
| 改配置后重启容器才生效，压测中被中断 | 加 `--web.enable-lifecycle` 用 `/-/reload` 热加载（或压测间隙重启） |

【我的理解】引导题（用自己的话回答）：
1. 请指出原文 YAML 里两处会直接导致"起不来"或"配置不生效"的问题，并写出正确写法。
2. 为什么"targets 写容器 IP"在压测环境里很危险？三种更稳的做法分别是什么？

---

### 知识点4：验证与排查清单（起来了 ≠ 有数据）

【课程原话/定义】
原文第 4 步：通过 `sudo docker ps` 检测容器是否在运行；打开浏览器输入 `localhost:9090` 来查看是否存在数据。

【为什么？】
原文的验证只有"容器在跑 + 页面能打开"，但对监控系统来说，**这两条都过了也可能一条数据都没有**。真正的验证是三层的：

1. **容器层**：`docker ps` 看到 Up；`docker logs <name>` 里没有反复重启的错误（配置错误常表现为容器"启动了又退出"）；
2. **拉取层**：`/targets` 页面每个 target 的 State 是否为 **UP**，并且 **Last Scrape** 时间在刷新——DOWN 的话点开 Error 看原因（连接拒绝＝Exporter 没起/端口错；超时＝网络/防火墙）；
3. **数据层**：`/graph` 里查一个最基础的指标（如 `up`，值为 1 表示目标在线），能看到点；再查一个主机指标（如 `node_cpu_seconds_total`）确认 Node Exporter 的指标真的进来了。

**这条清单是"能演示的监控"和"能用的监控"的分界线**，也是你排查任何监控问题的通用顺序（容器 → 拉取 → 数据）。

【必须掌握】

| 层级 | 检查 | 异常时的常见原因 |
|---|---|---|
| 容器 | `docker ps`、`docker logs` | 配置语法错误 → 容器启动后退出；端口被占用 |
| 拉取 | `/targets` 的 UP/DOWN 与 Last Scrape | Exporter 未启动、端口不通、防火墙、targets 地址写错（容器 IP 变化） |
| 查询 | `/graph` 查 `up`、`node_cpu_seconds_total` | 无数据：job/target 配错、指标名写错、时间范围不对 |
| 配置生效 | 修改配置后 `/targets` 是否按预期变化 | 挂载路径错（大写 P）、未热加载/未重启 |
| 持久化 | 容器重建后历史数据是否仍在 | 未挂 `/prometheus` 数据卷 |

【企业场景】
一次真实的"监控假成功"：压测完大家打开 Grafana 发现"曲线是空的"，回头排查 `/targets` 才发现 Node Exporter 那个 job 从压测开始就是 DOWN（targets 里写的是上次的容器 IP）。**如果压测前按上面三层验证一遍，这个事故就不会发生。** 所以把"三层验证"写进压测执行清单（和 [[Ch38-系统性能数据收集（cpu、mem、net、io）]] 的采集脚本一起），是性价比极高的一条纪律。

【面试考察】
面试官："Prometheus 起来了但 Grafana 没数据，你怎么排查？"

参考回答框架：
1. 容器层：`docker ps` / `docker logs` 看是否真的稳定运行（配置错误会启动即退出）；
2. 拉取层：`/targets` 看目标是否 UP；DOWN 看 Error 原因（拒绝连接＝Exporter 未起；超时＝网络/防火墙；地址错＝IP 变化）；
3. 数据层：`/graph` 用 `up` 指标确认基础通路，再查业务指标名是否正确、时间范围是否覆盖；
4. 前端层：Grafana 数据源 URL 是否正确（容器内 `localhost` 指向容器自己，需要用宿主地址或容器名）、时间范围与变量；
5. 收口：形成"容器 → 拉取 → 数据 → 展示"的固定排查顺序，并写进压测检查清单。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 看到 9090 页面能打开就认为部署成功 | 还要看 `/targets`（UP）与 `/graph`（有数据），三层都要过 |
| `/targets` 全 DOWN 却先怀疑 Prometheus | 通常是 Exporter 没起、端口不通、或 targets 地址过期（容器 IP 变化） |
| 改完配置不生效，反复重启排查 | 先确认挂载路径正确（`/etc/prometheus`）与是否热加载 |
| Grafana 里填 `http://localhost:9090` 却连不上 | **容器里的 localhost 是容器自身**；要用宿主 IP / `host.docker.internal` / 同一 docker 网络里的容器名 |
| 不记录"部署方式与配置" | 换机器重搭全靠回忆；应把命令与配置入 Git |

【我的理解】引导题（用自己的话回答）：
1. 请写出"容器 → 拉取 → 数据"三层各自的检查命令或页面，以及每层失败时你会先怀疑什么。
2. 为什么在容器里用 `localhost` 访问宿主服务会失败？有哪几种修法？

---

### 知识点5：从"搭建"到"压测可用"（与后续章节的衔接）

【课程原话/定义】
课程总结（原文）：简介 / 应用场景 / 如何搭建 Prometheus 服务。

【为什么？】
本章搭出的 Prometheus 只是"记账本"，要在压测里发挥作用，还需要三步衔接：

1. **接指标源**：主机指标靠 **[Node Exporter](9100)**（[[Ch42-Prometheus监控系统部署应用实战]]）；应用指标靠应用暴露 `/metrics`（如 Spring Boot Actuator）；压测结果靠 **JMeter → InfluxDB**（[[Ch43-jmeter实时压测结果收集]]）；
2. **接展示**：Prometheus 作为**数据源**接进 **Grafana**（[[Ch41-搭建数据分析系统Grafana]]），用社区看板或自建面板出图；
3. **接流程**：把"压测前检查 targets 全 UP + 抓取间隔调细 + 采基线"写进压测执行清单。

**验收标准**：压测开始时，你能量化地说出"数据链路是通的"——`/targets` 全 UP、Grafana 面板有实时曲线、采集文件在增长。这三条同时成立，报告的可信度才有基础。

【必须掌握】

| 衔接对象 | 作用 | 章节 |
|---|---|---|
| Node Exporter（9100） | 暴露主机 CPU/内存/磁盘/网络指标 | [[Ch42-Prometheus监控系统部署应用实战]] |
| Grafana（3000） | 把 Prometheus 数据画成看板与告警 | [[Ch41-搭建数据分析系统Grafana]] |
| InfluxDB（8086）+ JMeter Backend Listener | 存压测结果（TPS/RT/错误率） | [[Ch43-jmeter实时压测结果收集]] |
| 压测流程纪律 | 压前验证、压中盯板、压后归档 | 本模块全部章节 + [[../L1-性能测试体系/Ch08-性能测试计划|L1 Ch08]] |

【企业场景】
把本章成果包装成简历/面试素材的写法：**"使用 Docker 部署 Prometheus（9090）作为指标存储与查询中心，配置 job/targets 采集多实例指标，抓取间隔按压测需要调整到 5s；结合 Node Exporter 与 Grafana 建立压测实时看板，压测期间追踪 TPS/RT/CPU/IO 曲线并定位瓶颈"**——这段话里每一个动作你都在本章与后续章节里真实做过，可复现、可追问，是简历上很硬的一条。

【面试考察】
面试官："你的 Prometheus 用在哪？怎么和压测结合？"

参考回答框架：
1. 定位：指标采集与存储中心（pull + TSDB + PromQL），为压测与生产提供统一指标视图；
2. 数据来源：Node Exporter（主机）、应用 `/metrics`、JMeter → InfluxDB（压测结果）；
3. 展示与告警：Grafana 看板 + 告警规则（Alertmanager 通知）；
4. 流程：压测前 targets 全 UP + 抓取间隔调细 + 采基线；压测中盯板定位；压测后归档数据与报告。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 搭完 Prometheus 就结束，不接数据源与看板 | 它只是"账本"；没有 Exporter / Grafana 就没有可视价值 |
| 只用 Prometheus 界面看数据 | 长期观测与分享要用 Grafana 看板（且能接多数据源） |
| 压测期间才想起来调抓取间隔 | 间隔要在压测前设置好；中途改配置可能丢失数据点 |
| 忽略指标"单位/口径" | CPU 使用率要算 `1 - rate(node_cpu_seconds_total{mode="idle"}[5m])`，口径不统一会让结论无法对比 |
| 认为部署一次永久可用 | 容器重启 IP 变化、保留期到期、Exporter 升级都会影响；需要巡检 |

【我的理解】引导题（用自己的话回答）：
1. 请用"账本 / 数据源 / 画图"三个词，把 Prometheus、Exporter、Grafana 的关系说清楚。
2. 如果只能保留一条压测监控纪律，你会保留哪一条？为什么？

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Prometheus 定位 | 开源监控报警框架（源起 Google Borgmon）；7 条应用场景；多维数据模型（指标 + 标签） | ★★★★★ |
| 核心概念 | target / job / instance / labels；pull 模型；scrape_interval 与 evaluation_interval；PromQL；Alertmanager | ★★★★★ |
| 搭建四步 | `docker pull prom/prometheus`（小写）→ 写 `prometheus.yml` → `docker run -p 9090:9090 -v <dir>:/etc/prometheus` → 浏览器验证 | ★★★★★ |
| 原文 3 处勘误 | 镜像名大写 / YAML 冒号后缺空格 / 挂载路径写成 `/etc/Prometheus` | ★★★★☆ |
| 验证与衔接 | 容器 → 拉取（`/targets` 全 UP）→ 数据（`/graph` 有值）三层验证；接 Node Exporter（9100）与 Grafana（3000） | ★★★★★ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】`localhost:9090` 查看 Prometheus 是否有数据（原文 1 张）

## 关联笔记

- [[Ch39-性能监控系统价值]]（为什么选 Prometheus + Grafana）
- [[Ch38-系统性能数据收集（cpu、mem、net、io）]]（要采集哪些指标；手工采集 vs 系统化采集）
- [[Ch41-搭建数据分析系统Grafana]]（下一步：把它画成看板）
- [[Ch42-Prometheus监控系统部署应用实战]]（加 Node Exporter，形成主机监控闭环）
- [[Ch43-jmeter实时压测结果收集]]（JMeter + InfluxDB + Grafana 实时看板）
- [[../L1-性能测试体系/Ch05-行业流行性能监控工具介绍|L1 Ch05-行业流行性能监控工具介绍]]（Prometheus + Grafana 在监控体系中的位置）
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
