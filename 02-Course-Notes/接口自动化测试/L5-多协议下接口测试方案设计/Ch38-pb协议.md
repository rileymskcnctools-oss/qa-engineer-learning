---
tags: [课程笔记, 接口自动化]
course: "接口自动化测试"
chapter: "Ch38-pb协议"
created: 2026-09-17
status: in_progress
---

# Ch38 - pb 协议（Protocol Buffers）

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/requests_v2/L4

---

## 一、Protocol Buffers 序列化

### 知识点 1：IDL 定义 + protoc 编译 + 序列化

【课程原话/定义】
Protocol Buffers（protobuf）是 Google 的跨语言、跨平台序列化机制——类似 XML 但更小、更快、更简单。定义一次数据结构，用生成的代码读写各种数据流。

应用：Dubbo（服务治理）、gRPC（IDL + 消息格式）。

定义示例（.proto 文件）：
```protobuf
message Person {
    optional string name = 1;
    optional int32 id = 2;
    optional string email = 3;
}
```

使用流程：定义 Message → protoc 编译生成各语言代码 → 构建 Runtime → 序列化/反序列化。

编译：protoc --python_out=$DST_DIR demo.proto

Python 测试：
```python
import demo_pb2
def test_pb():
    person = demo_pb2.Person()
    person.id = 1234
    person.name = "John Doe"
    raw = person.SerializeToString()      # 序列化
    person2 = demo_pb2.Person()
    person2.ParseFromString(raw)          # 反序列化
    assert person == person2
```

【为什么？】
为什么要理解 pb？因为它是 gRPC 和 Dubbo3 的基础序列化格式，也是"比 JSON 更高效"的二进制序列化方案。它的核心价值：**紧凑（二进制，比 XML/JSON 小）+ 快速（解析快）+ 跨语言（protoc 生成各语言代码）**。对接口测试的意义：pb 接口的请求/响应是二进制，不能像 JSON 直接读，要用 protoc 编译 .proto 生成代码来序列化/反序列化。理解"IDL 定义 → 编译 → 序列化"这条链路，才能测 pb/gRPC 接口。

【必须掌握】
- pb = Google 跨语言二进制序列化（比 XML/JSON 更小更快）
- 应用：gRPC、Dubbo
- 定义：.proto 文件（message + 字段类型 + optional/required/repeated）
- 编译：protoc --python_out / --java_out
- 序列化：SerializeToString，反序列化：ParseFromString

【企业场景】
你在公司测 gRPC 接口，接口数据是 pb 二进制。你拿到 .proto 定义文件，用 protoc 编译生成 Python 代码（demo_pb2），用它构造请求对象、SerializeToString 序列化发送、ParseFromString 反序列化响应、断言。IDL 文件是接口契约，编译代码是测试工具。

【面试考察】
面试官：「pb（protobuf）是什么？怎么测 pb 接口？」

参考回答框架：
1. pb 是跨语言二进制序列化，比 JSON/XML 更小更快
2. 用 .proto 定义，protoc 编译生成代码
3. 序列化 SerializeToString / 反序列化 ParseFromString
4. 应用：gRPC、Dubbo

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 用 JSON 直接读 pb 数据 | pb 是二进制，要编译 .proto 生成代码处理 |
| 忘装 protobuf 库 | pip install protobuf |
| protoc 编译命令写错 | protoc --python_out=$DIR demo.proto |

【我的理解】
> （pb 是"二进制"序列化，和 JSON 的"文本"序列化相比，为什么"更小更快"？二进制和文本在传输时的本质区别是什么？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| pb 协议 | IDL 定义 + protoc 编译 + 序列化 | ★★☆☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch37-thrift协议]]
- [[Ch36-dubbo协议]]
