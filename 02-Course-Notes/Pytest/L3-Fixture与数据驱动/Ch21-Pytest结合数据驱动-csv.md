---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch21-Pytest结合数据驱动-csv"
created: 2026-09-17
status: in_progress
---

# Ch21 - Pytest 结合数据驱动 - CSV

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、CSV 文件实现数据驱动

### 知识点 1：csv.reader 读取 + parametrize

【课程原话/定义】
数据驱动测试（DDT）：将测试数据与测试逻辑分离，用外部数据源驱动测试。数据量大时用结构化文件（CSV/Excel/JSON/YAML）存储。

CSV 数据驱动：
```python
import csv, pytest

def get_csv():
    with open('../data/params.csv', 'r') as file:
        raw = csv.reader(file)
        data = []
        for line in raw:
            data.append(line)
        return data     # 返回 [[]] 格式

class TestWithCSV:
    @pytest.mark.parametrize('x,y,expected', get_csv())
    def test_add(self, x, y, expected):
        assert my_add(int(x), int(y)) == int(expected)
```

CSV 文件（params.csv，每行 x,y,expected）：
```
1,1,2
3,6,9
100,200,300
```

【为什么？】
为什么要用 CSV 做数据驱动？因为"数据量大的测试"硬编码在代码里不现实——几十上百组测试数据写死在 @parametrize 里，代码臃肿难维护。CSV 文件把数据"外置"，测试用例只写一次逻辑，数据从文件动态加载，加数据只需改 CSV 文件不用改代码。这是"数据与逻辑分离"的核心价值。CSV 用标准库 csv.reader 读取，返回列表嵌套列表格式，正好匹配 parametrize 的参数格式。

【必须掌握】
- DDT：数据与逻辑分离，外部数据源驱动
- csv.reader(file) 读取，返回 [[]] 格式
- 注意：CSV 读出来是字符串，要 int() 转换类型
- parametrize 直接接收读取的二维列表
- 目录：src（代码）/data（数据）/tests（用例）

【企业场景】
你在公司测接口，上百组测试数据（用户名/密码/预期结果）放 CSV 文件，测试用例用 parametrize 动态加载。新增测试数据只需在 CSV 加一行，不用改代码。数据和逻辑分离，维护成本大降。

【面试考察】
面试官：「怎么用 CSV 做数据驱动测试？」

参考回答框架：
1. DDT 数据与逻辑分离
2. csv.reader 读取文件返回二维列表
3. parametrize 接收数据动态生成用例
4. 注意类型转换（CSV 读出是字符串）

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| CSV 读出直接断言 | 读出是字符串，要 int() 转换 |
| 数据格式不匹配 parametrize | 要返回 [[]] 格式，每行对应一组参数 |
| 数据硬编码在代码 | 数据量大应外置到 CSV |

【我的理解】
> （为什么 CSV 读出来的数字是字符串？这会给数据驱动测试带来什么坑，怎么避免？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| CSV 数据驱动 | csv.reader + parametrize | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch20-Pytest结合数据驱动-YAML]]
- [[Ch22-Pytest结合数据驱动-excel]]
