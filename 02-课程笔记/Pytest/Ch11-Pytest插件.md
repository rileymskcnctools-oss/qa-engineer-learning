---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch11-Pytest插件"
date: 2026-07-23
status: draft
---

# Ch11 - Pytest 插件

## 课程来源

- 学习日期：

---

## 一、Pytest 插件概述

### 知识点1：什么是 Pytest 插件

【课程原话/定义】
Pytest 插件是 Python 包或模块，可以提供额外的功能、自定义行为或报告，根据项目需求选择并使用不同的插件。

【为什么？】
pytest 本身只提供核心的测试运行和断言能力（约 20%），其余 80% 的功能（HTML 报告、并发、重跑、顺序控制等）全部由插件生态提供。这个设计哲学叫"微内核 + 插件"——核心小而精，能力通过插件无限扩展。你不需要的插件不安装，框架保持轻量；需要什么能力就装什么插件。

【必须掌握】
- Pytest 插件的本质：Python 包/模块，通过 hook 机制扩展 pytest 功能
- 插件安装方式：`pip install 插件名`
- 为什么 pytest 采用插件架构（灵活性、按需加载、社区贡献）

【企业场景】
你的项目刚开始只写 20 条用例，pytest 原生功能足够。半年后到了 500 条，你需要 HTML 报告给 PM 看、需要并发加速 CI、需要失败重跑来减少 flaky 告警。你不需要换框架——只需 `pip install pytest-html pytest-xdist pytest-rerunfailures`，框架能力原地升级。这就是插件架构在企业中的真实价值。

【面试考察】
面试官："你们项目用了哪些 Pytest 插件？为什么选这些？"
参考回答框架：① 按需求列出：HTML 报告（pytest-html/allure）、并发（pytest-xdist）、顺序控制（pytest-order）、失败重跑（pytest-rerunfailures）② 每种插件的选择理由 ③ 不是越多越好，每个插件都要有明确的业务需求驱动

【易错点】

| 误区 | 正解 |
|------|------|
| 装越多插件越好 | 每个插件增加依赖和维护成本，按需安装 |
| 插件可以替代好的测试设计 | 插件是工具；如果用例设计差，并发跑也只是更快地暴露问题 |
| 所有插件兼容所有 pytest 版本 | 关注插件的 pytest 版本要求，升级前看 changelog |

【我的理解】

>

---

## 二、常用插件一览

### 知识点2：10 个核心插件分类

【课程原话/定义】

| 插件 | 用途 | 重要程度 | 安装命令 |
|------|------|------|------|
| pytest-order | 控制用例执行顺序 | 🔴 重点 | `pip install pytest-order` |
| pytest-xdist | 分布式并发执行 | 🔴 重点 | `pip install pytest-xdist` |
| pytest-html | 生成 HTML 测试报告 | 🔴 重点 | `pip install pytest-html` |
| allure-pytest | 企业级测试报告 | 🔴 推荐 | `pip install allure-pytest` |
| pytest-timeout | 用例超时控制 | 🟡 推荐 | `pip install pytest-timeout` |
| pytest-dependency | 用例依赖关系管理 | 🟢 了解 | `pip install pytest-dependency` |
| pytest-rerunfailures | 失败用例自动重跑 | 🟢 了解 | `pip install pytest-rerunfailures` |
| pytest-assume | 多重校验（失败不中断） | 🟢 了解 | `pip install pytest-assume` |
| pytest-random-order | 用例随机执行 | 🟢 了解 | `pip install pytest-random-order` |

【为什么？】
区分"重点"和"了解"的维度是**企业日常使用频率**。pytest-order + pytest-xdist + pytest-html/allure 几乎是每个公司的自动化测试必备三件套——顺序控制保证集成测试正确性，并发加速 CI 反馈，报告让非技术人员看懂结果。其余的插件按需引入即可。

【必须掌握】
- 重点 3 件套：order（顺序）、xdist（并发）、html/allure（报告）
- 了解其余插件的作用，面试能说出 5 个以上插件名称及用途
- 区分"重点"与"了解"——面试最常考的是你实际用过的插件

【企业场景】
你们的 CI 流水线每天跑 2000 条用例。配置：`pytest -n 4 --html=report.html --timeout=60 --reruns=2`。`-n 4` 四核并发，`--html` 生成报告给 PM，`--timeout` 防止某条用例卡死阻塞流水线，`--reruns` 给 flaky 用例一次重试机会减少误报。4 个参数覆盖了执行效率、报告、稳定性三个维度。

【面试考察】
面试官："说 5 个你用过的 Pytest 插件，各自解决什么问题？"
参考回答框架：
① pytest-xdist：分布式并发，加速大型套件执行
② pytest-order：集成测试场景控制执行顺序（登录→下单→支付）
③ allure-pytest：生成可视化企业级报告，趋势图/分类/附件
④ pytest-timeout：防止个别用例超时卡死 CI
⑤ pytest-rerunfailures：网络波动等 flaky 场景自动重试

【易错点】

| 插件 | 常见误用 | 正确用法 |
|------|------|------|
| pytest-order | 所有用例都加 order | 只给有依赖关系的集成测试用例加 |
| pytest-xdist | 用例之间有数据竞争还开并发 | 确保用例独立，共享数据加锁或用 scope=session |
| pytest-rerunfailures | 所有失败都重跑，掩盖真实 Bug | 设置合理的重试次数（2-3 次），分析重跑通过的用例 |
| allure-pytest | 只装不配，报告空白 | 需配套 `allure serve` 命令查看报告 |

【我的理解】

>

---

## 三、插件分类

### 知识点3：外部插件 vs 本地插件 vs 内置插件

【课程原话/定义】
- **外部插件**：通过 `pip install` 从 PyPI 安装，独立于项目，安装后所有项目可用
- **本地插件**：存储在项目 `conftest.py` 中（fixture、自定义 hook、marker），仅对当前项目可见
- **内置插件**：pytest 自带（如 `pytest.mark`），存储在 `_pytest/` 目录，自动加载

【为什么？】
三层架构的设计意图：
- **内置**：核心能力，所有 pytest 用户都需要的（不需要选择）
- **外部**：社区贡献的通用能力，按需安装（有选择权）
- **本地**：项目特有的定制能力（无限灵活、零依赖）

conftest.py 被归类为"本地插件"——它本质上就是一个不需要打包的 pytest 插件。

【必须掌握】
- 三种分类及代表
- 本地插件的载体就是 conftest.py
- 外部插件全局可用，本地插件项目级，内置插件自动加载

【企业场景】
你们团队维护了一个内部测试框架，有一些公司特有的逻辑（如：调用内部 SSO 登录、连接公司加密数据库、打点上报到自研监控平台）。你把这三块逻辑写在 `conftest.py` 作为本地插件——全公司 5 个项目共享这个 conftest.py，不需要发布到 PyPI，放在内部 Git 仓库即可。这就是本地插件的企业实践。

【面试考察】
面试官："Pytest 插件分哪几类？conftest.py 属于哪一类？"
参考回答框架：① 三类：内置（pytest 自带）、外部（pip 安装）、本地（项目 conftest.py）② conftest.py 是本地插件——它定义 fixture/hook，不需要安装，只对当前目录及子目录的测试生效 ③ 三者的关系：内置提供基础 → 外部社区扩展 → 本地项目定制

【易错点】

| 类型 | 安装方式 | 作用范围 | 举例 |
|------|------|------|------|
| 内置插件 | 无需安装 | 所有项目 | `pytest.mark`、`pytest.fixture` |
| 外部插件 | `pip install` | 全局（所有项目） | `pytest-html`、`pytest-xdist` |
| 本地插件 | 无需安装 | 当前项目 | `conftest.py` 中的 fixture |

【我的理解】

>

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Pytest 插件概述 | 微内核+插件架构，按需扩展 | ⭐⭐⭐ |
| 常用插件（10个） | order/xdist/html/allure/timeout 重点 | ⭐⭐⭐⭐⭐ |
| 插件分类 | 内置/外部/本地，conftest.py 是本地插件 | ⭐⭐⭐⭐ |

## 今天没搞懂的问题

-
-

## 关联笔记

- [[Ch09-Pytest测试用例生命周期管理-自动注册]]（conftest.py 作为本地插件）
- [[Ch12-Pytest测试用例执行顺序自定义]]
- [[Ch13-Pytest测试用例并行运行与分布式运行]]
