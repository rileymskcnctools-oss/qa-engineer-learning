---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch19-mock技术体系与分类"
created: 2026-09-15
status: draft
---

# Ch19 - mock 技术体系与分类

## 课程来源
- 学习日期：

---

## 一、Mock 的分类

### 知识点 1：Mock 的分类（Stub / Proxy / Fake / Spy / Mock）

【课程原话/定义】
Mock 分类：
- **Stub**：用简单实现替代真实服务，无法在测试中动态变更，比较死板
- **Proxy**：使用代理协议转发请求并返回真实内容，可抓发、监听、修改
- **Fake**：用假实现代替真实现，功能与真的基本一致，比 stub 更强大
- **Spy**：监听调用过程，不具备转发能力，主要监听调用过程
- **Mock**：可以根据测试场景动态修改被调用方的返回
- **Mock on stub**：直接转发并修改数据
- **Mock on proxy**：利用代理转发并修改数据

【为什么？**
为什么要区分这些概念？因为"替身"有不同层次的能力：Stub 是"死桩"（返回写死的数据，不能动态变）；Fake 是"活实现"（真跑一段逻辑，如内存数据库）；Spy 是"监听"（记录调用但不改）；Mock 是"可编程的期望"（按测试场景动态返回）。理解这个梯度，你就能在面试里说清"Stub vs Mock vs Fake 的区别"，也能在实际中选对替身类型（要写死数据用 Stub，要模拟真实逻辑用 Fake，要动态控制用 Mock）。

【必须掌握】
- Stub：返回预设数据，死板，不能动态变
- Fake：有真实实现（如内存数据库），比 stub 强大
- Spy：监听/记录调用过程，不转发
- Mock：按测试场景动态修改返回
- Mock on stub / on proxy：在桩或代理之上做数据修改

【企业场景】
你在公司做接口 Mock：如果只是想让登录接口"固定返回成功"，用 Stub 就够了；如果想模拟一个"能增删改查的内存数据库"，用 Fake；如果想"记录这个接口被调用了多少次、参数是什么"，用 Spy；如果想"根据测试场景动态返回不同结果"，用 Mock（如 Charles 的 Rewrite 就是 mock on proxy）。分清这几种，写测试代码时就不会选错。

【面试考察】
面试官："Stub 和 Mock 有什么区别？Fake 呢？"

参考回答框架：
1. Stub：返回预设数据的桩，不能动态变更，最死板
2. Mock：可按测试场景动态修改返回，能验证期望的调用
3. Fake：有真实工作实现（如内存数据库），功能接近真实
4. 递进关系：Stub（死桩）< Fake（活实现）< Mock（动态可控）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Stub 和 Mock 是一回事 | Stub 返回写死数据，Mock 可动态修改/验证调用 |
| Fake 是"假的，很弱" | Fake 反而有真实实现（内存数据库），比 Stub 强 |
| Spy 能转发数据 | Spy 只监听/记录调用，不具备转发能力 |

【我的理解】
> （用一个具体例子区分 Stub 和 Mock：如果测"登录"接口，用 Stub 和用 Mock 分别会怎么做？）

---

## 二、Test Double 测试替身

### 知识点 2：Test Double 测试替身体系

【课程原话/定义】
Test Double（测试替身）：
- **Dummy 占位对象**：被传递但从未实际使用，仅用于填充参数列表
- **Fake 假对象**：有工作实现但采取捷径，不适合生产（内存数据库）
- **Stubs 桩对象**：为测试提供预设答案，通常不响应测试外内容
- **Spies 间谍对象**：根据调用方式记录信息（如记录发送了多少消息）
- **Mocks 模拟对象**：预编程对象，期望形成它们期望接收的调用规范

【为什么？**
Test Double 是"测试替身"的统称（就像"车"是统称，下面有轿车/SUV/卡车）。面试高频问"Test Double 有哪几种"，本质是考察你是否理解"替身"的精细分类。五种替身的递进：Dummy（占位不用）→ Stub（写死答案）→ Fake（活实现）→ Spy（记录调用）→ Mock（验证期望调用）。理解这个体系，是写单元测试（pytest/unittest mock）的理论基础。

【必须掌握】
- Test Double = 测试替身的统称
- 五种：Dummy（占位）、Fake（假实现）、Stub（预设答案）、Spy（记录）、Mock（预编程期望）
- Dummy 只填参数、Fake 有真实逻辑、Stub 写死、Spy 记录、Mock 验证
- 这是单元测试 mock 的理论基础

【企业场景】
你在公司写单元测试（pytest + unittest.mock），会用到这些替身：测一个函数，传一个 Dummy 对象填参数；依赖数据库时用一个 Fake（内存 dict 模拟）；想让某方法返回固定值用 Stub；想断言"这个方法被调用了一次"用 Spy/Mock。理解 Test Double 体系，你就知道什么时候用 `unittest.mock.Mock`、什么时候用 `patch`、什么时候自己写个 Fake。

【面试考察】
面试官："Test Double 有哪几种？分别是什么？"

参考回答框架：
1. Dummy：占位对象，只填参数，不实际使用
2. Stub：返回预设答案的桩
3. Fake：有真实实现但不适合生产（如内存数据库）
4. Spy：记录调用信息的间谍对象
5. Mock：预编程期望、可验证调用的模拟对象

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Test Double 和 Mock 是同一个东西 | Mock 只是 Test Double 的一种 |
| Dummy 有实际逻辑 | Dummy 只是占位，从不实际使用 |
| Stub 和 Fake 没区别 | Stub 写死返回，Fake 有真实实现逻辑 |

【我的理解】
> （五种替身里，"最弱"的是哪个、"最接近真实"的是哪个？为什么说 Mock 是"预编程期望"而不是"写死答案"？）

---

## 三、常用 Mock 工具

### 知识点 3：常用 Mock 工具与 mitmproxy

【课程原话/定义】
常用 Mock 工具：Charles（测试工程师常用）、BurpSuite（黑客常用）、Fiddler（仅 Windows）、Nginx（服务器反向代理与修改）、Mitmproxy（代理工具，可 Python 编程）、Wiremock（基于 Java，可 Java 编程）。

**mitmproxy**：提供交互式、支持 SSL/TLS 的拦截代理（HTTP/1、HTTP/2、WebSockets）。有强大的插件机制（Addons：dns、tcp、cert、http/https、websocket），可通过 Python 第三方库 `mitmproxy` 做深度定制。

【为什么？**
为什么要认识这些工具？因为它们代表了"Mock 的三种实现层次"：
- **图形化工具**（Charles/Fiddler）：上手快，适合手工 Mock（Rewrite/MapLocal）
- **命令行/脚本工具**（mitmproxy/Wiremock）：可编程、可进自动化流水线，适合测试开发
- **服务器侧**（Nginx）：反向代理层做流量修改

其中 mitmproxy 是"测试开发工程师必备"——因为它能用 Python 写脚本，把 Mock 逻辑变成可维护、可版本管理的代码，而不是在 GUI 里点按钮。这就是"手工 Mock"和"工程化 Mock"的分水岭。

【必须掌握】
- Charles/Fiddler：图形化，适合手工 Mock
- mitmproxy：Python 可编程，测试开发必备，支持插件（Addons）
- Wiremock：Java 可编程
- BurpSuite：安全测试常用
- Nginx：反向代理层修改
- mitmproxy 的 mock on proxy：反向代理 + 内容替换

【企业场景】
你在公司要做"工程化的接口 Mock"（能进 CI、能版本管理、能复用），不会用 Charles 点按钮，而是用 mitmproxy 写 Python 脚本：定义一个 addon，在请求/响应里做正则替换，`mitmdump -s script.py` 启动。这样 Mock 逻辑就是代码，可以提交到 git、随 CI 跑。这是测试开发岗和普通测试岗在 Mock 能力上的核心差距。

【面试考察】
面试官："mitmproxy 和 Charles 做 Mock 有什么区别？"

参考回答框架：
1. Charles 是图形化工具，手动配置，适合临时/手工 Mock
2. mitmproxy 是命令行 + Python 可编程，可写脚本定制
3. mitmproxy 有插件机制（Addons），能处理 dns/tcp/http/websocket 等
4. 工程化 Mock（进 CI、版本管理）用 mitmproxy；快速验证用 Charles

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 只会用 Charles 点按钮 Mock | 工程化 Mock 要用 mitmproxy/Wiremock 写代码 |
| mitmproxy 没有 GUI 就不好用 | 它的优势正是命令行 + Python 编程，适合自动化 |
| Nginx 不能做 Mock | Nginx 反向代理可做流量修改/转发，也是一种 Mock 手段 |

【扩展知识】
mitmproxy 简单案例（mock on proxy）：
```bash
python3 -m http.server          # 先起一个本地服务（端口 8000）
mitmdump -p 8001 -m reverse:127.0.0.1:8000 --flow-detail 4 \
  -B '/~bs .*Directory.*/Directory/ceshiren.com mock'
```
说明：mitmdump 监听 8001 端口，反向代理 8000 端口，当内容出现 "Directory" 时替换成 "ceshiren.com mock"。

【我的理解】
> （为什么说 mitmproxy 是"测试开发工程师必备"？它相比 Charles 的 GUI 点按钮，多了什么工程化能力？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Mock 分类 | Stub/Proxy/Fake/Spy/Mock + on stub/on proxy | ★★★★☆ |
| Test Double | Dummy/Fake/Stub/Spy/Mock 五替身 | ★★★★☆ |
| Mock 工具 | Charles/mitmproxy/Wiremock 分工 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch18-mock的价值与意义]]
- [[Ch20-Charles mock实战]]
