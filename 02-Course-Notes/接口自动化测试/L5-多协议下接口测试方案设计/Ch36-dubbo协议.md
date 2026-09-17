---
tags: [课程笔记, 接口自动化]
course: "接口自动化测试"
chapter: "Ch36-dubbo协议"
created: 2026-09-17
status: in_progress
---

# Ch36 - dubbo 协议的接口测试

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/requests_v2/L4

---

## 一、Dubbo 协议与测试方法

### 知识点 1：telnet 调试 + 泛化调用测试

【课程原话/定义】
Dubbo 是高性能 RPC 框架，支持多种协议（dubbo、rest、http、hessian、redis、thrift、gRPC 等）。测试 Dubbo 接口的常用方法：

1. **telnet 调试**（临时调试，不适合写用例）：
```bash
telnet localhost 20880
ls                    # 显示服务列表
invoke XxxService.xxxMethod(1234, "abcd", {"prop": "value"})  # 调用方法
```
注意：telnet 仅作临时调试，最新版本有 bug。

2. **泛化调用**（无接口 API/模型类时，用 Map 表示 POJO，通用测试框架常用）：
```java
ReferenceConfig<GenericService> reference = new ReferenceConfig<>();
reference.setInterface("com.xxx.XxxService");
reference.setGeneric(true);
GenericService genericService = reference.get();
Object result = genericService.$invoke("sayHello",
    new String[]{"java.lang.String"}, new Object[]{"world"});
```

3. **跨语言调用**（Python 测 Dubbo）：利用 dubbo 的多协议支持，加 hessian 协议，用 python-hessian 调用。

【为什么？】
为什么要专门学 Dubbo 测试？因为 Dubbo 是 Java 微服务架构最主流的 RPC 框架，而 RPC 接口和 HTTP 接口完全不同——没有 URL、没有 HTTP 方法，而是"服务名 + 方法名 + 参数"。测试 Dubbo 接口的三条路径各有适用场景：telnet 最快（临时调试）、泛化调用最通用（没有接口代码也能测，适合做通用测试框架）、跨语言调用解决"Python 测试 Java 服务"的问题。理解这三条路径，就理解了"RPC 接口怎么测"这个进阶问题。

【必须掌握】
- Dubbo = Java 微服务 RPC 框架
- telnet：临时调试（ls/invoke），不适合写用例
- 泛化调用：GenericService + $invoke，无接口代码也能测
- 跨语言：加 hessian 协议，Python 用 python-hessian 调用
- Dubbo3 主推 triple 协议（基于 gRPC）

【企业场景】
你在公司测 Dubbo 服务，没有接口的 Java 代码（只有服务名和方法名）。用泛化调用：配置 ReferenceConfig + setGeneric(true)，用 $invoke("方法名", 参数类型, 参数值) 直接调，不用引入接口 jar 包。这是"无代码测 RPC"的标准做法，也适合搭通用 RPC 测试框架。

【面试考察】
面试官：「Dubbo 接口怎么测试？什么是泛化调用？」

参考回答框架：
1. Dubbo 是 RPC 框架，接口是"服务名+方法名+参数"
2. 三种方法：telnet 调试、泛化调用、跨语言调用
3. 泛化调用：GenericService + $invoke，无接口代码也能测
4. telnet 仅临时调试，泛化调用适合写用例

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 用 telnet 写测试用例 | telnet 只做临时调试，有 bug 且不适合自动化 |
| Dubbo 接口当 HTTP 测 | RPC 没有 URL，是服务名+方法名+参数 |
| 泛化调用忘 setGeneric(true) | 必须 setGeneric(true) 声明为泛化接口 |

【我的理解】
> （为什么"泛化调用"能"没有接口代码也能测"？它用 Map 和 $invoke 替代了"编译期类型"，这解决了什么问题？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Dubbo 测试 | telnet/泛化调用/跨语言 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch37-thrift协议]]
- [[Ch38-pb协议]]
