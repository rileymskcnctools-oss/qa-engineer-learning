---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch27-socket协议的接口测试"
created: 2026-09-17
status: in_progress
---

# Ch27 - socket 协议的接口测试

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L5

---

## 一、Socket 协议测试

### 知识点 1：Socket 通信与四步测试

【课程原话/定义】
Socket（套接字）是一种通信机制，允许不同计算机之间的进程进行数据交换。直接使用 Socket 的情况较少，但大部分协议（HTTP 等）都基于 Socket 抽象优化，所以了解 Socket 测试有助于理解其他协议。

Socket 测试四步：创建连接（host + 端口）→ 发送消息 → 接收消息 → 关闭连接。

Python 实现（echo 服务 socket.hogwarts.ceshiren.com:30001）：
```python
import socket
def send_socket(self, send_data: str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建
    s.connect(('socket.hogwarts.ceshiren.com', 30001))     # 连接
    s.send(send_data.encode("utf-8"))                      # 发送
    d = s.recv(1024)                                       # 接收
    s.close()                                              # 关闭
    return d.decode("utf-8")

def test_send_socket():
    socket_req = SocketReq()
    assert socket_req.send_socket("Hogwarts 测试开发学社") == "Hogwarts 测试开发学社"
```

【为什么？】
为什么要学 Socket 测试？因为它是所有网络协议（HTTP、Dubbo、WebSocket...）的"底层地基"。虽然日常接口测试很少直接碰 Socket（都是 HTTP），但理解了 Socket 的"连接→发→收→关"四步，你就理解了所有网络通信的本质。而且物联网、定制化通信等场景确实还在用裸 Socket。echo 服务（发什么回什么）是验证 Socket 通信最简单的方式——预期结果就是发送的内容本身。

【必须掌握】
- Socket = 进程间通信机制，是其他协议的地基
- 测试四步：创建连接 → 发送 → 接收 → 关闭
- Python：socket.socket() + connect + send + recv + close
- echo 服务：发什么回什么，断言"返回 == 发送"
- 消息要 encode 成字节发送，接收后 decode

【企业场景】
你在公司测物联网设备接口，设备通过 Socket 和服务器通信。你用 Python 的 socket 库建连接、发指令、收响应、断言。虽然大部分业务接口是 HTTP，但这类"底层/定制化通信"场景，Socket 测试是绕不开的基本功。

【面试考察】
面试官：「Socket 协议怎么测试？和 HTTP 接口测试有什么区别？」

参考回答框架：
1. Socket 测试四步：连接、发送、接收、关闭
2. 消息要编码成字节流传输
3. 区别：HTTP 是请求-响应模型（有 URL/方法/头），Socket 是底层字节流（要自己定协议）
4. HTTP 建立在 Socket 之上，理解了 Socket 就理解了网络通信本质

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 消息不 encode 直接 send | 要 encode("utf-8") 转字节再发 |
| recv 结果不 decode | 收到的字节流要 decode 转字符串 |
| 忘 close 连接 | 连接要关闭，否则资源泄漏 |

【我的理解】
> （Socket 和 HTTP 都是"网络通信"，为什么说 HTTP 建立在 Socket 之上？HTTP 相比裸 Socket 多做了什么封装？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Socket 测试 | 连接/发送/接收/关闭四步 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch28-websocket协议的接口测试]]
- [[Ch02-接口请求方法]]
