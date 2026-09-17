---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch10-接口请求体-form表单"
created: 2026-09-17
status: in_progress
---

# Ch10 - 接口请求体-form 表单

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L2

---

## 一、表单请求体

### 知识点 1：data 参数传表单数据

【课程原话/定义】
Form 请求代表请求体为表单类型，特点是数据量不大、层级不深、用键值对传递，Content-Type 对应 `application/x-www-form-urlencoded`。搜索、登录等场景常用表单。

Python 用 data 参数传表单（字典形式）：
```python
import requests, pprint
def req():
    data = {"school": "hogwarts"}
    r = requests.post("https://httpbin.ceshiren.com/post", data=data)
    pprint.pprint(r.json())   # 表单数据在响应的 form 字段里
req()
```

【为什么？】
为什么登录、搜索这些场景用表单（form）而不是 JSON？因为表单是最"古老"也最通用的提交方式——HTML 表单默认就是 x-www-form-urlencoded，浏览器点登录按钮发出去的就是这种格式。所以很多老系统、传统登录接口都用表单。测试时用 data 参数传 dict，requests 会自动设 Content-Type 为 form-urlencoded，把数据编码成 `key=value&key2=value2` 放进 body。

【必须掌握】
- 表单：Content-Type = application/x-www-form-urlencoded
- 特点：键值对、数据量小、层级浅
- Python 用 data 参数（dict），自动设 Content-Type
- 表单数据在响应的 form 字段里（可用 httpbin 验证）

【企业场景】
你在公司测一个登录接口，文档写"表单提交"，你就用 `requests.post(login_url, data={"username":"admin","password":"123"})`。如果误用 json 参数传，服务器拿到的是 application/json 而非 form-urlencoded，可能登录失败。分清"表单用 data、JSON 用 json"，是请求体格式的基本功（呼应 Ch05）。

【面试考察】
面试官："data 参数和 json 参数有什么区别？表单接口用什么传？"

参考回答框架：
1. data 参数传表单（x-www-form-urlencoded），json 参数传 JSON（application/json）
2. 表单接口（登录/搜索等键值对场景）用 data
3. 判断依据：看接口的 Content-Type
4. data 传 dict，requests 自动编码成 key=value 形式

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 表单接口用 json 传 | 表单用 data，JSON 才用 json 参数 |
| 分不清 data 和 json 的 Content-Type | data→form-urlencoded，json→application/json |
| 表单数据层级深还硬用表单 | 层级深的数据用 JSON，表单只适合扁平键值对 |

【我的理解】
> （表单（form）和 JSON 都是"键值对"，为什么说表单适合"层级浅"的数据、JSON 适合"层级深"的数据？用一个嵌套数据例子说明。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 表单请求体 | data 参数 + x-www-form-urlencoded | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch05-接口请求体-json]]
- [[Ch09-接口请求体-文件]]
- [[Ch11-接口请求体-xml]]
