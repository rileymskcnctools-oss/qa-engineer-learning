---
tags: [课程笔记, 接口自动化]
course: "接口自动化测试"
chapter: "Ch34-gor流量回放"
created: 2026-09-17
status: in_progress
---

# Ch34 - gor 流量回放

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/requests_v2/L5

---

## 一、GoReplay 流量回放

### 知识点 1：录制线上流量，回放测试/压测

【课程原话/定义】
GoReplay（gor）是开源工具，捕获实时 HTTP 流量并重放到测试环境，用真实数据持续测试系统。用途：流量跟踪（shadowing）、负载测试、监控分析。

四种模式：
```bash
# 监听模式（捕获并打印）
sudo ./gor --input-raw :8000 --output-stdout

# 转发模式（实时转发到测试环境）
sudo ./gor --input-raw :8000 --output-http="http://localhost:8001"

# 重放模式（从文件回放）
gor --input-file requests.gor --output-http="http://localhost:8001"

# 性能/加速模式（放大流量压测）
gor --input-file "requests.gor|200%" --output-http "staging.com"
```

请求过滤/重写：
```bash
gor --input-raw :8080 --output-http staging.com --http-allow-url /api
gor --input-raw :8080 --output-http staging.com --http-allow-method GET
gor --input-raw :8080 --output-http staging.com --http-rewrite-url /v1/user/([^/]+)/ping:/v2/user/$1/ping
```

经典案例：tcpdump 监听、线上流量同步（预发布测试）、流量放大（压测）。

【为什么？】
为什么要"流量回放"？因为真实生产流量是最有价值的测试数据——它覆盖了真实用户的行为、真实的参数组合、真实的边界情况，这是手写测试数据无法完全模拟的。gor 的价值是"把生产流量变成测试数据"：录制线上流量 → 回放到测试环境（预发布验证）→ 放大倍数做压测。这样新版本上线前，能用"真实流量"验证，比手写用例更贴近真实。核心是"用真实数据测试"的思想。

【必须掌握】
- GoReplay：捕获/回放 HTTP 流量
- 四模式：监听、转发、重放、性能（放大）
- 过滤：--http-allow-url/method、--http-disallow-url
- 重写：--http-rewrite-url、--http-set-param、--http-header
- 用途：流量同步（预发布）、回放（回归）、放大（压测）

【企业场景】
你在公司新版本上线前，用 gor 录制生产流量，回放到预发布环境，对比新旧版本的响应（结合 diffy），验证改动不影响现有功能。压测时把录制流量放大 10 倍回放，模拟高并发。这套"录制-回放-放大"是流量回放的经典用法。

【面试考察】
面试官：「怎么用真实流量做测试？gor 是干什么的？」

参考回答框架：
1. gor（GoReplay）捕获线上 HTTP 流量
2. 回放到测试环境，用真实数据测试
3. 三种用法：流量同步（预发布）、回放（回归）、放大（压测）
4. 支持过滤、重写请求

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 回放含写操作的流量 | 要过滤掉写操作，避免污染测试环境 |
| 放大倍数不加 | 压测要 --input-file "file|1000%" 放大 |
| 忽略请求过滤 | 用 --http-allow-url 只回放目标接口 |

【我的理解】
> （为什么"生产流量"比"手写测试数据"更有价值？gor 的"录制-回放"解决了手写数据的什么短板？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 流量回放 | gor 录制/回放/放大 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch33-diffy接口diff测试工具]]
- [[Ch35-har生成用例]]
