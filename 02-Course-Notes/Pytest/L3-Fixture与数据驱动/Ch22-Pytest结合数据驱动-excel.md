---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch22-Pytest结合数据驱动-excel"
created: 2026-09-17
status: in_progress
---

# Ch22 - Pytest 结合数据驱动 - Excel

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L3

---

## 一、openpyxl 实现数据驱动

### 知识点 1：openpyxl 读取 + parametrize

【课程原话/定义】
用 openpyxl 库读取 Excel（.xlsx）实现数据驱动。推荐 openpyxl（支持读写 xlsx，简单易用）。

```python
import openpyxl, pytest

def get_excel():
    book = openpyxl.load_workbook('../data/params.xlsx')   # 工作簿
    sheet = book.active                                     # 工作表
    values = []
    for row in sheet:                                       # 遍历行
        line = []
        for cell in row:                                    # 遍历单元格
            line.append(cell.value)
        values.append(line)
    return values

class TestWithEXCEL:
    @pytest.mark.parametrize('x,y,expected', get_excel())
    def test_add(self, x, y, expected):
        assert my_add(int(x), int(y)) == int(expected)
```

安装：pip install openpyxl

【为什么？】
为什么要用 Excel 做数据驱动？因为测试团队习惯用 Excel 管理测试用例（表格直观、易编辑、易分享）。openpyxl 让 pytest 能直接读 Excel 里的数据驱动测试，把"Excel 用例表"和"自动化脚本"打通。相比 CSV，Excel 支持多 sheet、格式、公式，适合更复杂的用例管理。核心思路和 CSV/JSON 一样：外部数据源 → 读取 → parametrize 驱动，只是读取库不同（openpyxl）。

【必须掌握】
- pip install openpyxl
- load_workbook 加载工作簿，book.active 取工作表
- 遍历 sheet 行/单元格取 value
- 返回 [[]] 格式给 parametrize
- 支持多 sheet（book["sheet名"]）

【企业场景】
你在公司测试用例都用 Excel 管理，用 openpyxl 读取 Excel 的数据直接驱动 pytest 用例。测试同学改 Excel 用例表，不用碰代码，自动化用例自动用新数据。这是"用例表 → 自动化"的常见打通方式。

【面试考察】
面试官：「怎么用 Excel 做数据驱动？openpyxl 怎么读？」

参考回答框架：
1. pip install openpyxl
2. load_workbook 加载 + book.active 取 sheet
3. 遍历行列取 cell.value
4. 返回二维列表给 parametrize

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 忘装 openpyxl | Excel 要 pip install openpyxl（不是内置） |
| 用 xlrd 读 xlsx | xlrd 新版不支持 xlsx，用 openpyxl |
| 遍历漏了表头行 | Excel 第一行若是表头要跳过 |

【我的理解】
> （openpyxl 读取 Excel 和 csv.reader 读取 CSV，在"返回数据格式"上有什么共同点？为什么都返回 [[]]？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Excel 数据驱动 | openpyxl + parametrize | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch21-Pytest结合数据驱动-csv]]
- [[Ch23-Pytest结合数据驱动-json]]
