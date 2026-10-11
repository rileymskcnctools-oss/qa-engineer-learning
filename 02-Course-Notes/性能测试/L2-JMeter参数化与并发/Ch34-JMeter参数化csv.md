---
tags: [课程笔记, 性能测试, JMeter]
course: "性能测试"
chapter: "Ch34-JMeter参数化csv"
created: 2026-10-11
status: draft
---

# Ch34 - JMeter参数化csv

## 课程来源

- 学习日期：
- 课程模块：性能测试 / L2-JMeter参数化与并发（站点：性能测试工具 / `L2.JMeter 参数化与并发`）
- 站点页：性能测试工具 / L2.JMeter 参数化与并发 → JMeter参数化csv
- 前置：[[Ch32-JMeter变量与引用]]（变量与求值时机）、[[Ch33-使用变量进行参数化测试]]（参数化总览页：四种类型与两种做法）
- 本章定位：**CSV 专页**——把 [[Ch33-使用变量进行参数化测试]] 里一带而过的那 8 步（尤其"配置 CSV Data Set Config"）讲透

> 📌 内容缺口提示：站点该页正文约 700 字 + **5 张截图**，"操作步骤"里除第一步外**全部只有截图、没有文字**，参数一个都没解释。本笔记按原文整理，**CSV Data Set Config 的 9 个参数、行与线程的分配关系、EOF 行为**全部依据 **JMeter 官方文档**（`usermanual/component_reference.html` → CSV Data Set Config）补齐——这部分是本模块最该硬背的实操内容。

---

### 知识点1：CSV 参数化是什么，为什么它是企业主力方案

【课程原话/定义】
利用 CSV（Comma-Separated Values，逗号分隔值）文件来提供参数值，以实现对测试数据的参数化。

课程给出的"CSV 参数化优点"（原文 5 条）：
1. **提高测试效率**：创建通用测试脚本，运行时动态替换参数值，避免为每个场景写单独脚本；
2. **灵活性和可重用性**：改参数值就能重用同一脚本跑不同场景；
3. **数据管理方便**：测试数据集中存储在外部文件（或数据库）中，便于管理与维护；
4. **模拟真实场景**：用不同用户名/密码组合测登录、不同订单数据测订单流程；
5. **易于扩展和维护**：脚本模块化，加场景只需更新参数值。

【为什么？】
这 5 条其实共同指向一个工程结论：**把数据从脚本里彻底搬出去**。UDV 虽然也"搬出去"了，但它是**一次性常量**；CSV 是**按迭代推进的数据流**，差别在于：

- **一份脚本 × N 套数据 = N 个场景**：环境回归、账号池、商品池、订单池都只是"换一个文件"；
- **数据可以"生成"而不是"手打"**：10 000 个订单号可以从生产库脱敏导出、可以脚本批量造——这是 UDV/用户参数做不到的规模；
- **官方明确推荐这种做法**：CSV Data Set Config 页原文——*"It is well suited to handling large numbers of variables"*，且解释了为什么**不要**在运行期硬造数据：*"Generating unique random values at run-time is expensive in terms of CPU and memory, so just create the data in advance of the test."*
- **支持"随机 + 唯一"数据**：官方原文接着说，如果确实需要每次运行的值不同，可以把文件里的"随机"数据与运行期参数**拼接**使用——*"much cheaper than generating everything at run-time"*（比全部在运行期生成便宜得多）。

用一句话记住取舍：**能让施压机少算一步，就别让它算**——施压机的 CPU/内存必须优先留给"发请求"，否则施压机自己先成为瓶颈，压测结论就废了。

【必须掌握】

| CSV 参数化优点（原文 5 条） | 实质 |
|---|---|
| 提高测试效率 | 通用脚本 + 运行时替换参数值，不为每个场景写脚本 |
| 灵活性与可重用性 | 换文件＝换场景，脚本不动 |
| 数据管理方便 | 数据集中在外部文件（或数据库） |
| 模拟真实场景 | 不同账号/密码/订单数据 → 贴近真实用户 |
| 易于扩展与维护 | 加场景只加数据行；脚本模块化 |

| 与另外两种参数化的分工 | 数据量 | 变化节奏 | 典型数据 |
|---|---|---|---|
| 用户定义的变量（UDV） | 极少 | 全程不变 | 域名、端口、tid/vid |
| 用户参数（User Parameters） | 少量 | 每线程一组、按迭代推进 | 给每个线程分一个固定用户 |
| **CSV Data Set Config** | **大量** | **每个迭代取一行** | 账号池、商品池、订单池（企业主力） |

【企业场景】
压测前一周，业务方给了你一份 5 万行的订单表（脱敏）。企业做法：导出成 `orders.csv`，放进脚本同目录，CSV Data Set Config 里指定文件名与列名，请求参数写 `${order_id}`；数据用完的策略按场景定——**容量测试**希望"每条数据只压一次"（`Recycle=False` + `Stop thread on EOF=True`），**稳定性测试**跑几小时则希望"数据循环复用"（`Recycle=True`）。**同一份数据文件，两种策略对应两类测试目的**，这就是 CSV 比 UDV 强的地方。

【面试考察】
面试官："JMeter 里数据量大怎么做参数化？为什么不用 ${__Random} 造唯一数据？"

参考回答框架：
1. 大数据量用 **CSV Data Set Config**（配置元件），数据放文件、每个迭代取一行；
2. 官方观点：唯一随机值在运行期生成**很耗 CPU 和内存**，应"提前把数据准备好"；需要变化时用文件数据 + 运行期参数拼接；
3. 优点：脚本与数据解耦（换文件＝换场景）、可批量生成（从数据库导出）、按迭代推进；
4. 收口：数据用完的行为由 `Recycle on EOF` / `Stop thread on EOF` 控制，按测试目的（容量 vs 稳定性）选择。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 用 `${__Random}` 造 5 万个"唯一"订单号 | 运行期造唯一值耗 CPU/内存，还会撞号；大数据量应提前生成到 CSV（官方观点） |
| 把 CSV 当"另一种 UDV"用 | UDV 全程不变；CSV **每个迭代换一行**，这是它能做参数化的原因 |
| 数据文件与脚本分离管理、路径写绝对路径 | 相对路径更利于换机器/CI；绝对路径在远程（分布式）压测时大概率找不到文件（官方原文提醒） |
| 只准备一份数据文件却要压多环境 | 数据文件应与环境对应（`data_test.csv` / `data_pre.csv`），否则环境间的数据冲突无法解释 |
| 认为"数据放文件里就一定不会重复" | 是否重复取决于 **行数 vs 线程数 vs Recycle/Sharing mode**（知识点3） |

【我的理解】引导题（用自己的话回答）：
1. 用"施压机资源"这个角度解释：官方为什么反对在运行期生成大量唯一随机值？
2. 你要压"容量测试（每条数据只压一次）"，会在 CSV Data Set Config 上做哪两处配置？为什么？

---

### 知识点2：CSV Data Set Config 参数全解（官方核对版）

【课程原话/定义】
操作步骤（原文）：创建线程组 → 创建 HTTP 请求 → 准备一个 `data.csv` 文件 → 创建 CSV Data Set Config 元件 → 配置 CSV Data Set Config → 在 HTTP 请求里进行变量引用 → 创建 Debug Sampler 和 View Results Tree 元件 → 查看结果。

（原文"配置"这一步只有截图，没有任何文字说明——下面的参数表按 **JMeter 官方文档**补全。）

【为什么？】
CSV Data Set Config 有 9 个参数，每一个都能让脚本"静默出错"（不报错、只是数据错）。逐个弄懂它们，比背操作步骤有用得多。官方文档里有几条容易忽略但极其实用的说明：
- **变量名列表可以留空**，此时文件**第一行被当作表头**：*"JMeter supports CSV header lines: if the variable name field empty, then the first line of the file is read and interpreted as the list of column names."*
- **"忽略首行"只在变量名非空时起作用**：*"Ignore first line of CSV file, it will only be used if Variable Names is not empty, if Variable Names is empty the first line must contain the headers."*
- **行内值少于变量名个数时，多余的变量保留上一次的值**（不会清空）：*"If there are fewer values on the line than there are variables the remaining variables are not updated - so they will retain their previous value (if any)."* ——这是"数据错位却看不出来"的常见原因。
- **分隔符写 `\t`（不带引号）会被当作 Tab**：*"the string '\t' (without quotes) in the delimiter field is treated as a Tab."*
- **允许引号后，值里可以包含分隔符**：如 `1,"2,3","4""5"` 会被解析成 `1`、`2,3`、`4"5"`（引号内两个双引号表示一个双引号）。

【必须掌握】

| 参数 | 官方含义 | 实践建议 |
|---|---|---|
| Filename | 数据文件；相对路径解析依赖脚本/启动目录，**绝对路径在远程模式下大概率不可用** | 与脚本放同目录，写文件名；换机器只需带文件 |
| File Encoding | 读文件用的编码 | 统一 UTF-8；中文乱码先查这里 |
| Variable Names | 变量名列表，用**分隔符**分隔，可用双引号包起来；**留空则首行当表头** | 推荐留空 + 文件首行写表头（数据文件自解释） |
| Ignore first line（新版界面写作 Use first line as Variable Names） | **仅当 Variable Names 非空时**才生效；Variable Names 为空时首行**必须**是表头 | 若写了 Variable Names 又有表头 → 勾上跳过首行 |
| Delimiter | 分隔符；写 `\t`（不带引号）＝ Tab | 数据里含逗号时用 Tab 或分号 |
| Allow quoted data? | 是否允许值用双引号包裹（值里可含分隔符） | 数据本身含引号/逗号时开启，并注意 `""` 转义 |
| Recycle on EOF? | 读到文件尾是否**从头重读**（默认 **true**） | 容量测试设 false；稳定性测试用默认 true |
| Stop thread on EOF? | Recycle＝false 时，EOF 是否**停止线程**（默认 false） | "每条数据只压一次"要设 true |
| Sharing mode | 文件在线程间的共享方式（默认 All threads） | 见知识点3；"每线程独立数据"用 Current thread |

【企业场景】
你把订单池放进 `orders.csv`，首行写表头 `order_id,amount`，Variable Names 留空（让 JMeter 自己读表头）——这样**文件自己说明了列名**，同事接手时不必问"第一列是什么"。若某天业务数据里出现了含逗号的字段（如商品名 `A,B 套餐`），你会把 Delimiter 换成 Tab 并相应调整 `\t` 写法，同时把 `Allow quoted data?` 打开——**这三处（分隔符、引号、编码）是 CSV 数据"看起来对、压出来错"的三大常见源头**。

【面试考察】
面试官："CSV Data Set Config 有哪些参数？Variable Names 留空会怎样？"

参考回答框架：
1. 参数：Filename / File Encoding / Variable Names / Ignore first line / Delimiter / Allow quoted data? / Recycle on EOF? / Stop thread on EOF? / Sharing mode；
2. Variable Names 留空 → **文件首行被当成表头**（官方）；写了 Variable Names 又想跳过表头 → 勾 Ignore first line；
3. 行内值少于变量名个数时，未赋值的变量**保留旧值**（不会清空），是数据错位的常见原因；
4. 分隔符 `\t` ＝ Tab；允许引号后值内可含分隔符（`""` 表示一个双引号）。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| Variable Names 写了名字、文件里又有表头，却没勾"忽略首行" | 表头那行会被当成**第一条数据**用掉（表现为"第一条数据怪怪的"） |
| Variable Names 为空，又在文件里删掉了表头 | 首行必须能当表头（官方）；否则列名变成整行文本，引用全错 |
| 中文数据乱码 | 先查 File Encoding 与文件真实编码是否一致，统一 UTF-8 |
| 行内列数少于变量名，以为会报错 | 不报错，**剩余变量保留上一次的值**（官方原文）——数据错位且难发现 |
| 分隔符用逗号，而数据里本来就有逗号 | 列被切错；改用 Tab（`\t`）或分号，并考虑开启 Allow quoted data? |
| 相对路径/绝对路径随手写 | 相对路径更可移植；绝对路径在分布式远程模式下大概率不可用（官方原文提醒） |

【我的理解】引导题（用自己的话回答）：
1. "Ignore first line 只在 Variable Names 非空时才起作用"——请解释这两者的配合关系，并说明你更推荐哪种组合（写 Variable Names + 勾忽略首行，还是 Variable Names 留空）。
2. 行内列数少于变量名个数时会发生什么？为什么这个行为比"报错"更危险？

---

### 知识点3：行与线程怎么分配（默认行为 / Sharing mode 四种 / 行数不够怎么办）

【课程原话/定义】
（原文未涉及，本节为官方文档补齐的机制部分。）

【为什么？】
这是 CSV 参数化**最容易想当然**的地方。官方原文给出了默认行为：*"By default, the file is only opened once, and each thread will use a different line from the file. However the order in which lines are passed to threads depends on the order in which they execute, which may vary between iterations. Lines are read at the start of each test iteration. The file name and mode are resolved in the first iteration."*

拆开就是四件事：
1. 默认 `Sharing mode = All threads`：**文件只打开一次，由所有线程共享**；
2. **每个线程取不同的行**（不会两个线程同时拿同一行）；
3. 但"哪一行给哪个线程"取决于**线程执行的顺序**，每次迭代都可能不同——所以**不要假设"线程 1 一定拿第 1 行"**；
4. **行是在每个测试迭代开始时读取的**（对应 [[Ch32-JMeter变量与引用]] 的"求值时机"：CSV 变量属于"每迭代"那一档）。

`Sharing mode` 四种取值（官方）：

| 取值 | 官方含义 | 什么时候用 |
|---|---|---|
| All threads（默认） | 文件在所有线程之间共享 | 常规账号池/商品池：数据量 ≥ 总请求数时"每行用一次" |
| Current thread group | 每个线程组各打开一次文件 | 多个线程组要各自从头开始读同一份数据 |
| Current thread | **每个线程各打开一次文件** | "每个线程用自己的数据集"——例如每人一个账号从头用到尾 |
| Identifier | 相同 identifier 的线程共享同一个文件 | 让不同线程组里"编号相同的线程"共享数据 |

官方还给了一个很实用的技巧：*"If you want each thread to have its own set of values, then you will need to create a set of files, one for each thread. For example test1.csv, test2.csv, …, testn.csv. Use the filename test${__threadNum}.csv and set the 'Sharing mode' to 'Current thread'."* ——**文件名里用 `${__threadNum}` + Sharing mode 选 Current thread**，就能做"每个虚拟用户一套独立数据文件"（例如每人的订单清单）。

行数与线程数的关系（工程换算）：
- 线程数 × 循环次数 ≤ 文件行数（且 `Recycle=false`）→ 每行最多用一次，数据不重复（容量测试理想态）；
- 行数不足时：`Recycle=true`（默认）→ 回到第一行重读，**同一行会被再次使用**（稳定性测试可接受）；
- `Recycle=false` + `Stop thread on EOF=false` → 变量被置为 `<EOF>`（假值继续发请求，**数据会错**）；
- `Recycle=false` + `Stop thread on EOF=true` → 线程在数据用完后停止（线程数会逐渐减少，报告里活动线程数下降是正常现象）。

【必须掌握】

| 关键结论 | 说明 |
|---|---|
| 默认 All threads：文件打开一次、线程间共享、每线程取不同行 | 官方原文 |
| 行的分配顺序与线程执行顺序相关，**每次迭代可能不同** | 不要依赖"第 N 个线程拿第 N 行"（官方原文） |
| 行在每个**迭代**开始时读取 | 迭代内的多个取样器共用同一行的值 |
| 文件与模式在**第一次迭代**解析 | 中途改配置不生效；依赖运行期变量的文件名要在首轮就可用（官方原文） |
| 每线程独立数据：`test${__threadNum}.csv` + Sharing mode = Current thread | 官方给出的标准做法 |
| 行数不够：Recycle 决定"重读"还是"停线程/填 `<EOF>`" | 与测试目的绑定（容量 vs 稳定性） |

【企业场景】
你压"100 个虚拟用户，每人 20 条订单"。企业做法：把 100 个用户的订单拆成 100 个文件 `orders_1.csv … orders_100.csv`，CSV Data Set Config 的 Filename 写 `orders_${__threadNum}.csv`、Sharing mode 选 `Current thread`、`Recycle=false` + `Stop thread on EOF=true`——每个虚拟用户只压"自己的"订单，压完即停。**这样报告能直接回答"某个用户的订单失败了吗"**，而用默认 All threads + 一个大文件时，你只能看到"整体失败率"。

【面试考察】
面试官："JMeter 用 CSV 参数化时，多个线程怎么分配数据行？怎么保证每个线程用自己的数据？"

参考回答框架：
1. 默认（All threads）：文件只打开一次，线程间共享，每个线程取不同行；**分配顺序取决于线程执行顺序，不保证"第 N 线程第 N 行"**（官方原文）；
2. 行在**每个迭代开始**时读取，文件与模式在第一次迭代解析；
3. 要让每个线程用自己的一套数据：官方做法是 `test${__threadNum}.csv` + `Sharing mode = Current thread`；或用 User Parameters / 自定义 identifier；
4. 数据不够时的策略与测试目的绑定：Recycle=true 重读（稳定性），Recycle=false + Stop thread on EOF=true 停线程（容量/每条只压一次）。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 认为"线程 1 一定用第 1 行数据" | 官方明确：行的分配顺序取决于线程执行顺序，**每次迭代可能不同** |
| 用默认 All threads 却想"每人固定账号" | 那要 `Sharing mode = Current thread`（或 User Parameters）；默认模式下同一线程不同迭代会换行 |
| 行数不足时以为 JMeter 会报错 | `Recycle=true`（默认）静默重读；`Recycle=false` + `Stop=false` 静默填 `<EOF>` —— 两种都不报错，数据已失真 |
| 迭代内的多个请求以为各自换行 | 行在**迭代开始时**读取，同一迭代内所有取样器共用同一行 |
| 文件名里用了运行期变量（`${token}.csv`）又指望它生效 | 文件名与模式在**第一次迭代**解析（官方原文），拿不到运行期值就会读文件失败 |

【我的理解】引导题（用自己的话回答）：
1. 为什么"分配顺序取决于线程执行顺序"这件事，会让"用第 N 行数据对应第 N 个用户"的验证方法失效？
2. 请设计一个配置，让"每个虚拟用户只压自己的 20 条订单、压完就停"——写出 Filename / Sharing mode / Recycle / Stop thread 四项取值。

---

### 知识点4：EOF 与边界情况（`<EOF>`、eofstring、配置时刻不可用）

【课程原话/定义】
（原文未涉及，本节为官方文档补齐的边界知识。）

【为什么？】
CSV 有三个"只在边界出现、但一出就整轮数据作废"的行为，官方原文都写清楚了：

1. **EOF 的两种处理**：*"When the end of file (EOF) is reached, and the recycle option is true, reading starts again with the first line of the file. If the recycle option is false, and stopThread is false, then all the variables are set to `<EOF>` when the end of file is reached."* ——注意那个字面值 **`<EOF>`**：它会**原样出现在请求参数里**，接口返回 200、业务全错。该字面值可以用 JMeter 属性 `csvdataset.eofstring` 改（企业里常改成 `NOT_FOUND` 之类显眼值，配合断言让失败暴露）。
2. **配置时刻 vs 运行时刻**：*"CSV Dataset variables are defined at the start of each test iteration. As this is after configuration processing is completed, they cannot be used for some configuration items - such as JDBC Config - that process their contents at configuration time (see Bug 40394). However the variables do work in the HTTP Auth Manager, as the username etc. are processed at run-time."* ——翻译成人话：**CSV 变量只对"运行期才读取内容"的元件有效**；JDBC Connection Configuration 这类"配置时刻就处理"的元件拿不到 CSV 变量（要在 `JDBC URL` 里用 CSV 变量会失败），而 HTTP 授权管理器、请求参数、请求头这些运行期元件都能用。
3. **文件身份按路径字符串判定**：*"If the same physical file is referenced in two different ways - e.g. csvdata.txt and ./csvdata.txt - then these are treated as different files."* ——同一个文件写成两种路径，JMeter 会当成两个文件**各自独立打开**（于是"其实只有一份数据"变成两套游标），并发下数据重复的诡异现象往往出在这里。

【必须掌握】

| 边界 / 参数 | 行为 | 应对 |
|---|---|---|
| Recycle=true（默认） | EOF 后从第一行重读 | 稳定性测试；数据行会被多次使用（可接受） |
| Recycle=false + Stop=false | EOF 后变量被设为 **`<EOF>`** | 危险默认：请求会带 `<EOF>` 发出；建议改 `csvdataset.eofstring` 为显眼值并配断言 |
| Recycle=false + Stop=true | EOF 后**停止线程** | 容量测试（每条数据只压一次）；报告里活动线程数会下降 |
| CSV 变量在配置时刻不可用 | JDBC Config 等元件拿不到（Bug 40394） | 这类元件用 UDV/属性传值；运行期元件（请求头/授权/参数）可用 |
| 同一文件两种路径写法 | 被视为**不同文件**（官方原文） | 统一写法，别混用 `data.csv` 与 `./data.csv` |
| `\t` 分隔符 | 不带引号的 `\t` ＝ Tab | 数据含逗号时使用 |
| 引号数据 | `1,"2,3","4""5"` → `1` / `2,3` / `4"5"` | 值内含分隔符时开启 Allow quoted data? |

【企业场景】
你压"10 000 条订单、每条只压一次"，配置 `Recycle=false` + `Stop thread on EOF=true`。压完看报告：活动线程数在后期逐步下降、总请求数≈10 000，符合预期。但如果同事把 `Stop thread on EOF` 忘了勾（默认 false），报告会显示"请求数超过 10 000、错误率飙升"——**因为多出来的请求把 `<EOF>` 当订单号发了出去**。排查时别怀疑被测系统，先看 CSV 的 `File Encoding`/路径/Recycle 三件事，再看结果树里参数是不是 `<EOF>`。**把 eofstring 改成 `NOT_FOUND` 这类显眼值，能让这类事故在第一眼就被看见。**

【面试考察】
面试官："CSV 数据用完了，JMeter 会怎样？变量能用在 JDBC 连接配置里吗？"

参考回答框架：
1. 数据用完：Recycle=true → 从头重读；Recycle=false + Stop=true → 停止线程；Recycle=false + Stop=false → 所有变量被置为 `<EOF>`（可用 `csvdataset.eofstring` 改）；
2. CSV 变量在**每个迭代开始**定义，属于运行期变量 → JDBC Connection Configuration 这类"配置时刻处理内容"的元件拿不到（Bug 40394），但 HTTP 授权管理器/请求头/参数能用；
3. 加分：同一物理文件写成两种路径会被当成两个文件；`\t` 即 Tab；引号数据的 `""` 转义规则。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 忘了 `Stop thread on EOF`（默认 false），又设了 `Recycle=false` | 变量会变成 `<EOF>` 继续发请求 → 数据全错、错误率飙升；建议改 eofstring 为显眼值 + 加断言 |
| 想在 JDBC 连接配置的 URL 里用 CSV 变量 | 拿不到（配置时刻 vs 运行时刻，Bug 40394）；这类值用 UDV/属性 |
| 数据文件路径一会儿 `data.csv`、一会儿 `./data.csv` | 会被当成**两个文件**分别打开（官方原文），并发下数据分布诡异 |
| 认为"变量名写对了就一定取到值" | 编码/分隔符/列数任一不对都可能取错或取空，且不报错；小样本 + Debug Sampler 验证 |
| 稳定性测试用 `Recycle=false` | 跑 2 小时时数据很快用完 → 线程陆续停止，场景"越压越轻"，指标失真 |

【我的理解】引导题（用自己的话回答）：
1. `Recycle=false` + `Stop thread on EOF=false` 时，请求参数里会出现什么？为什么说这个组合"最危险"？
2. 为什么 JDBC 连接配置用不了 CSV 变量，而 HTTP 授权管理器可以用？（提示：看"谁在什么时刻读内容"）

---

### 知识点5：实操 7 步 + 验证 + 事故排查清单

【课程原话/定义】
操作步骤（原文）：创建线程组 → 创建 HTTP 请求 → 准备一个 `data.csv` 文件 → 创建 CSV Data Set Config 元件 → 配置 CSV Data Set Config → 在 HTTP 请求里进行变量引用 → 创建 Debug Sampler 和 View Results Tree 元件 → 查看结果。

【为什么？】
把这 8 步的"验收标准"补上，才算真会：CSV 的所有失败都是**静默**的，因此每一步都要有可检查的证据，而不是"点完了就算做完"。

【必须掌握】

| 步骤 | 操作 | 验收证据 |
|---|---|---|
| 1–2 | 线程组 + HTTP 请求 | 先用 **1 线程 1 循环**（数据只有几行时最容易看出问题） |
| 3 | 准备 `data.csv` | 首行表头（或与 Variable Names 对应）；UTF-8 编码；列数一致 |
| 4–5 | CSV Data Set Config + 配置 | Filename（相对路径）/ Variable Names / Delimiter / Recycle / Stop thread on EOF / Sharing mode 六项明确 |
| 6 | 请求里 `${列名}` 引用 | 大小写与列名完全一致（变量名大小写敏感） |
| 7 | Debug Sampler + View Results Tree | Debug Sampler 看**取值**；View Results Tree 看**请求里是否替换** |
| 8 | 查看结果 | 断言校验业务；确认行使用分布（去重数量）与线程结束情况 |
| 收尾 | 正式压测前 | **删掉 Debug Sampler / View Results Tree**（否则施压机内存被响应数据吃掉） |

**排查清单（按顺序问自己）**：
1. 值取到了吗？（Debug Sampler 里变量是否为空 / `<EOF>` / 表头文本）
2. 请求引用对了吗？（View Results Tree → Request，看 `${order_id}` 是否原样发出）
3. 文件读对了吗？（路径是否与预期同一份；编码是否为 UTF-8；分隔符是否与文件一致）
4. 数据分配合理吗？（行数 vs 线程数 × 循环数；Sharing mode 是否符合预期；Recycle/Stop 组合是否符合测试目的）
5. 业务真的成功了吗？（断言；别只看 HTTP 200）

【企业场景】
交付评审时，这五问就是"数据可信度"的证据链。一个真实的高频事故：脚本从测试环境换到预发环境时，同事只改了 `host`，忘了换数据文件——账号在预发库里不存在，登录全部失败，但**脚本不报错**（HTTP 200 + 业务码 1001）。上线前评审的关键动作之一就是"指着 Debug Sampler 与结果树，把第 1~5 问各答一遍"。

【面试考察】
面试官："你的 CSV 参数化脚本怎么验证？数据重复了怎么排查？"

参考回答框架：
1. 双元件验证：Debug Sampler 看变量值、View Results Tree 看请求里是否替换；再加断言看业务；
2. 数据分布检查：行数 vs 线程数 × 循环数、行去重数量、`<EOF>` 出现与否、线程是否提前结束；
3. 常见原因：路径/编码/分隔符错误、Variable Names 与表头配合错误、Sharing mode 与 Recycle 配置不当、同一文件两种路径写法；
4. 纪律：小样本调通 → 放大并发 → 正式压测前删调试元件。

【易错点】

| 常见错误 | 正确理解 |
|---|---|
| 直接上 500 线程调 CSV | 先 1 线程 1 循环调通（数据少时错误更容易现形），再放大 |
| 只看 Debug Sampler，不看请求内容 | 取值正确 ≠ 引用正确；两层都要看 |
| 用"请求数够多"证明"数据分得开" | 要看去重数量（或按线程拆分文件），不是看总数 |
| 报告中活动线程数下降被当成故障 | 若 `Stop thread on EOF=true` 且数据用完，线程正常结束；要结合数据行数判断 |
| 交付时调试元件仍在脚本里 | 正式压测前必须删除（内存与结果失真），验证完就删 |

【我的理解】引导题（用自己的话回答）：
1. 把"排查清单五问"按你自己的理解重排一遍：哪一问应该最先问？为什么？
2. 如果压测报告显示"请求数远大于数据行数、错误率很高"，你会先怀疑哪三个配置项？

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| CSV 参数化的价值 | 数据与脚本解耦、大数据量、按迭代推进；官方：运行期造唯一值耗 CPU/内存，应提前准备数据 | ★★★★★ |
| 元件参数 9 项 | Filename / Encoding / Variable Names（留空＝首行表头）/ Ignore first line / Delimiter（`\t`）/ Allow quoted data / Recycle / Stop thread on EOF / Sharing mode | ★★★★★ |
| 行与线程的分配 | 默认 All threads：文件打开一次、线程共享、各取不同行；分配顺序**不保证**与线程序对应；每迭代读一行；每线程独立数据用 `test${__threadNum}.csv` + Current thread | ★★★★★ |
| EOF 与边界 | Recycle=true 重读；Recycle=false + Stop=false → 变量变 `<EOF>`（可用 `csvdataset.eofstring` 改）；CSV 变量配置时刻不可用（JDBC，Bug 40394）；同文件两种路径＝两个文件 | ★★★★☆ |
| 实操与排查 | 8 步 + 双元件验证 + "五问"排查清单；正式压测前删调试元件 | ★★★★★ |

## 今天没搞懂的问题

-
-
-

## 课程原图（截图占位清单）

> 📷 【截图占位】准备一个 data.csv 文件（原文 1 张）
> 📷 【截图占位】创建 CSV Data Set Config 元件（原文 1 张）
> 📷 【截图占位】配置 CSV Data Set Config（原文 1 张）
> 📷 【截图占位】在 HTTP 请求里进行变量引用（原文 1 张）
> 📷 【截图占位】创建 Debug Sampler 和 View Results Tree，查看结果（原文 1 张）

## 关联笔记

- [[Ch32-JMeter变量与引用]]（变量求值时机：CSV 属于"每个迭代"那一档）
- [[Ch33-使用变量进行参数化测试]]（参数化总览页：四种类型与两种做法）
- [[../L1-JMeter常用组件/Ch22-JMeter常用配置元件剖析|L1 Ch22-常用配置元件剖析]]（CSV Data Set Config 首次出现；配置元件的作用范围与执行时机）
- [[../L1-JMeter常用组件/Ch25-JMeter执行顺序|L1 Ch25-执行顺序]]（配置元件在取样器之前处理）
- [[../L1-JMeter常用组件/Ch24-JMeter后置处理器|L1 Ch24-后置处理器]]（关联：值从响应来，与 CSV 的"值从数据源来"互补）
- [[../L1-JMeter常用组件/Ch21-JMeter断言元件的使用|L1 Ch21-断言元件的使用]]（用断言让 `<EOF>` 这类静默失败暴露）
- [[../L1-性能测试体系/Ch10-性能测试场景设计|L1 Ch10-性能测试场景设计]]（容量 vs 稳定性 → 决定 Recycle / Stop thread 组合）
- [[../../../01-Learning-Path/投简历冲刺-复习优先级|投简历冲刺 · 复习优先级]]
