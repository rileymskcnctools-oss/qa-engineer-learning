---
tags: [课程笔记, AI大模型, Agent, 智能体, ReAct]
course: "AI大模型"
chapter: "Ch04-智能体Agent介绍"
created: 2026-08-03
status: draft
---

# Ch04 - 智能体 Agent 介绍

> 前置：[[Ch03-AI工作流应用开发]] — 工作流与工具节点
> 关联：[[Ch01-OpenAI-ChatGPT大语言模型]] — Function calling、Assistants

## 课程来源

- 学习日期：2026-08-03

---

## 一、智能体 Agent 是什么

### 知识点 1：多方定义

【课程原话/定义】

| 来源 | 定义 |
|------|------|
| 百度百科 | 能够感知环境并采取行动以实现特定目标的代理体，具备自主性、适应性和交互能力 |
| LangChain | 代理的核心思想是使用语言模型来选择要采取的一系列操作，LLM 被用作推理引擎来决定采取哪些操作及顺序 |
| AWS | 一种可与环境交互、收集数据并利用数据执行自我决定任务以达到预定目标的软件程序，人类设定目标，AI 独立选择最佳行动 |
| IBM | 能通过设计工作流和利用可用工具，代表用户或其他系统自主执行任务的系统，包括决策、解决问题、与环境交互、执行操作 |

【为什么？】

四个定义从不同角度描述同一个东西，但有一个共同点：**Agent = 有"决策权"的 LLM 应用**。

关键区别在于"自主性"：
- 普通 LLM 应用：人写死流程，LLM 只负责"生成内容"
- Agent：LLM 自己决定"下一步做什么"——用哪个工具、按什么顺序、是否已完成

这和工作流（Ch03）形成对比：
- **工作流**：固定编排，流程由人预先画好
- **Agent**：动态决策，流程由 LLM 在运行时选择

【必须掌握】

- Agent 核心：LLM 作为"推理引擎"，自主决定操作序列
- 人类设定目标，Agent 独立选择实现目标的最佳行动
- Agent vs 工作流：动态决策 vs 固定编排

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| Agent = 聊天机器人 | 聊天机器人只对话；Agent 能调工具、执行动作、影响环境 |
| Agent = 工作流 | 工作流是固定流程图，Agent 是运行时自主决策 |
| Agent 一定用大模型 | 决策层用 LLM，但执行层可以是任何工具/代码 |

【我的理解】

> 用自己的话解释：为什么说"Agent 使用 LLM 来决定应用程序的控制流"？这和传统程序里 `if/else` 决定控制流有什么本质不同？

---

## 二、Dify Agent

### 知识点 2：Dify 的 Agent 应用与工具

【课程原话/定义】

Dify 的 Agent 应用支持多种工具：
- **搜索工具**：联网检索
- **代码解释器**：运行 Python/JavaScript 代码
- **文生图工具**：文本生成图像
- **更多工具**：内置工具、自定义工具、工作流工具

【为什么？】

Agent 的能力边界由它的**工具集**决定。一个 Agent 如果没有工具，就退化成普通聊天机器人；工具越多，它能完成的动作越多。Dify 的三种工具来源：
1. **内置工具**：开箱即用（搜索、代码解释器、文生图）
2. **自定义工具**：把外部 HTTP API 通过 OpenAPI/Swagger 规范导入
3. **工作流工具**：把上一章做的工作流封装成工具

【必须掌握】

- Agent 能力 = LLM（决策）+ 工具集（执行）
- 自定义工具：外部服务暴露 HTTP API → 用 Swagger/OpenAPI 描述 → 导入 Dify

【企业场景】

> 你想让 Agent 能操作被测系统：把一个"自动化测试执行服务"（提供 run_test、query_result 等 HTTP 接口）用 OpenAPI 规范描述后导入 Dify，Agent 就能自主调用这些接口执行测试、查询结果，再用 LLM 分析测试报告。

---

### 知识点 3：Web 自动化 Agent

【课程原话/定义】

通过自定义工具，把 Web 自动化能力暴露给 Agent。示例 OpenAPI 定义（`open/open/click/send_keys` 等端点）：

```json
{
  "openapi": "3.1.0",
  "info": { "title": "Web自动化Agent", "version": "0.1" },
  "paths": {
    "/open": {
      "get": {
        "summary": "Open",
        "description": "Opens a URL in the default browser.",
        "operationId": "open",
        "parameters": [
          {"name": "url", "in": "query", "required": true, "schema": {"type": "string"}}
        ]
      }
    },
    "/click": {
      "get": {
        "summary": "Click",
        "description": "click element. by: 尽可能使用css selector定位",
        "operationId": "click",
        "parameters": [
          {"name": "by", "in": "query", "required": true, "schema": {}},
          {"name": "value", "in": "query", "required": true, "schema": {}}
        ]
      }
    }
  }
}
```

【为什么？】

这是"AI 驱动 UI 自动化"的雏形：把浏览器操作（打开页面、点击、输入）封装成 HTTP 接口，再用 OpenAPI 描述，Agent 就能通过自然语言"帮我打开 ceshiren.com 并点击登录按钮"来驱动浏览器。

关键在于 `description` 字段——它是给 LLM 看的"说明书"，LLM 靠它理解每个工具该在什么时候用、传什么参数。所以 description 写得越清楚，Agent 用工具越准。

【必须掌握】

- 自定义工具的 description 是给 LLM 看的说明书，决定调用准确性
- 定位策略：尽量用 css selector，带 id/class 组合

【扩展知识】

为什么用 OpenAPI/Swagger 规范？因为它是标准化的 API 描述格式，Dify（以及多数 Agent 平台）能自动解析它，把每个端点转换成一个"工具"，让 LLM 理解参数和用途。

---

## 三、Agent 架构

### 知识点 4：Agent 的核心 —— LLM 决定控制流

【课程原话/定义】

智能体是使用 LLM 来决定应用程序的控制流的系统。

- LLM 可以在潜在路径之间路由
- LLM 可以决定调用众多工具
- LLM 可以决定生成的答案是否足够或需要更多工作

【为什么？】

这是理解 Agent 最关键的一句话。传统程序的控制流是程序员写死的（`if 条件: 调函数A else: 调函数B`）；Agent 的控制流是 LLM 在运行时"想"出来的。LLM 扮演的角色从"内容生成器"升级为"控制流路由器"——它根据当前状态，动态决定走哪条路。

---

### 知识点 5：规划模式 —— Plan-and-Execute 与 ReAct

【课程原话/定义】

**Plan-and-Execute（计划-执行）：**

先制定完整计划，再逐步执行。相比 ReAct 的"一步一步想"：

- 优势：显式长期规划（即使强大的 LLM 也难处理长链）
- 优势：执行步骤可用较小/较弱模型，只在规划步骤用较大/较好模型（省成本）

**ReAct 推理（Reasoning + Acting）：**

把推理（Thought）和行动（Action）交替进行：

```
问题：输入要回答的问题
想法：考虑之前和后续步骤
操作：{"action": "google_search", "action_input": "..."}
观察：操作结果
...（重复 想法/操作/观察 N 次）
想法：我知道该如何回应
操作：{"action": "最终答案", "action_input": "对人类的最终回应"}
```

【为什么？】

这是两种不同的 Agent 决策范式：

| | ReAct | Plan-and-Execute |
|---|---|---|
| 思路 | 边想边做，走一步看一步 | 先想完整计划，再照计划做 |
| 优点 | 灵活，能根据观察调整 | 有全局规划，执行阶段可降级模型 |
| 缺点 | 长任务易"迷路" | 计划错了执行就偏 |
| 类比 | 即兴演讲 | 先写提纲再演讲 |

ReAct 的核心是 **Thought → Action → Observation 循环**：模型每次先"思考"，再决定"调用哪个工具"，然后"观察结果"，如此往复直到能给出最终答案。这就是 LangChain 定义里"LLM 作为推理引擎"的具体实现。

【面试考察】

> 面试官："什么是 ReAct？它和 Plan-and-Execute 有什么区别？"

**参考回答框架：**

1. ReAct = Reasoning + Acting，让 LLM 交替进行"思考"和"行动"，用 Thought-Action-Observation 循环逐步逼近答案
2. Plan-and-Execute = 先让 LLM 生成完整计划，再逐步执行，执行阶段可用更小的模型
3. 区别：ReAct 灵活但长任务易偏；Plan-and-Execute 有全局规划、省成本，但计划错误会连带执行错误
4. 选型：任务步骤明确可预测 → Plan-and-Execute；任务开放需动态调整 → ReAct

---

### 知识点 6：结构化输出

【课程原话/定义】

三种方式让 LLM 输出结构化数据：

| 方式 | 做法 |
|------|------|
| 提示工程 | 指示 LLM 以特定格式（json/xml）响应 |
| 输出解析器 | LLM 调用后用代码解析（如 pydantic 校验） |
| 工具调用输出 | 利用 LLM 原生 structured output 能力（如 ChatGPT function calling） |

【为什么？】

Agent 的"行动"要能被程序执行，输出必须是结构化、可解析的。ReAct 的 `{"action": ..., "action_input": ...}` 就是结构化输出——程序读到这个 JSON，才知道该调哪个工具、传什么参数。三种方式可靠性递增：提示工程最弱（可能输出非法 JSON），原生工具调用最强（模型内部保证格式）。

【易错点】

| 方式 | 可靠性 | 成本 |
|------|--------|------|
| 提示工程 | 低（可能格式错） | 低 |
| 输出解析器 | 中（需兜底处理） | 中 |
| 工具调用输出 | 高（模型保证） | 依赖模型能力 |

---

### 知识点 7：工具调用代理与记忆

【课程原话/定义】

**工具调用代理：** LLM 可以选择并使用多种工具完成任务。常用工具：代码解析器、搜索、通用工具调用、通用函数调用。

**记忆（Memory）：**

| 类型 | 作用 |
|------|------|
| 短期记忆 | 访问当前序列早期步骤获取的信息（如本次对话上下文） |
| 长期记忆 | 调用以前交互的信息（如过去对话消息） |

【为什么？】

记忆解决的是 LLM "无状态"的问题。LLM 每次调用都是独立的，不记得上一轮说过什么。短期记忆把当前任务的前序步骤塞进上下文，长期记忆则持久化跨会话的信息。没有记忆，Agent 就"失忆"，无法完成多步、多轮任务。

【必须掌握】

- 短期记忆 = 当前任务上下文窗口内的信息
- 长期记忆 = 跨会话持久化的信息（通常存向量库/数据库）

---

## 四、Agent 核心元素总结

### 知识点 8：五大核心元素

【课程原话/定义】

```
Agent = LLM + Planning + Parser + Tools + Memory
```

| 元素 | 作用 |
|------|------|
| LLM（大模型） | 推理引擎，chatgpt/qwen/llama |
| Planning（规划） | 路由、ReAct、Plan-and-Execute |
| Parser（解析） | 结构化输出解析（json） |
| Tools（工具） | 工具集合与调用能力 |
| Memory（记忆） | 短期记忆、长期记忆 |

【为什么？】

这五个元素构成 Agent 的完整能力栈，缺一不可：
- 缺 LLM → 没有大脑
- 缺 Planning → 只会闲聊，不会拆解任务
- 缺 Parser → 输出无法被程序理解
- 缺 Tools → 只能动口不能动手
- 缺 Memory → 金鱼记忆，无法完成多步任务

【面试考察】

> 面试官："一个完整的 Agent 系统包含哪些核心组件？"

**参考回答框架：**

1. LLM：推理引擎，负责理解和决策
2. Planning：任务规划策略（ReAct / Plan-and-Execute），决定"下一步做什么"
3. Parser：结构化输出解析，把 LLM 输出变成可执行的格式
4. Tools：工具集，让 Agent 能执行实际操作（搜索、代码、API）
5. Memory：短期+长期记忆，让 Agent 记住上下文和历史

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Agent 概念 | LLM 决定控制流，自主决策 | ⭐⭐⭐⭐⭐ |
| Dify Agent | 工具集（内置/自定义/工作流） | ⭐⭐⭐⭐ |
| Web 自动化 Agent | OpenAPI 暴露工具，自然语言驱动 | ⭐⭐⭐⭐⭐ |
| Plan-and-Execute | 先计划后执行，执行可降级模型 | ⭐⭐⭐⭐ |
| ReAct | Thought-Action-Observation 循环 | ⭐⭐⭐⭐⭐ |
| 结构化输出 | 提示/解析器/工具调用三种方式 | ⭐⭐⭐⭐ |
| 记忆 | 短期 vs 长期 | ⭐⭐⭐⭐ |
| 五大核心元素 | LLM+Planning+Parser+Tools+Memory | ⭐⭐⭐⭐⭐ |

---

## 今天没搞懂的问题

-
-
-

## 关联笔记

- [[Ch03-AI工作流应用开发]] — Agent 与工作流的关系（动态决策 vs 固定编排）
- [[Ch01-OpenAI-ChatGPT大语言模型]] — Function calling 是工具调用基础
- [[../接口测试/README|接口测试]] — Web 自动化 Agent 与 UI 自动化测试
