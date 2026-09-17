---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch23-Pytest结合数据驱动-json"
created: 2026-09-17
status: in_progress
---

# Ch23 - Pytest 结合数据驱动 - JSON

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、JSON 文件实现数据驱动

### 知识点 1：json.loads 读取 + parametrize

【课程原话/定义】
用内置 json 库读取 JSON 文件实现数据驱动。

JSON 语法：对象（{} 键值对）和数组（[] 有序列表）。

```python
import json, pytest

def get_json():
    with open('../data/params.json', 'r') as f:
        data = json.loads(f.read())
    return list(data.values())     # 返回 [[]] 格式

class TestWithJSON:
    @pytest.mark.parametrize('x,y,expected', get_json())
    def test_add(self, x, y, expected):
        assert my_add(int(x), int(y)) == int(expected)
```

JSON 文件（params.json）：
```json
{
  "case1": [1, 1, 2],
  "case2": [3, 6, 9],
  "case3": [100, 200, 300]
}
```

【为什么？】
为什么要用 JSON 做数据驱动？因为 JSON 是接口测试里最常用的数据格式（接口请求/响应多是 JSON），而且 JSON 支持嵌套结构（对象套对象、套数组），能表达比 CSV 更复杂的数据。用 JSON 做数据驱动，测试数据格式和接口数据格式一致，天然适合接口自动化。json.loads 读取后转 Python 字典，list(data.values()) 提取值为二维列表给 parametrize。

【必须掌握】
- JSON 两种结构：对象 {}、数组 []
- json.loads 读字符串转字典，json.load 读文件
- list(data.values()) 提取值为列表
- 支持嵌套结构（比 CSV 更灵活）
- 适合接口测试（数据格式一致）

【企业场景】
你在公司接口自动化测试，测试数据（请求参数 + 预期响应）用 JSON 存，格式和接口本身一致。测试用例 json.loads 读取后 parametrize 驱动，数据即接口数据，直观且灵活。

【面试考察】
面试官：「怎么用 JSON 做数据驱动？json.loads 和 json.load 区别？」

参考回答框架：
1. JSON 对象/数组两种结构
2. json.loads 读字符串，json.load 读文件
3. list(data.values()) 提取值给 parametrize
4. 适合接口测试，支持嵌套

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| json.loads 和 json.load 混淆 | loads 读字符串，load 读文件对象 |
| JSON 格式写错（单引号/尾逗号） | JSON 要双引号、不能尾逗号 |
| 提取数据格式不对 | list(data.values()) 转二维列表 |

【我的理解】
> （JSON 相比 CSV，在"表达复杂数据"上有什么优势？为什么接口测试更常用 JSON 做数据源？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| JSON 数据驱动 | json.loads + parametrize | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch22-Pytest结合数据驱动-excel]]
- [[Ch20-Pytest结合数据驱动-YAML]]
