---
tags: [课程笔记, 接口自动化]
course: "接口自动化测试"
chapter: "Ch37-thrift协议"
created: 2026-09-17
status: in_progress
---

# Ch37 - thrift 协议的接口测试

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/requests_v2/L4

---

## 一、Thrift 跨语言服务框架

### 知识点 1：IDL 定义 + 编译 + 序列化

【课程原话/定义】
Apache Thrift 是跨语言服务框架（C++/Java/Python 等），用 IDL（接口定义语言）定义数据类型和服务接口，编译生成各语言代码，实现跨语言 RPC 通信。

技术架构：transport（传输）+ protocol（协议）+ server/client + processor。

使用流程：定义消息 Message → 编译生成各语言代码 → 构建 Runtime → 序列化/反序列化/网络传输。

IDL 定义示例：
```thrift
service Calculator {
    void ping(),
    i32 add(1:i32 num1, 2:i32 num2),
    i32 calculate(1:i32 logid, 2:Work w) throws (1:InvalidOperation ouch),
}
struct Work {
    1: i32 num1 = 0,
    2: i32 num2,
    3: Operation op,
}
```

编译：thrift -r --gen py -o python tutorial.thrift

Python 测试代码：
```python
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
transport = TSocket.TSocket('localhost', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = Calculator.Client(protocol)
transport.open()
assert 2 == client.add(1, 1)
```

【为什么？】
为什么要理解 Thrift？因为它是和 Protobuf（pb）并列的两大"跨语言序列化 + RPC"框架，都遵循同一条链路："用 IDL 定义 → 编译生成各语言代码 → 序列化传输"。理解 Thrift（或 pb），就理解了"接口自动化里非 HTTP 协议怎么测"——先看 IDL 定义了解接口结构，编译生成客户端代码，再用客户端调用 + 断言。这类协议测试的核心是"IDL 是接口契约，编译生成的客户端是测试入口"。

【必须掌握】
- Thrift = 跨语言 RPC 框架（IDL 定义 + 编译生成代码）
- 技术架构：transport + protocol + server/client + processor
- 流程：定义 IDL → 编译（thrift --gen）→ 客户端调用
- Python 测试：TSocket 连接 + Client 调用 + 断言
- 与 pb 类似：pb 属 Google，thrift 属 Apache（更开放）

【企业场景】
你在公司测 Thrift 服务（跨语言微服务），先看 .thrift 的 IDL 定义（了解有哪些服务和方法），编译生成 Python 客户端，用客户端调方法 + 断言结果。IDL 文件就是"接口文档"，编译生成的客户端就是"测试入口"。

【面试考察】
面试官：「Thrift 协议怎么测试？」

参考回答框架：
1. Thrift 用 IDL 定义接口，编译生成各语言代码
2. 流程：定义 IDL → 编译 → 客户端调用
3. Python 用 thrift 库：TSocket 连接 + Client 调用
4. 和 pb 类似，都是跨语言序列化 RPC 框架

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 直接手写序列化 | 要先用 IDL 定义，编译生成代码 |
| 忘 transport.open() | 连接要先 open，用完 close |
| 混淆 thrift 和 pb | 都跨语言序列化，thrift 是 Apache，pb 是 Google |

【我的理解】
> （Thrift 和 pb 都遵循"IDL 定义 → 编译生成代码"的链路，为什么"编译生成客户端代码"是这类协议测试的关键一步？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Thrift 协议 | IDL 定义 + 编译 + 客户端调用 | ★★☆☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch38-pb协议]]
- [[Ch36-dubbo协议]]
