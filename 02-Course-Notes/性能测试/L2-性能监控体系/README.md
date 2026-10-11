---
tags: [课程笔记, 性能测试, MOC, 性能监控, Prometheus, Grafana]
created: 2026-10-11
status: in_progress
---

# L2 · 性能监控体系（Prometheus + Grafana）

> 复习优先级：⭐⭐⭐ 投简历必掌握 · ⭐⭐ 重要加分 · ⭐ 了解即可
> 课程站点：`performance.tutorial.hogwarts.ceshiren.com` → `performance/性能监控/L2/tutorial/...`
> 编号说明：**章节编号按站点**（一页一章，全仓库连续）——本模块 **Ch38~Ch43**（Ch35~Ch37 = [[../L1-服务端统计工具/README|L1 服务端统计工具]]）。
> **编号排序依据**：站点 sitemap 是字母序、无法反映 nav；本章顺序按"**采集 → 价值/选型 → 搭建 → 整合 → 压测实时看板**"的学习依赖排列（站点 sidebar 顺序待核对，届时如需要再统一重编号）。

## 一句话定位

L1 服务端统计工具讲"**在一台机器上敲命令看状态**"（人工、瞬时、单机）；本模块讲"**把这件事实系统化**"——**采集（Node Exporter / 脚本）→ 存储（Prometheus / InfluxDB）→ 展示与告警（Grafana）**，最终交付两块看板：**机器指标看板**（Prometheus + Node Exporter）与**压测实时看板**（JMeter + InfluxDB）。这是"会用工具"升级为"能交付可观测体系"的一步。

## 章节清单（站点该层页 = 章节）

| 章节 | 站点页 | 重要性 | 状态 | 学习日期 | 内容概要 |
|------|--------|--------|------|---------|----------|
| [[Ch38-系统性能数据收集（cpu、mem、net、io）]] | 系统性能数据收集（cpu、mem、net、io） | ⭐⭐⭐ | 📝 | 2026-10-11 | 监控定义与 6 条意义对"采集"的要求；四链命令清单（原文完整保留）；**采集三形态**（脚本 → 定时落库 → 监控系统）；采集纪律（时间对齐/基线/开销/容器视角）；可直接用的采集脚本骨架 |
| [[Ch39-性能监控系统价值]] | 性能监控系统价值 | ⭐⭐⭐ | 📝 | 2026-10-11 | 监控系统 4 条价值（稳定性/资源/体验/安全）与 4 个使用场景；**体系选择**（Grafana / Prometheus / Zipkin / SkyWalking = 看图 / 记数 / 追链路）；可观测性三支柱；本模块路线图 |
| [[Ch40-搭建服务端性能监控系统Prometheus]] | 搭建服务端性能监控系统Prometheus | ⭐⭐⭐ | 📝 | 2026-10-11 | Prometheus 定位（Borgmon 血统、CNCF）与 7 条应用场景；核心概念（target/job/instance/labels、pull、两个 interval、PromQL）；**搭建四步 + YAML 逐行**；**原文 3 处勘误**（镜像名大小写 / 冒号缺空格 / `/etc/Prometheus`）；三层验证 |
| [[Ch41-搭建数据分析系统Grafana]] | 搭建数据分析系统Grafana | ⭐⭐⭐ | 📝 | 2026-10-11 | Grafana 定位（**不采集不存储**，只连数据源画图与告警）与 7 条场景；核心概念（Data Source / Dashboard / Panel / Query / **Variables** / Alerting）；两条 docker 命令 + 挂载 `/var/lib/grafana`；容器内 localhost 陷阱；压测看板面板清单 |
| [[Ch42-Prometheus监控系统部署应用实战]] | Prometheus监控系统部署应用实战 | ⭐⭐⭐ | 📝 | 2026-10-11 | 三件套数据流（Node Exporter 9100 → Prometheus 9090 → Grafana 3000）；5 条场景与体系优点；**搭建四步 + 验收点**；常见指标 9 类 + Node Exporter 指标名（`rate()`、`MemAvailable`、`node_load1`、`up`）；压测前中后检查清单 |
| [[Ch43-jmeter实时压测结果收集]] | jmeter实时压测结果收集 | ⭐⭐⭐ | 📝 | 2026-10-11 | JMeter + InfluxDB + Grafana 实时体系与 4 条优点；推 vs 拉（push/pull）；InfluxDB 1.8 搭建与建库；**Backend Listener 参数逐个说清**（`influxdbUrl`、`application`、`testTitle`、`percentiles`、`summaryOnly`）；TPS/QPS/并发数/吞吐量/RT 口径（**原文 3 处勘误**） |

> **本层站点 tutorial 页共 6 页，已建 6 章（Ch38~Ch43）——本模块已全覆盖**。站点该层另有 `chapter/`（目标/章节）、`plan/`（学习计划）、`homework/`（考试）等页，非 tutorial 知识页，不建章。

## 学习进度

- 6 / 6 章已建笔记（站点「性能监控 / L2」6 个 tutorial 页全覆盖）
- 建章纪律：每章七个内容标记齐全（按知识点逐项校验）、无空表格、无悬空链接；**勘误必须先核对官方文档再写**

## 建议学习顺序

| 轮次 | 章节 | 目标 |
|---|---|---|
| 第 1 轮 想清楚 | Ch38 → Ch39 | 采集什么（四链 + 纪律）、为什么要体系、选择哪套（Prometheus + Grafana） |
| 第 2 轮 搭起来 | Ch40 → Ch41 | Prometheus（9090）与 Grafana（3000）分别起来，数据源连通（Save & Test 通过） |
| 第 3 轮 接闭环 | Ch42 → Ch43 | 加 Node Exporter（9100）看机器指标；加 InfluxDB 看压测实时结果 |
| 第 4 轮 用起来 | 全部 | 压测前检查（targets 全 UP + 采集脚本）、压测中盯板找拐点、压测后归档进报告 |

## 本模块必须能"背下来"的四件事

1. **数据流**：采集（Exporter/脚本）→ 存储（Prometheus/InfluxDB）→ 展示告警（Grafana）；**9100 → 9090 → 3000** 三层验证，Grafana 出问题先往上查。
2. **推 vs 拉**：主机/服务指标用 **pull**（Prometheus 主动拉 `/metrics`）；压测结果用 **push**（JMeter Backend Listener 推到 InfluxDB）。
3. **口径纪律**：`*_total` 是累计值必须 `rate()`；内存看 `MemAvailable`；响应时间看分位值（P95/P99）；TPS 与 QPS 报数必须说明口径。
4. **容器网络陷阱**：容器里的 `localhost` 是容器自己——Grafana 连 Prometheus、JMeter 连 InfluxDB 都必须写"从对端可达"的地址。

## 关联

- [[../L1-服务端统计工具/Ch35-性能分析系统级别指标io cpu mem net|L1 Ch35-性能分析系统级别指标io cpu mem net]]（人工命令版：本章体系的"原始形态"）
- [[../L1-性能测试体系/Ch05-行业流行性能监控工具介绍|L1 Ch05-行业流行性能监控工具介绍]]（Prometheus + Grafana 在监控体系中的定位）
- [[../L1-性能测试体系/Ch08-性能测试计划|L1 Ch08-性能测试计划]]（压测执行与监控清单）
- [[../L1-性能测试体系/Ch09-性能测试报告|L1 Ch09-性能测试报告]]（看板数据如何进入报告）
- [[../L2-JMeter参数化与并发/Ch32-JMeter变量与引用|L2 Ch32-JMeter变量与引用]]（JMeter 侧基础：变量、断言、Backend Listener 的前置知识）
- [[../L1-JMeter常用组件/Ch19-JMeter监听器|L1 Ch19-JMeter监听器]]（Backend Listener 元件首次出现）
- [[../README|性能测试（课程 MOC）]]
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
