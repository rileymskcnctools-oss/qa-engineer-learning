---
tags: [课程笔记, 接口自动化]
course: "接口自动化"
chapter: "Ch05-接口请求体-json"
created: 2026-09-17
status: in_progress
---

# Ch05 - 接口请求体-json

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/L1

---

## 一、JSON 语法规则与 JSON vs Python 字典

### 知识点 1：JSON 的数据类型与语法规则

【课程原话/定义】
JSON（JavaScript Object Notation）是轻量级的文本数据交换格式，独立于语言，用 JavaScript 语法描述数据对象。目前非常多编程语言（PHP/JSP/.NET）都支持 JSON。

JSON 语法规则与数据类型：
- **数字**（整数或浮点）：`{"age": 18, "score": 70.5}`
- **字符串**（只能双引号包裹）：`{"name": "zs", "sex": "女"}`
- **逻辑值**（true/false）：`{"flag": true}`
- **数组**（中括号）：`{"score": [100, 80, 90]}`
- **对象**（大括号）：`{"stu1": {"name": "zs"}}`
- **null**：`{"score": null}`

JSON 与 Python 字典的区别：
- JSON 的键只能是字符串，值可以是字符串/数字/对象/数组/布尔/null
- Python 字典的键可以是数字/字符串/元组，值更灵活（还可元组/列表/字典）
- JSON 是"数据交换格式"（简洁通用），Python 字典是"数据结构"（灵活，用于程序内处理）

【为什么？】
为什么要专门学 JSON 的语法规则？因为接口测试里，请求体、响应体几乎都是 JSON。理解 JSON 的"死规矩"（键必须双引号、字符串必须双引号、用 true/false 而不是 True/False）才能：① 正确构造请求体；② 看懂响应；③ 避免 Python 字典和 JSON 字符串之间转换时的坑。JSON 是"跨语言的中间格式"，Python 字典是"程序里的数据结构"，两者通过 json.dumps/json.loads 互转。

【必须掌握】
- JSON 六种数据类型：数字、字符串（双引号）、布尔（true/false）、数组、对象、null
- JSON 键必须是字符串，且用双引号
- JSON ≠ Python 字典：JSON 是交换格式，dict 是数据结构
- json.dumps() 把 dict 转 JSON 字符串，json.loads() 反向

【企业场景】
你在公司写接口用例，用 Python dict 组织请求数据，但发出去前要 `json.dumps()` 转成 JSON 字符串（或直接交给 requests 的 json 参数自动转）。响应回来是 JSON 字符串，你要 `r.json()` 解析成 dict 才能断言。这个"dict ↔ JSON 字符串"的转换，是每个接口测试脚本里都在发生的事。

【面试考察】
面试官："JSON 和 Python 字典有什么区别？"

参考回答框架：
1. JSON 是跨语言的数据交换格式（文本），Python dict 是 Python 的数据结构
2. JSON 的键只能是字符串（双引号），dict 的键可以是数字/字符串/元组
3. JSON 的布尔是 true/false，Python 是 True/False
4. 通过 json.dumps/json.loads 互转

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| JSON 字符串用单引号 | JSON 字符串必须双引号 |
| JSON 写 True/False | JSON 是 true/false（小写），Python 才是 True/False |
| 直接把 dict 当 JSON 发 | dict 要 json.dumps 或交给 requests 的 json 参数转换 |
| JSON 的 null 写成 None | JSON 是 null，Python 是 None |

【我的理解】
> （为什么 JSON 的键"只能是字符串"，而 Python 字典的键"可以是数字"？从"JSON 是跨语言交换格式"这个定位来想。）

---

## 二、常用请求体类型与 content-type 判断

### 知识点 2：五种请求体类型 + 用 content-type 判断传参

【课程原话/定义】
常用接口请求体类型：

| 类型 | 介绍 | Content-Type |
|------|------|--------------|
| JSON | 轻量级数据交换格式，最常见 | application/json |
| 表单（Form Data） | 键值对提交，如 HTML 表单 | application/x-www-form-urlencoded |
| XML | 标记语言，常用于配置文件 | application/xml / text/xml |
| 文件（File） | 上传图片/视频等文件 | multipart/form-data 或 image/jpeg |
| 纯文本（Text） | 发邮件、发短信等 | text/plain |

判断传参：看请求头的 content-type——
- `application/json` → json 格式 → 用 `json` 参数
- `application/x-www-form-urlencoded` → 表单格式 → 用 `data` 参数

【为什么？】
为什么要"看 content-type 决定用 json 还是 data"？因为服务器是根据 Content-Type 头来判断"请求体是什么格式"的——你传的数据格式必须和 Content-Type 声明一致，否则服务器解析不了。这是接口测试的高频坑：用 data 传 JSON 数据（或反之），Content-Type 对不上，接口就报错。记住"json 格式用 json 参数、表单格式用 data 参数"，能避开一大类请求失败。

【必须掌握】
- 五种请求体：JSON、表单、XML、文件、纯文本
- JSON→application/json，表单→x-www-form-urlencoded
- json 格式用 requests 的 `json=` 参数，表单用 `data=` 参数
- 判断依据是 Content-Type 头

【企业场景】
你在公司调一个接口，文档写"请求体为 JSON 格式"，你就要用 `requests.post(url, json={...})`（它会自动设 Content-Type: application/json）；如果文档写"表单提交"，就用 `data={...}`。搞混了服务器就会报"格式错误"或"参数缺失"，这是接口测试新手最常见的坑之一。

【面试考察】
面试官："requests 里 json 参数和 data 参数有什么区别？怎么选？"

参考回答框架：
1. json= 传 JSON 格式请求体，自动设 Content-Type: application/json
2. data= 传表单格式请求体（Content-Type: x-www-form-urlencoded）
3. 看接口文档/抓包里的 Content-Type 决定用哪个
4. 传错格式，服务器解析不了，请求失败

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| JSON 数据用 data 传 | JSON 用 json 参数（自动设对 Content-Type） |
| 表单数据用 json 传 | 表单用 data 参数 |
| 不看 Content-Type 瞎传 | 先看 Content-Type 再决定 json 还是 data |

【我的理解】
> （如果接口要求 JSON 格式，你却用 `data={...}` 传，会发生什么？从 Content-Type 头和服务器解析的角度解释。）

---

## 三、JSON 请求体构造

### 知识点 3：Python 与 Java 构造 JSON 请求体

【课程原话/定义】
Python 用 json 参数传 JSON 请求体：
```python
import requests
def test_post_json():
    url = "https://httpbin.ceshiren.com/post"
    json = {"post_key": "post_value"}
    r = requests.post(url, json=json)
    print(r)
test_post_json()
```

Java（REST-assured）用 `given().body()` 传请求体，两种方式：
1. JSONObject 对象（put 键值对后 toString）
2. 直接传 JSON 字符串

```java
// JSONObject 方式
JSONObject requestBody = new JSONObject();
requestBody.put("username", "hogwarts");
requestBody.put("password", "test12345");
given().body(requestBody.toString()).when().post(url)...

// 直接字符串方式
String jsonData = "{\"username\":\"hogwarts\",\"password\":\"test12345\"}";
given().body(jsonData).when().post(url)...
```

【为什么？】
为什么 Python 传 JSON 这么简单（`json={...}` 一行），而 Java 要么建 JSONObject、要么手拼字符串？因为 Python 的 dict 天然就是"键值对"，和 JSON 结构一一对应；Java 没有这种内置结构，要么用 JSONObject 类构建、要么直接写 JSON 字符串。理解这个差异，你就明白为什么 Python 在接口测试里更"顺手"——数据结构更贴近 JSON。

【必须掌握】
- Python：requests.post(url, json=dict) 一行传 JSON
- Java：given().body(jsonData) 传 JSON，可用 JSONObject 或字符串
- JSONObject.put() 构建、toString() 转字符串
- 实战可用高德开放平台等免费 API 练习

【企业场景】
你在公司用 Python 测接口，登录接口这样写：`requests.post(login_url, json={"username":"admin","password":"123456"})`，一行搞定；响应里的 token 再提取出来传给后续接口。Python 的 dict 让"构造 JSON 请求体"这件事几乎零成本。

【面试考察】
面试官："怎么构造一个 JSON 格式的 POST 请求体？"

参考回答框架：
1. Python：requests.post(url, json={"key":"value"})
2. json 参数会自动设置 Content-Type: application/json
3. Java：given().body(jsonData)，用 JSONObject 或 JSON 字符串
4. 响应解析：Python 用 r.json()，Java 用 extract().path()

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| json 参数传字符串 | Python 的 json= 应传 dict（自动转 JSON），不是字符串 |
| Java 忘 body 的 toString | JSONObject 要 .toString() 转字符串再 body() |
| 响应当字符串处理 | 用 r.json() 解析成对象再断言 |

【我的理解】
> （Python 传 JSON 用 `json=dict`，Java 传 JSON 用 `body(字符串)`——为什么 Python 能直接传 dict，Java 却要先转成字符串？这和两种语言的数据结构设计有什么关系？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| JSON 语法 | 六种类型、双引号、true/false/null | ★★★★☆ |
| JSON vs dict | 交换格式 vs 数据结构，dumps/loads 互转 | ★★★★☆ |
| 请求体类型 | JSON/表单/XML/文件/文本 + Content-Type | ★★★★★ |
| 构造 JSON | Python json=dict，Java body() | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch04-接口请求头]]
- [[Ch06-接口响应断言]]
