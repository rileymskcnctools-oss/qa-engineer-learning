---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch06-Pytest结合数据驱动-YAML"
date: 2026-07-23
status: draft
---

# Ch06 - Pytest 结合数据驱动 - YAML

## 课程来源

- 学习日期：

---

## 一、数据驱动测试（DDT）

### 知识点1：DDT 概念与应用场景

【课程原话/定义】
数据驱动测试（Data-Driven Testing）是将测试数据与测试逻辑分离，使用外部数据源提供测试输入数据并驱动测试执行的方法。数据量小时用代码参数化，数据量大时用结构化文件（CSV、Excel、JSON、YAML）存储。

【为什么？】
硬编码测试数据的最大问题是：加一组新数据就得改代码。DDT 把"测什么"（数据）和"怎么测"（逻辑）解耦，测试人员只需维护数据文件而不用动 Python 代码。对于非开发背景的 QA 同事，改 YAML 文件比改 Python 代码门槛低得多。

【必须掌握】
- DDT 的核心思想：数据与逻辑分离
- 三种应用场景：测试步骤驱动、测试数据驱动、配置数据驱动
- 量与格式的选择：少量 → @parametrize；大量 → YAML/JSON/CSV

【企业场景】
你维护了一个电商下单接口的自动化测试套件。产品经理频繁调整满减规则（满 100-20、满 200-50...），每次调整你不需要改测试代码，只需要在 data/order_promotion.yaml 里增删数据行，测试框架自动读取并生成对应的测试用例。PM 甚至可以直接看 YAML 文件确认测试覆盖了哪些场景。

【面试考察】
面试官："什么是数据驱动测试？为什么要用它？"
参考回答框架：① 核心思想：数据与逻辑分离 ② 好处：提高复用性、降低维护成本、非技术人员也能维护数据 ③ 实现方式：少量用 @parametrize，大量用 YAML/JSON/CSV 文件 ④ 一句话总结：同样的测试逻辑 + 不同的输入数据 → 生成 N 条用例

【易错点】

| 误区 | 正解 |
|------|------|
| DDT = @parametrize 参数化 | @parametrize 只是 DDT 的一种实现方式；DDT 更广，包括文件驱动 |
| 所有数据都放 YAML | 少量固定数据直接用 @parametrize 更简洁；YAML 适合几十行以上的数据集 |
| DDT 只用于接口测试 | App、Web UI、接口、单元测试都可以用 DDT |

【我的理解】

>

---

## 二、YAML 语法基础

### 知识点2：YAML 数据存储规则

【课程原话/定义】
YAML 是一种人类可读的数据序列化格式。三种数据结构：
- **对象**：键值对，用冒号 `:` 表示
- **数组**：有序值，用 `-` 开头
- **纯量**：单个不可再分的值（字符串、布尔值、整数、浮点数、Null、时间、日期）

【为什么？】
YAML 比 JSON 更适合写测试数据：不用引号（除非特殊字符）、支持注释（`#`）、缩进表示层级（直观）、自动类型识别。JSON 写 50 条测试数据没有注释的话完全看不懂每条数据测什么场景，YAML 可以用注释标注"# 正常登录" "# 密码为空" 等。

【必须掌握】
- 对象用 `:` — 等价于 Python dict
- 数组用 `-` — 等价于 Python list
- 纯量自动识别类型（`30` = int、`30.0` = float、`true` = bool）
- 缩进代表层级关系
- `#` 写注释

【企业场景】
你的测试数据 YAML 文件被产品经理打开审查。如果这是 JSON 文件，PM 看到一堆 `"` `{` `}` 会直接放弃。但 YAML 的缩进和注释让非技术人员也能看懂：哪些场景覆盖了、哪些还没测。这在跨团队协作（QA + PM + 开发）里非常重要。

【面试考察】
面试官："YAML 和 JSON 相比，在测试数据管理中有哪些优势？"
参考回答框架：① YAML 支持注释（`#`），JSON 不支持 → 可以标注每条数据的测试意图 ② YAML 更简洁，不需要引号和括号 ③ 类型自动识别，不需要手动转换 ④ 缩进层级比括号更人类可读 ⑤ 劣势：解析速度比 JSON 慢一点，但测试数据量不构成瓶颈

【易错点】

| YAML 语法        | Python 等价          | 注意                |
| -------------- | ------------------ | ----------------- |
| `name: John`   | `{"name": "John"}` | 冒号后必须有空格          |
| `- a`<br>`- b` | `["a", "b"]`       | `-` 后必须有空格        |
| `age: 30`      | `{"age": 30}`      | 自动识别为 int，非字符串    |
| `active: true` | `{"active": True}` | `true`/`false` 小写 |
| 缩进             | 表示嵌套               | 只能用空格，不能用 Tab     |

【我的理解】

>

---

## 三、操作 YAML 文件

### 知识点3：PyYAML 读写

【课程原话/定义】
- 安装：`pip install pyyaml`
- 读取：`yaml.safe_load(f)` — 将 YAML 格式数据转为 Python 对象
- 写入：`yaml.safe_dump(data, f)` — 将 Python 对象转为 YAML 格式写入文件

【为什么？】
`safe_load` 而不是 `load`：`yaml.load()` 可以执行任意 Python 代码（反序列化安全漏洞），`safe_load()` 只解析标准 YAML 类型，企业在安全扫描中会标记 `yaml.load()` 为高危。PyYAML 选择 `safe_load` 是行业安全最佳实践。

【必须掌握】
- `yaml.safe_load(f)` 读取
- `yaml.safe_dump(data, f)` 写入
- `with open()` 上下文管理器 + `encoding='utf-8'` 标准写法
- 读取后数据类型：list/dict/int/str 等 Python 原生类型

【企业场景】
你们团队的测试框架有一个 `data/` 目录，里面全是 YAML 文件。每次新增接口测试，你只需要：① 在 data 下新建一个 YAML ② 按模板填数据行 ③ 测试框架自动读取并生成用例。你写了一个通用的 `get_yaml()` 工具函数放在 `conftest.py` 里，所有测试模块共享。

【面试考察】
面试官："为什么用 `yaml.safe_load()` 而不是 `yaml.load()`？"
参考回答框架：① `yaml.load()` 存在安全漏洞，可以反序列化任意 Python 对象 ② `safe_load()` 只处理标准 YAML 类型（dict/list/str/int 等）③ 这是企业安全扫描的常见检查项 ④ 举例：如果 YAML 文件被恶意注入 `!!python/object/apply:os.system ['rm -rf /']`，`load()` 会执行，`safe_load()` 会报错

【易错点】

| 常见错误 | 正确做法 |
|------|------|
| `yaml.load(f)` | 用 `yaml.safe_load(f)` |
| `open(file)` 不指定 encoding | 加 `encoding='utf-8'`，否则 Windows 可能用 GBK |
| `safe_load()` 后类型对不上 | 检查 YAML 缩进和 `-` 的使用，读取后 `print(type(data))` 确认 |
| 路径写死 `./data.yaml` | 用相对于项目根的路径，或用 `os.path` 动态计算 |

【我的理解】

>

---

## 四、YAML 实现数据驱动测试

### 知识点4：工程结构与实战

【课程原话/定义】
标准工程结构：
```
├── data/
│   └── data.yaml          ← 测试数据
├── src/
│   └── operation.py       ← 被测函数
└── tests/
    └── test_add.py        ← 测试用例
```
通过 `yaml.safe_load()` 读取数据 → `@pytest.mark.parametrize` 传入 → 生成多条用例。

【为什么？】
把数据文件和测试代码分开放在独立的 `data/` 目录，而不是硬编码在测试文件里，有三大好处：① 数据变更不触发代码 review 流程 ② 多个测试模块可以共享同一份数据 ③ CI 中可以根据环境切换数据文件（dev.yaml / staging.yaml / prod.yaml）。

【必须掌握】
- 标准目录结构：`data/`、`src/`、`tests/`
- 读取函数 `get_yaml()` 的写法
- `@pytest.mark.parametrize('x,y,expected', get_yaml())` 的三元组模式
- YAML 数据格式与 parametrize 参数的对应关系

【企业场景】
你维护一个支付接口的自动化测试。测试数据有 80 条（正常支付、余额不足、超时、重复支付...），放在 `data/payment_cases.yaml`。开发和产品都可以在这个 YAML 里增删场景，你只需要在 Python 里写一次测试逻辑，框架自动把 80 条数据变成 80 个独立用例。某条数据有问题时，pytest 精确告诉你第几条失败了，而不是"test_payment 失败"让你去猜是哪个数据。

【面试考察】
面试官："你如何用 YAML 驱动 Pytest 参数化？说一下完整流程。"
参考回答框架：① 在 `data/` 目录建 YAML 文件，按 pytest parametrize 需要的参数结构组织数据 ② 写一个 `get_yaml()` 工具函数，用 `yaml.safe_load()` 读取 ③ 在测试函数上用 `@pytest.mark.parametrize('参数名列表', get_yaml())` ④ pytest 自动把 YAML 中每行数据作为一个独立用例执行 ⑤ 目录结构保持 data/src/tests 三层分离

【易错点】

| 常见错误                        | 原因                       | 正确做法                                                                  |
| --------------------------- | ------------------------ | --------------------------------------------------------------------- |
| YAML 读回来是字符串 `'1'` 不是整数 `1` | YAML 默认类型推断，但某些写法可能产生字符串 | 在测试断言前做 `int(x)` 显式转换，或确保 YAML 数据不带引号                                 |
| `parametrize` 参数数量不匹配       | YAML 每行元素数 ≠ 参数名数量       | YAML 每行数组长度必须等于 parametrize 的参数个数                                     |
| 文件路径在 CI 中找不到               | 相对路径的工作目录不同              | 用 `os.path.join(os.path.dirname(__file__), '../data/data.yaml')` 构造路径 |

【我的理解】

>

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| DDT 概念 | 数据与逻辑解耦，三种应用场景 | ⭐⭐⭐⭐ |
| YAML 语法 | 对象/数组/纯量，注释，类型自动识别 | ⭐⭐⭐⭐ |
| PyYAML 操作 | safe_load / safe_dump | ⭐⭐⭐⭐⭐ |
| YAML 驱动测试 | 目录结构 + parametrize + get_yaml() | ⭐⭐⭐⭐⭐ |

## 今天没搞懂的问题

-
-

## 关联笔记

- [[Ch03-Pytest参数化用例]]
- [[Ch05-Pytest运行用例]]
