---
tags: [课程笔记, 接口测试, Flask, Jinja2]
course: "接口测试"
chapter: "Ch04-Jinja2模板技术"
created: 2026-07-30
status: draft
---

# Ch04 - Jinja2 模板技术

> 前置：[[Ch03-请求与响应处理]] — `render_template()` 基础用法
> 后置：[[Ch05-xxx]]（待补充）

## 课程来源
- 学习日期：

---

## 一、模板渲染基础

### 知识点 1：什么是模板和渲染

【课程原话/定义】
包含变量和运算逻辑的 HTML（或其他格式的文本）叫做模板。执行变量替换和逻辑计算工作的过程被称为渲染。Flask 使用 Jinja2 引擎完成模板渲染，默认从模块同级的 `templates/` 目录下寻找模板。

目录结构：
```
xx.py              # Flask 主程序
templates/         # 模板目录（名字必须叫 templates）
    hogwarts.html
```

视图函数用 `render_template()` 渲染：
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("hogwarts.html")
```

【为什么？】
模板引擎解决的核心问题：**数据与表现的分离**。把 HTML 写死在 Python 字符串里（`return "<h1>" + title + "</h1>"`）是噩梦——不可维护、不可复用、前端没法独立工作。模板让你把 HTML 放在 `.html` 文件里，只把"会变的部分"用占位符标记，Flask 在渲染时替换。

底层流程：
1. 浏览器请求 `/`
2. Flask 调用视图函数
3. 视图函数调用 `render_template("hogwarts.html", name="Riley")`
4. Jinja2 读取 `hogwarts.html`，把 `{{ name }}` 替换成 `"Riley"`
5. 返回完整的 HTML 字符串给浏览器

【必须掌握】
- 模板目录名必须是 `templates/`，和 Flask 主程序同级
- `render_template("文件名")` 渲染模板
- Jinja2 是 Flask 默认的模板引擎（依赖项之一）
- 模板 = HTML 骨架 + 占位符变量 + 控制逻辑

【企业场景】
模板渲染在接口测试中不常用（接口测试主要处理 JSON），但做 Mock 服务时有两种场景用到：
1. **Mock 一个返回 HTML 的接口**（比如邮件预览、报告页面）
2. **搭建测试辅助工具**（比如一个简单的测试数据管理页面，方便手工测试时查数据）

不过更重要的是——理解模板语法后，你会接触到 Jinja2 的核心概念（变量插值、条件、循环），这和 Ansible、SaltStack、Airflow 等工具的配置模板语法几乎一样。

【面试考察】
面试官："Flask 的模板引擎是什么？模板文件默认放在哪个目录？"

参考回答框架：
1. Jinja2，Flask 的两大核心依赖之一（另一个是 Werkzeug）
2. 默认在 `templates/` 目录下，和 Flask 主程序同级
3. Jinja2 负责解析模板中的 `{{ }}` 变量和 `{% %}` 控制语句，替换后生成纯 HTML

【易错点】

| 常见错误                       | 正确做法                            |
| -------------------------- | ------------------------------- |
| 模板目录叫 `template`（少一个 s）    | 必须叫 `templates`（Flask 默认查找的名称）  |
| 模板文件放在项目根目录                | 必须放在 `templates/` 目录内           |
| `render_template()` 写了完整路径 | 只写文件名，Flask 自动从 `templates/` 里找 |

【扩展知识】
Flask 查找模板的顺序：
1. 应用同级的 `templates/` 目录
2. 如果用了 Blueprint（蓝图），还会查找 Blueprint 指定的 `template_folder`
3. 可以通过 `app = Flask(__name__, template_folder='my_templates')` 自定义模板目录名

【我的理解】
> （手写一个完整的模板渲染流程：创建 `templates/hello.html`，里面写 `<h1>Hello {{ name }}</h1>`。在视图函数中传入 `name='Riley'`，访问页面后右键"查看网页源代码"——页面里还有 `{{ name }}` 吗？渲染是在浏览器端还是服务器端完成的？）

---

## 二、模板语法核心

### 知识点 2：两种代码块 — {{ }} 和 {% %}

【课程原话/定义】
Jinja2 模板中有两种核心语法：

| 语法         | 用途             | 示例                                   |
| ---------- | -------------- | ------------------------------------ |
| `{{ 变量 }}` | 变量代码块 — 显示变量内容 | `{{ name }}`、`{{ person.age }}`      |
| `{% 语句 %}` | 控制代码块 — 逻辑控制   | `{% if %}`、`{% for %}`、`{% block %}` |

Jinja2 支持大部分 Python 对象（字符串、列表、字典、元组、整数、浮点数、布尔值），支持基本运算（`+` `-` `*` `/`）、比较（`==` `!=`）、逻辑（`and` `or` `not`）以及 `in`、`is`。

【为什么？】
这两种语法的设计哲学：**变量只负责"展示"，控制只负责"逻辑"**。这和 MVC 模式的 View 层理念一致——模板中可以有简单的展示逻辑（if/for），但不能有复杂的业务逻辑。如果你发现自己在模板里写了几十行 `{% %}`，说明业务逻辑应该移到视图函数里。

另外，Jinja2 不支持所有 Python 语法——比如不能 `import` 模块、不能定义函数、不能修改全局变量。这是有意为之的安全设计：模板只负责渲染，不能做"破坏性"操作。

【必须掌握】
- `{{ }}` = 输出变量值，里面的内容会被 HTML 转义（防 XSS）
- `{% %}` = 执行控制语句，不直接输出内容
- 模板中 `.` 可以取属性也可以取字典键值：`person.name` 等价于 `person['name']`
- 模板中不能定义函数、不能 import、不能修改全局变量

【企业场景】
这两种语法在测试领域中不只是 Flask 在用——很多测试工具的配置模板也用类似的语法：
- Ansible playbook 的 `.j2` 模板
- Airflow DAG 的动态生成
- 测试报告模板（如 Allure 的自定义模板）

掌握了 `{{ }}` 和 `{% %}`，这些工具的模板你就都能看懂。

【面试考察】
面试官："Jinja2 的 `{{ }}` 和 `{% %}` 有什么区别？Jinja2 支持所有 Python 语法吗？"

参考回答框架：
1. `{{ }}` 用于输出变量值，`{% %}` 用于控制逻辑（if/for/block）
2. 不支持所有 Python 语法，不能 import、定义函数、修改全局变量
3. 这是安全设计——模板只负责渲染展示，不负责业务逻辑
4. `.` 语法同时支持属性访问和字典键值访问

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 在 `{{ }}` 中写赋值语句 `{{ x = 5 }}` | `{{ }}` 只能输出，赋值要在视图函数中完成 |
| 在模板中写 `import os` | Jinja2 不支持 import，需要的数据通过视图函数传入 |
| `{{ person['name'] }}` 和 `{{ person.name }}` 混用 | 两者等价，推荐用 `.` 更简洁 |

【我的理解】
> （在模板中分别用 `{{ }}` 输出字符串、整数、列表、字典、布尔值。观察：`{{ True }}` 和 `{{ None }}` 分别显示什么？列表和字典在 HTML 中是怎么显示的（直接打印 vs 遍历）？）

---

### 知识点 3：传递数据到模板

【课程原话/定义】
在 `render_template()` 中使用关键字参数将数据传递给模板。

```python
@app.route("/data")
def hogwarts():
    return render_template("hogwarts.html", name="hogwarts")
```

```html
<!-- hogwarts.html -->
<h2>{{ name }}</h2>
```

访问 `/data`，`{{ name }}` 处显示 `hogwarts`。

【为什么？】
数据传递方向永远是单向的：**Python（视图函数） → 模板**。模板不能"回传"数据给 Python——这是因为 HTTP 是无状态协议，模板渲染完成后，生成的 HTML 就发送给浏览器了，模板本身不再存在。

关键理解：`render_template()` 接收关键字参数的本质——参数名成为模板变量名，参数值成为模板变量值。这是"命名约定"而不是"魔法"。

【必须掌握】
- `render_template('模板', key=value)` 关键字传参
- 模板中直接用 `{{ key }}` 取值
- 可以传任意 Python 对象：字符串、数字、列表、字典、对象
- 传递字典时两种取值方式等价：`{{ person.name }}` = `{{ person['name'] }}`

【企业场景】
Mock 接口返回 HTML 时，数据通过 `render_template()` 传入：

```python
@app.route('/report')
def test_report():
    report_data = {
        "total": 100,
        "passed": 95,
        "failed": 3,
        "skipped": 2,
        "pass_rate": "95%"
    }
    return render_template("report.html", data=report_data)
```

模板里就可以用 `{{ data.passed }}` 显示通过数——测试数据管理页面就做出来了。

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 模板中用了 `{{ data }}` 但视图函数没传 | 报错 `UndefinedError`，检查 `render_template()` 的参数 |
| 关键字参数名和模板变量名不一致 | 保持一致：`render_template(..., name="Riley")` → `{{ name }}` |
| 传了对象但模板里访问了不存在的属性 | Jinja2 返回空字符串（不报错），和 Python 的 AttributeError 不同 |

【我的理解】
> （在视图函数中创建一个包含 name、age、hobbies（列表）的字典 person，传入模板。在模板中分别用 `{{ person.name }}`、`{{ person['name'] }}`、`{{ person.hobbies[0] }}` 三种方式取值。哪种写法最清晰？）

---

## 三、控制结构

### 知识点 4：判断语法 — if / elif / else

【课程原话/定义】
Jinja2 支持条件判断，语法和 Python 几乎一样：

```
{% if 条件表达式 %}
    ...
{% elif 条件表达式 %}
    ...
{% else %}
    ...
{% endif %}
```

注意：必须有 `{% endif %}` 关闭——和 Python 用缩进不同，Jinja2 用显式的结束标签。

示例——根据性别显示不同称呼：
```python
@app.route("/person")
def person():
    person = {"name": "lily", "age": 18, "gender": "female"}
    return render_template("person.html", person=person)
```

```html
<p>
  您好,
  {% if person.gender == "male" %}
    {{ person.name }} 先生
  {% else %}
    {{ person.name }} 女士
  {% endif %}
</p>
```

【为什么？】
Jinja2 用 `{% endif %}` 而不是 Python 的缩进——因为 HTML 本身就有缩进（为了代码可读性），如果 Jinja2 也用缩进表示代码块，会跟 HTML 的缩进冲突。所以 Jinja2 选择了"显式结束标签"的设计：`{% endif %}`、`{% endfor %}`、`{% endblock %}`。这个设计理念和许多模板引擎（Smarty、Twig、Liquid）一致。

【必须掌握】
- 语法：`{% if %} ... {% elif %} ... {% else %} ... {% endif %}`
- `{% endif %}` 不能省略
- 条件表达式支持：`==`、`!=`、`>`、`<`、`>=`、`<=`、`and`、`or`、`not`、`in`、`is`
- `person.gender` 等价于 `person['gender']`

【企业场景】
测试报告模板中，根据测试结果状态显示不同颜色：

```html
{% for case in test_cases %}
<tr>
    <td>{{ case.name }}</td>
    <td>
        {% if case.status == "passed" %}
            <span style="color: green">PASS</span>
        {% elif case.status == "failed" %}
            <span style="color: red">FAIL</span>
        {% elif case.status == "skipped" %}
            <span style="color: gray">SKIP</span>
        {% else %}
            <span>{{ case.status }}</span>
        {% endif %}
    </td>
</tr>
{% endfor %}
```

【面试考察】
面试官："Jinja2 的 if 语句中可以使用哪些运算符？和 Python 的 if 有什么不同？"

参考回答框架：
1. 支持比较运算符（`==` `!=` `>` `<`）、逻辑运算符（`and` `or` `not`）、成员运算符（`in`）、身份运算符（`is`）
2. 主要不同：Jinja2 用 `{% endif %}` 显式关闭，Python 用缩进
3. 不支持 Python 的 `elif True:` 后面没有内容的写法
4. `.` 访问同时支持属性和字典键值

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 忘记 `{% endif %}` | Jinja2 会报模板语法错误 |
| 用 `&&` `||` `!` 代替 `and` `or` `not` | Jinja2 用 Python 风格的关键字，不是 JS/C 风格 |
| `{% if person.gender == male %}`（male 没加引号） | 字符串必须加引号：`"male"` |
| if 条件里写赋值 `{% if x = 5 %}` | 用 `==` 比较，`=` 是赋值（Jinja2 不支持） |

【我的理解】
> （创建一个 `/score` 路由，传入一个 score 字典（包含 name 和 score 字段）。模板中根据 score 的值判断：≥90 显示"优秀"、≥80 显示"良好"、≥60 显示"及格"、否则显示"不及格"。用小数据验证每个分支。）

---

### 知识点 5：循环语法 — for

【课程原话/定义】
Jinja2 的 for 循环用于迭代序列（列表、字典等）：

```
{% for item in list_or_dict %}
    {{ item }}
{% endfor %}
```

示例——遍历人员列表：
```python
@app.route("/people")
def people():
    people = [
        {"name": "lily", "age": 18, "gender": "female"},
        {"name": "tom", "age": 19, "gender": "male"},
    ]
    return render_template("people.html", people=people)
```

```html
{% for p in people %}
<p>
  Hello,
  {% if p.gender == "male" %}
    Mr. {{ p.name }}
  {% else %}
    Ms. {{ p.name }}
  {% endif %}
  Your age is {{ p.age }}
</p>
{% endfor %}
```

【为什么？】
for 循环让模板具备了"批量渲染"的能力——一个 100 人的列表，不需要写 100 段 HTML，一段 `{% for %}` 搞定。这和接口测试中的"数据驱动"思想一致：模板 = 显示框架，数据 = 驱动内容。

Jinja2 的 for 循环还提供了循环内变量（Loop Variables），在测试报告模板中特别有用：

| 变量 | 含义 |
|------|------|
| `loop.index` | 当前迭代序号（从 1 开始） |
| `loop.index0` | 当前迭代序号（从 0 开始） |
| `loop.first` | 是否为第一次迭代 |
| `loop.last` | 是否为最后一次迭代 |
| `loop.length` | 序列总长度 |

【必须掌握】
- `{% for item in list %} ... {% endfor %}`
- 支持嵌套（for 里面套 if，if 里面套 for）
- `loop.index` 从 1 开始，`loop.index0` 从 0 开始
- 遍历字典时，默认遍历 keys：`{% for key in dict %}`
- 遍历字典的 key-value：`{% for key, value in dict.items() %}`

【企业场景】
测试用例列表渲染——Mock 一个测试结果展示页面：

```html
<table border="1">
    <tr><th>序号</th><th>用例名</th><th>状态</th></tr>
    {% for case in test_cases %}
    <tr>
        <td>{{ loop.index }}</td>
        <td>{{ case.name }}</td>
        <td>
            {% if case.status == "passed" %}
                ✅
            {% else %}
                ❌
            {% endif %}
        </td>
    </tr>
    {% endfor %}
</table>
```

`loop.index` 自动生成行号，不需要在 Python 里手动维护计数器。

【面试考察】
面试官："Jinja2 的 for 循环有哪些内置变量？`loop.index` 和 `loop.index0` 有什么区别？"

参考回答框架：
1. `loop.index`：当前迭代序号，从 1 开始
2. `loop.index0`：从 0 开始
3. `loop.first` / `loop.last`：判断是否第一个/最后一个元素（常用于分隔符处理）
4. `loop.length`：列表总长度

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 忘记 `{% endfor %}` | 和 if 一样必须显式关闭 |
| 用 `for key, value in dict`（不加 .items()） | Jinja2 遍历字典默认只给 key，要 key+value 需 `.items()` |
| 在模板中做复杂计算 | 数据预处理放在视图函数里，模板只负责展示 |
| 列表为空时 for 循环什么都不输出 | 可以配合 `{% if list %}` 先判断，或使用 `{% else %}` 显示空状态 |

【扩展知识】
Jinja2 的 for-else 语法：
```
{% for item in items %}
    {{ item }}
{% else %}
    <p>列表为空</p>
{% endfor %}
```
当列表为空时，渲染 `{% else %}` 块内的内容——比先 if 再 for 更优雅。

【我的理解】
> （创建一个 `/students` 路由，传入一个包含 5 个学生信息的列表。模板中用 for 循环渲染表格，包含序号（loop.index）、姓名、年龄、成绩。额外练习：如果列表为空，用 `{% else %}` 显示"暂无学生数据"。）

---

## 四、模板复用

### 知识点 6：模板继承 — extends + block

【课程原话/定义】
模板继承允许创建"父模板"（骨架），定义可被子模板重写的区域（`{% block %}`）。子模板通过 `{% extends %}` 继承父模板，只重写需要定制的 block。

**定义父模板（layout.html）：**
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <div id="content">{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2023 by <a href="https://ceshiren.com">测试人社区</a>.
        {% endblock %}
    </div>
</body>
</html>
```

**子模板（son.html）：**
```html
{% extends "layout.html" %}

{% block title %}Son Page{% endblock %}

{% block content %}
<h1>子模板</h1>
<button>按钮</button>
{% endblock %}
<!-- footer 不写 = 使用父模板的默认 footer -->
```

【为什么？】
模板继承解决的是"页面骨架复用"问题。一个网站通常有统一的导航栏、侧边栏、页脚——如果每个页面都复制粘贴这些 HTML，维护成本是灾难级的（改一个导航栏要改 50 个文件）。

继承的设计类似 Python 的类继承：
- 父模板 = 基类（定义骨架 + 默认实现）
- `{% block %}` = 可重写的方法
- `{% extends %}` = 继承声明
- 子模板不重写的 block = 继承父模板的默认内容

三层复用策略：
1. `{% include %}` → 复用小组件（导航条、按钮）
2. `{% extends %}` + `{% block %}` → 复用页面骨架（布局、页脚）
3. 宏（macro）→ 复用带参数的 HTML 片段（类似函数，进阶内容）

【必须掌握】
- 父模板用 `{% block 名称 %}{% endblock %}` 定义可重写区域
- 子模板用 `{% extends "父模板名" %}` 声明继承
- `{% extends %}` 必须在子模板的第一行
- 子模板只写需要重写的 block，不写的使用父模板默认值
- block 名称在同一模板中不能重复

【企业场景】
搭建测试辅助工具时的页面组织：

```
templates/
├── base.html          # 骨架：导航栏 + 侧边栏 + 页脚
├── test_list.html     # 继承 base，重写 content → 测试用例列表
├── test_detail.html   # 继承 base，重写 content → 单条用例详情
└── report.html        # 继承 base，重写 content → 测试报告
```

改导航栏只需改 `base.html`，所有页面自动更新。

【面试考察】
面试官："Flask 中 `{% extends %}` 和 `{% include %}` 有什么区别？各自的使用场景是什么？"

参考回答框架：
1. `{% extends %}` = 模板继承，子模板继承父模板的骨架，可以重写 block 区域
2. `{% include %}` = 模板导入，把另一个模板完整嵌入到当前位置
3. extends 用于页面级复用（不同页面用同一布局），include 用于组件级复用（导航条、页脚等小组件）
4. extends 必须在第一行，一个模板只能 extends 一个父模板

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| `{% extends %}` 不放在第一行 | 必须放在模板文件的第一行（注释也不行） |
| block 名称重复（如两个 `{% block content %}`） | 每个 block 名称唯一 |
| 子模板写了父模板不存在的 block | 会被忽略（不报错），但也不会有任何输出 |
| `{% extends %}` 后写 HTML（不在任何 block 内） | extends 后不在 block 内的内容会被忽略 |

【扩展知识】
`{{ super() }}` — 在子模板的 block 中调用父模板的同名 block 内容：
```html
{% block footer %}
    {{ super() }}  <!-- 先输出父模板的 footer 内容 -->
    <p>额外的子模板 footer 内容</p>
{% endblock %}
```
这在"追加内容"而非"完全替换"时很有用。

【我的理解】
> （创建 base.html（包含 title + content + footer 三个 block）和两个子模板 page1.html、page2.html。page1 只重写 content，page2 重写 title 和 content 并用 `{{ super() }}` 在 footer 中追加内容。启动 Flask，分别访问两个页面，用"查看网页源代码"确认继承关系。footer 处的 `super()` 效果是怎样的？）

---

### 知识点 7：模板导入 — include

【课程原话/定义】
`{% include %}` 将另一个模板的内容完整加载到当前位置。和继承不同——include 不涉及 block 重写，就是直接"复制粘贴"。

```html
{% include "top.html" %}
```

**top.html：**
```html
<a>首页</a>
<a>关于</a>
```

**son.html 中导入：**
```html
{% extends "layout.html" %}
{% include "top.html" %}   <!-- 导航条直接嵌入 -->

{% block content %}
<h1>子模板</h1>
{% endblock %}
```

【为什么？】
include 解决的是"组件级复用"。一个导航条可能在 20 个页面出现——把导航条提取为 `nav.html`，每个页面 `{% include "nav.html" %}` 即可。改导航条时只改一个文件。

include 和 extends 的分工：
- extends → "我是某种页面的变体"（页面级）
- include → "这个组件放在这里"（组件级）

可以同时使用：先 extends 骨架，再在某个 block 里 include 组件。

【必须掌握】
- `{% include "模板名" %}` 直接嵌入
- include 可以放在模板任意位置（不要求和 extends 一样在第一行）
- 导入列表：`{% include ["a.html", "b.html"] %}` — 找第一个存在的
- 忽略报错：`{% include "missing.html" ignore missing %}` — 文件不存在时不报错

【企业场景】
测试报告模板的组件化拆分：

```
templates/
├── base.html            # 骨架
├── nav.html             # 导航栏（include）
├── sidebar.html         # 侧边栏（include）
├── test_report.html     # 测试报告页
└── test_detail.html     # 用例详情页
```

`test_report.html` 和 `test_detail.html` 都 include `nav.html` 和 `sidebar.html`，保持一致性。

【面试考察】
面试官："`{% include ['a.html', 'b.html'] %}` 的行为是什么？如果两个文件都不存在呢？"

参考回答框架：
1. Jinja2 按列表顺序依次查找文件
2. 第一个被找到的模板被加载，后面的忽略
3. 如果都没找到，默认抛出 `TemplateNotFound` 异常
4. 可以加 `ignore missing` 静默跳过：`{% include ['a.html', 'b.html'] ignore missing %}`

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| include 的文件找不到导致整个页面 500 | 加 `ignore missing` 或确保文件存在 |
| 认为 include 会继承父模板的变量 | include 的模板可以访问当前上下文的所有变量 |
| extends 和 include 功能混淆 | extends = 继承骨架（1对1），include = 嵌入组件（1对多） |

【我的理解】
> （创建 header.html（导航条）、footer.html（页脚）、base.html（骨架）。在 base.html 中用 include 导入 header 和 footer。再创建一个 index.html 继承 base.html，重写 content block。最终效果：index.html 渲染时，header 来自 include，footer 也来自 include，content 由自己定义。用"查看网页源代码"确认最终 HTML 的拼接结果。）

---

## 五、全部语法速查

### 知识点 8：Jinja2 模板语法汇总

【课程原话/定义】
Jinja2 的全部核心语法：

| 语法 | 用途 | 示例 |
|------|------|------|
| `{{ var }}` | 输出变量 | `{{ name }}` |
| `{{ obj.prop }}` | 输出属性/键值 | `{{ person.age }}` |
| `{% if %}...{% endif %}` | 条件判断 | `{% if x > 0 %}正数{% endif %}` |
| `{% for %}...{% endfor %}` | 循环遍历 | `{% for item in list %}{{ item }}{% endfor %}` |
| `{% block %}...{% endblock %}` | 定义可重写区域 | `{% block content %}{% endblock %}` |
| `{% extends "file" %}` | 继承父模板 | `{% extends "base.html" %}` |
| `{% include "file" %}` | 导入子模板 | `{% include "nav.html" %}` |
| `{# 注释 #}` | 模板注释（不渲染到 HTML） | `{# 这是注释 #}` |
| `{{ loop.index }}` | 循环内获取序号 | `{{ loop.index }}` |

【为什么？】
这张表是 Jinja2 的"操作手册"。模板中 95% 的需求都可以用这 9 种语法组合解决。复杂的逻辑不应该放在模板里——如果你的模板有很多层嵌套的 `{% if %}` + `{% for %}`，说明数据预处理应该在视图函数中完成。

【必须掌握】
- 以上全部语法
- 模板注释 `{# #}` 和 HTML 注释 `<!-- -->` 的区别：前者不渲染到 HTML，后者会
- 模板语法不能混用：`{{ }}` 里不能写 `{% %}`，反之亦然

【企业场景】
掌握 Jinja2 语法的投入产出比极高——不仅 Flask 用，以下工具都用类似语法：
- Ansible（配置管理）：`.j2` 模板文件
- SaltStack：Jinja 模板
- Airflow：DAG 模板
- dbt（数据转换）：Jinja 宏
- Django：虽然用自家模板引擎，但语法 90% 相似

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| HTML 注释 `<!-- -->` 和 Jinja2 注释 `{# #}` 混用 | `<!-- -->` 会出现在最终 HTML 中，`{# #}` 不会 |
| 在 `{{ }}` 里写 `{% %}` | 它们不能嵌套——各自独立使用 |
| 模板里写太多逻辑 | 复杂计算放视图函数，模板只展示 |

【我的理解】
> （不看书，凭记忆画出 Jinja2 全部语法的速查表。然后对照上面的表格检查，缺了哪个？缺的那个就是你最容易忘的，重点练习。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 模板渲染 | Jinja2 引擎、`templates/` 目录、`render_template()` | ★★★★☆ |
| 变量代码块 | `{{ }}` 输出变量、数据传递、`.` 取值 | ★★★★★ |
| 控制代码块 | `{% %}` 逻辑控制、if/for/block | ★★★★★ |
| 判断语法 | `{% if %}...{% elif %}...{% else %}...{% endif %}` | ★★★★☆ |
| 循环语法 | `{% for %}...{% endfor %}`、`loop.index` | ★★★★☆ |
| 模板继承 | `{% extends %}` + `{% block %}`、`{{ super() }}` | ★★★★★ |
| 模板导入 | `{% include %}`、导入列表、`ignore missing` | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch03-请求与响应处理]] — `render_template()` 基础
- [[Ch02-Flask入门]] — Flask 路由和视图函数
