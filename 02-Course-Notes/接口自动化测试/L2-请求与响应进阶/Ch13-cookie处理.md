---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch13-cookie处理"
created: 2026-09-17
status: in_progress
---

# Ch13 - cookie 处理

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L2

---

## 一、Cookie 原理与传递方式

### 知识点 1：Cookie 是什么、怎么在请求里传递

【课程原话/定义】
Cookie 是服务器发送到用户浏览器并保存到本地的一小块数据，下次向同一服务器请求时被携带发送，用于告知服务端两个请求是否来自同一浏览器（如保持登录状态）。

原理：服务器响应报文的 Set-Cookie 首部通知客户端保存 Cookie；客户端再请求时，在请求报文中加入 Cookie 值；服务器据此识别客户端和之前的状态。

传递 Cookie 的两种方式：
1. 通过请求头传递：`headers={"Cookie": "working=1"}`
2. 通过 cookies 关键字参数：`cookies=dict(cookies_are='working2')`

```python
# 方式一：header
headers = {"Cookie": "working=1"}
r = requests.get(url, headers=headers)
# 方式二：cookies 参数
cookies = dict(cookies_are='working2')
r = requests.get(url, cookies=cookies)
```

【为什么？】
为什么要学 Cookie 的传递？因为接口测试里，很多接口要求"已登录"才能访问，而登录态就是靠 Cookie 维持的。不带 Cookie 请求就返回未登录。理解 Cookie 的两种传递方式（塞 header vs 用 cookies 参数），以及它的原理（Set-Cookie 下发 → 请求回传），是处理"需要登录态"接口的基础。cookies 参数更规范（自动处理编码/格式），header 方式更直接（手动拼字符串）。

【必须掌握】
- Cookie = 服务器下发、客户端保存并回传的小块数据，用于维持登录态
- 原理：Set-Cookie 响应头下发 → 请求头 Cookie 回传
- 两种传递：headers={"Cookie":...} / cookies 参数（dict）
- 应用场景：判断登录、记录用户信息、记录搜索关键词

【企业场景】
你在公司测一个"需要登录"的接口，先调登录接口拿到 Cookie（或 session），再把这个 Cookie 带到业务接口的请求里，接口才返回正常数据。不带 Cookie 会返回 401 未登录。这是接口测试里最常见的"会话维持"场景。

【面试考察】
面试官："Cookie 是什么？Requests 里怎么传递 Cookie？"

参考回答框架：
1. Cookie 是服务器下发、客户端保存并回传的数据，用于维持登录态/会话
2. 原理：Set-Cookie 下发 → 请求头 Cookie 回传
3. 传递方式：headers={"Cookie":"..."} 或 cookies=dict
4. cookies 参数更规范，header 方式更直接

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Cookie 和 token 混为一谈 | Cookie 是会话状态（浏览器自动带），token 是显式凭证（放 Authorization） |
| 用 cookies 参数还手动拼 "Cookie: ..." | 二选一，别重复传 |
| 忘记带 Cookie 就调需要登录的接口 | 会返回 401/未登录，先登录拿 Cookie |

【扩展知识】
Cookie 和 Session 的关系：Cookie 通常只存一个 session_id（会话标识），真正的用户数据存在服务器的 Session 里。请求带上 session_id（通过 Cookie），服务器查到对应 Session，就知道用户是谁、登录状态如何。这是"有状态"的会话机制，和"无状态"的 token 鉴权形成对比（详见 Ch01 知识点 4、Ch04 知识点 1 的相关讨论）。

【我的理解】
> （Cookie 是"服务器让客户端保存并回传"的，而 token 是"客户端主动带在请求头"的——为什么说 Cookie 是"有状态"、token 是"无状态"？这对服务器设计有什么影响？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Cookie 原理 | Set-Cookie 下发 + 请求回传，维持登录态 | ★★★★☆ |
| Cookie 传递 | headers 方式 / cookies 参数 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch04-接口请求头]]
- [[Ch14-超时处理]]
