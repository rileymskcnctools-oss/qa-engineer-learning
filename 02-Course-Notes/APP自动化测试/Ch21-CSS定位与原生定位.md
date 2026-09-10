---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 元素定位
  - CSS
  - 原生定位
course: APP自动化测试
chapter: Ch21-CSS定位与原生定位
created: 2026-09-10
status: draft
---

# Ch21 - CSS 定位与原生定位

## 课程来源
- 学习日期：

> 本章补全 [[Ch18-自动化测试定位策略]] 知识点 1 里"点到为止"的两类进阶定位：**原生定位（Android UiSelector）** 和 **CSS Selector**。Ch18 只给了定位策略总表，本章展开每个策略的具体写法与适用场景。

---

## 一、App 的三种类型

### 知识点 1：原生 / Web / 混合 App

【课程原话/定义】

| 类型 | 开发方式 | 特点 |
|------|---------|------|
| 原生 App（Native） | 基于 Android/iOS 平台官方语言、工具开发 | 速度最优 |
| Web App | 用 Web 语言开发，依托浏览器运行 | 成本低、支持广 |
| 混合 App（Hybrid） | 同时用原生技术 + HTML5 | 开发周期短、功能更新快 |

【为什么？】

1. App 类型决定"用什么定位"：原生控件用 UiSelector/XCUITest 定位，Web 视图（WebView 里的 H5 页面）要用 Web 那套（css/xpath）——混合 App 两套都要会。
2. 原生速度最优是因为直接调系统 API，Web App 慢在要过浏览器/WebView 这层壳。
3. 判断"这是不是 WebView"是定位前的第一步：看到控件树里出现 `XCUIElementTypeWebView` / `android.webkit.WebView`，就要切 Web 上下文再用 Web 定位。

【必须掌握】

- 三种 App 类型的定义与各自优缺点
- 混合 App 定位要"两套切换"

【企业场景】

你在企业里，拿到一个 App 先判断它是不是混合 App：如果有内嵌 H5 页面（活动页、资讯详情页），定位那部分元素要 `driver.contexts` 切到 `WEBVIEW_xxx`，再用 Web 的 css/xpath，否则原生定位永远找不到。

【面试考察】

面试官："原生 App、Web App、混合 App 有什么区别？对自动化定位有什么影响？"

参考回答框架：原生用平台官方语言开发、速度最优；Web 依托浏览器、成本低；混合两者结合、更新快。定位上原生控件用 UiSelector/XCUITest，混合 App 里的 H5 部分要切 WebView 上下文用 Web 定位。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为所有 App 定位方式都一样 | 混合 App 的 H5 部分必须切 WebView 上下文，原生定位找不到 |
| 原生一定最快、混合一定最差 | 各有利弊：原生速度优、Web 成本低、混合更新快，选型看场景 |

【我的理解】

> （混合 App 里有个 H5 活动页，你直接用 UiSelector 定位里面的按钮为什么找不到？需要先做什么操作？）

---

## 二、Android 原生定位——UiSelector 基础

### 知识点 2：UiSelector 单属性 + 组合定位

【课程原话/定义】

Android 原生定位：Appium 调底层 UIAutomator2 框架，借 UIAutomator API（UiSelector 类）搜索元素。

单属性格式：`'new UiSelector().属性名("<属性值>")'`（外层单引号、内层双引号，顺序不能变）。

```python
# ID 定位
ass_id = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("android:id/text1")'
)
# 文本定位
ass_text = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("Accessibility")'
)
# className 定位
ass_classname = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.TextView")'
)
```

组合定位（多属性任意组合、不限长度）：

```python
ass_mul = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("android:id/text1").text("App")'
)
```

【为什么？】

1. UiSelector 是**链式调用**：`new UiSelector().resourceId(...).text(...)` 一路点下去，本质是"多属性 AND 过滤"，和 XPath 的 `[@a and @b]` 等价但更原生、更快。
2. 整个 UiSelector 表达式是**一个字符串**传给 AppiumBy.ANDROID_UIAUTOMATOR，服务器端把它解析成 UIAutomator 的查询——这就是为什么外面单引号、里面双引号。
3. resourceId 是原生 ID，稳定且唯一性最好，是 Android 原生定位的首选。

【必须掌握】

- `new UiSelector().属性("值")` 链式写法
- resourceId / text / className 三种单属性定位
- 组合定位 = 链式多属性（等价 AND）

【企业场景】

你在企业里，Android 原生元素优先用 UiSelector 的 resourceId（比 XPath 快一个量级，且不依赖页面层级）；一个 resourceId 不唯一时链式加 `.text("xx")` 收窄，这是原生定位的标准姿势。

【面试考察】

面试官："Android 原生定位的 UiSelector 怎么用？单属性定位和组合定位怎么写？"

参考回答框架：`new UiSelector().属性名("值")`，定位策略用 AppiumBy.ANDROID_UIAUTOMATOR；单属性如 resourceId/text/className，组合是链式多属性 `.resourceId(...).text(...)`，等价于多条件 AND。

【易错点】

| 误区 | 纠正 |
|------|------|
| 引号顺序写反 | Python 外层**单引号**、内层**双引号**（Java 相反），顺序不能变 |
| 把 UiSelector 当普通方法调用 | 它是**字符串**传给 AppiumBy.ANDROID_UIAUTOMATOR，不是直接 import 的类 |
| 组合定位不会写 | 链式 `.resourceId("...").text("...")` 一路点下去，不是数组参数 |

【我的理解】

> （为什么 UiSelector 表达式要"外层单引号、内层双引号"？如果写成 `'new UiSelector().text("App")'`，Appium 到底把它当什么传给了服务器？）

---

## 三、Android 原生定位——模糊匹配 + 层级定位

### 知识点 3：textContains / textStartsWith / textMatches + fromParent / childSelector

【课程原话/定义】

模糊匹配：

```python
# 包含
driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textContains("ssi")')
# 以 x 开头
driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textStartsWith("Ani")')
# 正则匹配
driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textMatches("^Pre.*")')
```

层级定位：

```python
# 兄弟元素：fromParent
ass_bro = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("App").fromParent(text("Text"))')
# 父子元素：childSelector
ass_fa = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.ListView").childSelector(text("Text"))')
```

【为什么？】

1. textContains/textStartsWith/textMatches 是 XPath contains() / 正则 在原生里的等价物，但走 UIAutomator 更快。
2. textMatches 用的是**正则**，`^Pre.*` 表示"以 Pre 开头"，能表达比 contains 更复杂的匹配。
3. fromParent（找兄弟）和 childSelector（找子）本质是"原生版轴定位"——从当前元素沿层级走到目标，比 XPath 轴更稳（不依赖页面 XML 字符串）。

【必须掌握】

- 三种模糊匹配：textContains（包含）/ textStartsWith（开头）/ textMatches（正则）
- 层级：fromParent（兄弟）/ childSelector（父子）

【企业场景】

你在企业里，文案带动态内容（如"共 3 件""余额 ¥12.50"）用 textStartsWith/textContains 定位；要严格模式用 textMatches 正则。层级定位在"目标元素自己没 id、但父/子/兄弟有 id"时用。

【面试考察】

面试官："UiSelector 的模糊匹配有哪几种？分别对应什么语义？"

参考回答框架：textContains 包含、textStartsWith 开头、textMatches 正则匹配；正则能表达更复杂模式（如 `^Pre.*`）。三者都比精确 text 宽松，应对文案不确定的场景。

【易错点】

| 误区 | 纠正 |
|------|------|
| textMatches 用通配符不是正则 | textMatches 是**正则**，`^Pre.*` 里 `^` 表开头、`.*` 表任意，不是 SQL 通配 |
| 课程源码里 `fromParent(text("Text"))` / `childSelector(text("Text"))` 缺 new UiSelector() | 正确写法应内嵌完整 UiSelector：`fromParent(new UiSelector().text("Text"))`，照抄源码会跑不通（`text` 不是独立函数） |
| Java 父子示例末尾多一个引号 | 源码 `...childSelector(text('Text'))'"))` 末尾多一个 `'`，是笔误，会语法报错 |

【我的理解】

> （textContains("ssi") 和 textMatches("^ssi.*") 在什么情况下命中结果不同？举一个两者结果不一致的文案例子。）

---

## 四、Android 原生定位——滑动查找

### 知识点 4：UiScrollable + scrollIntoView

【课程原话/定义】

面对长列表、元素在屏幕外时，用 UiScrollable 滚动到目标元素再定位：

```python
"new UiScrollable(new UiSelector().scrollable(true).instance(0))\
    .scrollIntoView(new UiSelector().text('查找的元素文本').instance(0))"
```

【为什么？】

1. 屏幕外的元素不在当前控件树里，直接 find_element 找不到；scrollIntoView 会**边滚边找**，直到目标进入视野。
2. `scrollable(true)` 圈定"可滚动的容器"，`instance(0)` 指定第几个滚动容器（页面可能有多个列表）。
3. 这和 [[Ch17-滑动交互方法]] 的 scroll 目标一致，但 UiScrollable 是**原生层**实现，比 Appium 层的 swipe 循环更稳更快。

【必须掌握】

- `new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(...)` 结构
- 用途：长列表里定位屏幕外元素

【企业场景】

你在企业里，商品列表 100+ 条、目标在第 80 条，用 UiScrollable 的 scrollIntoView 一次性滚到位并定位，比手动 swipe 循环"滚一下查一下"稳定得多，也是长列表用例的标准写法。

【面试考察】

面试官："要定位长列表里屏幕外的元素，怎么做？"

参考回答框架：用 UiScrollable 的 scrollIntoView——`new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text('目标'))`，边滚动边查找直到元素可见；比手动 swipe 循环稳定。

【易错点】

| 误区 | 纠正 |
|------|------|
| 屏幕外元素直接 find_element | 屏幕外元素不在控件树里，要先 scrollIntoView 滚到可见 |
| 忘了 scrollable(true) | 不指定 scrollable(true) 的容器，UiScrollable 不知道滚哪个列表 |

【我的理解】

> （为什么"屏幕外的元素"直接 find_element 找不到？这跟 Ch14 的"元素在 DOM ≠ 可交互"有什么联系和区别？）

---

## 五、iOS 原生定位

### 知识点 5：UIAutomation → XCUITest

【课程原话/定义】

- iOS 9.2 及以下：唯一自动化技术为 UIAutomation，运行在 Instruments 中。
- iOS 9.3 及以上：苹果淘汰 UIAutomation，改用 XCUITest；Appium 1.6 起支持 XCUITest。

【为什么？】

1. 这是 iOS 自动化引擎的**代际更替**：旧 UIAutomation 已废弃，现在 iOS 自动化统一走 XCUITest（Apple 官方测试框架）。
2. 对应到 Appium capability 就是 `automationName=xcuitest`，对应 Android 的 `uiautomator2`。
3. 面试常问"iOS 用什么引擎"，答 XCUITest + 知道它取代了 UIAutomation 即可。

【必须掌握】

- iOS 自动化引擎演进：UIAutomation（≤9.2）→ XCUITest（≥9.3）
- Appium capability 对应 `automationName=xcuitest`

【企业场景】

你在企业里，跑 iOS 用例时 `automationName` 写 xcuitest，并配合 bundleId + udid（真机）；遇到 iOS 定位，用 accessibility-id / XCUIElementType 那套（见 Ch13 跨平台对照）。

【面试考察】

面试官："iOS 的自动化测试用什么技术？Appium 从哪个版本支持 XCUITest？"

参考回答框架：iOS 9.3 起用 XCUITest（取代旧的 UIAutomation），Appium 1.6 起支持；capability 里 `automationName=xcuitest`。

【易错点】

| 误区 | 纠正 |
|------|------|
| iOS 还用 UIAutomation | 9.3+ 已淘汰 UIAutomation，统一 XCUITest |
| 把 Android 的 uiautomator2 用到 iOS | Android 用 uiautomator2，iOS 用 xcuitest，两个不同引擎 |

【我的理解】

> （`automationName=uiautomator2` 和 `automationName=xcuitest` 分别是给谁用的？为什么这是"必填" capability（回想 Ch11）？）

---

## 六、CSS Selector 定位

### 知识点 6：CSS 语法 + 原理分析

【课程原话/定义】

CSS 选择器由 W3C 制定，Appium 上的 CSS 与 Web 大致相同，但有些许差异。适合"复杂结构但元素属性相对独立"的应用。

| 定位方式 | 语法 | 描述 |
|------|------|------|
| 标签名 | `"input"` | 所有 input 元素 |
| id | `"#elementId"` | id 为 elementId（`#` 表 id） |
| class | `".elementClass"` | class 为 elementClass（`.` 表 class） |
| 属性定位 | `"input[name='username']"` | name 为 username 的 input |
| 层级关系 | `"div > input"` | div 下所有 input |
| 文本内容 | `"button:contains('Submit')"` | 文本含 Submit 的 button |

查找：Python `driver.find_element(AppiumBy.CSS_SELECTOR, selector)` / `find_elements`；Java `findElement(AppiumBy.cssSelector(selector))`。

【原理分析】CSS 表达式传入 Appium 服务器后：①解析 CSS 选择器语法结构 → ②映射到移动测试框架的原生定位方式。所以 `#com\.xueqiu\.android\:id\/tv_search` 最终被转成 `new UiSelector().resourceId("com.xueqiu.android:id/tv_search")`——CSS 定位本质是**原生定位的包装**，多一层解析，效率不如直接原生定位。

【为什么？】

1. CSS 是 Web 领域的定位方式，Appium 为兼容把它**翻译**成原生定位——这个翻译层就是它"不如原生高效"的根因（原理分析图说明了这条链路）。
2. `#`、`.`、`[]`、`>` 这些语法与 Web 完全一致，会 Web 自动化的同学能零成本上手。
3. 但 App 的 id 常带 `.` `:` `/` 等特殊字符（如 `com.xueqiu.android:id/tv_search`），必须转义（`\.` `\:` `\/`），反而繁琐。

【必须掌握】

- CSS 常见语法：标签/#id/.class/[属性]/层级
- CSS 定位原理 = 解析后映射成原生定位
- App id 特殊字符要转义

【企业场景】

你在企业里，App 自动化**默认不用 CSS**（多一层解析、id 又要转义），除非团队已有 Web 自动化经验、想统一心智。真要跨 Web/App 复用定位思路，用 XPath 或原生定位更合适——这也正是课程"推荐 XPath 或原生定位"的原因。

【面试考察】

面试官："App 里能用 CSS Selector 定位吗？和 Web 有什么区别？"

参考回答框架：能，语法与 Web 类似，但 Appium 会把 CSS 解析后映射成原生定位（多一层开销、不如原生高效）；且 App 的 id 带 `.` `:` `/` 需转义。所以实际多推荐 XPath 或原生定位。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 App 的 CSS 和 Web 完全一样 | 语法类似，但 Appium 多一层"解析→映射原生"，效率低 |
| App id 直接写 `#com.xueqiu.android:id/tv_search` | 特殊字符要转义：`#com\.xueqiu\.android\:id\/tv_search` |
| 课程源 `:contains('Submit')` 当标准 CSS | `:contains` 是 jQuery/Sizzle 扩展，**不是** W3C 标准 CSS，Appium 的 CSS 解析不一定支持，别照搬 |

【我的理解】

> （课程源码里"CSS 定位原理"说 CSS 最终被转成 UiSelector——那既然都要转，为什么不直接用 UiSelector？多出来的这层解析带来了什么代价？）

---

## 七、雪球实战：原生定位 vs CSS 定位

### 知识点 7：同一场景两套写法对比

【课程原话/定义】

场景：打开雪球 → 点击搜索框 → 输入 alibaba → 判断"阿里巴巴"可见。

原生定位（UiSelector）：

```python
self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.xueqiu.android:id/home_search")').click()
self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().resourceId("com.xueqiu.android:id/search_input_text")').send_keys("阿里巴巴")
alibaba_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("阿里巴巴")')
result = alibaba_element.get_attribute("displayed")
assert result == 'true'
```

CSS 定位：

```python
self.driver.find_element(AppiumBy.CSS_SELECTOR,
    "#com\.xueqiu\.android\:id\/home_search").click()
self.driver.find_element(AppiumBy.CSS_SELECTOR,
    "#com\.xueqiu\.android\:id\/search_input_text").send_keys("阿里巴巴")
alibaba_element = self.driver.find_element(AppiumBy.CSS_SELECTOR, "*[text='阿里巴巴']")
result = alibaba_element.get_attribute("displayed")
assert result == "true"
```

【为什么？】

1. 同一场景两种写法对比，直接体现知识点 6 的结论：CSS 版每个 id 都要转义（`\.` `\:` `\/`），写法更啰嗦。
2. `*[text='阿里巴巴']` 是 CSS 属性选择器等价 XPath 的 `//*[@text='阿里巴巴']`。
3. `get_attribute("displayed")` 返回字符串 `'true'`/`'false'`，断言要 `== 'true'`（不是布尔 True）——这是 Appium 取属性的常见坑。

【必须掌握】

- 原生定位 vs CSS 定位的同一场景对照
- `get_attribute("displayed")` 返回字符串，断言 `== 'true'`

【企业场景】

你在企业里，雪球这类真实 App 优先 UiSelector 的 resourceId（不用转义、更快）；CSS 只在团队统一 Web/App 心智时才考虑。判断"元素是否可见"用 `get_attribute("displayed") == 'true'` 或 `is_displayed()`。

【面试考察】

面试官："给你一个 App 搜索场景，你会用原生定位还是 CSS 定位？为什么？"

参考回答框架：优先原生 UiSelector 定位——不用转义特殊字符、直接走 UIAutomator 更快；CSS 要 `\.` `\:` `\/` 转义且多一层解析映射，性能更差，只在团队有 Web 背景、统一心智时用。

【易错点】

| 误区 | 纠正 |
|------|------|
| `get_attribute("displayed")` 当布尔用 | 它返回**字符串** `'true'`/`'false'`，断言要 `== 'true'` 或 `is_displayed()` |
| 源码 `load_capabilities(cpas)` 变量名笔误 | capability 变量定义叫 `caps`，调用处却写 `cpas`，照抄会 NameError，应为 `load_capabilities(caps)` |
| `shouldTerminateApp=true` 注释"设置 app 不重启" | 语义写反（见 Ch11 笔误清单）：true 是"会话结束终止 app"，"不清数据"是 noReset |

【我的理解】

> （同样是定位 `home_search`，原生写法和 CSS 写法哪个更稳？从"转义成本 + 解析层数 + 执行效率"三个角度分别说明。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| App 三种类型 | 原生/Web/混合 + 定位影响 | ★★★★☆ |
| UiSelector 基础 | 单属性 + 组合（链式） | ★★★★★ |
| 模糊 + 层级 | textContains/StartsWith/Matches + fromParent/childSelector | ★★★★☆ |
| 滑动查找 | UiScrollable + scrollIntoView | ★★★★☆ |
| iOS 原生 | UIAutomation → XCUITest | ★★★☆☆ |
| CSS 定位 | 语法 + 原理（映射原生）+ 转义 | ★★★★☆ |
| 雪球实战 | 原生 vs CSS 对比 | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch13-常见控件定位方法]]（基础 5 种定位 + find_element/find_elements）
- [[Ch18-自动化测试定位策略]]（定位策略全景表，本章是其中原生/CSS 的展开）
- [[Ch20-XPath高级定位技巧]]（XPath 轴定位，与 UiSelector 的 fromParent/childSelector 是同一思想的不同实现）
- [[Ch17-滑动交互方法]]（scroll 滑动，与 UiScrollable 目标一致）
- [[Web自动化测试/README|Web自动化测试]]（CSS 语法源自 Web 端，可对照）
