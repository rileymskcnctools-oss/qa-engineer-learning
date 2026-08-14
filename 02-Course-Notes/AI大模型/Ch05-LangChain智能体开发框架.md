---
tags:
  - 课程笔记
  - AI大模型
  - LangChain
  - Agent
  - 智能体
  - RAG
  - MCP
course: AI大模型
chapter: Ch05-LangChain智能体开发框架
created: 2026-08-14
status: draft
---

# Ch05 - LangChain 智能体开发框架

> 前置：[[Ch04-智能体Agent介绍]] — ReAct、Plan-and-Execute、五大核心元素
> 关联：[[Ch03-AI工作流应用开发]] — 工作流与工具节点
> 关联：[[Ch01-OpenAI-ChatGPT大语言模型]] — LLM 调用、Function calling

## 课程来源

- 学习日期：2026-08-14

---

## 一、LangChain 是什么与生态

### 知识点 1：LangChain 定位

【课程原话/定义】

LangChain 是一个由大型语言模型 (LLM) 驱动的应用程序开发框架，为开发者提供简单易用的接口来构建基于大语言模型的应用。

```
LangChain = Language + Chains
```

【为什么？】

"Language + Chains" 这个拆解说明了框架的两层设计意图：

- **Language**：框架围绕 LLM 构建，把"调用大模型"这一件原本需要手写 HTTP 请求、拼接参数、解析响应的事，抽象成一行 `llm.invoke()`。
- **Chains（链）**：把多个组件（模型调用、提示词、检索、工具、输出解析）像链条一样串起来，形成可复用的处理流水线。

传统做法里，你调一次模型要自己管理 API Key、请求体、超时、重试、响应解析；LangChain 把这些打包成统一的抽象，让你专注于"业务逻辑"而不是"胶水代码"。

【必须掌握】

- LangChain = 大模型应用开发框架，核心抽象是"链式"结构
- 一句话概括：用统一接口串联 LLM 调用、提示词、工具、检索、解析

【易错点】

| 易混淆              | 正确理解                                                      |
| ---------------- | --------------------------------------------------------- |
| LangChain 是大模型本身 | 不是。它是**开发框架**，模型是 OpenAI/通义/Ollama 等提供的，LangChain 只负责"调度" |
| LangChain 只能做聊天  | 能做 RAG、Agent、多智能体、文档处理、工具调用等，聊天只是最基础用法                    |
| Chains 是历史遗留概念   | Chains 至今仍是核心抽象，Agent 本质也是"动态选择链的链"                       |

【我的理解】

> 用自己的话解释：为什么说"用 LangChain 写一个 LLM 应用"比"直接调 OpenAI SDK"更省事？省掉的是哪部分工作？

---

### 知识点 2：LangChain 生态架构

【课程原话/定义】

LangChain 不是一个孤立的库，而是一个**生态**：

| 组件              | 作用                                                                |
| --------------- | ----------------------------------------------------------------- |
| LangChain 核心    | 基础框架：模型调用、链、工具、Agent                                              |
| LangChain 社区生态  | 大量第三方集成包（langchain-ollama、langchain-openai、langchain-community 等） |
| LangChain 智能体   | Agent 能力（create_agent）                                            |
| Templates 提示词模板 | 可复用的提示词模板（Prompt Hub）                                             |
| LangServe       | 服务运行框架（把链部署成 REST 服务）                                             |
| LangSmith       | 监控分析工具（trace、调试、评估）                                               |
| LangGraph       | 智能体开发框架（基于图的流程编排）                                                 |

【为什么？】

生态架构的背后是"分层解耦"的设计哲学：核心框架只负责最通用的抽象，具体到某个模型（OpenAI/Ollama）、某个向量库（FAISS/Chroma）、某个工具协议（MCP），都交给独立的"社区集成包"去实现。

好处是：换模型、换向量库时，核心代码几乎不用改，只换 import 和初始化参数。这也解释了为什么 LangChain 有那么多 `langchain-xxx` 的独立包——不是碎片化，而是插件化。

【必须掌握】

- LangChain 核心 + 社区生态 + 智能体 + Templates + LangServe + LangSmith + LangGraph 七大组件各自定位
- 社区生态 = 插件化集成，解决"模型无关、数据库无关"

【面试考察】

> 面试官："LangChain 的生态包括哪些部分？LangGraph 和 LangChain 是什么关系？"

**参考回答框架：**

1. 核心框架（模型调用、链、Agent）+ 社区集成包（langchain-openai/ollama/community）
2. 上层工具链：LangServe（部署）、LangSmith（监控调试）、LangGraph（图编排）、Templates（提示词模板）
3. LangGraph 是 LangChain 团队推出的、基于图的智能体开发框架，比 Chains 更适合有循环/分支/多智能体的复杂流程

---

### 知识点 3：开源 OSS vs 商业 Commercial

【课程原话/定义】

不推荐使用官方的商业方案（很多服务在海外，访问不方便），推荐开源替代：

| 官方商业 | 开源替代 | 理由 |
|---------|---------|------|
| LangServe | FastAPI | 同样能把 Python 代码部署成 REST 服务，国内可用 |
| LangSmith | Jaeger | 开源分布式追踪，同样能看到调用链路 |
| Prompt Hub（Templates 云） | 本地提示词 | 提示词存本地文件，随代码进 Git |

【为什么？】

这个选择的本质是**"能力本地化"和"可控性"**：

1. **访问成本**：LangSmith/Prompt Hub 等服务部署在海外，国内访问慢或不稳定，开发调试体验差。
2. **数据安全**：把提示词、调用日志传到第三方云，企业场景下可能有合规风险。
3. **可移植**：开源替代（FastAPI/Jaeger）可部署在自家内网，且和团队现有技术栈（Python 后端、可观测性）天然契合。

LangSmith 和 Jaeger 对比：

| 维度 | LangSmith | Jaeger |
|------|-----------|--------|
| 定位 | LLM 应用专用监控/调试 | 通用分布式链路追踪 |
| 追踪对象 | LLM 调用、token、提示词、输出 | 微服务调用链路 |
| 开源 | 否（商业 SaaS） | 是（CNCF 项目） |
| 部署 | 海外云 | 可自建 |

【必须掌握】

- 商业方案（LangSmith/LangServe/Prompt Hub）→ 开源替代（Jaeger/FastAPI/本地提示词）
- 选择理由：海外访问不便 + 数据可控 + 可自建

【企业场景】

> 你在公司里用 LangChain 做测试智能体，公司内网不能访问 LangSmith。你的方案是：用 FastAPI 把 Agent 包成内部服务，用 Jaeger 追踪每一次 LLM 调用和工具调用的耗时与结果，提示词全部存本地 Git 仓库——这样调试、审计、上线都不依赖任何海外服务。

---

### 知识点 4：为什么学 LangChain + 同类框架对比

【课程原话/定义】

学习 LangChain 的理由：

- 功能强大，接口简约，架构设计先进
- 文档丰富，工具齐全，示例丰富
- 生态丰富，最早最流行的 LLM 开发框架，很多成熟项目基于它

同类智能体框架对比：

| 框架                  | 简介                                     | 优势                                 |
| ------------------- | -------------------------------------- | ---------------------------------- |
| LangChain           | 模块化、"链式"结构（Chains）                     | 灵活性最强、生态成熟、社区庞大、模型无关性好、易集成各种工具和数据库 |
| LangGraph           | 基于图的流程编排（Graph-based）                  | 明确的流程控制（节点和边）、支持循环和分支、方便调试和高级错误处理  |
| LlamaIndex          | RAG（检索增强生成）与 Agent 结合                  | 专注数据索引和检索，高效为 Agent 注入大量外部数据知识     |
| CrewAI              | 基于角色的多智能体协作（Role-based Crew）           | 强调角色/任务/团队结构化，易创建并行、有记忆的工作流        |
| AutoGen (Microsoft) | 多智能体聊天（Multi-Agent Conversation）       | 大厂出品                               |
| Google ADK          | 强调多智能体协作                               | 大厂出品                               |
| Pydantic.AI         | 类型化，把 FastAPI 的感觉带入 GenAI 应用和 Agent 开发 | 技术特色强：MCP / A2A / AG-UI            |

【为什么？】

LangChain 的护城河是"先发 + 生态"：它最早把 LLM 应用开发标准化，积累了最丰富的集成（几乎每个模型、每个向量库、每个工具都有对接）和最庞大的社区（遇到问题一搜就有答案）。

但要区分两类框架：

- **LangChain / LangGraph / LlamaIndex**：通用能力层，关注"怎么把 LLM 能力组织起来"
- **CrewAI / AutoGen / Google ADK**：多智能体协作层，关注"多个 Agent 怎么分工协作"

作为测试开发，优先掌握 LangChain（基础 + 最流行）和 LangGraph（复杂流程编排），其余框架了解定位即可。

【必须掌握】

- LangChain 的三大优势：生态成熟、模型无关、社区庞大
- 能说清每个框架"一句话定位"和"优势"，重点是 LangGraph（图编排）和 LlamaIndex（RAG）

【面试考察】

> 面试官："LangChain、LangGraph、LlamaIndex、CrewAI 有什么区别？什么时候选哪个？"

**参考回答框架：**

1. LangChain：通用 LLM 应用框架，最灵活、生态最全，适合大多数场景
2. LangGraph：需要明确流程控制（循环/分支/多步骤编排）时用，是 LangChain 官方出的图编排框架
3. LlamaIndex：重 RAG、需要高效索引和检索大量文档时用
4. CrewAI：需要多个"角色分工"的 Agent 协作时用（角色/任务/团队三要素）
5. 选型原则：先 LangChain 起步，流程复杂了上 LangGraph，检索密集换 LlamaIndex，多角色协作才考虑 CrewAI

【易错点】

| 易混淆                              | 正确理解                                        |
| -------------------------------- | ------------------------------------------- |
| LangGraph 是 LangChain 的替代品       | 不是，是 LangChain 生态里面向"图编排"场景的进阶框架，可配合使用      |
| LlamaIndex 和 LangChain 是竞品，只能二选一 | 可以混用，LangChain 做编排、LlamaIndex 做检索           |
| Pydantic.AI 是"玩具"框架              | 它把类型安全带入 Agent 开发，MCP/A2A/AG-UI 协议支持很全，值得关注 |

---

## 二、LangChain 核心能力

### 知识点 5：核心能力全景

【课程原话/定义】

LangChain 核心能力分三大类：

| 类别     | 组件                                                                                 |
| ------ | ---------------------------------------------------------------------------------- |
| 模型调用类  | Chat models、Messages、Prompt templates、Example selectors、LLMs、Output parsers        |
| 数据检索类  | Document loaders、Text splitters、Embedding models、Vector stores、Retrievers、Indexing |
| 智能体工具类 | Tools、Multimodal、Agents、Callbacks、Custom、Serialization                             |

【为什么？】

这三大类对应 LLM 应用的三大支柱：**怎么调用模型**（模型调用类）、**怎么喂数据**（数据检索类）、**怎么让它动手**（智能体工具类）。一个完整的 RAG 应用，就是这三类的组合：Document loader 加载文档 → Text splitter 切分 → Embedding 向量化 → Vector store 存储 → Retriever 检索 → 拼进 Prompt template → Chat model 生成。

记住这个分类，遇到需求就能快速定位"该用哪个组件"。

【必须掌握】

- 三大类组件及各自包含的子组件
- 能画出 RAG 的完整组件链路

---

### 知识点 6：大模型调用

【课程原话/定义】

基本的大模型调用，发起一次请求。增加一行代码初始化模型的能力，简化大模型的使用：

```python
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama


def test_llm():
    # 用 "provider:model" 字符串统一初始化
    llm = init_chat_model("openai:gpt-4.1")
    llm.invoke('北京天气如何')


def test_llm_oop():
    # OOP 方式，指定具体模型类和连接参数
    llm = ChatOllama(model='qwen3', base_url='http://127.0.0.1', temperature=0)
    llm.invoke('北京天气如何')
```

【为什么？】

两种调用方式对应两种使用场景：

1. **`init_chat_model("provider:model")`**：字符串声明式初始化。好处是**模型无关**——换模型只改字符串 `"openai:gpt-4.1"` → `"ollama:qwen3"`，业务代码不变。适合模型频繁切换、需要配置化的场景。
2. **`ChatOllama(...)` OOP 方式**：直接实例化具体模型类，能精确控制 `base_url`、`temperature` 等参数。适合需要精细控制连接（如本地 Ollama 服务）的场景。

统一的 `invoke()` 接口是所有模型类的共同契约——无论底层是 OpenAI 还是 Ollama，调用方式完全一致。这是"模型无关性"的具体体现。

【必须掌握】

- `init_chat_model`：声明式、模型无关、换模型只改字符串
- `ChatOllama`：OOP、精细控制 base_url/temperature
- 所有模型统一 `invoke()` 接口

【企业场景】

> 你在公司做接口测试智能体，开发环境用本地 Ollama 的 qwen3（省钱、离线），生产环境用 OpenAI。代码里用 `init_chat_model` 把模型名放进配置文件：开发读 `ollama:qwen3`，生产读 `openai:gpt-4.1`，业务代码一行不改。

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| `init_chat_model` 和 `ChatOllama` 二选一 | 可以混用，前者是统一入口，后者是具体实现 |
| `temperature=0` 表示"随机" | 恰恰相反，`temperature=0` 是最确定、最保守的输出（测试断言类场景常用） |
| `invoke` 返回的是字符串 | 返回的是 LangChain 的 `AIMessage` 对象，取文本要用 `.content` |

【我的理解】

> 如果明天公司把模型从 OpenAI 换成国产通义千问，用 `init_chat_model` 写法的代码需要改几处？用 `ChatOllama` 写法的呢？

---

## 三、智能体与工具调用

### 知识点 7：智能体最小 Demo（create_agent）

【课程原话/定义】

```python
# pip install -qU "langchain[openai]" to call the model

from langchain.agents import create_agent
from langchain_core.globals import set_debug

set_debug(True)


def get_weather(city: str) -> str:
    """查询特定城市天气"""
    return f"{city} 总是晴天!"


agent = create_agent(
    model="openai:gpt-4",
    tools=[get_weather],
    prompt="你是一位乐于助人回答简洁高效的助手",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "北京天气如何"}]}
)
```

ReAct 执行流程：

```
query → thought → action(调用 tool) → observation(工具结果) → ... → finish(最终答案)
```

【为什么？】

这个 20 行的 Demo 体现了 Agent 的全部核心机制：

1. `tools=[get_weather]`：把普通 Python 函数注册成"工具"，函数 docstring（`查询特定城市天气`）就是给 LLM 看的说明书。
2. `create_agent`：框架自动把 model + tools + prompt 组装成一个 ReAct 循环的 Agent。
3. `set_debug(True)`：打开调试，能打印出 LLM 每一步的 thought/action/observation，是开发期定位"Agent 为什么调用错了工具"的关键手段。

用户问"北京天气如何"时，Agent 不是直接回答，而是：思考 → 决定调用 `get_weather("北京")` → 拿到返回"北京 总是晴天!" → 组织成最终答案。这就是 Ch04 讲的 ReAct 循环（[[Ch04-智能体Agent介绍]] 知识点5）在 LangChain 里的落地实现。

【必须掌握】

- `create_agent(model=, tools=, prompt=)` 三参数最小可用
- 工具函数的 docstring 决定 LLM 能否正确调用它
- `set_debug(True)` 是调试 Agent 的第一步

【面试考察】

> 面试官："LangChain 里如何把一个普通函数变成一个 Agent 可调用的工具？LLM 是怎么知道何时调用它的？"

**参考回答框架：**

1. 直接把函数放进 `tools=[...]` 列表（或用 `@tool` 装饰器），LangChain 会把函数签名 + docstring 转成工具描述
2. LLM 通过函数签名知道"有哪些参数"，通过 docstring 知道"这个工具干什么用、何时调用"
3. 所以 docstring 写得好不好，直接决定工具调用准确率
4. 用户提问后，Agent 进入 ReAct 循环，LLM 输出结构化 action，框架据此执行函数并回填 observation

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| 工具函数写完了就能被正确调用 | 必须写清 docstring（参数含义 + 用途），否则 LLM 可能调错参数或根本不用 |
| `set_debug` 只影响报错信息 | 它能打印完整的 ReAct 推理过程，是定位 Agent 行为问题的主要手段 |

【我的理解】

> `get_weather` 的 docstring 如果删掉，Agent 还能正确回答"北京天气如何"吗？为什么 docstring 这么重要？

---

### 知识点 8：对接 MCP

【课程原话/定义】

MCP 与 OpenAPI 是当下主流的 2 类工具注册协议。LangChain 通过扩展支持 MCP：

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",       # 本地子进程通信
            "command": "python",
            "args": ["/path/to/math_server.py"],  # 绝对路径
        },
        "weather": {
            "transport": "streamable_http",  # 基于 HTTP 的远程服务
            "url": "http://localhost:8000/mcp",  # 先启动 weather server
        }
    }
)

tools = await client.get_tools()
agent = create_agent("anthropic:claude-3-7-sonnet-latest", tools)

math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
)
weather_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
)
```

【为什么？】

MCP（Model Context Protocol）解决的是"工具接入标准化"的问题：

- **没有 MCP**：每个工具都要单独写集成代码，Agent 要调 N 个工具就得写 N 套适配逻辑。
- **有了 MCP**：工具提供方按 MCP 协议暴露一个"服务器"（stdio 本地子进程 或 streamable_http 远程 HTTP），Agent 侧用统一的 `MultiServerMCPClient` 一次性把多个服务器转换成工具列表。

注意两种 transport 的区别：

| transport | 通信方式 | 适用场景 |
|-----------|---------|---------|
| stdio | 本地子进程，标准输入输出 | 本机工具（如本地 Python 脚本） |
| streamable_http | HTTP 远程调用 | 远程服务（如天气服务） |

MCP 与 OpenAPI 的关系：两者都是"工具注册协议"，MCP 是 AI 原生协议（为 LLM 调用工具设计），OpenAPI 是传统的 REST API 描述规范（Ch04 的 Web 自动化 Agent 用的就是 OpenAPI）。LangChain 对两者都支持。

【必须掌握】

- MCP = 工具注册协议，让 Agent 用统一方式接入工具
- 两种 transport：stdio（本地子进程）、streamable_http（远程 HTTP）
- `MultiServerMCPClient` 一次性接入多个 MCP 服务器

【企业场景】

> 你在公司把"自动化测试执行引擎"包装成一个 MCP 服务器（提供 run_testcase、get_result 等能力），测试智能体通过 MCP 接入后，就能用自然语言"跑一下登录模块的回归用例"来驱动测试执行——工具对 Agent 是"即插即用"的。

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| MCP 和 OpenAPI 是同一回事 | 都是工具注册协议，但 MCP 是 AI 原生（为 LLM 设计），OpenAPI 是传统 REST 描述 |
| stdio 是远程调用 | stdio 是本地子进程通信，streamable_http 才是远程 |
| `get_tools()` 是同步调用 | 用 `await client.get_tools()`，MCP 客户端方法是异步的 |

---

### 知识点 9：RAG 与文档处理

【课程原话/定义】

RAG（Retrieval-Augmented Generation，检索增强生成）：先检索外部知识，再让 LLM 基于检索结果生成答案。

用工具实现检索的 RAG：

```python
import requests
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent


@tool
def fetch_url(url: str) -> str:
    """Fetch text content from a URL"""
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text


system_prompt = """\
Use fetch_url when you need to fetch information from a web-page; quote relevant snippets.
"""

agent = create_agent(
    model=init_chat_model("ollama:qwen3"),
    tools=[fetch_url],  # A tool for retrieval
    prompt=system_prompt,
)
```

文档加载（Document loader）：

```python
from langchain_community.document_loaders import WebBaseLoader

loader_multiple_pages = WebBaseLoader(
    ["https://www.example.com/", "https://google.com"]
)
docs = loader.load()

# docs[0] 输出
# Document(metadata={'source': '...', 'title': 'Example Domain', ...},
#           page_content='...Example Domain...')
```

文档分割（Text splitter）：

```python
from langchain_text_splitters import HTMLHeaderTextSplitter

url = "https://plato.stanford.edu/entries/goedel/"

headers_to_split_on = [
    ("h1", "Header 1"),
    ("h2", "Header 2"),
    ("h3", "Header 3"),
    ("h4", "Header 4"),
]

html_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
html_header_splits = html_splitter.split_text_from_url(url)
```

【为什么？】

RAG 解决的是 LLM 的三大痛点：

1. **知识过时**：训练数据有截止时间，不知道最新信息。
2. **私有知识**：LLM 不知道公司内部的文档、测试用例库。
3. **幻觉**：没有依据时容易瞎编。RAG 先检索再生成，答案有出处可溯源。

LangChain 里实现 RAG 有两条路线：

- **工具式 RAG**（上面的 `fetch_url`）：把"取网页"做成工具，让 Agent 自己决定何时检索、检索什么。灵活，但依赖 Agent 判断。
- **链式 RAG**（Document loader → splitter → embedding → vector store → retriever）：固定管线，把文档预处理成可检索的向量，查询时自动召回。可靠、可控，是生产主流。

文档处理三件套的分工：

| 组件 | 作用 | 类比 |
|------|------|------|
| Document loader | 从各种来源加载原始文档 | 把书搬进书房 |
| Text splitter | 把长文档切成小块 | 把书拆成书页/段落 |
| Embedding + Vector store | 把文本转成向量并存储 | 给每页建索引卡片 |

`HTMLHeaderTextSplitter` 的 `headers_to_split_on` 表示"按标题层级切分"——h1/h2/h3/h4 作为切分边界，比按固定字符数切分更能保留文档的语义结构。

【必须掌握】

- RAG = 检索 + 生成，解决知识过时/私有知识/幻觉三大痛点
- 链式 RAG 的完整管线：loader → splitter → embedding → vector store → retriever
- 工具式 RAG（`@tool`）vs 链式 RAG（管线）的区别

【面试考察】

> 面试官："什么是 RAG？为什么要用 RAG？LangChain 里怎么实现？"

**参考回答框架：**

1. RAG = Retrieval-Augmented Generation，先检索外部知识再让 LLM 生成，答案有据可查
2. 解决三大问题：知识过时、私有知识无法注入、幻觉
3. LangChain 实现：Document loader 加载 → Text splitter 切分 → Embedding 向量化 → Vector store 存储 → Retriever 检索 → 拼接 Prompt → LLM 生成
4. 也可用工具式 RAG：把检索能力做成 `@tool`，让 Agent 自主决定何时检索

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| RAG 就是"给 LLM 喂文档" | 不是直接喂原始文档，而是"切分 → 向量化 → 相似度检索 → 只喂最相关的片段" |
| Text splitter 随便切 | 切分粒度直接影响检索质量；按语义结构（标题）切分优于按固定字符数 |
| RAG 能根治幻觉 | RAG 能**降低**幻觉（有出处），但不能完全消除（检索错或生成错仍可能） |

---

### 知识点 10：嵌入模型与向量存储

【课程原话/定义】

嵌入模型（Embedding model）：

```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3")

embeddings.embed_query("Hello, world!")
```

向量存储（Vector store）：

```python
from pprint import pprint
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="qwen3-embedding")
vector_store = InMemoryVectorStore(embedding=embeddings)
vector_store.add_texts(
    texts=[
        'hello world',
        '你好世界',
        '你好思寒',
        'hello',
        '无关内容',
    ]
)
r = vector_store.similarity_search_with_score('hello', k=5)
pprint(r, indent=4)

# 输出（按相似度降序）
# [ (Document('hello'),         1.0000),   # 完全相同，得分最高
#   (Document('hello world'),   0.8890),
#   (Document('你好世界'),       0.7463),
#   (Document('你好思寒'),       0.6467),
#   (Document('无关内容'),       0.3366) ]
```

索引与查询两阶段：

```
索引阶段：Documents → Embedding model → Embedding vectors → Vector store
查询阶段：Query text → Embedding model → Query vector → Similarity search → Top-k results
```

【为什么？】

向量检索的核心是"把语义相似度变成数学距离"。文本无法直接比较"意思有多像"，但可以：

1. 用 Embedding 模型把文本转成高维向量（语义相近的文本，向量也相近）
2. 用相似度算法（如余弦相似度）计算查询向量与候选向量的距离
3. 按距离排序，返回 Top-k

从输出能验证一个关键事实：`'hello'` 和 `'hello world'` 得分最高（0.89），`'你好世界'` 次之（0.75），`'无关内容'` 最低（0.34）——**语义越接近，得分越高**，而且跨语言（英文 hello 和中文你好世界）也能捕捉到相关性。这正是向量检索比关键词检索（`LIKE '%hello%'`）强的地方：关键词检索只匹配字面，向量检索匹配"意思"。

注意两个模型的不同：`OllamaEmbeddings(model="llama3")` 用的是通用模型做 embedding，而 `qwen3-embedding` 是**专门的 embedding 模型**——实践中应使用专用 embedding 模型，效果和效率都更好。

【必须掌握】

- Embedding：把文本转成向量，语义相近 → 向量相近
- 向量检索两阶段：索引（存储）和查询（检索）
- `similarity_search_with_score` 返回的是"相似度得分"，分数越高越相似

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| 向量检索 = 关键词匹配 | 向量检索匹配语义，跨语言也能匹配（hello ↔ 你好世界）；关键词只匹配字面 |
| embedding 模型随便选个 LLM | 应用专用 embedding 模型（如 qwen3-embedding），不是拿聊天模型硬凑 |
| 得分越高越不相似 | 得分（相似度）越高越相似，1.0 表示完全相同 |

【我的理解】

> 为什么 `'hello'` 和 `'你好世界'`（一个英文一个中文）在向量检索里也能排到第 3 名？这体现了向量检索相比 SQL 的 `LIKE` 关键词匹配有什么本质优势？

---

### 知识点 11：多智能体（Subagent）

【课程原话/定义】

两种多智能体拓扑：

```
拓扑1（主从）：User → Controller Agent → Tool Agent 1 / Tool Agent 2 → Controller → User Response
拓扑2（链式）：User → Agent A → Agent B → User
```

把子智能体包装成工具：

```python
from langchain.tools import tool
from langchain.agents import create_agent

subagent1 = create_agent(..)

@tool(
    name="subagent1_name",
    description="subagent1_description"
)
def call_subagent1(query: str):
    result = subagent1.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"].text

agent = create_agent(..., tools=[call_subagent1])
```

【为什么？】

多智能体的核心思想是**"把一个 Agent 当成另一个 Agent 的工具"**。主 Agent 不直接干活，而是把子任务分发给子 Agent，自己负责编排和汇总。

为什么需要多智能体？

1. **职责分离**：每个子 Agent 只精通一个领域（如"接口测试专家"、"SQL 专家"），主 Agent 负责路由，比一个大而全的 Agent 更专注、更可控。
2. **上下文隔离**：子 Agent 的推理过程不占用主 Agent 的上下文，避免上下文爆炸。
3. **可独立调试**：每个子 Agent 可以单独测试、单独替换。

两种拓扑的区别：

| 拓扑 | 结构 | 适用场景 |
|------|------|---------|
| 主从（Controller + Worker） | 一个主 Agent 调度多个子 Agent | 任务可分解为多个独立子任务 |
| 链式（A → B） | Agent 顺序传递 | 后一步依赖前一步结果 |

代码里的关键点：`@tool` 装饰器把 `call_subagent1` 这个"调用子 Agent 的函数"包装成工具，主 Agent 就能像调用普通工具一样调用子 Agent。`description` 描述子 Agent 的职责，帮助主 Agent 判断"该把什么任务分给它"。

【必须掌握】

- 多智能体的本质：把子 Agent 包装成工具（`@tool` + 内部 `subagent.invoke`）
- 两种拓扑：主从（controller/worker）、链式（A→B）
- 多智能体价值：职责分离、上下文隔离、可独立调试

【面试考察】

> 面试官："什么时候需要多智能体？LangChain 里怎么实现一个多智能体系统？"

**参考回答框架：**

1. 需要多智能体：任务可拆成多个专业子任务（如一个测试 Agent 拆成"接口测试 Agent"+"UI 测试 Agent"），或需要上下文隔离、职责分离
2. 实现方式：先 `create_agent` 创建子 Agent，再用 `@tool` 把它包装成工具（内部 `subagent.invoke`），最后把工具交给主 Agent
3. 主 Agent 通过 description 判断何时把任务分给哪个子 Agent
4. 更复杂的编排（循环、条件分支）可用 LangGraph

---

## 四、软件测试智能体

### 知识点 12：测试智能体的应用形态

【课程原话/定义】

利用 Agent 根据任务进行探索测试，形成四类测试智能体：

| 类型            | 能力              |
| ------------- | --------------- |
| Web 自动化测试智能体  | 驱动浏览器做 UI 测试    |
| App 自动化测试智能体  | 驱动移动端做 App 测试   |
| 接口自动化测试智能体    | 调用接口做 API 测试    |
| 通用自动化智能体（MCP） | 通过 MCP 接入任意测试工具 |

进阶应用：

- **智能化测试平台演示**：把多类测试智能体整合成统一平台
- **AI 爬虫**：自动探索被测系统并创建**知识图谱**（把页面/接口的关系结构化成图，供后续测试用例生成）

Agent 核心元素回顾（详见 [[Ch04-智能体Agent介绍]] 知识点8）：

```
Agent = LLM + Planning + Parser + Tools + Memory
```

【为什么？】

这是本课程与测试开发的"交集"，也是 Riley 学习路径的最终落点——**用 AI 做自动化测试**。

传统自动化测试的三个痛点，恰好是 Agent 的优势：

1. **脚本脆弱**：元素定位、断言写死在代码里，页面一改脚本就挂。→ Agent 用自然语言描述意图，运行时动态决策，抗变更。
2. **用例固化**：用例是预先写好的，探索新路径要靠人。→ Agent 能"探索测试"，自主发现未覆盖的路径。
3. **工具割裂**：Web/App/接口各用一套框架，学习成本高。→ MCP 统一接入，一个 Agent 能驱动多类工具。

四类测试智能体的本质，都是 Ch03/Ch04 里讲的"把测试能力封装成工具/OpenAPI/MCP，再交给 Agent 调度"。

"AI 爬虫 → 知识图谱"这一步尤其值得注意：Agent 自动探索被测系统，把"页面 A 能跳转到页面 B""接口 X 依赖接口 Y 的 token"这类**关系**结构化存储。有了知识图谱，后续能自动推导测试路径、生成测试用例——这是"智能测试"从"自动执行"走向"自动设计"的关键。

【必须掌握】

- 四类测试智能体：Web / App / 接口 / 通用（MCP）
- Agent 做测试的三大优势：抗变更、探索测试、工具统一接入
- 知识图谱 = 自动探索 + 关系结构化，支撑测试用例自动生成

【企业场景】

> 你在公司负责一个"接口自动化测试智能体"：把测试执行引擎（跑用例、查结果、对比断言）通过 MCP 暴露，Agent 接入后，测试同学输入"回归登录模块"，Agent 自主规划：先查登录模块有哪些用例 → 调 MCP 执行 → 分析失败结果 → 输出缺陷报告。从"写脚本"变成"下指令"，回归测试的人力成本大幅下降。

【面试考察】

> 面试官："怎么用 AI/Agent 改造传统自动化测试？"

**参考回答框架：**

1. 思路：把测试能力（浏览器驱动、接口调用、断言）封装成工具/OpenAPI/MCP，交给 Agent 调度
2. 四类智能体：Web / App / 接口 / 通用（MCP），分别对应不同被测对象
3. 优势：自然语言驱动、运行时动态决策（抗变更）、探索测试（补盲区）、MCP 统一接入多类工具
4. 进阶：Agent 自动探索 + 知识图谱，支撑测试用例自动生成

【我的理解】

> 传统自动化测试"脚本脆弱"的根因是什么？为什么"Agent 用自然语言描述意图、运行时动态决策"能缓解这个问题？它又会引入什么新的风险（提示一下：断言和定位仍然需要确定性）？

---

## 五、版本差异与官方文档

### 知识点 13：LangChain 版本差异

【课程原话/定义】

课程中会用到不同版本，整体差异并不大：

| 版本 | 特点 |
|------|------|
| 1.0 版本 | 更加规范，丢失了一些老版本的细节文档 |
| 0.3 版本 | 更加规范，丢失了一些老版本的细节文档 |
| 0.1 版本 | 内容很详细，有很多底层知识 |

版本使用策略：

- 录播视频：优先使用**稳定版本**
- 直播授课：优先使用**最新版本**

【为什么？】

LangChain 发展快，API 变化频繁，这是它最大的"坑"。理解版本策略能少踩坑：

1. **1.0/0.3 更规范但文档变薄**：框架重构后接口更统一（如 `create_agent`、`init_chat_model` 取代了早期散落的 API），但早期版本里那些"深入底层"的细节文档被删掉了。
2. **0.1 底层知识多**：适合想深入理解原理时查阅，但很多 API 已废弃。
3. **录播稳定、直播最新**：录播视频录制时锁定的是当时的稳定版本，跟着视频学就该用同版本；直播是当下讲，用最新版本能学到最新写法。

【必须掌握】

- 三个版本特点：1.0/0.3 规范但细节文档少，0.1 底层知识全但 API 旧
- 学习策略：录播用稳定版，直播用最新版

【易错点】

| 易混淆 | 正确理解 |
|--------|---------|
| 版本号越高文档越全 | 相反，1.0/0.3 更规范但丢失了早期底层细节文档 |
| 网上随便找段代码就能跑 | LangChain API 变化快，网上老代码可能是 0.1 的写法，需核对版本 |
| 稳定版 = 旧版 = 不好 | 稳定版适合录播跟学，接口变化小、不会"教程跑不通" |

---

## 今日课程总结

| 模块           | 核心内容                                                          | 面试权重  |
| ------------ | ------------------------------------------------------------- | ----- |
| LangChain 定位 | Language + Chains，LLM 应用开发框架                                  | ⭐⭐⭐⭐⭐ |
| 生态架构         | 核心+社区+智能体+Templates+LangServe+LangSmith+LangGraph             | ⭐⭐⭐⭐  |
| 开源 vs 商业     | FastAPI/Jaeger/本地提示词 替代 LangServe/LangSmith/Prompt Hub        | ⭐⭐⭐   |
| 框架对比         | LangChain/LangGraph/LlamaIndex/CrewAI 等选型                     | ⭐⭐⭐⭐⭐ |
| 大模型调用        | init_chat_model（模型无关）/ ChatOllama（OOP）                        | ⭐⭐⭐⭐  |
| 智能体 Demo     | create_agent + tools + set_debug，ReAct 落地                     | ⭐⭐⭐⭐⭐ |
| 对接 MCP       | MultiServerMCPClient，stdio/streamable_http                    | ⭐⭐⭐⭐  |
| RAG          | 工具式 RAG vs 链式 RAG（loader→splitter→embedding→vector→retriever） | ⭐⭐⭐⭐⭐ |
| 向量存储         | Embedding + 相似度检索，语义匹配                                        | ⭐⭐⭐⭐  |
| 多智能体         | 子 Agent 包装成工具，主从/链式拓扑                                         | ⭐⭐⭐⭐  |
| 测试智能体        | Web/App/接口/通用（MCP），探索测试 + 知识图谱                                | ⭐⭐⭐⭐⭐ |
| 版本差异         | 1.0/0.3 规范 vs 0.1 底层，录播稳定/直播最新                                | ⭐⭐    |

---

## 今天没搞懂的问题

-
-
-

## 关联笔记

- [[Ch04-智能体Agent介绍]] — ReAct 循环、五大核心元素（本课的 Agent 机制基础）
- [[Ch03-AI工作流应用开发]] — 工作流 vs Agent（固定编排 vs 动态决策）
- [[Ch01-OpenAI-ChatGPT大语言模型]] — LLM 调用、Function calling（工具调用基础）
- [[../接口测试/README|接口测试]] — 接口自动化测试智能体的被测对象
