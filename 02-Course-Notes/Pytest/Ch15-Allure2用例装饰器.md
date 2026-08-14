---
tags: [课程笔记, Pytest, Allure]
course: "Pytest"
chapter: "Ch15-Allure2用例装饰器"
created: 2026-07-28
status: draft
---

# Ch15 - Allure2 用例装饰器

## 课程来源
- 学习日期：

---

## 一、装饰器速览总表

| 装饰器 | 用途 | 粒度 |
|--------|------|------|
| `@allure.epic()` | 项目/需求 | 类 |
| `@allure.feature()` | 功能模块 | 类 |
| `@allure.story()` | 子功能/场景 | 方法 |
| `@allure.title()` | 用例标题（支持中文） | 方法 |
| `@allure.step()` | 测试步骤 | 方法/内部 |
| `@allure.link()` | 自定义链接 | 方法 |
| `@allure.testcase()` | 用例管理系统链接 | 方法 |
| `@allure.issue()` | Bug 管理系统链接 | 方法 |
| `@allure.description()` | 文本描述 | 方法 |
| `@allure.description_html()` | HTML 描述 | 方法 |
| `@allure.severity()` | 严重级别 | 方法/类 |

---

## 二、用例标题 — @allure.title

### 知识点1：用例标题

【课程原话/定义】
`@allure.title("自定义标题")` 可以为用例添加便于阅读的标题，支持中文。支持参数化动态生成标题。

【为什么？】
> 为什么不能直接用函数名当标题？企业里谁会看不带标题的 Allure 报告？

【必须掌握】

```python
# 方式1：固定标题
@allure.title("登录成功用例")
def test_login_success():
    pass

# 方式2：参数化动态标题
@allure.title("参数化：用户名={username}，密码={password}")
@pytest.mark.parametrize("username,password", [("admin","123"),("user","456")])
def test_login(username, password):
    pass

# 方式3：运行时动态修改
@allure.title("原始标题")
def test_dynamic():
    assert True
    allure.dynamic.title("运行时修改后的标题")
```

【企业场景】
> 你用 Pytest 参数化跑 20 组登录数据，如果不用动态标题，报告里 20 条结果都叫 `test_login`，根本分不清哪组数据过了哪组挂了。加了 `@allure.title("用户名={username}")` 后，一眼就能看出是哪个账户的问题。

【面试考察】
> 面试官：Allure 怎么给参数化用例生成不同的标题？
> 
> 参考回答框架：用占位符 `{参数名}` 在 title 中引用参数化变量，报告会自动替换。

【易错点】

| 错误写法 | 为什么错 |
|----------|----------|
| `@allure.title("用例" + username)` | 装饰器在函数定义时执行，此时 `username` 还没值 |
| 不用占位符直接写死标题 | 参数化时所有用例标题一样，失去意义 |

【我的理解】
> （请用自己的话写一个参数化用例的例子，说明占位符是怎么工作的）

---

## 三、用例步骤 — @allure.step

### 知识点2：测试步骤

【课程原话/定义】
通过 `@allure.step()` 装饰器或 `with allure.step():` 上下文管理器添加测试步骤。

【为什么？】
> 一个测试方法里有 5 个操作，不加步骤的话，失败了你知道是哪一步吗？

【必须掌握】

```python
# 方式1：装饰器
@allure.step("登录：用户名={user}")
def step_login(user, pwd):
    print(f"输入用户名{user}")

# 方式2：with 语句块
def test_search():
    with allure.step("打开首页"):
        print("navigate to home")
    with allure.step("输入搜索词"):
        print("type keyword")
    with allure.step("点击搜索"):
        print("click search")
    with allure.step("断言结果"):
        assert True
```

| 方式 | 适用场景 |
|------|----------|
| 装饰器 `@allure.step` | 可复用的步骤函数（多个用例共用） |
| `with allure.step()` | 一次性步骤，写在用例方法内部 |

【企业场景】
> 你的电商项目里，每个用例都需要"登录→加购→结算"这三个步骤。你把它们封装成 `step_login()` / `step_add_to_cart()` / `step_checkout()` 三个带 `@allure.step` 的函数，所有用例复用。报告里每个用例都有完整的三步流程，失败时精确定位到"加购"这一步的接口超时。

【面试考察】
> 面试官：Allure 报告里怎么展示测试步骤？失败了能定位到第几步吗？
> 
> 参考回答框架：用 @allure.step + with allure.step，报告中每个步骤独立展示，失败步骤会标红高亮。

【易错点】

| 易混淆 | 区别 |
|--------|------|
| `@allure.step`（装饰器） | 定义独立步骤函数，可复用 |
| `with allure.step()` | 在用例方法内定义内联步骤 |
| 普通 print() | 在报告里只是一段日志，不是结构化步骤 |

【我的理解】
> （请自己写一个包含 3 个步骤的测试用例，分别用装饰器和 with 方式，说明你选哪种为什么）

---

## 四、用例链接 — @allure.link / @allure.testcase / @allure.issue

### 知识点3：链接管理

【课程原话/定义】
三种链接装饰器，分别用于：自定义链接、关联用例管理系统、关联 Bug 管理系统。

【为什么？】
> 测试报告里为什么要放链接？测试人员和开发是怎么通过报告协作的？

【必须掌握】

```python
# 普通链接
@allure.link('https://wiki.company.com/login-spec', name='登录需求文档')

# 用例管理系统链接（TAPD/Jira/禅道）
@allure.testcase('https://tapd.cn/project/123/bug/456', name='TC-LOGIN-001')

# Bug 管理系统链接（带 Bug 图标）
@allure.issue('BUG-789', name='登录页验证码不刷新')
```

| 装饰器 | 图标 | 用途 |
|--------|------|------|
| `@allure.link()` | 普通链接图标 | 需求文档、Wiki、设计稿 |
| `@allure.testcase()` | 用例图标 | 测试管理平台用例链接 |
| `@allure.issue()` | Bug 图标 | 缺陷管理平台 Bug 链接 |

【企业场景】
> 你发现 `test_order_refund` 挂了，报告里点击 `@allure.issue('BUG-234')` 直接跳转到 TAPD 的 Bug 详情页，看到开发备注"已修复，待部署"。你不用再到处问"这个 Bug 修了没"，链接已经告诉你了。

【面试考察】
> 面试官：`@allure.link`、`@allure.testcase`、`@allure.issue` 有什么区别？你们实际怎么用的？
> 
> 参考回答框架：link 是通用链接，testcase 关联测试平台用例，issue 关联缺陷平台 Bug。我们项目规范是：每个用例必须加 testcase 链接指向 TAPD 用例，发现 Bug 时加 issue 链接。

【我的理解】
> （请用自己的话说明这三种链接的区别和各自的使用场景）

---

## 五、用例分类 — @allure.epic / @allure.feature / @allure.story

### 知识点4：三层分类体系

【课程原话/定义】
epic（史诗/项目）→ feature（功能模块）→ story（用户故事/场景），三层父子关系。

【为什么？】
> 2000 条用例如果不分类，怎么快速找到"订单模块的退款场景"？

【必须掌握】

```python
@allure.epic("电商系统")
@allure.feature("订单模块")
class TestOrder:

    @allure.story("创建订单")
    @allure.title("正常创建订单")
    def test_create_order(self):
        pass

    @allure.story("取消订单")
    @allure.title("超时自动取消")
    def test_cancel_order(self):
        pass
```

层级关系：**epic > feature > story > title**

| 装饰器 | 粒度 | 通常加在 | 类比 |
|--------|------|----------|------|
| `@allure.epic()` | 项目级别 | 类 | 一个产品 |
| `@allure.feature()` | 模块级别 | 类 | 一个菜单 |
| `@allure.story()` | 场景级别 | 方法 | 菜单里的一个按钮功能 |

【企业场景】
> 你的项目有三条产品线：用户端、商家端、管理后台。你给每个产品线设置一个 epic。商家端下面有"商品管理"、"订单管理"、"数据报表"三个 feature。"订单管理"下面有"创建订单"、"取消订单"、"退款"、"导出"等多个 story。PM 想看"商家端退款相关用例"，直接点 epic=商家端 → feature=订单管理 → story=退款，5 秒定位。

【面试考察】
> 面试官：Allure 的 epic、feature、story 有什么区别？怎么按分类执行用例？
> 
> 参考回答框架：先解释三层层级，然后给出筛选命令。
> ```
> pytest --allure-epics=电商系统 --allure-features=订单模块
> pytest --allure-stories=退款,取消订单
> ```
> **注意：多个条件取并集**，即 feature + story 同时指定时会跑所有满足任一条件的用例。

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| story 放在类上 | story 粒度最细，放在方法上 |
| 混淆 feature 和 story 的粒度 | feature = 功能模块（粗），story = 子场景（细） |
| 以为多条件筛选是交集 | epic + feature + story 筛选是**并集** |

【我的理解】
> （请画一个你们熟悉的 App/网站的三个功能模块，每个模块 2 个场景，标注 epic/feature/story 分别是什么）

---

## 六、用例描述 — @allure.description

### 知识点5：用例描述

【课程原话/定义】
为测试用例添加详细描述信息，支持纯文本、HTML 格式、文档注释、动态修改四种方式。

【为什么？】
> 复杂用例怎么在报告里体现前置条件和业务背景？

【必须掌握】

```python
# 方式1：装饰器传字符串
@allure.description("这是用例描述，支持换行符<br/>第二行")

# 方式2：HTML 描述
@allure.description_html("""
<h3>用例说明</h3>
<table><tr><td>前置</td><td>已登录</td></tr></table>
""")

# 方式3：文档注释（docstring）
def test_example():
    """
    这是文档注释
    会自动作为描述展示在报告中
    """
    pass

# 方式4：动态修改
@allure.description("原始描述")
def test_dynamic():
    assert True
    allure.dynamic.description("最终描述")
```

【企业场景】
> 你有一个复杂的退款流程用例：用户下单→支付→申请退款→商家审核→退款到账，涉及 5 个接口。你在 description 里写了前置条件、数据准备、预期结果。新人看了报告里的描述就懂这个用例做了什么，不用找你口述。

【面试考察】
> 面试官：Allure 添加用例描述有几种方式？哪种最常用？
> 
> 参考回答框架：四种。最常用的是装饰器传字符串（灵活）+ 文档注释（最简单）。

【易错点】

| 错误 | 正确 |
|------|------|
| 纯文本描述不加 `<br/>` 换行 | `@allure.description` 纯文本需要用 `<br/>` 换行 |
| 文档注释直接放多行 | docstring 会自动保留格式，不需要 `<br/>` |

【我的理解】
> （请写一个包含前置条件、步骤、预期结果的描述，尝试用 HTML 表格格式）

---

## 七、用例优先级 — @allure.severity

### 知识点6：严重级别

【课程原话/定义】
五个级别：Blocker > Critical > Normal > Minor > Trivial。类上设置的级别对所有方法生效，方法上可以覆盖。

【为什么？】
> 冒烟测试跑 2000 条还是 20 条？如何让 CI 只跑最重要的用例？

【必须掌握】

```python
@allure.severity(allure.severity_level.BLOCKER)    # 阻塞
@allure.severity(allure.severity_level.CRITICAL)   # 严重
@allure.severity(allure.severity_level.NORMAL)     # 正常（默认）
@allure.severity(allure.severity_level.MINOR)      # 次要
@allure.severity(allure.severity_level.TRIVIAL)    # 轻微
```

| 级别 | 含义 | 典型场景 |
|------|------|----------|
| Blocker | 阻塞 | 登录失败、支付崩溃 |
| Critical | 严重 | 核心功能异常但可绕过 |
| Normal | 正常 | 常规功能验证（默认） |
| Minor | 次要 | 非核心功能的小问题 |
| Trivial | 轻微 | UI 文案、颜色等不影响功能的 |

运行时筛选：
```bash
pytest --allure-severities blocker,critical    # 只跑高优先级
```

【企业场景】
> 每次提测前，CI 先跑 `--allure-severities blocker,critical`，20 条冒烟用例 3 分钟跑完。冒烟过了再跑全量 500 条。如果冒烟不过直接打回开发，整个团队不用等 30 分钟全量结果。

【面试考察】
> 面试官：怎么在 CI 里只跑高优先级用例？
> 
> 参考回答框架：给用例标 severity，命令行 `--allure-severities blocker,critical` 筛选。可以配置两个 Job：冒烟 Job 只跑 blocker+critical，全量 Job 跑全部。

【易错点】

| 错误 | 正确 |
|------|------|
| 不标 severity | 默认为 Normal，无法区分优先级 |
| 所有用例都标 Blocker | 失去筛选意义 |
| 类上标了，方法上忘记特殊用例需要覆盖 | 方法上的 severity 会覆盖类上的 |

【我的理解】
> （请给以下场景分配 severity 级别：1) 用户无法登录 2) 收藏功能图标颜色不对 3) 支付完成后金额显示错误 4) 个人资料页生日选 2月30日仍可保存）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| @allure.title | 中文化标题 + 参数化动态标题 | ⭐⭐⭐⭐ |
| @allure.step | 装饰器 vs with 两种方式 | ⭐⭐⭐⭐⭐ |
| 链接三部曲 | link / testcase / issue 区别 | ⭐⭐⭐⭐ |
| 三层分类 | epic → feature → story 层级 | ⭐⭐⭐⭐⭐ |
| 用例描述 | 四种添加方式 | ⭐⭐⭐ |
| 严重级别 | 五个级别 + 筛选执行 | ⭐⭐⭐⭐⭐ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch14-Allure2安装与报告生成]]
- [[Ch16-Allure2标签与失败重试]]
