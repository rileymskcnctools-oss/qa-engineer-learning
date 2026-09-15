---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch22-抓包分析TCP协议"
created: 2026-09-15
status: draft
---

# Ch22 - 抓包分析 TCP 协议

## 课程来源
- 学习日期：

---

## 一、抓包工具分类

### 知识点 1：接口测试工具分类（嗅探 / 代理 / 分析）

【课程原话/定义】
接口测试工具分类：
1. **网络嗅探工具**：Tcpdump、Wireshark
2. **代理工具**：Fiddler、Charles、AnyProxy、BurpSuite、mitmproxy
3. **分析工具**：curl、Postman、Chrome DevTools

【为什么？**
为什么要按"嗅探/代理/分析"分类？因为这三类工具工作在网络的**不同层次**，用途不同：
- **嗅探工具**（Tcpdump/Wireshark）：在网络层/数据链路层抓原始数据包，能看到 TCP/IP 层细节（SYN/ACK、端口、IP），但看不到应用层明文（除非解密）
- **代理工具**（Charles/Fiddler）：在应用层做中间人，看 HTTP/HTTPS 明文，但不能看底层 TCP 握手
- **分析工具**（curl/Postman）：主动发请求 + 看响应，用于构造和验证

理解这三层，你就知道"想看三次握手用哪个（Wireshark）、想看接口明文用哪个（Charles）、想构造请求用哪个（curl/Postman）"。

【必须掌握】
- 嗅探工具：Tcpdump/Wireshark，抓底层网络包（TCP/IP 层）
- 代理工具：Charles/Fiddler/mitmproxy，抓应用层 HTTP/HTTPS 明文
- 分析工具：curl/Postman/Chrome DevTools，构造请求 + 看响应
- 三层分工：底层抓包 / 应用层明文 / 主动构造

【企业场景】
你在公司排查"接口超时"：先看是哪一层——如果是 TCP 握手就失败（连不上），用 Wireshark 抓包看 SYN 有没有回 ACK；如果 HTTP 层返回了错误，用 Charles 看明文；如果要主动验证，用 curl/Postman 发请求。不同工具对应不同排查层次，这是接口测试的基本功。

【面试考察】
面试官："接口测试的工具有哪些分类？各抓什么？"

参考回答框架：
1. 嗅探工具（Tcpdump/Wireshark）：抓底层网络包，看 TCP/IP 细节
2. 代理工具（Charles/Fiddler/mitmproxy）：抓 HTTP/HTTPS 应用层明文
3. 分析工具（curl/Postman）：主动构造请求、查看响应
4. 三者互补：底层协议 / 应用明文 / 主动构造

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 用 Charles 看三次握手 | Charles 是应用层代理，看不到底层 TCP 握手（用 Wireshark） |
| 用 Wireshark 看 HTTPS 明文 | Wireshark 抓的是加密包，要解密才见明文（用 Charles） |
| curl/Postman 是"抓包工具" | 它们是"主动发请求"的分析工具，不是被动抓包 |

【我的理解】
> （想排查"TCP 三次握手有没有完成"，应该用哪类工具？为什么 Charles 做不了这件事？）

---

## 二、Tcpdump 与 Wireshark

### 知识点 2：Tcpdump 与 Wireshark

【课程原话/定义】
**Tcpdump**：把网络中传送的数据包"头"完全截获下来提供分析的工具。支持针对网络层、协议、主机、网络或端口的过滤，并提供 and/or/not 逻辑语句。
示例：`sudo tcpdump port 443 -v -w /tmp/tcp.log`（监听 443 端口，详细输出，写入 log）

常用参数：`port 443`（监听端口）、`-v`（详细）、`-w`（写 log）。

**Wireshark**：网络嗅探工具，除 tcpdump 功能外还有分析工具。但服务器通常无 UI，所以用 tcpdump 抓包生成 log，再导入 Wireshark 在有 UI 的客户端上分析。

【为什么？**
为什么"服务器用 tcpdump、分析用 Wireshark"？因为服务器一般是 Linux 无图形界面，只能跑命令行 tcpdump 抓包存成文件；而 Wireshark 有强大的图形分析能力（着色、过滤、追踪流、协议解析），适合人眼看。所以标准流程是"服务器 tcpdump 抓包 → 导出 log → 本地 Wireshark 分析"。这也是为什么 tcpdump 的 `-w`（写文件）参数特别重要——它是"把服务器上的包搬回本地分析"的关键。

【必须掌握】
- Tcpdump：命令行抓包，支持端口/协议/主机过滤，`-w` 写文件
- Wireshark：图形分析工具，导入 tcpdump 的 log 分析
- 标准流程：服务器 tcpdump 抓包 → 本地 Wireshark 分析
- 服务器无 UI，所以抓包用命令行、分析用图形工具

【企业场景】
你在公司服务器上排查一个接口异常：`sudo tcpdump port 443 -v -w /tmp/tcp.log` 抓几分钟的包，然后把 log 下载到本地，用 Wireshark 打开，过滤、看握手、追踪 TCP 流，定位问题。这就是"服务器抓包 + 本地分析"的标准排查流程。

【面试考察】
面试官："Tcpdump 和 Wireshark 有什么区别？怎么配合用？"

参考回答框架：
1. Tcpdump 是命令行抓包工具，Wireshark 是图形分析工具
2. 服务器无 UI，用 tcpdump 抓包存 log（-w）
3. 把 log 导入 Wireshark 在有 UI 的客户端分析
4. 配合：tcpdump 负责"抓"，Wireshark 负责"看"

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 在服务器上跑 Wireshark | 服务器通常无 UI，应用 tcpdump 抓包 |
| 抓包忘了 -w 存文件 | 不存文件就没法搬到本地分析 |
| tcpdump 和 Wireshark 是同一层次 | tcpdump 抓底层包，Wireshark 抓+分析（带 GUI） |

【我的理解】
> （为什么"服务器抓包、本地分析"要拆成两个工具？如果服务器有图形界面，还需要 tcpdump 吗？）

---

## 三、三次握手与四次挥手（抓包视角）

### 知识点 3：用 Wireshark 看三次握手与四次挥手

【课程原话/定义】
抓取一个 HTTP GET 请求（如 `http://www.baidu.com/s?wd=mp3`），用 tcpdump 截获生成 log，用 Wireshark 打开。log 前几段是**三次握手**：

1. **第一次握手**：客户端发 SYN 包（syn=j）给服务器，进入 SYN_SENT 状态
2. **第二次握手**：服务器确认客户 SYN（ack=j+1），同时发自己的 SYN（seq=k），即 SYN+ACK，进入 SYN_RECV 状态
3. **第三次握手**：客户端发 ACK（ack=k+1），双方进入 ESTABLISHED 状态，连接建立

结束交流时**四次挥手**：
1. 客户端发 FIN，请求关闭
2. 服务器回 ACK（ack=FIN+SEQ）
3. 服务器发 FIN，告诉客户端关闭
4. 客户端回 ACK

【为什么？**
为什么抓包能"看到"三次握手？因为 TCP 是传输层协议，它的握手是真实的数据包（SYN/ACK/FIN），Wireshark 在底层抓到的就是这些包。这让你从"背概念"升级到"亲眼看到"——面试问三次握手时，你能说"我用 Wireshark 抓过，前三个包就是 SYN、SYN+ACK、ACK"。三次握手的本质是"确认双方收发能力正常"（详见 [[Ch01-接口协议基础]] 知识点 2），抓包是验证这个过程的实证手段。

【必须掌握】
- 三次握手：SYN → SYN+ACK → ACK（ESTABLISHED 建立连接）
- 四次挥手：FIN → ACK → FIN → ACK（关闭连接）
- 用 Wireshark 抓包，前三个包就是三次握手
- 握手比挥手少一次，因为挥手是"半关闭"（双方各关一次）

【企业场景】
你在公司排查"连接建立慢"：用 Wireshark 抓包，看三次握手的三个包之间间隔多久——如果 SYN 发出去很久才收到 SYN+ACK，说明是网络延迟或服务器响应慢；如果 SYN 一直没回，可能是防火墙拦截或服务器没监听。抓包让"连接问题"从黑盒变白盒。

【面试考察】
面试官："三次握手和四次挥手分别是哪几个步骤？为什么挥手比握手多一次？"

参考回答框架：
1. 三次握手：SYN → SYN+ACK → ACK，建立连接
2. 四次挥手：FIN → ACK → FIN → ACK，关闭连接
3. 握手三次：双方各发一次 SYN + 确认一次
4. 挥手四次：因为 TCP 是"半关闭"，双方各关一次（FIN 和 ACK 分开）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 三次握手是"三次都发数据" | 握手只传 SYN/ACK 控制包，不传业务数据 |
| 挥手是三次 | 挥手是四次（FIN→ACK→FIN→ACK），比握手多一次 |
| 混淆 SYN_SENT 和 SYN_RECV | 客户端 SYN_SENT（已发 SYN），服务器 SYN_RECV（已收 SYN） |

【扩展知识】
为什么要"三次"而不是"两次"？两次握手无法确认"客户端能收到服务器的数据"——第二次握手后服务器以为连接建立，但客户端可能根本收不到（网络单向问题）。第三次 ACK 就是确认"客户端收到了服务器的 SYN+ACK"，双向收发能力都确认了才能开始传数据。

【我的理解】
> （结合 [[Ch01-接口协议基础]] 知识点 2：为什么三次握手能保证"双方收发能力都正常"？如果只握两次会有什么问题？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 工具分类 | 嗅探/代理/分析三层分工 | ★★★☆☆ |
| Tcpdump/Wireshark | 服务器抓包 + 本地分析 | ★★★☆☆ |
| 三次握手四次挥手 | SYN→SYN+ACK→ACK；FIN→ACK→FIN→ACK | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-接口协议基础]]
- [[Ch21-使用curl发送请求]]
- [[Ch23-RPC与Socket接口测试]]
