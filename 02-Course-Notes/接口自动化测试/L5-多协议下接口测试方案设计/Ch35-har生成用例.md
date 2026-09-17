---
tags: [课程笔记, 接口自动化]
course: "接口自动化测试"
chapter: "Ch35-har生成用例"
created: 2026-09-17
status: in_progress
---

# Ch35 - har 生成用例

## 课程来源
- 学习日期：
- 课程源：霍格沃兹教程站 auto_interface/requests_v2/L5

---

## 一、从 har 自动生成测试用例

### 知识点 1：har + Mustache 模板 → 测试脚本

【课程原话/定义】
har（HTTP Archive Format）是记录 HTTP 会话信息的文件格式，多个浏览器都能生成。

har 生成用例的价值：把 har 格式的接口数据转换为测试脚本，提升编写效率、降低出 Bug 概率（如 HttpRunner 的 har2case）。

实现思路：读取 har 数据 → 准备测试用例模板 → 把 har 数据写入模板。

模板技术 Mustache（轻量模板语言）：
```
# 模板
Hello {{ name }}!
# 填充后
Hello AD!
```

Python 实现（chevron）：
```python
import chevron
chevron.render('Hello, {{ mustache }}!', {'mustache': 'World'})
```

生成用例：
```python
import json, pymustache
class GenerateCase:
    def __load_har(self, har_filename):
        with open(har_filename) as f:
            har_data = json.load(f)
        return har_data["log"]["entries"][0]["request"]
    def generate_case_by_har(self, origin_template, testcase_filename, har_filename):
        with open(origin_template) as f:
            template_data = pymustache.render(f.read(), self.__load_har(har_filename))
        with open(f"{testcase_filename}.py", "w") as f:
            f.write(template_data)
```

【为什么？】
为什么要"har 生成用例"？因为手写测试脚本慢且易错，而 har 已经包含了"完整的请求信息"（URL、方法、参数、头）。用 har 生成用例的思路是：把 har 里的请求数据，用 Mustache 模板填充成测试脚本，实现"抓包数据 → 测试用例"的自动化转换。这大幅提升了脚本编写效率（不用手动抄 URL/参数），也降低了手写出错的可能。核心是"模板 + 数据填充"的代码生成思想。

【必须掌握】
- har = HTTP 归档格式，记录请求会话
- Mustache 模板：{{ 变量 }} 占位，填充数据
- 实现：读 har → 渲染模板 → 写测试文件
- Python 用 chevron/pymustache，Java 用 mustache.java
- HttpRunner 的 har2case 就是这套思路

【企业场景】
你在公司用 Charles/浏览器抓了接口请求（导出 har），用 har2case 或自写模板，一键生成 pytest/httprunner 测试用例，不用手动写请求代码。抓一次包，生成一批用例，效率翻倍。

【面试考察】
面试官：「怎么用 har 快速生成测试用例？」

参考回答框架：
1. har 记录 HTTP 请求信息
2. 用 Mustache 模板定义测试用例骨架
3. 读 har 数据填充模板，生成脚本
4. 工具：HttpRunner har2case

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 手动抄 har 里的 URL/参数 | 用模板自动填充，别手抄 |
| Mustache 变量名不匹配 | 模板 {{ url }} 要和 har 数据字段对应 |
| har 数据只取第一个 entry | 要遍历所有 entry 生成多个用例 |

【我的理解】
> （"har 生成用例"为什么能"降低出 Bug 概率"？自动填充相比手写，在哪些环节避免了人为错误？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| har 生成用例 | har + Mustache 模板 | ★★☆☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch34-gor流量回放]]
- [[Ch36-dubbo协议]]
