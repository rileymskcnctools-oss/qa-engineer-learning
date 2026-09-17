---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch11-接口请求体-xml"
created: 2026-09-17
status: in_progress
---

# Ch11 - 接口请求体-xml

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L2

---

## 一、XML 请求体

### 知识点 1：text/xml 类型请求体

【课程原话/定义】
接口参数数据可能通过 XML 传递。POST 请求 body 常见四种类型：application/x-www-form-urlencoded、application/json、text/xml、multipart/form-data。

XML 是可扩展标记语言，用标签标识数据结构，用户可自定义标签。XML 数据交换、信息配置时常用。

Python 发送 XML 请求体（设 Content-Type，遇编码错误对 body encode）：
```python
import requests, pprint
xml = """<?xml version="1.0" encoding="UTF-8"?>
<COM>
  <REQ name="北京-hogwarts">
    <USER_ID>bjhogwarts</USER_ID>
    <COMMODITY_ID>123456</COMMODITY_ID>
    <SESSION_ID>abcdefg123</SESSION_ID>
  </REQ>
</COM>"""
headers = {'Content-Type': 'application/xml'}
r = requests.post('https://httpbin.ceshiren.com/post', data=xml.encode('utf-8'), headers=headers)
pprint.pprint(r.json())
```

【为什么？】
为什么 XML 请求体要"设 Content-Type + encode"？因为 requests 默认把 data 当表单处理（设 form-urlencoded），但 XML 需要明确告诉服务器"这是 XML"（Content-Type: application/xml/text-xml），服务器才知道按 XML 解析。而 `xml.encode('utf-8')` 是处理中文等非 ASCII 字符的编码问题——XML 声明了 UTF-8，但直接传字符串可能编码出错，encode 成字节更保险。XML 请求体少见但存在（老系统、金融/政务接口），掌握它能应对这类"非 JSON"接口。

【必须掌握】
- POST body 四种常见类型：form-urlencoded、json、text/xml、multipart
- XML 用标签定义结构，可自定义标签
- 发 XML 请求体：data=xml.encode('utf-8') + Content-Type: application/xml
- XML 数据可放文件里，用 open 读出来再发（便于维护）

【企业场景】
你在公司测一个老系统接口，请求体是 XML 格式（金融/政务系统常见）。你用 `data=xml_str.encode('utf-8')` + `headers={"Content-Type":"application/xml"}` 发送。XML 内容长时，放到 .xml 文件里用 open 读取，比硬编码在代码里好维护。

【面试考察】
面试官："接口请求体除了 JSON，还有哪些格式？XML 请求体怎么发？"

参考回答框架：
1. 常见四种：表单、JSON、XML、multipart（文件）
2. XML 请求体：设 Content-Type: application/xml
3. 用 data=xml.encode('utf-8') 发送（处理编码）
4. XML 内容可放文件，open 读取后发送

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| XML 请求体不设 Content-Type | 服务器按默认解析，XML 会解析失败 |
| 中文不 encode 直接传 | 编码错误，用 .encode('utf-8') |
| XML 当 JSON 发 | XML 和 JSON 是两种格式，Content-Type 不同 |

【我的理解】
> （XML 和 JSON 都是"结构化数据格式"，为什么现在接口大多用 JSON，而 XML 只剩老系统在用？从"可读性"和"数据量"两个角度想。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| XML 请求体 | text/xml + Content-Type + encode | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch05-接口请求体-json]]
- [[Ch10-接口请求体-form表单]]
- [[Ch12-xml响应断言]]
