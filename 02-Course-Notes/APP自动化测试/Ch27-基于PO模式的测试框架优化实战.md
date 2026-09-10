---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - PageObject
  - PO模式
  - 实战
course: APP自动化测试
chapter: Ch27-基于PO模式的测试框架优化实战
created: 2026-09-10
status: draft
---

# Ch27 - 基于 Page Object 模式的测试框架优化实战

## 课程来源
- 学习日期：

> 本章是 APP 自动化课程的第一个"框架实战收口章"：把 Ch24（留证）、Ch25（容错）、Ch26（架构）全部落到一个真实的 PO 框架里，用雪球 App 搜索功能走通"分层封装 → 数据驱动 → 黑名单 → Allure 报告"的完整闭环。被测应用：雪球 App（应用商店直接安装）。

---

## 一、PO 模式六大原则

### 知识点 1：属性意义 + 方法意义

【课程原话/定义】

> 📷 【截图占位】PO 模式六大原则 UML 图

**属性意义**：

1. 不要暴露页面内部的元素给外部。
2. 不需要建模 UI 内的所有元素。

**方法意义**：

1. 用公共方法代表 UI 所提供的功能。
2. 方法应该返回其他 PageObject 或者返回用于断言的数据。
3. 同样的行为不同的结果可以建模为不同的方法。
4. 不要在方法内加断言。

【为什么？】

1. "不暴露元素"：外部只调 `goto_search_page()`，不知道、也不该知道里面定位器长什么样——定位器变化只改页面类内部。
2. "方法返回其他 PageObject"：点击搜索框跳转到搜索页，方法就 `return SearchPage(driver)`——这实现了**链式调用**（`main.goto_search_page().input(...).get_result()`）。
3. "不在方法内加断言"：断言留给用例层，页面方法只负责"做动作/取数据"，职责单一，否则页面类既当运动员又当裁判。

【必须掌握】

- 六大原则：属性 2 条 + 方法 4 条
- 两条最关键的：方法返回 PageObject（链式跳转）、方法内不加断言

【企业场景】

你在企业里，PO 写得好不好就看这六条：页面类只暴露功能方法、定位器私有；方法链式返回下一页；断言都在用例层。这样定位器改了只动一个页面类，断言逻辑和页面逻辑不耦合。

【面试考察】

面试官："PO 模式有哪些原则？为什么方法内不要加断言？"

参考回答框架：属性上不暴露内部元素、不建模所有元素；方法上用公共方法代表功能、返回 PageObject 或断言数据、不同结果建不同方法、方法内不加断言。断言放用例层，页面类只负责操作和取数据，职责单一、易维护。

【易错点】

| 误区 | 纠正 |
|------|------|
| 页面类里写 assert | 断言属于用例层，页面方法只"做动作/返回数据" |
| 方法不返回 PageObject | 跳转类方法要 return 下一个 PageObject，才能链式调用 |
| 建模页面所有元素 | 只建模"用得到"的元素，不是把整个页面控件都定义一遍 |

【我的理解】

> （"方法应该返回其他 PageObject"这条原则，如何让测试用例能写出 `main.goto_search_page().input(x).get_result(x)` 这种链式调用？如果方法返回 None 会怎样？）

---

## 二、项目分层与启动封装

### 知识点 2：五层结构 + XueqiuApp 启动类

【课程原话/定义】

> 📷 【截图占位】测试框架分层 UML 图

五层：**基础层**（底层工具二次封装，如元素查找）、**公共业务层**（app 启动配置）、**页面层**（每个页面/功能模块一个类，含元素和操作）、**测试用例层**（pytest 写用例，调业务层方法）、**公共方法层**（日志、数据读取等工具函数）。

app 启动封装（公共业务层）：

```python
class XueqiuApp(BasePage):
    def start(self):
        caps = {
            "platformName": "Android",
            "appium:automationName": "uiautomator2",
            "appium:deviceName": "emulator-5554",
            "appium:appPackage": "com.xueqiu.android",
            "appium:appActivity": ".view.WelcomeActivityAlias",
            "appium:noReset": True,
            "appium:forceAppLaunch": True,
            "appium:skipDeviceInitialization": True
        }
        self.driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=UiAutomator2Options().load_capabilities(caps)
        )
        self.driver.implicitly_wait(15)
        return self

    def stop(self):
        self.driver.quit()

    def goto_main(self):
        from auto_test_app.xueqiu_app_po.page.main_page import MainPage
        return MainPage(self.driver)
```

【为什么？】

1. 启动/关闭 App 是"公共业务"——所有用例都要做，抽到 XueqiuApp.start()/stop()，用例只需 `self.app.start().goto_main()`。
2. `start()` 返回 self（链式）、`goto_main()` 返回 MainPage，让"启动 → 进首页"一行写完，呼应 Ch12 应用控制 + Ch11 capability。
3. 页面类继承 XueqiuApp（或 BasePage），共享 driver 和 find 封装。

【必须掌握】

- 五层结构 + 各自职责
- start（返回 self）/ stop / goto_main（返回 MainPage）三个方法

【企业场景】

你在企业里，XueqiuApp 就是"被测应用"的入口封装：换被测 App 只改 start() 里的 capability（appPackage/appActivity），页面类和用例零改动。这是"应用级复用"的体现。

【面试考察】

面试官："为什么把 app 启动封装成独立类？start 返回 self 有什么好处？"

参考回答框架：启动是公共业务，封装避免每个用例重复写 capability；start 返回 self 支持链式调用（`app.start().goto_main()`），goto_main 返回 MainPage 进入首页对象。

【易错点】

| 误区 | 纠正 |
|------|------|
| 每个用例重复写 capability | 抽到 XueqiuApp.start()，一处定义处处复用 |
| goto_main 不返回 MainPage | 要 return MainPage(driver)，才能链式进入首页 |

【我的理解】

> （start() 返回 self、goto_main() 返回 MainPage——这两个返回值分别支撑了什么样的链式写法？为什么设计成"返回对象"而不是"返回 None"？）

---

## 三、BasePage 与页面封装

### 知识点 3：BasePage + Main/Search/SearchResult 三页链式跳转

【课程原话/定义】

BasePage 封装：

```python
class BasePage:
    def __init__(self, driver: WebDriver=None):
        self.driver = driver

    def find_ele(self, by, value):
        return self.driver.find_element(by, value)

    def find_eles(self, by, value):
        return self.driver.find_elements(by, value)
```

页面封装（首页 → 搜索页 → 结果页 链式跳转）：

```python
class MainPage(XueqiuApp):
    _SEARCH_BAR = AppiumBy.XPATH, "//*[@resource-id='com.xueqiu.android:id/tv_banner']"
    def goto_search_page(self):
        self.find_ele(*self._SEARCH_BAR).click()
        return SearchPage(self.driver)

class SearchPage(XueqiuApp):
    _SEARCH_BAR = AppiumBy.ID, "com.xueqiu.android:id/search_input_text"
    _FIRST_SEARCH_RESULT = AppiumBy.XPATH, "//*[@resource-id='com.xueqiu.android:id/name']"
    def goto_search_result_page(self, search_text):
        self.find_ele(*self._SEARCH_BAR).send_keys(search_text)
        self.find_eles(*self._FIRST_SEARCH_RESULT)[0].click()
        return SearchResultPage(self.driver)

class SearchResultPage(XueqiuApp):
    def get_search_result(self, search_text):
        results = self.find_eles(AppiumBy.XPATH, f"//*[@text='{search_text}']")
        return [r.text for r in results] if results else []
```

【为什么？】

1. 定位器用 `_SEARCH_BAR = AppiumBy.ID, "..."` 这种**类属性元组**存，`find_ele(*self._SEARCH_BAR)` 解包传参——定位器私有、集中在页面类顶部，一眼看全。
2. 每个页面方法"做完动作就 return 下一个页面对象"，三个页面串成一条链：首页点搜索 → 搜索页输入 → 结果页取数据。
3. get_search_result 返回"断言用的数据"（文本列表），而不是在页面里 assert——呼应 PO 原则"方法返回用于断言的数据"。

【必须掌握】

- 定位器用类属性元组存 + `*` 解包
- 三页链式跳转：goto_search_page → goto_search_result_page → get_search_result
- get_search_result 返回数据不断言

【企业场景】

你在企业里，页面类的定位器集中顶部、方法语义化（goto_xxx/get_xxx），用例层读起来像"业务步骤"而不是"找元素代码"。定位器漂移了只改对应页面类顶部的 `_XXX` 常量。

【面试考察】

面试官："PO 框架里定位器怎么管理？页面之间怎么跳转？"

参考回答框架：定位器用类属性元组存（如 `_SEARCH_BAR = AppiumBy.ID, "..."`），集中页面类顶部；页面跳转方法返回下一个 PageObject，实现链式调用，如 `goto_search_page().goto_search_result_page(x).get_search_result(x)`。

【易错点】

| 误区 | 纠正 |
|------|------|
| 定位器散落在方法里 | 用类属性元组集中顶部，find_ele(*self._XXX) 解包使用 |
| 跳转方法不返回下一页对象 | 要 return 下一个 PageObject，否则链式断掉 |
| 页面方法里 assert | get_search_result 只返回数据列表，断言留给用例层 |

【我的理解】

> （`_SEARCH_BAR = AppiumBy.ID, "..."` 为什么要设计成"元组"？`find_ele(*self._SEARCH_BAR)` 里的 `*` 起什么作用？）

---

## 四、编写测试用例

### 知识点 4：链式调用 + setup/teardown

【课程原话/定义】

```python
class TestSearch:
    def setup_method(self):
        self.app = XueqiuApp()
        self.main = self.app.start().goto_main()

    def teardown_method(self):
        self.app.stop()

    def test_search_stock(self):
        search_text = "阿里巴巴"
        result = self.main.goto_search_page().\
            goto_search_result_page(search_text).\
            get_search_result(search_text)
        assert search_text in result
```

【为什么？】

1. 用例层只做三件事：setup 启动进首页、调用业务链、assert 结果——业务逻辑全在页面层，用例极简。
2. `setup_method`/`teardown_method`（方法级）每个用例各建一个干净 driver，避免用例间状态污染（呼应 Ch12 fixture 级别）。
3. 链式调用让一个测试场景浓缩成一行"首页点搜索 → 输入 → 取结果"，读起来就是测试步骤本身。

【必须掌握】

- 用例三件套：setup 启动 / 调用链式方法 / assert
- setup_method / teardown_method 方法级 fixture

【企业场景】

你在企业里，测试用例就是"业务步骤的可读化描述"，测试同学写用例不碰定位器、不碰 driver 细节，只调页面方法。这是 PO 模式"让用例表达业务意图"的最终价值。

【面试考察】

面试官："PO 模式下，一个测试用例应该长什么样？"

参考回答框架：setup 里启动 App 进首页，测试体里用链式调用表达业务步骤（`goto_search_page().goto_search_result_page(x).get_search_result(x)`），最后 assert 结果。用例层不写定位器、不写 driver 操作。

【易错点】

| 误区 | 纠正 |
|------|------|
| 用例里直接 find_element | 用例层只调页面方法，find 逻辑在 BasePage/页面层 |
| 用 setup_class 而不是 setup_method | 搜索场景用方法级 fixture，每个用例独立 driver，避免污染 |

【我的理解】

> （这条用例 `test_search_stock` 里没有一行 find_element、没有一行 capability——这些细节都去哪了？这体现了 PO 的什么价值？）

---

## 五、优化框架（数据驱动 + 黑名单 + 报告）

### 知识点 5：三个优化点落地

【课程原话/定义】

**数据驱动**：股票名抽到 yaml（`datas/stock_name.yaml` 存"阿里巴巴/平安银行"），用 parametrize 注入：

```python
@pytest.mark.parametrize("search_text",
    Utils.get_yaml_data(Utils.get_file_path("./datas/stock_name.yaml")))
def test_search_stock(self, search_text):
    result = self.main.goto_search_page().\
        input_search_key(search_text).\
        get_search_result(search_text)
    assert search_text in result
```

**黑名单处理**：装饰器 black_wrapper 挂到 find_ele/find_eles，异常时截图 + page_source 进 allure、遍历黑名单点掉弹窗、重试。

**测试报告**：feature/story/title 描述 + 生成报告：

```python
@allure.feature("雪球搜索")
class TestSearch:
    @allure.story("雪球搜索股票")
    @allure.title("参数化搜索股票名称 {search_text}")
    @pytest.mark.parametrize(...)
    def test_search_stock(self, search_text):
        ...
```

```bash
pytest --alluredir=./results --clean-alluredir
allure serve ./results
allure generate --clean ./results -o ./report/html
```

【为什么？】

1. 三个优化点正好对应 Ch26 的"框架层"能力：数据驱动（数据与逻辑分离）、黑名单（异常弹框容错）、Allure（报告留证）——PO 是骨架，这三项是血肉。
2. 数据驱动让"搜索阿里巴巴"和"搜索平安银行"共用一条用例逻辑，加股票只加 yaml 一行。
3. 黑名单 + allure.attach 让"用例失败"变成"报告里能点开看截图和源码的完整现场"——Ch24/Ch25/Ch26 全串起来了。

【必须掌握】

- 数据驱动：yaml + parametrize（加数据不加代码）
- 黑名单：black_wrapper 挂 find 方法
- Allure：feature/story/title + 三条命令

【企业场景】

你在企业里，这就是一个完整 APP 自动化框架的雏形：PO 分层 + 数据驱动 + 黑名单容错 + Allure 报告。往后扩展就是加页面类、加 yaml 数据、加用例，框架骨架不变——这是"可扩展、可维护"的标志。

【面试考察】

面试官："完整描述你的 APP 自动化框架是怎么搭的？"

参考回答框架：PO 模式分层（base 封装 find、page 页面对象、cases 用例、datas 数据、utils 工具）+ 数据驱动（yaml + parametrize）+ 黑名单异常处理（装饰器 + 弹窗点击重试）+ 失败留证（日志/截图/page_source 进 Allure 报告）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 源码黑名单 `//*[@text=['取消']` 多一个 `[` | 应为 `//*[@text='取消']`，`@text=` 后面直接跟 `'`，不能带 `[` |
| 只搭 PO 不做数据驱动/黑名单/报告 | PO 是骨架，数据驱动 + 容错 + 报告是让它"可用"的血肉 |
| 生成报告命令参数写错 | `allure generate --clean ./results -o ./report/html`（结果→输出），别混参数 |

【我的理解】

> （这个框架里，PO 分层、数据驱动、黑名单、Allure 报告四者分别解决了什么痛点？缺了其中任意一个，框架会退化为什么状态？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| PO 六大原则 | 属性 2 条 + 方法 4 条 | ★★★★★ |
| 分层与启动 | 五层结构 + XueqiuApp | ★★★★★ |
| 页面封装 | BasePage + 三页链式跳转 | ★★★★★ |
| 用例编写 | 链式调用 + 方法级 fixture | ★★★★★ |
| 优化三点 | 数据驱动 + 黑名单 + Allure | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch24-自动化关键数据记录]]（失败留证三件套，进 Allure 报告）
- [[Ch25-app弹窗异常处理]]（黑名单 + 装饰器，挂到 find 方法）
- [[Ch26-自动化测试架构优化]]（四层结构 + 数据驱动 + 报告）
- [[Ch19-雪球app搜索功能实战]]（雪球搜索的"裸脚本"版，本章是其 PO 化）
- [[Ch11-Capability配置参数解析]]（start() 里的 capability）
- [[Pytest/README|Pytest]]（parametrize 参数化）
