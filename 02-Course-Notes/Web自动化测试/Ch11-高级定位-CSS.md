---
tags:
  - 课程笔记
  - Web自动化测试
  - Selenium
  - CSS定位
  - 高级定位
course: Web自动化测试
chapter: Ch11-高级定位-CSS
created: 2026-08-28
status: draft
---

# Ch11 - 高级定位 · CSS

## 课程来源
- 学习日期：

---

## 一、CSS 定位概述

### 知识点 1：相对定位 vs 绝对定位

【课程原话/定义】
Web 自动化测试中的高级 CSS 定位是指使用复杂的 CSS 选择器来选择页面上的元素。CSS 定位可分为**相对定位**和**绝对定位**，可以根据元素的标签、类、ID、属性、关系和状态等多种因素进行定位。

```css
/* 绝对定位：从根一路写到底 */
$("#ember63 > td.main-link.clearfix.topic-list-data > span > span > a")
/* 相对定位：从某个稳定锚点往下写 */
$("#ember63 [title='新话题']")
```

【为什么？】
相对定位和绝对定位的本质区别：**锚点选在哪**。

- **绝对定位**：从最外层开始，一层层 `>` 写到最后，路径里任何一层结构变了，整条选择器作废
- **相对定位**：先找一个**稳定的锚点**（本例的 `#ember63`），再用关系/属性往下精确定位，锚点以下的结构变化不影响锚点以上

相对定位的三个优点（课程原文）：①更易维护（结构变化只需更新相关选择器）②更简洁易读 ③元素嵌套多层时更轻松选中目标而无需冗长选择器。

一句话：**绝对定位是"从山顶走到山脚"，相对定位是"先坐缆车到半山腰，再走几步"**。

【必须掌握】
- 相对 vs 绝对：锚点是否"稳定、可复用"
- 相对定位三优点：易维护、简洁、嵌套场景好用
- CSS 定位依据：标签、类、ID、属性、关系、状态

【企业场景】
你在测一个列表页，每条数据的 DOM 结构一样但都嵌在 `#ember63`、`#ember64`… 这种动态 id 的容器里。用绝对定位（`td.main-link.clearfix > span > span > a`）改版就废；用相对定位（先锚定一个语义化容器，再找 `[title='新话题']`）就能抗住大部分改版。

【面试考察】
面试官："CSS 相对定位和绝对定位的区别？你倾向用哪个？"

参考回答框架：
1. 绝对定位从根节点逐层写，结构一改就全废
2. 相对定位锚定一个稳定元素再往下找，抗改版能力强
3. 倾向相对定位：易维护、简洁、嵌套场景好用
4. 加分：绝对定位常来自"F12 Copy selector"，是反面教材

【易错点】

| 误区 | 纠正 |
|------|------|
| 从 F12 "Copy selector" 直接粘贴 | 得到的常是绝对/脆弱选择器，要自己写相对定位 |
| 相对定位 = 随便锚定一个元素 | 锚点必须稳定（语义 id / 不变的父容器） |

【我的理解】
> （把"绝对定位"和"相对定位"的差别，用你自己想的一个生活类比讲一遍。为什么相对定位"改版后只需改一处"？）

---

## 二、CSS 基础语法

### 知识点 2：四种基础选择器

【课程原话/定义】

| 类型 | 表达式 |
|------|--------|
| 标签 | 标签名 |
| 类 | `.class` 属性值 |
| ID | `#id` 属性值 |
| 属性 | `[属性名="属性值"]` |

```javascript
// 调试方式：F12 → Console，$("css 表达式") 就是 document.querySelectorAll 的别名
$('input')              // 标签名：所有 input
$('.s_ipt')             // 类：class 含 s_ipt 的元素
$('#kw')                // id：id 为 kw 的元素
$('[name="wd"]')        // 属性：name 为 wd 的元素
```

课程在测试人社区（ceshiren.com）上的实战：

```javascript
$("div")                                             // 所有 div 标签
$(".logo-big")                                       // class 定位 Logo
$(".header-dropdown-toggle.search-dropdown")         // 复合 class：空格换点
$("#site-logo")                                      // id 定位 Logo
$("[alt='测试人社区']")                                // 属性定位（img 的 alt）
```

【为什么？】
四种选择器对应"元素身上四种可用的标识"。关键细节：

1. **复合 class 要把空格换成 `.`**：HTML 里 `class="header-dropdown-toggle search-dropdown"` 是两个 class，CSS 要写成 `.header-dropdown-toggle.search-dropdown`（中间无空格）。这正好对应 Ch06 讲的"`By.CLASS_NAME` 不能传复合 class 值"——CSS 里能写复合，`By.CLASS_NAME` 里不能。
2. **属性选择器是"万金油"**：`[alt='测试人社区']`、`[name='wd']`、`[data-test-id='x']`，任何属性都能用，是"没有 id/class"时的兜底。
3. **调试用 `$()`**：Chrome 控制台的 `$("...")` 等价 `document.querySelectorAll("...")`，输入后直接看到匹配的元素列表和数量。

【必须掌握】
- 四种基础选择器：标签 / `.class` / `#id` / `[属性="值"]`
- 复合 class 空格换点：`.a.b`
- 控制台 `$("css")` 调试（= querySelectorAll）
- 属性选择器是"无 id/class"时的兜底

【企业场景】
你定位一个 Logo `<img alt="测试人社区">`，它既没有 id 也没有语义 class，你用 `[alt='测试人社区']` 属性选择器精准命中。属性选择器在企业里最常见的用途是 `[data-test-id='xxx']`——Ch06/Ch09 反复强调的"契约化定位"就是靠它。

【面试考察】
面试官："CSS 基础选择器有哪几种？复合 class 怎么写？"

参考回答框架：
1. 四种：标签名、`.class`、`#id`、`[属性名="值"]`
2. 复合 class 把空格换成 `.`（`.a.b`），不能写 `.a b`（那是后代关系）
3. 属性选择器是"无 id/class"时的兜底，`[data-test-id]` 是契约化定位的载体
4. 调试：控制台 `$()` / `querySelectorAll().length`

【易错点】

| 误区 | 纠正 |
|------|------|
| 复合 class 写成 `.a b` | 空格是"后代"关系，复合类要 `.a.b` |
| `By.CLASS_NAME` 传 `"a b"` | Selenium 报 invalid selector，复合类用 CSS 的 `.a.b` |
| 只会用 id/class，忘了属性选择器 | `[alt=...]`/`[data-test-id=...]` 是重要兜底 |

【我的理解】
> （`.a.b` 和 `.a .b` 有什么区别？为什么差一个空格，选中的元素就完全不同了？）

---

## 三、CSS 关系定位

### 知识点 3：五种关系选择器

【课程原话/定义】

| 类型 | 格式 |
|------|------|
| 并集 | `元素,元素` |
| 邻近兄弟（了解即可） | `元素+元素` |
| 兄弟（了解即可） | `元素1~元素2` |
| 父子（重点） | `元素>元素` |
| 后代（重点） | `元素 元素` |

```javascript
$('.bg,.s_ipt_wr,.new-pmd,.quickdelete-wrap')   // 并集：多个选择器一起选
$('#s_kw_wrap>input')                           // 父子：直接子元素
$('#form input')                                // 后代：所有子孙元素
$('.soutu-btn+input')                           // 邻近兄弟：紧邻的下一个
$('.soutu-btn~i')                               // 兄弟：后面所有同级
```

【为什么？】
这五种是"关系定位"，核心区别在**两个重点**上：

| 符号 | 关系 | 选中范围 | 区别 |
|------|------|----------|------|
| `A>B` | 父子 | A 的**直接子**元素 B | 只下一层 |
| `A B` | 后代 | A 的**所有子孙**元素 B | 任意深度 |

`#main>#ember4` 只选"main 的直接子 ember4"；`#main #ember4` 选"main 下面任意层级的 ember4"。前者更精确，后者更宽松。

并集 `A,B` 是"一次选多个"：`$("#main,#ember6")` 同时拿到两个元素——适合**批量操作或批量断言**。

邻近兄弟 `+`、兄弟 `~` 标记"了解即可"，因为它们的应用场景窄（要元素紧挨着），且前端一加节点就失效，日常定位很少用。

【必须掌握】
- 父子 `>`（直接子）vs 后代 ` `（所有子孙）的区别——面试高频
- 并集 `,` 一次选多个
- 邻近兄弟 `+`、兄弟 `~` 了解即可，少用

【企业场景】
你定位一个表单里的输入框：`#login-form input` 会选中表单里**所有** input（包括隐藏的）；`#login-form>input` 只选**直接子级** input。如果你要的输入框是直接子级但页面里还有嵌套的子表单，用 `>` 能精准避开嵌套的那些——这就是"父子 vs 后代"的真实价值。

【面试考察】
面试官："CSS 里 `>` 和空格有什么区别？"

参考回答框架：
1. `>` 是父子（直接子元素），空格是后代（所有子孙）
2. `#a>b` 只选 a 的直接子 b；`#a b` 选 a 下任意深度的 b
3. 实际：要精确用 `>`，要宽松用空格；选错会命中到不该选的元素

【易错点】

| 误区 | 纠正 |
|------|------|
| `>` 和空格混用不分 | `>` 只下一层，空格任意深度 |
| 邻近兄弟/兄弟当主力用 | 应用场景窄、前端加节点就失效，了解即可 |
| 并集 `,` 忘写第二个选择器 | 并集用于"多选"，`A,B` 两个都要写 |

【我的理解】
> （`#main>#ember4` 和 `#main #ember4` 什么时候结果一样、什么时候不一样？举一个"结果不一样"的场景。）

---

## 四、CSS 顺序关系

### 知识点 4：nth-child 与 nth-of-type

【课程原话/定义】

| 类型 | 格式 |
|------|------|
| 父子关系 + 顺序 | `:nth-child(n)` |
| 父子关系 + 标签类型 + 顺序 | `:nth-of-type(n)` |

```javascript
$('#form>input:nth-child(2)')      // form 直接子 input 中，是"第2个子元素"的那个
$('#form>input:nth-of-type(1)')    // form 直接子 input 中，"第1个 input"的那个
```

（课程表格原文两行"格式"都写成了"元素 元素"，是复制粘贴笔误，正确写法见上表。）

【为什么？】
`nth-child` 和 `nth-of-type` 是**最容易搞混的一对**，本质区别在"数谁"：

| 选择器 | 数的对象 | 例子 `#form>input:nth-child(2)` |
|--------|----------|-------------------------------|
| `:nth-child(n)` | 父元素**所有子元素**里的第 n 个（不限类型） | 第 2 个子元素**必须是 input**，否则选不中 |
| `:nth-of-type(n)` | 父元素**同类型子元素**里的第 n 个 | 第 2 个 **input**（中间夹别的标签不算） |

经典翻车场景：`<form>` 里第一个子元素是 `<label>`、第二个才是 `<input>`。此时 `input:nth-child(1)` **选不中任何元素**（因为第 1 个子元素是 label 不是 input），而 `input:nth-of-type(1)` 能选中第一个 input。**这就是为什么 `nth-of-type` 更常用、更稳**。

【必须掌握】
- `:nth-child(n)`：所有子元素里第 n 个（必须同类型才算）
- `:nth-of-type(n)`：同类型里第 n 个（更常用）
- 两者区别是面试高频陷阱

【企业场景】
你定位导航栏第 3 个菜单项：`#navigation-bar>li:nth-child(3)`。如果导航栏里每个 `<li>` 之间没有别的标签，nth-child 和 nth-of-type 结果一样；但如果有人插了个 `<span>` 分隔符，nth-child 就错位了——所以团队规范里统一用 `nth-of-type`，抗干扰。

【面试考察】
面试官："`:nth-child(2)` 和 `:nth-of-type(2)` 有什么区别？"

参考回答框架：
1. `nth-child(n)` 看父元素所有子元素的第 n 个（跨类型计数）
2. `nth-of-type(n)` 看同类型子元素的第 n 个
3. 举例：form 里 label 在前 input 在后，`input:nth-child(1)` 选不中，`input:nth-of-type(1)` 能选中
4. 实践：统一用 `nth-of-type`，抗"中间插标签"的干扰

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 nth-child 和 nth-of-type 一样 | 计数范围不同：所有子 vs 同类型子 |
| `input:nth-child(1)` 在 label 后选不中 | 第 1 个子是 label 不是 input → 换 nth-of-type |
| 课程表格"格式"两行都写"元素 元素" | 笔误，正确是 :nth-child(n) / :nth-of-type(n) |

【我的理解】
> （构造一个 `<form>`：`<label>`、`<input>`、`<input>`。`input:nth-child(1)` 选得中吗？`input:nth-of-type(1)` 选中的是哪个？）

---

## 五、CSS 定位实战

### 知识点 5：实战 + 调试方法

【课程原话/定义】
测试步骤：打开测试人社区（https://ceshiren.com/）→ 用 CSS 高级定位进入【类别】页面 → 获取文本断言。

Python 实现：

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Test:
    def setup(self):
        self.service = Service()
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.implicitly_wait(10)

    def teardown(self):
        self.driver.quit()

    def test_get_ceshiren(self):
        self.driver.get("https://www.ceshiren.com")
        self.driver.find_element(By.CSS_SELECTOR, ".categories").click()        # 点击"类别"
        text = self.driver.find_elements(By.CSS_SELECTOR, ".category-name")[0].text  # 取第一个类别名
        assert text == "提问区"                                                 # 断言
```

【为什么？】
这条实战把前面四节串起来：`.categories` 是 class 定位，`.category-name` 是 class 定位 + `find_elements` 取集合里的第 0 个（Ch06 讲的单数/复数差异）。

调试方法是本章的隐性重点——**写之前先在控制台验证，别写进代码再试**：

| 调试方式 | 操作 | 用途 |
|----------|------|------|
| Console `$("css")` | 输入选择器直接看匹配结果 | 快速验证 CSS |
| Console `$x("xpath")` | 验证 XPath | Ch12 会讲 |
| Elements 面板 Ctrl+F | 粘贴选择器看"1 of N" | 验证匹配数 |

匹配数必须是 1（或明确知道要取第几个），否则就是 Ch06 讲的"静默点错元素"。

【必须掌握】
- CSS 实战链路：定位（CSS）→ 点击 → 取值 → 断言
- `find_elements(...)[0]` 取集合第一个（要先确认有元素）
- 调试：Console `$()` 或 Elements Ctrl+F 验证匹配数

【企业场景】
你在写用例前，先在 Console 里把每个 CSS 选择器跑一遍、确认匹配数，再写进代码。这个习惯能把"脚本点错元素"的 bug 消灭在编码阶段——比跑挂之后逐行排查高效得多（Ch06 知识点4 讲过的验证方法）。

【面试考察】
面试官："你写完一个 CSS 定位器，怎么确认它是对的？"

参考回答框架：
1. 控制台 `$("css")` 看匹配结果，或 Elements 面板 Ctrl+F 看"1 of N"
2. 匹配数必须是 1；如果是 N，说明不够精确，会点错元素
3. 再跑脚本验证，配合失败截图/打印元素文本兜底

【易错点】

| 误区 | 纠正 |
|------|------|
| 写完定位器直接跑脚本试 | 先在 Console/Elements 验证匹配数，省时 |
| `find_elements(...)[0]` 不判空 | 空列表 → IndexError，先确认有元素 |
| 断言用 `==` 且文案带后缀 | 标题常带前后缀，用 `in` 包含匹配 |

【扩展知识】
CSS 的能力边界（Ch06 已预告，本章正式确认）：CSS 简洁、执行快，但**不能按元素文本内容匹配**（没有 `text()`）、**不能向上找父级/祖先**（只能往下）。这两个短板恰好是 XPath 的强项——见 [[Ch12-高级定位-XPath]]。"CSS 为主、XPath 补位"是团队常见规范。

【我的理解】
> （CSS 定位"不能按文本匹配、不能向上找父级"——想一想什么时候你必须要用 XPath 而不是 CSS？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 相对 vs 绝对定位 | 锚点稳定、抗改版 | ★★★★☆ |
| 四种基础选择器 | 标签/.class/#id/[属性] | ★★★★★ |
| 复合 class | 空格换点 `.a.b` | ★★★☆☆ |
| 五种关系选择器 | 并集/邻近兄弟/兄弟/父子>/后代空格 | ★★★★☆ |
| 顺序关系 | :nth-child vs :nth-of-type | ★★★★☆ |
| 调试方式 | Console `$()` / Elements Ctrl+F | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch06-八大元素定位方式]]（CSS 基础定位、定位器优先级）
- [[Ch09-自动化测试定位策略]]（CSS 是"组合定位/父子定位"的载体）
- [[Ch12-高级定位-XPath]]（CSS 的短板正是 XPath 的强项，互补）
