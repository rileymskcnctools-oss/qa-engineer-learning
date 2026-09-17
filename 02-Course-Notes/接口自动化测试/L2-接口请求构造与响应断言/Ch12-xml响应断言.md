---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch12-xml响应断言"
created: 2026-09-17
status: in_progress
---

# Ch12 - xml 响应断言

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L2

---

## 一、XML 解析与响应断言

### 知识点 1：三种解析方式 + requests_xml + XPath 断言

【课程原话/定义】
XML 断言验证 XML 文档结构和内容是否符合预期。当响应是 XML 类型时，需要先转换才能断言。

XML 三种解析方式：
- **DOM**：文档对象模型，W3C 标准，把 XML 解析成内存中的树，操作树
- **SAX**：事件驱动，逐行扫描，边扫边解析，适合大型文档
- **ElementTree**：比 DOM 性能好，与 SAX 性能接近，API 方便

Python 用 requests_xml 库（`pip install requests_xml`）解析，支持 XPath：
```python
from requests_xml import XMLSession
session = XMLSession()
r = session.get("https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss")
print(r.text)          # 全部内容
print(r.xml.links)     # 所有链接
print(r.xml.raw_xml)   # 字节形式内容
print(r.xml.text)      # 标签中的内容

# XPath 断言
item = r.xml.xpath("//link")   # 取所有 link 标签
result = [i.text for i in item]
assert all('https://www.nasa.gov/' in link for link in result)
```

【为什么？】
为什么要学 XML 的响应断言？因为不是所有接口都返回 JSON——有些老系统、RSS 订阅、配置文件接口返回 XML。而 XML 不像 JSON 能直接 `r.json()`，必须用解析器（DOM/SAX/ElementTree）或 requests_xml 库处理。理解"三种解析方式的区别"（DOM 全载入内存 vs SAX 流式）能帮你根据文档大小选对工具；XPath 则和 JSONPath 是"同构"的——都是"路径表达式定位数据"，学会一个，另一个也通了。

【必须掌握】
- XML 三种解析：DOM（树/内存）、SAX（流式/大文档）、ElementTree（性能好）
- Python：requests_xml 库，XMLSession + r.xml.xpath()
- XPath 表达式定位 XML 字段（如 //link）
- 断言：提取 → 列表 → assert

【企业场景】
你在公司测一个返回 XML 的接口（如 RSS 订阅、老系统配置接口），用 requests_xml 的 XPath 提取字段做断言。虽然现在 JSON 是主流，但遇到 XML 接口时，这套"XMLSession + XPath"是标准解法，不会手足无措。

【面试考察】
面试官："XML 有哪些解析方式？接口返回 XML 怎么断言？"

参考回答框架：
1. DOM（树模型，全载内存）、SAX（流式，适合大文档）、ElementTree（性能好）
2. Python 用 requests_xml 库解析
3. 用 XPath 表达式提取字段
4. 提取到列表后 assert 断言

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 把 XML 响应当 JSON 调 r.json() | XML 要用 XML 解析器（requests_xml/ElementTree） |
| 大文档用 DOM | 大文档用 SAX（流式），DOM 会占满内存 |
| XPath 和 JSONPath 混淆 | XPath 用于 XML，JSONPath 用于 JSON |

【扩展知识】
XPath 之于 XML，相当于 JSONPath 之于 JSON——都是"路径表达式定位数据"。XPath 用 `//link` 表示"所有 link 节点"，JSONPath 用 `$..link` 表示"递归查找所有 link"。两者思想一致：用声明式路径替代手写逐层取值。理解了这种"路径查询语言"的共性，遇到任何结构化数据都能快速上手。

【我的理解】
> （DOM 和 SAX 解析 XML 的区别是什么？为什么说 SAX 适合"大型文档"？从"内存占用"的角度解释。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| XML 解析 | DOM/SAX/ElementTree 三种方式 | ★★★☆☆ |
| requests_xml | XMLSession + XPath 断言 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch11-接口请求体-xml]]
- [[Ch07-json响应体断言]]
