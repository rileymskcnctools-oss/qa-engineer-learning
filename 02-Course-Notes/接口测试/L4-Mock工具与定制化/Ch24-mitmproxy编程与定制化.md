---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch24-mitmproxy编程与定制化"
created: 2026-09-15
status: draft
---

# Ch24 - mitmproxy 编程与定制化

## 课程来源
- 学习日期：

---

## 一、mitmproxy 简介与安装

### 知识点 1：mitmproxy 是什么 + 安装

【课程原话/定义】
mitmproxy 是一款开源、免费的代理工具，支持 Mac、Windows、Linux。相比其他代理工具，它能通过 Python 和插件机制实现**对 mitmproxy 的完全控制**。强大的可拓展性和可定制性，让测试工程师能以 mitmproxy 为基础二次开发，打造更适合自己业务的 mock 工具。官网：https://mitmproxy.org/

安装（推荐 pipx）：
```bash
pip install pipx
pipx install mitmproxy
mitmdump --version   # 验证安装
```

【为什么？】
为什么测试开发工程师要学 mitmproxy？因为它是"**可编程的 Charles**"——Charles/Fiddler 靠 GUI 点按钮做 mock，做完就丢了，无法复用、无法进 CI、无法版本管理。mitmproxy 用 Python 脚本控制整个代理，mock 逻辑就是代码，能提交 git、随流水线跑、随意定制。这就是 Ch19 说的"手工 Mock"和"工程化 Mock"的分水岭，也是测试开发岗的核心能力之一。

【必须掌握】
- mitmproxy 是开源跨平台的 Python 可编程代理工具
- 安装：`pipx install mitmproxy`（推荐），或 pip 安装
- 验证：`mitmdump --version`
- 相比 Charles：可编程、可进 CI、可版本管理、可二次开发

【企业场景】
你在公司要做一个"团队共用的接口 mock 平台"，用 Charles 点按钮行不通（不能复用、不能共享）。用 mitmproxy 写 Python 脚本，把 mock 规则存成代码，团队共享、git 管理、CI 集成。这就是 mitmproxy 在企业里的定位——"用代码做 mock"的基础设施。

【面试考察】
面试官："mitmproxy 和 Charles 有什么区别？为什么要用 mitmproxy？"

参考回答框架：
1. Charles 是图形化工具，手动点按钮配置
2. mitmproxy 是命令行 + Python 可编程，能写脚本完全控制
3. mitmproxy 的 mock 是代码，可复用、版本管理、进 CI
4. 工程化 mock 用 mitmproxy，快速调试用 Charles

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| mitmproxy 是"另一个 Charles" | mitmproxy 的核心是"可编程"，不是图形界面 |
| 只会 mitmproxy 的 GUI（mitmweb） | mitmdump 脚本才是工程化 Mock 的核心 |
| 认为 mock 只能用 GUI 工具 | mitmproxy 用代码做 mock，可进 CI、可复用 |

【我的理解】
> （"可编程"为什么是 mitmproxy 相对 Charles 的核心优势？如果一个 mock 规则要"团队共享 + 版本管理 + 进 CI"，为什么必须用代码而不是 GUI？）

---

## 二、三大核心工具

### 知识点 2：mitmproxy / mitmweb / mitmdump

【课程原话/定义】
mitmproxy 有三大核心工具：
- **mitmproxy**：交互式命令行工具（`mitmproxy` 启动），**不支持 Windows**
- **mitmweb**：图形界面（`mitmweb` 启动），类似 Chrome DevTools 的 Network
- **mitmdump**：编写强大插件和脚本的核心工具（`mitmdump` 启动），脚本 API 可完全控制 mitmproxy

【为什么？**
为什么三个工具里 mitmdump 最重要？因为它们定位不同：mitmproxy 是"人在终端里交互操作"（Linux/Mac 用）、mitmweb 是"人在浏览器里看"（类似 GUI）、mitmdump 是"脚本在跑"（无交互，纯自动化）。测试开发要的是**自动化、可脚本化**，所以 mitmdump 是核心——它用 `-s` 参数加载 Python 脚本，让 mock 逻辑完全由代码控制，适合进 CI、无人值守运行。

【必须掌握】
- mitmproxy：交互式命令行，不支持 Windows
- mitmweb：浏览器图形界面，类似 DevTools Network
- mitmdump：脚本核心，`-s` 加载 Python 脚本，适合自动化
- 测试开发重点学 mitmdump（可编程、可进 CI）

【企业场景】
你在公司写了一个 mock 脚本，用 `mitmdump -s mock_script.py` 启动，它就在后台自动跑（无人值守），拦截请求、按脚本规则改响应。这和"手动开 Charles 点按钮"完全不同——脚本可以挂在 CI 流水线里，每次构建自动起一个 mock 环境。

【面试考察】
面试官："mitmproxy 的三个工具分别是什么？测试开发主要用哪个？"

参考回答框架：
1. mitmproxy：交互式命令行（不支持 Windows）
2. mitmweb：图形界面，类似 DevTools
3. mitmdump：脚本核心，-s 加载 Python 脚本
4. 测试开发主要用 mitmdump（可编程、可自动化、可进 CI）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 在 Windows 上用 mitmproxy 命令 | mitmproxy 不支持 Windows，用 mitmweb 或 mitmdump |
| 只学 mitmweb 的 GUI | mitmdump 脚本才是工程化核心 |
| mitmdump 只是"命令行版 mitmproxy" | mitmdump 是脚本引擎，-s 加载 Python 脚本做自动化 |

【我的理解】
> （mitmproxy / mitmweb / mitmdump 三者定位有什么不同？为什么"测试开发"重点学 mitmdump 而不是 mitmweb？）

---

## 三、mitmdump 脚本实战

### 知识点 3：mitmdump 脚本 + 插件 + 事件

【课程原话/定义】
mitmdump 通过 `-s` 参数执行 Python 脚本。示例（每次请求打印一句话）：
```python
# mitm_demo.py
from mitmproxy import http
def request(flow: http.HTTPFlow):
    print("this is a demo")
```
执行：`mitmdump -s ./mitm_demo.py`

**插件（addons）**：通过全局变量 `addons` 把一个类实例与 mitmproxy 关联，每个插件都是实例对象（如 `Counter()`），方法名（如 `request`）是事件。

**事件**：每个函数/方法代表一个事件，在请求响应的不同过程自动调用。如 `request(flow)`（请求后调用）、`response(flow)`（响应后调用），通过修改 flow 对象即可改变流量。

【为什么？**
为什么 mitmdump 的脚本模型是"事件 + addons"？因为它本质是一个**事件驱动框架**：mitmdump 在请求生命周期的各个节点（收到请求、返回响应、建立连接……）触发"事件"，你的脚本里定义对应名字的方法，就会被自动调用。`addons = [Counter()]` 就是"注册我的插件对象"，`request`/`response` 方法就是"我关心的事件"。理解这个模型，你就能写出"改请求、改响应、记录日志"等任意定制逻辑。

【必须掌握】
- `mitmdump -s script.py` 执行脚本
- 插件：`addons = [实例]` 注册对象
- 事件：`request(flow)`、`response(flow)` 等方法在对应时机自动调用
- 修改 `flow.request` / `flow.response` 即可改流量
- flow 对象代表一次请求响应的完整数据

【企业场景】
你在公司写 mock 脚本：定义一个类，`request` 方法里改请求头（模拟不同客户端），`response` 方法里改响应体（mock 返回数据），`addons = [MyMock()]` 注册，`mitmdump -s mock.py` 启动。之后所有经过代理的流量都按你的脚本规则被修改。这就是"用代码做 mock"的完整形态。

【面试考察】
面试官："mitmdump 的脚本是怎么工作的？"

参考回答框架：
1. `mitmdump -s script.py` 加载脚本
2. 脚本用 `addons` 全局变量注册插件对象
3. 定义 `request`/`response` 等方法作为事件处理器
4. 请求生命周期中自动调用对应方法，修改 flow 对象即可改流量

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 忘了注册 addons | 定义了类但没加到 addons，方法不会被调用 |
| request/response 方法名写错 | 方法名是 mitmproxy 约定的事件名，写错不触发 |
| 直接改 flow.request 而不是 flow.request.headers | 要改请求头得定位到具体字段 |

【我的理解】
> （"事件驱动"是什么意思？`request(flow)` 和 `response(flow)` 分别在什么时机被自动调用？为什么 `addons` 注册是必须的？）

---

### 知识点 4：mitmproxy 实现 map local

【课程原话/定义】
mitmproxy 用脚本实现 map local：在 `request` 事件里，判断 URL 匹配时，把 `flow.response` 赋值为本地文件内容。

```python
import json
from mitmproxy import ctx, http

class Counter:
    def request(self, flow):
        if "https://httpbin.testing-studio.com/get" in flow.request.pretty_url:
            with open("./res.json", encoding="utf-8") as f:
                flow.response = http.HTTPResponse.make(
                    200,
                    f.read(),
                    {"Content-Type": "text/html"}
                )

addons = [Counter()]
```
执行：`mitmdump -s ./mitm_map_local.py`

【为什么？**
为什么 mitmproxy 实现 map local 是"在 request 事件里直接赋值 flow.response"？因为这就是中间人代理的"截胡"逻辑：请求到达时（request 事件），我不转发给服务器，而是直接把 flow.response 设成本地数据——相当于"拦截并返回伪造响应"，请求根本不出代理。这和你用 Charles 的 MapLocal 效果一样，但它是代码实现的，可复用、可进 CI。关键 API 是 `http.HTTPResponse.make(状态码, 内容, headers)`。

【必须掌握】
- map local 脚本逻辑：request 事件里匹配 URL → 赋值 flow.response
- `http.HTTPResponse.make(200, content, headers)` 构造响应
- 效果等同 Charles 的 MapLocal，但是代码实现
- 请求被拦截，不转发到真实服务器

【企业场景】
你在公司用 mitmproxy 写 map local 脚本，把某个第三方接口的响应"截胡"成本地预设数据，这样测试环境不依赖第三方、返回可控。脚本提交 git，同事复用、CI 集成——这是 Charles 点按钮做不到的工程化能力。

【面试考察】
面试官："用 mitmproxy 怎么实现 map local？"

参考回答框架：
1. 在 request 事件里判断 flow.request.pretty_url 是否匹配
2. 匹配时用 http.HTTPResponse.make 构造响应赋值给 flow.response
3. 请求被拦截，不转发真实服务器
4. 效果等同 Charles MapLocal，但是代码实现

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 在 response 事件里做 map local | map local 应在 request 事件拦截（响应还没发生） |
| HTTPResponse.make 参数写错 | make(状态码, 内容, headers)，内容是 str |
| 忘了用 pretty_url 匹配 | pretty_url 是完整 URL，用于精确匹配 |

【我的理解】
> （为什么 map local 要写在 `request` 事件而不是 `response` 事件？这体现了 map local 的什么本质？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| mitmproxy 简介 | 开源跨平台可编程代理，pipx 安装 | ★★★☆☆ |
| 三大工具 | mitmproxy/mitmweb/mitmdump 分工 | ★★★☆☆ |
| mitmdump 脚本 | -s 加载脚本 + addons + 事件 | ★★★★☆ |
| map local | request 事件赋值 flow.response | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch19-mock技术体系与分类]]
- [[Ch20-Charles mock实战]]
- [[Ch25-WireMock与mock工程化]]
