---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch15-抓包工具Fiddler"
created: 2026-09-15
status: draft
---

# Ch15 - 抓包工具 Fiddler

## 课程来源
- 学习日期：

---

## 一、Fiddler 是什么

### 知识点 1：Fiddler 简介与原理

【课程原话/定义】
Fiddler 是最常用的 Web 调试工具之一，是一个 HTTP 协议调试代理工具，由 C# 编写，包含一个基于 JScript.NET 事件脚本子系统，能用 .NET 框架语言扩展，可记录并检查客户端与服务器之间的 HTTP/HTTPS 请求，支持监视、设置断点、修改输入输出数据，以及请求构造、设置网络丢包和延迟做 APP 弱网测试。官网：https://www.telerik.com/fiddler

**原理**：Fiddler 以 Web 代理服务器形式工作。对 Web 客户端来说，Fiddler 扮演服务器的角色（接受请求、返回响应）；对 Web 服务器来说，Fiddler 扮演客户端的角色（发送请求、接受响应）。

【为什么？】
Fiddler 的原理和 Charles 完全一样——都是**中间人代理**。区别在于技术栈和平台：Fiddler 是 C#/.NET 写的、**仅 Windows**，Charles 是跨平台（Mac/Windows/Linux）。理解"中间人"这个共同原理，你就同时掌握了 Charles 和 Fiddler 两个工具，它们只是界面和细节不同。Fiddler 的杀手锏是 **FiddlerScript**（JScript.NET 脚本），可以编程扩展抓包逻辑，这是 Charles 不如它的地方。

【必须掌握】
- Fiddler 是 HTTP/HTTPS 调试代理工具，仅 Windows（C#/.NET 编写）
- 原理 = 中间人代理（对客户端扮服务器、对服务器扮客户端）
- 能力：记录/检查请求、断点、改数据、请求构造、弱网模拟
- 特色：FiddlerScript（JScript.NET）可编程扩展
- 与 Charles 对比：Charles 全平台，Fiddler 仅 Windows 但脚本扩展更强

【企业场景】
你在公司做接口测试，Windows 环境下常用 Fiddler 抓包：前端用 Fiddler 调 JS/CSS/HTML，后端用 Fiddler 看请求响应定位问题，你用 Fiddler 改请求参数、模拟后端返回、快速定位缺陷。如果公司同事用 Mac，则统一用 Charles；Windows 机器上 Fiddler 是很多人的首选。

【面试考察】
面试官："Fiddler 和 Charles 有什么区别？"

参考回答框架：
1. 都是 HTTP/HTTPS 中间人代理抓包工具，原理相同
2. Fiddler 仅 Windows（C#/.NET），Charles 全平台
3. Fiddler 有 FiddlerScript 可编程扩展；Charles 界面更友好、弱网模拟更直观
4. 默认端口都是 8888，都需装证书抓 HTTPS
5. 选型：Windows 团队常用 Fiddler，跨平台团队用 Charles

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Fiddler 是跨平台的 | Fiddler 仅 Windows（Fiddler Everywhere 才跨平台，是另一款产品） |
| Fiddler 和 Charles 原理不同 | 都是中间人代理，原理一致，只是实现和界面不同 |
| 把 FiddlerScript 当普通脚本 | 它是 JScript.NET，基于 .NET 框架，能扩展 Fiddler 功能 |

【我的理解】
> （Fiddler 和 Charles 都是"中间人代理"，但一个仅 Windows、一个跨平台。如果你们团队一半 Mac 一半 Windows，你会选哪个工具统一抓包？为什么？）

---

### 知识点 2：Fiddler 下载安装

【课程原话/定义】
下载：官网 → FIDDLER TOOLS → Fiddler Classic → Try For Free → 选择用途 + 填邮箱 + 选 Country + 勾选 I agree / I accept → Download For Windows。
安装：双击运行 → I agree → 可改安装路径 → Install → 等待完成 → 双击 Fiddler.exe 运行。首次运行弹 AppContainer 提示框，点 Cancel 即可。

【为什么？】
为什么要提 AppContainer 弹窗？因为 Windows 的 AppContainer 隔离技术会干扰对 Edge/沉浸式应用流量的捕获，Fiddler 用 WinConfig 按钮（工具栏）或 `Tools → Win8 Loopback Exemptions` 来解除这个隔离。了解这一点，遇到"抓不到 Edge 浏览器的包"就知道不是 Fiddler 坏了，而是 Windows 隔离机制在作怪。

【必须掌握】
- 官网 telerik.com/fiddler → Fiddler Classic（免费）
- 首次运行的 AppContainer 提示点 Cancel（或用 WinConfig 解除隔离）
- 抓不到 Edge/沉浸式应用流量时，用 WinConfig / Win8 Loopback Exemptions

【企业场景】
你在公司装好 Fiddler 后发现抓不到 Edge 的请求，排查时先点工具栏的 WinConfig 解除 AppContainer 隔离。这是 Windows 特有的坑，Mac 上装 Charles 不会遇到。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 抓不到 Edge 流量以为 Fiddler 坏了 | 是 AppContainer 隔离，用 WinConfig 解除 |
| 下载 Fiddler Everywhere 当 Classic | Everywhere 是另一款跨平台收费产品，Classic 才是免费版 |

【我的理解】
> （为什么 Windows 的 Edge/沉浸式应用流量 Fiddler 默认抓不到？这和 Windows 的什么安全机制有关？）

---

## 二、界面简介

### 知识点 3：界面六大区域（菜单栏 / 工具栏 / 会话面板）

【课程原话/定义】
Fiddler 界面分六部分：菜单栏、工具栏、会话面板、辅助标签+工具、命令行、状态栏。

**菜单栏**：File（Session 操作）、Edit（复制/删除/查找）、Rules（Hide Image Request、Hide CONNECTS、Automatic Breakpoints、Customize Rules 打开 FiddlerScript）、Tools（Options、Clear Cache/Cookies、TextWizard、Compare Session）、View（布局/Inspectors/Composer/Statistics 等）、Help。

**工具栏**：WinConfig（解除 AppContainer）、备注、数据重放（Replay，快捷键 R）、清空面板（Ctrl+X）、debug 断点放行（Go）、流/缓冲模式切换、解压、保存会话（saz）、保存截图、计时器、快速启动浏览器、清缓存、编码解码（TextWizard）、拆分窗口、搜索、在线帮助、显示本机 IP、关闭工具栏。

**会话面板（表头字段）**：
| 字段 | 含义 |
|------|------|
| # | 请求顺序（从 1 递增） |
| Result | 响应状态码 |
| Protocol | 协议（HTTP/HTTPS/FTP） |
| Host | 请求域名 |
| URL | 路径 + 文件名 + GET 参数 |
| Body | 请求大小（byte） |
| Caching | 缓存信息 |
| Content-Type | 响应类型 |
| Process | 发出请求的进程及 PID |
| Comments | 备注 |

【为什么？】
为什么要记"会话面板表头字段"？因为抓包后第一步是"在会话列表里快速读懂每个请求"——Result 看状态码、Host/URL 看请求去哪、Process 看是哪个进程发的、Body 看大小。这些字段就是"抓包结果的元信息"，能读懂才能快速过滤和定位目标请求。工具栏里最关键的是**流/缓冲模式**：流模式实时返回（有请求就有响应），缓冲模式等数据齐了再返回，影响你看到响应内容的时机。

【必须掌握】
- 界面六部分：菜单栏/工具栏/会话面板/辅助标签/命令行/状态栏
- 会话表头核心字段：# / Result / Host / URL / Process / Body
- 工具栏关键按钮：Replay（重放）、Go（放行断点）、流/缓冲模式切换
- Rules → Customize Rules 打开 FiddlerScript 编辑器

【企业场景】
你在公司抓包时，先扫一眼会话面板：Process 列找到 App 进程发的请求，Result 列看有没有 4xx/5xx 异常，Host 列定位到目标服务的域名。找到目标请求后，再进 Inspectors 看详细内容。会话面板是"快速定位"，Inspectors 是"深入分析"。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 分不清流模式和缓冲模式 | 流模式实时返回，缓冲模式等数据齐了再返回 |
| 找不到目标请求 | 先看 Process/Host 列过滤，或用 Filters 过滤 |
| Replay 和 Go 混淆 | Replay 是重发请求，Go 是放行断点 |

【我的理解】
> （会话面板的 Process 字段有什么用？如果抓了一堆包，你怎么快速找到"某个 App 进程发的请求"？）

---

### 知识点 4：核心标签页（Inspectors / Statistics / AutoResponder / Composer / Filters）

【课程原话/定义】
辅助标签页：
- **Inspectors**：查看选定会话的请求和响应（上面请求、下面响应），子选项卡有 Headers/TextView/SyntaxView/WebForms/HexView/Raw/JSON/XML 等
- **Statistics**：统计选中会话的性能（Request Count、Bytes sent/received、ClientConnected → ClientDoneResponse 各阶段耗时、Response Codes、Per Host 请求数）
- **AutoResponder**：创建规则自动响应请求，可返回之前捕获的响应而不访问服务器（常用作 mock）
- **Composer**：手动构建和发送 HTTP/HTTPS/FTP 请求（Parsed/Raw/Scratchpad/Options 四个子选项卡）
- **Filters**：过滤器（Hosts 主机过滤、Client Process 进程过滤、Request Headers 请求头过滤、URL contains 过滤）
- **Timeline**：瀑布图查看 1~250 个会话，用于性能分析

【为什么？】
这五个标签页是 Fiddler 的"实战核心"，各有分工：
- **Inspectors** = 看内容（请求/响应的 header、body、json/xml 树）
- **Statistics** = 看性能（一次请求的各阶段耗时分解）
- **AutoResponder** = 做 mock（不访问服务器，直接返回预设响应）
- **Composer** = 构造请求（手动发、改参数、序列化请求）
- **Filters** = 过滤（大海捞针时聚焦目标流量）

理解这五个分工，你就知道"看请求用哪个、做 mock 用哪个、构造请求用哪个"。

【必须掌握】
- Inspectors：看请求+响应详情（Header/TextView/Raw/JSON/XML 子视图）
- Statistics：性能统计（各阶段耗时、响应码分布）
- AutoResponder：自动响应 = 轻量 mock（返回预设响应不访问服务器）
- Composer：手动构造请求（Parsed 可视化 / Raw 纯文本）
- Filters：Hosts/Process/Header/URL 过滤

【企业场景】
你在公司：想看某接口返回的数据 → Inspectors；想分析某接口慢在哪一段 → Statistics（看 DNS/TCP/HTTPS 握手各阶段耗时）；想 mock 掉还没开发好的接口 → AutoResponder 返回预设响应；想手动改参数重发 → Composer；抓包太多想只看目标域名 → Filters。这就是 Fiddler 五个标签页的日常分工。

【面试考察】
面试官："Fiddler 怎么做 mock？"

参考回答框架：
1. 用 AutoResponder 标签页创建规则
2. 规则匹配目标 URL，返回之前捕获的响应（或本地文件）
3. Enable rules 勾选激活，请求匹配时不访问真实服务器
4. 适合模拟"还没开发好的接口"或"特定返回场景"

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 用断点做所有 mock | 断点要手动放行，AutoResponder 是自动响应，更适合批量 mock |
| Statistics 只看 Overall Elapsed | 各阶段耗时（DNS/TCP/HTTPS握手）才是定位慢的根因 |
| Composer Raw 格式写错仍 Execute | Raw 里请求头后没空行（CRLF）会导致请求发不出去 |

【扩展知识】
课程源笔误提示：Statistics 里的 `Elasped` 实为 `Elapsed`（总耗时）；QuickExec 示例中 `Mozilia` 实为 `Mozilla`。这是霍格沃兹课程源的常见笔误，读到这些词按正确拼写理解即可。

【我的理解】
> （"看内容、看性能、做 mock、构造请求、过滤"这五件事分别对应哪个标签页？如果同事问你"怎么 mock 一个没开发好的接口"，你告诉他用哪个标签页？）

---

## 三、命令行与状态栏

### 知识点 5：命令行 QuickExec 与状态栏

【课程原话/定义】
命令行（QuickExec）：Web 会话列表下方的输入框，提供常见操作快捷方式（Alt+Q 定位光标）。

常用快捷命令：
- `?searchtext`：高亮包含 searchtext 的会话
- `>size` / `<size`：高亮响应大于/小于 size 字节的会话
- `=状态` / `=方法`：高亮指定状态码/方法的会话
- `@host`：高亮请求主机包含 host 的会话
- `bpafter sometext`：按字符串创建响应断点；`bps status`：按状态码创建响应断点；`bpv/bpm method`：按方法创建请求断点；`bpu sometext`：按字符串创建请求断点
- `g` / `go`：恢复所有断点会话
- `cls` / `clear`：清理会话列表；`dump`：会话备份到 zip
- `urlreplace str1 str2`：替换 URL 字符串
- `start` / `stop`：开启/停止抓包；`quit`：关闭 Fiddler
- `select someText`：按响应 Content-Type 过滤

状态栏：Capturing（抓包开关）、All Processes（抓取进程范围）、Breakpoint（断点开关，点击切换：请求断点→响应断点→关闭）、Session Counter（会话数）、Status Information（URL 等）。

【为什么？】
为什么要学命令行 QuickExec？因为它是 Fiddler 的"快捷键层"——鼠标点菜单要好几步，命令行一条命令搞定（尤其断点：`bpu 关键词` 一条命令就设好请求断点）。状态栏的 **Breakpoint 按钮**则是"全局断点"的开关：点一下=请求断点、再点=响应断点、再点=关闭，配合工具栏的 Go 按钮放行。这两个（命令行断点 + 状态栏断点）是 Fiddler 改包的核心操作入口。

【必须掌握】
- QuickExec 定位：Alt+Q；核心命令：`?`查找 / `>`大小过滤 / `=`状态过滤 / `@`主机
- 断点命令：bpafter/bps（响应断点）、bpu/bpv/bpm（请求断点）、`g` 放行
- 状态栏 Breakpoint 按钮：点击切换 请求断点→响应断点→关闭
- `start`/`stop` 控制抓包开关
- 断点放行：工具栏 Go 按钮 / `g` 命令

【企业场景】
你在公司想对"包含 keyword=xxx 的请求"设断点改参数，不用去菜单翻，直接 QuickExec 输入 `bpu keyword` 回车，之后匹配的请求就会停在断点，改完点 Go 放行。这比 Charles 的菜单操作快得多，是 Fiddler 的实战效率优势。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 设了断点不点 Go | 请求一直停在断点，客户端收不到响应 |
| 状态栏 Breakpoint 按钮点几次分不清 | 空白=无断点，点1次=请求断点，点2次=响应断点，点3次=关闭 |
| bpafter/bpu 记混 | bpafter=响应断点(after response)，bpu=请求断点(before request/URI) |

【我的理解】
> （状态栏的 Breakpoint 按钮点 1 次、2 次、3 次分别是什么状态？"请求断点"和"响应断点"各在哪个时机拦截？）

---

## 四、常用实战功能

### 知识点 6：抓 HTTPS 包、手机 App 抓包、序列化请求、上传文件

【课程原话/定义】
1. **抓 HTTPS 包**：默认 Fiddler 不支持抓 https。`Tools → Options → HTTPS`，勾选 `Capture HTTPS CONNECTs` 和 `Decrypt HTTPS traffic`，首次会弹提示安装证书，点 Yes → 是 → 是完成证书安装。
2. **手机 App 抓包**：手机和电脑同一局域网 → 查电脑 IP（悬停工具栏 Online / ipconfig）→ `Tools → Options → Connections` 勾选 `Allow remote computers to connect`（默认端口 8888）→ 手机设代理（电脑 IP:8888）→ 手机浏览器访问 `电脑IP:8888` 下载 FiddlerRoot certificate 并安装。
3. **序列化请求**：Composer 的 Parsed 选项卡里，URL 序号部分用 `#` 代替（如 `png-#.png`），Execute 后输入起止序号，自动发送一串请求。
4. **上传文件请求**：Composer Parsed 右上角 Upload File 选择文件，PUT 选一个、POST 选多个，请求体 `@INCLUDE` 替换为文件内容。

【为什么？】
这四项是 Fiddler 的"高频实战操作"：
- **抓 HTTPS**：和 Charles 一样要"装证书 + 开 Decrypt"，缺一不可（对应 Ch12 的知识）
- **手机抓包**：和 Charles 一样的"同局域网 + 设代理 + 装证书"三件套（对应 Ch12 知识点 3）
- **序列化请求**：批量请求"只有序号不同"的资源（如图片 png-001~png-007），比手动发快得多
- **上传文件**：测文件上传接口时，用 Composer 构造 multipart 请求

【必须掌握】
- 抓 HTTPS：Tools→Options→HTTPS，勾 Capture HTTPS CONNECTs + Decrypt HTTPS traffic + 装证书
- 手机抓包：同局域网 + Allow remote computers to connect + 手机代理 IP:8888 + 装 FiddlerRoot 证书
- 序列化请求：Composer Parsed 里 URL 用 `#` 代替序号
- 上传文件：Composer Parsed → Upload File（PUT 单文件 / POST 多文件）
- 注意：部分 App 做了防抓包处理，抓不到是正常的

【企业场景】
你在公司测一个图片批量加载的接口（png-001~png-007），用 Composer 的 `#` 序列化一次发完 7 个请求；测上传头像接口，用 Composer 的 Upload File 构造 multipart 请求。手机 App 抓包时，先确认手机电脑同 WIFI、Fiddler 开了 Allow remote、手机装好证书，三步缺一就抓不到。

【面试考察】
面试官："Fiddler 怎么抓手机 App 的 https 包？"

参考回答框架：
1. 手机与电脑连同一局域网
2. Fiddler 里 Tools→Options→Connections 勾选 Allow remote computers to connect
3. 手机设置代理：电脑 IP + 端口 8888
4. 手机浏览器访问 电脑IP:8888 下载并安装 FiddlerRoot 证书
5. 打开 App，即可在 Fiddler 看到 https 明文

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 只勾 Decrypt HTTPS 不装证书 | 两件套缺一，https 抓不到明文 |
| 手机抓包忘了 Allow remote | Fiddler 拒绝远程连接，手机连不上代理 |
| 序列化请求用 Raw 选项卡 | Raw 里 `#` 被当纯文本，序列化只在 Parsed 生效 |
| 抓不到某些 App 的包 | 部分 App 做了防抓包（证书校验/双向校验），属正常 |

【扩展知识】
Fiddler 与 Charles 手机抓包流程本质一致（同网 + 代理 + 装证书），区别只在入口：Fiddler 在 Tools→Options（Connections/HTTPS），Charles 在 Proxy 菜单（Proxy Setting / SSL Proxying）。学会一个工具的三件套，另一个只是换个菜单位置。详见 [[Ch12-抓包工具证书配置]]。

【我的理解】
> （手机 App 抓包要"同局域网 + 设代理 + 装证书"三件事，哪一件漏了会导致什么现象？和 Charles 的抓包流程对比，本质区别在哪？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Fiddler 简介 | 仅 Windows 的 HTTP 调试代理，中间人原理 | ★★★☆☆ |
| 界面六区域 | 菜单栏/工具栏/会话面板/标签页/命令行/状态栏 | ★★☆☆☆ |
| 核心标签页 | Inspectors/Statistics/AutoResponder/Composer/Filters | ★★★★☆ |
| 命令行 QuickExec | 断点/过滤/查找等快捷命令 | ★★★☆☆ |
| 抓 HTTPS + 手机抓包 | Decrypt + 装证书 + 代理三件套 | ★★★★☆ |
| 序列化/上传请求 | Composer `#` 序列化 + Upload File | ★★☆☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch11-抓包工具Charles]]
- [[Ch12-抓包工具证书配置]]
- [[Ch13-App抓包实战练习]]
