---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch25-WireMock与mock工程化"
created: 2026-09-15
status: draft
---

# Ch25 - WireMock 与 mock 工程化

## 课程来源
- 学习日期：

---

## 一、WireMock 简介

### 知识点 1：为什么要学 Mock + WireMock 简介

【课程原话/定义】
为什么要学 Mock：**提高测试深度、提高测试效率、降低成本**。例如测试股票软件：模拟当天股票全部上涨、全部下跌、部分涨幅 10%——这些真实环境难以构造的场景，用 Mock 轻松实现。

WireMock：一款灵活构建 mock API 的工具（Java）。可创建稳定的开发环境、隔离不稳定的第三方、模拟还不存在的 API。

【为什么？**
为什么 Mock 能"提高测试深度"？因为真实环境有诸多限制：股票不会"全部上涨"、第三方不会"随时挂"、数据库不会有"特定脏数据"。Mock 让你**任意构造这些极端场景**，测出真实环境测不到的边界。WireMock 是 Java 生态的 mock 工具，和 mitmproxy（Python）形成对照——理解"mock 工具有多种语言实现、原理相通"，你就掌握了工程化 mock 的全貌。

【必须掌握】
- Mock 价值：提高测试深度、效率、降低成本
- WireMock：Java 的 mock API 工具，`java -jar wiremock-standalone.jar` 启动
- 可模拟真实环境难构造的场景（股票全涨/全跌）
- 与 mitmproxy 对照：Python vs Java，原理都是"匹配规则 + 模拟响应"

【企业场景】
你在公司测一个"股票"相关功能，要验证"当天股票全部上涨"时页面的表现——真实股市不可能全涨。用 WireMock（或 mitmproxy）把行情接口 mock 成"全部上涨"，就能稳定、重复地测这个场景。这就是 Mock"提高测试深度"的含义：测出真实环境测不到的场景。

【面试考察】
面试官："Mock 能提高测试深度，具体指什么？"

参考回答框架：
1. 真实环境受限于数据（股票不会全涨、第三方不会随时挂）
2. Mock 可任意构造极端/边界场景
3. 测出真实环境测不到的 case（全涨/全跌/特定异常）
4. 同时提高效率（不依赖外部）、降低成本（不调用收费第三方）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Mock 只能"代替第三方" | Mock 还能构造极端场景，提高测试深度 |
| WireMock 和 mitmproxy 是"两个世界" | 都是 mock 工具，原理相同，只是语言不同（Java vs Python） |
| 以为 Mock 降低测试质量 | 恰恰相反，Mock 能测真实环境测不到的场景 |

【我的理解】
> （"股票全部上涨"这个场景，真实环境为什么测不了？Mock 为什么能测？这体现了 Mock 的什么价值？）

---

## 二、WireMock 的 stub 与 mock on stub

### 知识点 2：WireMock stub（mock on stub）

【课程原话/定义】
WireMock 启动：`java -jar wiremock-jre8-standalone-2.33.2.jar`。

JSON 方式定义 stub：
```json
{
  "request": { "method": "GET", "url": "/wiremock" },
  "response": { "status": 200, "body": "Easy!" }
}
```

Java 方式（mock on stub）：
```java
stubFor(get(urlEqualTo("/some/thing"))
    .willReturn(aResponse()
        .withHeader("Content-Type", "text/plain")
        .withBody("Hello world!")));
```

【为什么？**
为什么 WireMock 的 stub 是"mock on stub"？因为 WireMock 的默认模式就是"桩"——你定义"请求匹配规则 + 返回内容"，WireMock 对匹配的请求直接返回预设内容，不访问真实服务。这正好对应 Ch19 讲的 Stub（返回预设答案）。`stubFor(get(urlEqualTo(...)).willReturn(aResponse()...))` 是它的核心 API：匹配 URL → 返回响应。理解这个，你就理解了"mock on stub"（在桩上做 mock）的落地方式。

【必须掌握】
- WireMock 启动：`java -jar wiremock-standalone.jar`
- stub 定义：JSON（request 匹配 + response 返回）或 Java（stubFor + willReturn）
- mock on stub = 直接返回预设数据，不访问真实服务
- 核心 API：`stubFor(get(urlEqualTo(x)).willReturn(aResponse()...))`

【企业场景】
你在公司（Java 技术栈）做一个"还没开发完的接口"的 stub，用 WireMock 定义一条规则：匹配 `GET /some/thing` 就返回 "Hello world!"。前端/其他团队就能对着这个 stub 开发测试，不被后端阻塞。这就是 WireMock 的典型用法——"接口还没好，先给个桩"。

【面试考察】
面试官："WireMock 怎么定义 mock 接口？"

参考回答框架：
1. 启动 `java -jar wiremock-standalone.jar`
2. 定义 stub：request（匹配规则）+ response（返回内容）
3. Java 方式：stubFor(get(urlEqualTo(...)).willReturn(aResponse()...))
4. 匹配的请求直接返回预设内容（mock on stub）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| stubFor 匹配规则写太宽 | urlEqualTo 是精确匹配，太宽会误匹配 |
| JSON stub 和 Java stub 混淆 | JSON 是静态配置，Java 是代码（stubFor） |
| WireMock 只能 Java | 核心是 Java，但也支持 JSON 配置（无需写代码） |

【我的理解】
> （WireMock 的 `stubFor(get(urlEqualTo(x)).willReturn(...))` 对应 Ch19 的哪种替身？为什么说它是"mock on stub"？）

---

## 三、mock on proxy 与 transformer

### 知识点 3：mock on proxy 与 transformer

【课程原话/定义】
**mock on proxy**（WireMock）：
```java
wm.stubFor(get(urlPathEqualTo("/templated"))
    .willReturn(aResponse()
        .proxiedFrom("$!request.headers.X-WM-Proxy-Url")
        .withTransformers("response-template")));
```

**transformer**（响应模板）：
```java
public class ExampleTransformer extends ResponseDefinitionTransformer {
    public ResponseDefinition transform(...) {
        String content = responseDefinition.getTextBody().replace("霍格沃兹", "mock");
        return new ResponseDefinitionBuilder()
            .withHeader("MyHeader", "Transformed")
            .withStatus(200)
            .withBody(content)
            .build();
    }
}
```

【为什么？**
为什么需要 "mock on proxy" 和 "transformer"？因为纯 stub（mock on stub）返回的是**写死的静态数据**，而实际测试常常需要"**基于真实响应做修改**"——比如真实接口返回了股票列表，我只想把其中某只股票的名字改掉。这时就要"代理转发真实请求 + 对响应做变换（transformer）"。`proxiedFrom` 就是"转发到真实服务"，`withTransformers` 就是"对响应做自定义修改"。这就是 mock on proxy（在代理上做 mock）+ transformer（响应变换）的意义。

【必须掌握】
- mock on stub：返回写死数据（静态）
- mock on proxy：转发真实请求 + 修改响应（动态）
- proxiedFrom：转发到真实服务（或指定 URL）
- transformer：对响应做自定义变换（如替换字符串）
- 场景：基于真实响应做局部修改（改某个字段）

【企业场景】
你在公司测"股票列表"接口，真实服务返回了 100 只股票，你只想把"第 3 只的名字改掉"来测展示逻辑。用 WireMock 的 mock on proxy：`proxiedFrom` 转发真实请求，`transformer` 把响应里"霍格沃兹"替换成"mock"。这样 99% 的数据是真实的，只有你要改的那个字段被 mock 掉——比整个响应写死灵活得多。

【面试考察】
面试官："mock on stub 和 mock on proxy 有什么区别？"

参考回答框架：
1. mock on stub：返回写死的预设数据，静态
2. mock on proxy：转发真实请求 + 修改响应，动态
3. mock on proxy 适合"基于真实数据做局部修改"
4. transformer 是响应变换器，做自定义字符串替换

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| mock on proxy 不访问真实服务 | proxy 恰恰是"转发到真实服务"再改 |
| transformer 改的是请求 | transformer 改的是响应（ResponseDefinition） |
| 想改一个字段却整个响应写死 | 用 mock on proxy + transformer，只改目标字段 |

【扩展知识】
mitmproxy 的 adb mock 案例（Python 侧，改 TCP 消息）：
```python
from mitmproxy import ctx, tcp
def tcp_message(flow: tcp.TCPFlow):
    message = flow.messages[-1]
    old_content = message.content
    message.content = old_content.replace(
        b":0;localabstract:webview_devtools_remote_",
        b":   0;localabstract:xweb_devtools_remote_")
    ctx.log.info("[tcp_message] ...")
```
这是 mitmproxy 在 TCP 层做 mock 的例子，和 WireMock 的 HTTP 层 mock 形成对照——不同工具、不同协议层，原理都是"匹配 + 修改"。

【我的理解】
> （"想改真实响应里的一个字段"和"整个返回写死数据"，分别是 mock on proxy 和 mock on stub 的哪种场景？为什么 proxy 模式更灵活？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Mock 价值 | 提高深度/效率/降成本 | ★★★☆☆ |
| WireMock stub | stubFor + willReturn（mock on stub） | ★★★★☆ |
| mock on proxy | proxiedFrom + transformer | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch24-mitmproxy编程与定制化]]
- [[Ch19-mock技术体系与分类]]
- [[Ch18-mock的价值与意义]]
