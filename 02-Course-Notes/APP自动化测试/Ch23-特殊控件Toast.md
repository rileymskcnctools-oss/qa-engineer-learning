---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - Toast
  - 特殊控件
course: APP自动化测试
chapter: Ch23-特殊控件Toast
created: 2026-09-10
status: draft
---

# Ch23 - 特殊控件 Toast

## 课程来源
- 学习日期：

> 本章展开 [[Ch18-自动化测试定位策略]] 知识点 6 里"特殊控件"提到但没展开的 Toast。Ch18 只给了一句"page_source + xpath"，本章补全：Toast 的特点、定位原理、以及 API Demo 的完整实战用例。

---

## 一、Toast 是什么

### 知识点 1：Toast 的特点

【课程原话/定义】

Toast 是一种轻量级消息提示，常以小弹框形式出现，一般 1~2 秒自动消失，可出现在屏幕上/中/下任意位置。

特点：

1. **无法被点击**：不同于 Dialog，永远不会获得焦点。
2. **显示时间有限**：按用户设置的显示时间自动消失。
3. **系统级控件**：属于系统 settings。
4. 设计思想：尽可能不引人注意，同时向用户显示信息。

> 📷 【截图占位】Toast 消息框类型示例

【为什么？】

1. Toast 的"短暂 + 无焦点"决定了它**不能用常规 find_element 稳定定位**——还没等你定位它就消失了，所以要用"等待 + 抓文本"的组合拳。
2. Toast 是系统级控件，不属于被测 App 自身 UI，所以抓取要借 uiautomator 底层把它放进控件树。
3. 理解"无焦点"才能理解为什么点不到它、为什么它不阻塞操作。

【必须掌握】

- Toast 四大特点：无法点击 / 限时显示 / 系统级 / 轻量不打扰
- Toast 定位难的根本原因：短暂显示

【企业场景】

你在企业里，"操作成功""已保存""登录失败"这类一次性提示基本都是 Toast。断言这类提示时，不能当普通元素定位，要抓它的 text 做短暂断言（见知识点 2），否则用例会因"抓不到"而偶发失败。

【面试考察】

面试官："Toast 和 Dialog 有什么区别？对自动化定位有什么影响？"

参考回答框架：Toast 轻量、短暂（1~2 秒）、无焦点、不可点击、系统级；Dialog 是模态弹窗、可获得焦点、可点击。Toast 因短暂显示，定位要"等它出现 + 快速抓 text"，不能当普通控件。

【易错点】

| 误区 | 纠正 |
|------|------|
| 把 Toast 当普通控件定位 | Toast 短暂显示、无焦点，普通 find_element 容易抓不到，要等待 + 抓 text |
| Toast 和 Dialog 混为一谈 | Dialog 可点击、有焦点、模态；Toast 不可点击、无焦点、自动消失 |

【我的理解】

> （为什么说 Toast"永远不会获得焦点"会导致它"无法被点击"？这两件事的因果是什么？）

---

## 二、Toast 的定位原理

### 知识点 2：page_source + class + XPath

【课程原话/定义】

Appium 抓 Toast 时，使用 uiautomator 底层，把 Toast 元素放入控件树。Toast 出现时间短，可通过**等待**或**打印页面元素**判断是否存在，用 XPath 或 class name（Android 里 class name 相当于组件路径名 `android.widget.Toast`）定位。

页面结构里 Toast 元素大致如下：

```xml
<android.widget.Toast
  index="1"
  package="com.android.settings"
  class="android.widget.Toast"
  text="Clicked popup menu item Search"
  displayed="true"
/>
```

一个页面一般只有一个 Toast。

【为什么？】

1. Toast 短暂出现，Appium 抓它的窗口期极短，所以必须配合**显式等待**（等它出现在控件树）再抓，否则找不到。
2. Toast 的 class 固定是 `android.widget.Toast`，用 XPath `//android.widget.Toast` 或 `//*[contains(@text,'xxx')]` 都能定位——因为"一个页面一般只有一个 Toast"，class 定位也够唯一。
3. `displayed="true"` 说明 Toast 出现时是可被 uiautomator 捕获的，抓 text 断言即可。

【必须掌握】

- Toast 定位三件套：page_source 看结构 + class `android.widget.Toast`/XPath 定位 + 显式等待
- Toast 元素结构里 text 字段就是提示内容

【企业场景】

你在企业里，断言"登录成功"这类 Toast：先显式等待 `//*[contains(@text,'登录成功')]` 出现，再 `.text` 拿内容断言。因为一个页面只有一个 Toast，用 class `android.widget.Toast` 定位再取 text 也常见。

【面试考察】

面试官："App 的 Toast 提示怎么定位断言？"

参考回答框架：Toast 短暂显示，用显式等待等它出现在控件树（page_source），再用 XPath `//*[contains(@text,'xxx')]` 或 class `android.widget.Toast` 定位取 text 断言；不能当普通元素用 find_element 直接抓。

【易错点】

| 误区 | 纠正 |
|------|------|
| 直接 find_element 抓 Toast | Toast 短暂出现，先显式等待它进控件树，否则 NoSuchElement |
| 以为 Toast 有稳定 id | Toast 无稳定 id，靠 class（android.widget.Toast）+ text/XPath 定位 |
| 拿 Toast 去 click | Toast 无焦点不可点击，只能取 text 断言 |

【我的理解】

> （一个页面"一般只有一个 Toast"——这句话让定位变简单在什么地方？如果同时可能出现两个 Toast，定位策略要怎么改？）

---

## 三、API Demo 实战

### 知识点 3：Make a Popup → Search → 断言 Toast 文本

【课程原话/定义】

用 Appium 官方 Demo APK（API Demos）练习，进入 toast 页面：Views → Make a Popup。

```python
class TestToast:
    def setup_class(self):
        caps = {
            'platformName': 'android',
            'appium:appPackage': 'io.appium.android.apis',
            'appium:appActivity': 'io.appium.android.apis.view.PopupMenu1',
            "appium:noReset": True,
            "appium:shouldTerminateApp": True
        }
        self.driver = webdriver.Remote(
            "http://127.0.0.1:4723",
            options=UiAutomator2Options().load_capabilities(caps)
        )
        self.driver.implicitly_wait(15)

    def teardown_class(self):
        self.driver.quit()

    def test_get_toast(self):
        # 点击 Make a Popup! 按钮
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Make a Popup!").click()
        # 消息框类型选择 Search
        self.driver.find_element(AppiumBy.XPATH, "//*[@text='Search']").click()
        # 获取 Toast 弹框文本
        result = self.driver.find_element(
            AppiumBy.XPATH, "//*[contains(@text, 'Clicked popup')]"
        ).text
        assert result == "Clicked popup menu item Search"
```

【为什么？】

1. 用例走的是"触发 Toast → 等它出现 → 抓 text 断言"三步，触发动作（点击 Make a Popup → 选 Search）是产生 Toast 的前提。
2. 用 `contains(@text,'Clicked popup')` 而非精确 text，是因为 Toast 文本是拼接的（"Clicked popup menu item Search"），用 contains 更稳。
3. `appActivity` 直接指向 `PopupMenu1`（进入页面即触发 Toast 的入口 Activity），省去手动导航。

【必须掌握】

- 完整 Toast 用例：触发 → 等待 → 抓 text 断言
- `contains(@text,'Clicked popup')` 用包含匹配抓拼接文本

【企业场景】

你在企业里，把 Toast 断言封装成通用方法：传一个"预期文本片段"，内部用 `WebDriverWait(...).until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text,'{片段}')]")))` 等它出现再断言。这样所有"操作成功/失败"类提示都能复用。

【面试考察】

面试官："写一个断言 Toast 文本的用例，你会怎么组织？"

参考回答框架：先触发产生 Toast 的操作（点击按钮/提交），再用显式等待等 `//*[contains(@text,'预期片段')]` 出现，最后 `.text` 断言等于预期；不直接 find_element 抓（会因 Toast 短暂而抓不到）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 用精确 `@text='Clicked popup menu item Search'` 断言 | Toast 文本是拼接的、易变，用 contains 片段匹配更稳 |
| 忘了 setup 里配 appActivity 到 PopupMenu1 | appActivity 指向入口 Activity，否则要手动导航到 Views→Popup |

【我的理解】

> （为什么断言用 `contains(@text,'Clicked popup')` 而不是精确 text？如果你换了另一种 Toast 提示"Item deleted"，断言条件该怎么写？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Toast 特点 | 无法点击/限时/系统级/轻量 | ★★★★☆ |
| Toast 定位原理 | page_source + class + XPath + 等待 | ★★★★★ |
| API Demo 实战 | 触发 → 等待 → 抓 text 断言 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch18-自动化测试定位策略]]（特殊控件概览：alert/toast/下拉/上传，本章是 toast 展开）
- [[Ch14-三种等待机制]]（Toast 短暂显示 → 必须显式等待）
- [[Ch22-显式等待高级使用]]（Toast 断言里的显式等待 + EC 条件）
- [[Web自动化测试/README|Web自动化测试]]（Web alert 与 App toast 的"特殊控件"对照）
