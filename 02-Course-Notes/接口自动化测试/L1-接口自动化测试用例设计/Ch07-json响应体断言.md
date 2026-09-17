---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch07-json响应体断言"
created: 2026-09-17
status: in_progress
---

# Ch07 - json 响应体断言

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L1

---

## 一、JSON 响应体断言入门

### 知识点 1：简单响应体断言

【课程原话/定义】
JSON 响应断言是针对 API 响应数据进行验证的方法，用于确认 API 是否按预期返回正确数据。响应体格式通常为 JSON/XML/HTML。

简单响应断言：直接取字段比对。
```python
import requests, pprint
def res_json():
    r = requests.get("https://httpbin.ceshiren.com/get")
    pprint.pprint(r.json())
    assert r.status_code == 200
    assert r.json()["url"] == "https://httpbin.ceshiren.com/get"   # 断言顶层字段
    assert r.json()["headers"]["Host"] == "httpbin.ceshiren.com"   # 断言嵌套字段
res_json()
```

【为什么？】
为什么要专门学"响应体断言"？因为 Ch06 只断了状态码（200），但状态码对不代表数据对。响应体断言就是去验证"返回的具体数据对不对"——url 字段对不对、嵌套的 Host 对不对。这是接口测试真正"验数据"的部分。当响应简单时直接取字段即可，但当响应层级深、嵌套复杂时（见知识点 2），就要用 JSONPath。

【必须掌握】
- 响应体断言 = 验证返回数据是否符合预期
- 简单断言：r.json()["字段"] 直接取值比对
- 嵌套断言：r.json()["外层"]["内层"] 逐层取值
- 断言格式：assert r.json()["xxx"] == 预期值

【企业场景】
你在公司测一个查询接口，返回 JSON 里有用户 id、姓名、地址。你断言 `r.json()["name"] == "张三"` 确认返回的是张三的数据。这就是"响应体断言"——确认接口不仅通了（200），而且返回了正确的数据。

【面试考察】
面试官："接口测试里，除了状态码，还要断言什么？"

参考回答框架：
1. 状态码断言（200/400 等）只说明请求通了
2. 还要做响应体断言：验证返回的具体字段和值对不对
3. 简单响应直接取字段：r.json()["字段"]
4. 复杂嵌套响应用 JSONPath（见下）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 只断状态码不断内容 | 数据对不对才是接口测试的核心 |
| 取嵌套字段路径写错 | 逐层取：r.json()["a"]["b"]，别跳层 |
| 忘了先 r.json() 解析 | 要先 r.json() 转成对象，再取字段 |

【我的理解】
> （`assert r.json()["headers"]["Host"]` 里，为什么要一层层 `["headers"]["Host"]` 取？能不能直接 `r.json()["Host"]`？为什么？）

---

## 二、JSONPath 表达式

### 知识点 2：多层嵌套数据提取的利器

【课程原话/定义】
当 JSON 层级多、嵌套复杂时，普通提取很麻烦（如取 `extattr` 下的 title 要写一长串 `res["extattr"]["external_profile"]["external_attr"][1]["web"]["title"]`）。JSONPath 是定位和提取 JSON 数据的查询语言，用类似 XPath 的路径表达式提取数据，更灵活、支持定制化。

JSONPath 表达式（15 个）：

| 表达式 | 含义 |
|--------|------|
| `$` | JSON 对象的根节点 |
| `.property` | 某个对象的属性 |
| `[n]` | 数组下标为 n 的元素 |
| `[index1,index2,...]` | 数组多个下标的元素 |
| `..property` | 递归查找所有该属性，返回 list |
| `*` | 通配符，匹配所有属性名 |
| `[start:end]` | 数组 start 到 end（不含 end） |
| `[:n]` | 数组最开始的 n 个元素 |
| `[-n:]` | 数组最后的 n 个元素 |
| `[?(@.expression)]` | 过滤器，expression 是过滤条件 |

例如提取嵌套 title：普通方式要写长路径，JSONPath 用 `$..title` 一条搞定。

【为什么？】
为什么 JSONPath 能成为接口测试的"必修技能"？因为真实接口的响应往往不是平铺的，而是多层嵌套（用户信息里套部门、套扩展属性、套数组）。用手写 `res["a"]["b"][1]["c"]` 这种路径，又长又易错，数组下标一变动就崩。JSONPath 用 `$..title` 这种声明式表达式，把"我要所有 title 字段"说清楚，让框架去找——更简洁、更健壮。这是从"手动取值"到"声明式提取"的跃迁。

【必须掌握】
- JSONPath = 定位/提取 JSON 的查询语言（类似 XPath for JSON）
- 核心表达式：`$` 根、`.prop` 属性、`..prop` 递归、`[n]` 下标、`[?()]` 过滤
- `..property` 是最常用的"递归查找所有该字段"
- 嵌套越深，JSONPath 相对手写路径的优势越明显

【企业场景】
你在公司测一个"获取员工详情"接口，响应有 5 层嵌套，要断言里面某个 title 字段。手写 `res["extattr"]["external_profile"]["external_attr"][1]["web"]["title"]` 又长又脆，改用 `$..title` 直接拿到所有 title。响应结构再复杂、数组再多，JSONPath 都能优雅地定位。

【面试考察】
面试官："JSONPath 是什么？`$`、`..`、`[?()]` 分别表示什么？"

参考回答框架：
1. JSONPath 是定位和提取 JSON 数据的查询语言
2. `$` 表示根节点，`.prop` 取属性
3. `..prop` 递归查找所有该属性（最常用）
4. `[n]` 取数组下标，`[?(@.price<10)]` 是过滤器（按条件筛选）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| `$..title` 和 `$.title` 混淆 | `..` 递归查找所有，`.` 只取直接子属性 |
| 数组下标从 1 开始 | 数组下标从 0 开始 |
| 过滤器语法写错 | `[?(@.字段 条件)]`，@ 表示当前元素 |

【我的理解】
> （`$..title` 和 `$.store.book[0].title` 都能拿到 title，它们定位的范围有什么不同？什么场景该用哪个？）

---

## 三、JSONPath 断言应用

### 知识点 3：Python jsonpath 与 Java body/extract 断言

【课程原话/定义】
Python 用第三方库 jsonpath（`pip install jsonpath`）做 JSONPath 断言：

```python
import jsonpath
# 验证包含四位作者
author_list = jsonpath.jsonpath(response, '$.store.book[*].author')
assert author_list == ['Nigel Rees', 'Evelyn Waugh', 'Herman Melville', 'J. R. R. Tolkien']
# 验证所有价格
price_list = jsonpath.jsonpath(response, '$..price')
# 过滤器：价格小于10的书
cheap = jsonpath.jsonpath(response, '$..book[?(@.price<10)]')
```

Java（REST-assured）两种断言方式：
1. 直接断言：`then().body("origin", equalTo("..."))`，结合 hamcrest
2. 提取后断言：`then().extract().path("json.username")`，再 assertEquals

```java
// 直接断言（hamcrest）
.body("headers.Host", equalTo("httpbin.hogwarts.ceshiren.com"))
.body("json.code", hasItem(1))   // 数组包含
// 提取后断言
String username = response.path("json.username");
assertEquals("hogwarts", username);
```

【为什么？】
为什么 Python 和 Java 的 JSONPath 断言方式不一样？因为语言生态不同：Python 用独立的 jsonpath 库（返回 list 再自己 assert），Java 的 REST-assured 把断言内嵌进了链式调用（body() 结合 hamcrest 的 equalTo/hasItem）。但底层思想一致——都是用"路径表达式"定位字段、再和预期对比。理解这点，你就能在两种语言间自由切换。

【必须掌握】
- Python：pip install jsonpath，jsonpath.jsonpath(obj, '表达式') 返回 list
- Python 断言：assert 返回的 list == 预期
- Java 直接断言：then().body("路径", equalTo(值))，hamcrest 的 hasItem 判包含
- Java 提取断言：then().extract().path("路径")
- 过滤器：`$..book[?(@.price<10)]`

【企业场景】
你在公司做接口回归，用 JSONPath 写断言：`assert jsonpath.jsonpath(resp, '$..price') == [8.95, 12.99, ...]` 一次校验所有价格；用过滤器 `$..book[?(@.price<10)]` 校验"价格低于 10 的书有几本"。JSONPath 让复杂响应体的断言从"手写几十行取值"变成"一行表达式"。

【面试考察】
面试官："接口测试里怎么对复杂的嵌套 JSON 响应做断言？"

参考回答框架：
1. 用 JSONPath 表达式定位字段
2. Python：jsonpath 库，jsonpath.jsonpath(obj, '$..字段')
3. Java：then().body("路径", equalTo(值)) 或 extract().path()
4. 过滤器 `[?(@.条件)]` 做条件筛选，`..` 做递归查找

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| jsonpath 返回单个值误当标量 | jsonpath.jsonpath() 返回 list，要 [0] 或直接比 list |
| Java body() 路径用 `$` 开头 | REST-assured 的 body() 路径不用 `$`，直接写字段路径 |
| 过滤条件比较符写错 | `<10` 不是 `lt 10`，JSONPath 用 `<` `<=` `==` 等 |

【扩展知识】
JSONPath 的 `[?(@.price<10)]` 过滤器是它最强的能力——相当于"JSON 版的 SQL WHERE"。除了比较（<、>、==），还支持逻辑组合。它是处理"动态数组里筛选满足条件的元素"这类断言的关键，很多测试框架（如 REST-assured、HttpRunner）都内置了 JSONPath 支持。

【我的理解】
> （`$..book[?(@.price<10)]` 这条表达式，`..`、`[?()]`、`@` 分别起了什么作用？如果不用过滤器，要写几行 Python 才能达到同样效果？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 响应体断言 | r.json()["字段"] 简单取值断言 | ★★★★☆ |
| JSONPath 表达式 | $ / . / .. / [n] / [?()] 过滤 | ★★★★★ |
| JSONPath 应用 | Python jsonpath 库 / Java body+hamcrest | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch06-接口响应断言]]
- [[Ch08-宠物商店接口自动化测试实战]]
