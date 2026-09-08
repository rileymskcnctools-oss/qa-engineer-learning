---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 实战项目
course: APP自动化测试
chapter: Ch19-雪球app搜索功能实战
created: 2026-09-08
status: draft
---

# Ch19 - 雪球 app 搜索功能自动化测试实战

## 课程来源
- 学习日期：

---

## 一、需求分析

### 知识点 1：被测应用与测试场景

【课程原话/定义】

- 被测应用：雪球 App（股票平台，提供热点资讯、实时行情、证券交流交易、公募理财；功能含搜索股票、查看行情、交易、浏览热门文章、发帖、登录注册等）。
- 测试场景：搜索股票。

【为什么？】

1. 这是第一个"真实第三方 App"实战（之前都用 ApiDemos 官方 Demo），定位、capability、流程都更接近真实工作。
2. 雪球需要登录才能进首页看到搜索框，引出"登录态保持"的关键点。
3. 需求分析先行：明确"测什么"（搜索股票）再写用例。

【必须掌握】

- 雪球 app 场景（搜索股票）
- 真实 App 需要处理登录态

【企业场景】

你在企业里，接手一个要登录的 App，第一件事是搞清楚"登录态怎么保持"——用 noReset 保留本地登录态，还是每次用例前用账号密码/短信登录。这是真实 App 自动化与官方 Demo 最大的区别。

【面试考察】

面试官："测一个需要登录的 App，登录态怎么处理？"

参考回答框架：用 noReset=true 保留本地登录态（提前手动登录一次），或用 fixture 每次登录；noReset 省时省事但依赖"首次登录成功"。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为所有 App 打开就能测 | 真实 App 常需登录，要先解决登录态 |
| noReset 和 fullReset 搞反 | noReset=保留状态（保登录），fullReset=卸载重装（清状态） |

【我的理解】

> （为什么雪球要先解决登录态？如果不用 noReset，每次跑用例会发生什么？）

---

## 二、用例设计

### 知识点 2：四步用例设计

【课程原话/定义】

1. 打开雪球首页
2. 点击搜索框（点击前判断是否可用，查看 name 属性值，获取坐标和宽高）
3. 向搜索框输入 alibaba
4. 判断【阿里巴巴】是否可见：可见打印"搜索成功"，不可见打印"搜索失败"

【为什么？】

1. 用例拆成"定位→检查状态→操作→断言"四步，是标准 App 用例骨架。
2. 步骤 2 的"先判断是否可用 + 取属性"是 Ch15 状态判断 + 属性获取的落地：真实工作里点击前先确认元素可交互。
3. 步骤 4 是断言：is_displayed 判断结果，打印 + assert 双保险。

【必须掌握】

- 四步用例骨架
- 点击前 is_enabled 判断 + 属性获取

【企业场景】

你在企业里，写用例不是"定位→点"两步，而是"定位→状态检查→操作→断言"四步。点搜索框前 is_enabled() 判断，避免"框还没渲染好就点"的偶发失败。

【面试考察】

面试官："写一个搜索功能的用例，你会拆成哪几步？"

参考回答框架：打开首页 → 定位搜索框并检查可用/取属性 → 点击 → 输入关键词 → 断言结果可见。核心是"检查状态→操作→断言"。

【易错点】

| 误区 | 纠正 |
|------|------|
| 定位到就点，不判断可用 | 点前 is_enabled() 判断，避免点灰置/未加载元素 |
| 只 print 不 assert | print 是给人看，assert 才是自动化判定，两者都要 |

【我的理解】

> （步骤 2 里"判断搜索框是否可用"有什么用？如果直接 click 不判断，可能出什么问题？）

---

## 三、capability 与登录态

### 知识点 3：capability 设置（noReset 保登录态）

【课程原话/定义】

```python
caps = {
    "platformName": "Android",
    "appium:automationName": "uiautomator2",
    "appium:deviceName": "emulator-5554",
    "appium:appPackage": "com.xueqiu.android",
    "appium:appActivity": ".view.WelcomeActivityAlias",
    "appium:noReset": True,              # 不清空缓存，保存登录信息
    "appium:forceAppLaunch": True,       # 测试运行前强制重启 app
    "appium:skipDeviceInitialization": True,  # 跳过安装/权限设置
}
```

【为什么？】

1. noReset=True 是本用例的核心：保留登录态，因为雪球登录后才能看到搜索框。
2. forceAppLaunch=True：每次运行前强制重启 app，保证从干净首页开始。
3. skipDeviceInitialization=True：跳过重复安装/权限设置，提速。
4. 包名 com.xueqiu.android、入口 .view.WelcomeActivityAlias 是雪球的两个关键标识。

【必须掌握】

- noReset 保登录态（核心）
- forceAppLaunch / skipDeviceInitialization 的作用

【企业场景】

你在企业里，测需登录 App 的标准配置就是 noReset=True + 提前手动登录一次。forceAppLaunch 保证每次从首页开始，skipDeviceInitialization 让回归跑得快。

【面试考察】

面试官："noReset、fullReset、forceAppLaunch 分别什么作用？"

参考回答框架：noReset 不重置应用状态（保留登录态）、fullReset 卸载重装重置、forceAppLaunch 每次运行前强制重启 app。

【易错点】

| 误区 | 纠正 |
|------|------|
| Java 示例注释 "shouldTerminateApp=设置 app 不重启" | shouldTerminateApp=true 是"会话结束终止 app"，不是"不重启"；"不清数据"是 noReset。雪球里同时配 noReset=true(保登录) 和 shouldTerminateApp=true，注释还写反了，语义打架 |
| Java 用 "appPackage" 无 appium: 前缀 | Appium 2.x 非标准 capability 要 appium: 前缀（Python 示例是对的） |

【我的理解】

> （noReset=True 和"提前手动登录一次"是怎么配合的？为什么这样比"每次用例里输账号密码"更常用？）

---

## 四、搜索框定位与操作

### 知识点 4：定位搜索框 + 取属性 + 点击 + 输入

【课程原话/定义】

```python
searchbox_ele = self.driver.find_element(
    AppiumBy.ID, "com.xueqiu.android:id/home_search"
)
if searchbox_ele.is_enabled():
    print(searchbox_ele.text)      # 查看 text
    print(searchbox_ele.location)  # 坐标
    print(searchbox_ele.size)      # 宽高
    searchbox_ele.click()
    self.driver.find_element(
        AppiumBy.ID, "com.xueqiu.android:id/search_input_text"
    ).send_keys("alibaba")
```

【为什么？】

1. 定位用 ID（com.xueqiu.android:id/home_search），是雪球搜索框的 resource-id，稳定。
2. is_enabled 判断可用 → text/location/size 取属性（Ch15 落地）→ click → 切到输入框再 send_keys。
3. 注意搜索框（home_search）和输入框（search_input_text）是两个不同元素：点击搜索框后页面切到搜索页，输入框是另一个 id。

【必须掌握】

- 搜索框/输入框是两个元素（不同 id）
- is_enabled + text/location/size + click + send_keys 链路

【企业场景】

你在企业里，搜索类功能常是"点搜索框（首页入口）→ 切搜索页 → 输入框输入"两个元素。定位时先点入口、再等输入框出现（可加显式等待），别把两个 id 混了。

【面试考察】

面试官："搜索框的 home_search 和 search_input_text 为什么是两个元素？"

参考回答框架：home_search 是首页的搜索入口框，点击后切到搜索页，真正输入的是 search_input_text 输入框，两者 resource-id 不同、功能不同。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为搜索框和输入框是同一个元素 | 首页搜索框(home_search) ≠ 搜索页输入框(search_input_text) |
| 点击前不判断可用 | is_enabled() 判断，避免点灰置元素 |

【我的理解】

> （为什么"点击搜索框"和"输入关键词"要用两个不同的元素定位？它们分别在哪个页面？）

---

## 五、断言结果

### 知识点 5：find_element 返回第一个 + is_displayed 断言

【课程原话/定义】

```python
alibaba_element = self.driver.find_element(
    AppiumBy.XPATH, "//*[@text='阿里巴巴']"
)
result = alibaba_element.is_displayed()
if result:
    print("搜索成功")
else:
    print("搜索失败")
assert result
```

列表下方还有一个"阿里巴巴"，XPath 会定位到两个元素。find_element 找到第一个就返回；要定位下方的另一个用 find_elements 取多个再选。

【为什么？】

1. XPath 用 text 定位"阿里巴巴"（结果列表项），因为列表项通常没有稳定 id，text 是唯一可用的。
2. find_element 返回第一个匹配元素（页面第一个"阿里巴巴"），find_elements 返回全部——这正是 Ch13 知识点的实战应用。
3. is_displayed 断言结果可见，print + assert 双保险。

【必须掌握】

- 结果用 XPath + text 定位
- find_element 返回第一个 vs find_elements 返回全部

【企业场景】

你在企业里，搜索结果列表项常没有唯一 id，用 text 定位。如果页面上有多个同名结果（如"阿里巴巴"出现在热门搜索 + 结果列表），要清楚 find_element 只给第一个，需要第二个用 find_elements 下标取。

【面试考察】

面试官："XPath 定位到多个相同元素时，find_element 返回哪个？要第 2 个怎么办？"

参考回答框架：find_element 返回第一个匹配元素；要第 2 个用 find_elements 返回列表再按下标 [1] 取。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 find_element 会报"多个匹配"错误 | find_element 静默返回第一个，不报错 |
| 多个同名元素要第 N 个还用 find_element | 用 find_elements 取列表再下标 |

【我的理解】

> （页面上有两个"阿里巴巴"，find_element 返回哪个？如果要第二个，代码怎么写？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 需求分析 | 雪球 + 搜索股票场景 | ★★★☆☆ |
| 用例设计 | 四步骨架 | ★★★★★ |
| capability | noReset 保登录态 | ★★★★★ |
| 定位操作 | 搜索框/输入框两元素 | ★★★★☆ |
| 断言 | find_element 第一个 + is_displayed | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch15-常见交互方法]]（is_enabled/text/location/size 的属性获取与状态判断）
- [[Ch13-常见控件定位方法]]（ID/XPath 定位 + find_element/find_elements）
- [[Ch14-三种等待机制]]（搜索页切换后等输入框加载）
- [[Ch17-滑动交互方法]]（搜索结果列表滑动查看）
