---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - Capability
course: APP自动化测试
chapter: Ch11-Capability配置参数解析
created: 2026-09-07
status: draft
---

# Ch11 - Capability 配置参数解析

## 课程来源
- 学习日期：

---

## 一、Capability 是什么

### 知识点 1：Desired Capabilities 与 Session

【课程原话/定义】

Capability 是用于启动 Appium 会话的一组参数的名称，描述 session 所希望具备的"功能"。功能表示为键值对的集合，值可以是任何有效的 JSON 类型，包含其他对象。

Appium 的客户端和服务端之间通信都必须在一个 Session 的上下文中进行。客户端发起通信时先发送一个叫 "Desired Capabilities" 的 JSON 对象给服务器；服务器收到后创建 session 并把 session ID 返回客户端，之后客户端用该 session ID 发送后续命令。

【为什么？】

1. Capability 是"启动前告诉服务器测什么"的唯一入口——平台、引擎、设备、App 全部通过它传，Server 拿到才知道怎么初始化会话。
2. 值是任意 JSON 类型（可嵌套对象），所以既能传字符串（包名）也能传布尔（noReset）甚至数组/对象，表达能力强。
3. Session 是"上下文"：一次会话 = 一个 App 的一次自动化生命周期。命令必须挂在一个 session 下，否则服务器不知道操作哪个 App 实例。

【必须掌握】

- Capability = 描述 session 能力的键值对集合（JSON）
- 客户端 → 发 Desired Capabilities → 服务器创建 session → 返回 session ID → 后续命令带 session ID

【企业场景】

你在企业里，一套 capability 通常抽成一个 `caps.py` 配置文件（或 fixture 返回 dict），不同环境（测试机/真机/不同 App）切换时只改这个文件。session ID 你平时看不到，但报错里出现 "session not found" 就是会话断了（App 崩溃、服务器重启、driver 被误 quit）。

【面试考察】

面试官："Appium 客户端和服务端是怎么建立一次会话的？"

参考回答框架：客户端先发 Desired Capabilities（JSON 键值对）给服务器，服务器创建 session 并返回 session ID，之后所有命令都挂在这个 session ID 下执行；session 是客户端与服务器通信的上下文。

【易错点】

| 误区 | 纠正 |
|------|------|
| Capability 就是"启动参数" | 它不止启动参数，还是整个会话的能力描述（等待超时、是否重置、日志等都在里面） |
| 原文写 "Desire capability" | 标准术语是 **Desired Capabilities**（复数），标题里的 "Desire" 是笔误 |

【我的理解】

> （"一次会话"对应现实中的什么？如果 App 中途崩溃了，session 会怎样，后续 find_element 会报什么错？）

---

## 二、W3C 标准 Capability 与平台

### 知识点 2：W3C 标准 capability

【课程原话/定义】

W3C WebDriver 关于平台的标准 capability 的一小部分：

| Capability Name | 类型 | 描述 |
|------|------|------|
| browserName | string | 要启动和自动化的浏览器名称 |
| browserVersion | string | 具体浏览器版本 |
| platformName | string | 平台名称 |

Appium 在 W3C 标准基础上引入了更适配不同平台的附加功能，任何非标准的扩展 capability 都必须包含 `appium:` 前缀。Appium 支持的平台：Browsers、iOS apps、Android apps、React apps、Unity。

【为什么？】

1. Appium 底层是 W3C WebDriver 协议，所以它兼容 WebDriver 的标准 capability（browserName/platformName 等）。
2. Appium 是为"原生 App"扩展了 WebDriver，所以新增了很多 WebDriver 没有的键（appPackage、bundleId 等）。为避免和标准键冲突，Appium 2.x 要求这些非标准键加 `appium:` 前缀。
3. 支持 React/Unity 说明 Appium 不止测原生 App，还能测混合/H5/游戏，覆盖范围广。

【必须掌握】

- 三个标准 capability：browserName / browserVersion / platformName
- Appium 2.x 非标准 capability 必须加 `appium:` 前缀

【企业场景】

你在企业里，`platformName` 是必填项，决定走 Android 还是 iOS 驱动分支；`browserName` 只有当测移动端 H5 页面时才填（如 "Chrome"），纯原生 App 不用填。前缀问题在升级 Appium 1.x → 2.x 时最容易踩坑：旧脚本的 `appPackage` 没前缀会直接报错。

【面试考察】

面试官："为什么 Appium 的很多 capability 要加 appium: 前缀？"

参考回答框架：Appium 基于 W3C WebDriver 协议，为了和标准 capability（browserName 等）区分，所有非标准的扩展键统一加 `appium:` 前缀，避免命名冲突，也符合 W3C 的扩展命名约定。

【易错点】

| 误区 | 纠正 |
|------|------|
| 原文表写 "browerName / browerVersion" | 正确拼写是 **browserName / browserVersion**（brower 少了 s，原文笔误） |
| 以为 Appium 只能测原生 App | 还能测 H5（browserName）、React Native、Unity 游戏 |

【我的理解】

> （`browserName` 什么时候填、什么时候不填？它和 `appPackage` 是二选一还是一起用？）

---

## 三、公共 Capability（不区分平台）

### 知识点 3：通用参数

【课程原话/定义】

| 键 | 描述 | 值 | 是否必填 |
|------|------|------|------|
| appium:automationName | Appium 驱动程序名称 | uiautomator2、xcuitest | 是 |
| appium:deviceName | 设备名称（目前仅对 iOS 模拟器有用，其他情况建议用 udid） | iPhone14 | 否 |
| appium:platformVersion | 平台版本 | 7.1, 4.4 | 否 |
| appium:newCommandTimeout | 等待客户端发命令的秒数，超时会话关闭 | 120 | 否 |
| appium:noReset | true 则不重置应用状态（默认 false） | true | 否 |
| appium:fullReset | true 则增强重置逻辑保证环境可复现（默认 false） | true | 否 |
| appium:printPageSourceOnFindFailure | true 则查找失败时打印页面源到日志 | true | 否 |
| appium:eventTimings | true 则收集事件计时 | true | 否 |
| appium:shouldTerminateApp | 会话结束时是否终止 App（默认 true，除非 noReset=true） | true | 否 |
| appium:forceAppLaunch | App 已在运行是否强制重启（默认 true，除非 noReset=true） | true | 否 |

【为什么？】

1. `automationName` 是唯一必填的——它决定用哪个驱动（Android 的 uiautomator2、iOS 的 xcuitest），不同驱动支持的能力和定位方式不同。
2. `noReset` / `fullReset` / `shouldTerminateApp` / `forceAppLaunch` 这四个控制"会话前后的 App 状态"，直接决定用例是否稳定、是否残留脏数据。
3. `newCommandTimeout` 是防"僵尸会话"：客户端异常退出时，服务器等一段时间没命令就自动关会话，避免占着设备不放。

【必须掌握】

- automationName 必填，Android 用 uiautomator2、iOS 用 xcuitest
- noReset vs fullReset 的区别
- newCommandTimeout 的作用

【企业场景】

你在企业里，回归测试通常配 `noReset=True`：不清登录态和数据，用例跑得快且连续；冒烟/首轮才用 `fullReset=True` 追求干净环境。`newCommandTimeout` 在调试时设大点（如 300），防止你断点调试时服务器把会话关了。

【面试考察】

面试官："noReset 和 fullReset 有什么区别？"

参考回答框架：noReset=true 是不重置应用状态（保留数据/登录态），fullReset=true 是做最大限度的重置（卸载重装/清数据）保证环境干净可复现，两者默认都 false。

【易错点】

| 误区 | 纠正 |
|------|------|
| noReset 是"不清缓存" | noReset 是**不重置应用状态/数据**（保留登录态、缓存、本地数据），"缓存"只是其中一部分，原文描述过窄 |
| automationName 漏配 | 它是唯一必填的通用参数，漏了服务器不知道用哪个驱动 |
| deviceName 必填 | 实际可省略，真机建议用 appium:udid 精确指定设备 |

【我的理解】

> （为什么回归测试倾向 noReset=True，而首轮冒烟倾向 fullReset=True？用"数据残留会不会影响断言"来解释。）

---

## 四、Android 特有参数

### 知识点 4：appPackage / appActivity 等

【课程原话/定义】

| 键 | 描述 | 值 |
|------|------|------|
| appium:appActivity | 要启动的 Android Activity 名，通常前面加 `.`（如 .MainActivity 代替 MainActivity） | MainActivity, .Settings |
| appium:appPackage | 运行的 Android 应用包名 | com.example.android.myApp, com.android.settings |
| appium:appWaitActivity | 等待启动的 Android Activity 名称 | SplashActivity |
| appium:unicodeKeyboard | 启用 Unicode 输入，默认 false | true/false |
| appium:resetKeyboard | 重置键盘 | true/false |
| appium:dontStopAppOnReset | 首次启动时不停止 App | true/false |
| appium:skipDeviceInitialization | 跳过安装、权限设置等操作 | true/false |

【为什么？】

1. `appPackage` + `appActivity` 是 Android 启动 App 的核心：包名定位"哪个 App"，Activity 定位"进哪个页面"（呼应 Ch10 知识点3）。
2. Activity 前面加 `.` 是相对包名的简写——`.MainActivity` 会自动补全为 `com.example.app.MainActivity`，省去写全限定名。
3. `unicodeKeyboard` + `resetKeyboard` 成对使用解决中文输入：Appium 会装一个 Unicode 输入法解决中文/特殊字符输入，用完 resetKeyboard 恢复默认键盘。

【必须掌握】

- appPackage（包名）+ appActivity（入口 Activity，注意前导点）
- unicodeKeyboard + resetKeyboard 解决中文输入

【企业场景】

你在企业里，换被测 App 就是改 appPackage 和 appActivity；appActivity 的准确值可以用 `adb shell dumpsys window | grep mCurrentFocus` 或 `aapt dump badging` 拿到，别靠猜。测试里要输入中文（登录名、搜索词）必须开 unicodeKeyboard，否则 send_keys 中文会乱码或失败。

【面试考察】

面试官："为什么 appActivity 有时要写 .MainActivity 带个点？"

参考回答框架：前导 `.` 是相对包名的简写，Appium 会自动补全成 `包名.MainActivity` 的完整限定名，写全名也行但带点更简洁。

【易错点】

| 误区 | 纠正 |
|------|------|
| appActivity 漏掉前导点 | 有的入口要写 .MainActivity，漏点会找不到 Activity |
| 中文输入失败不查键盘 | 先确认是否开了 unicodeKeyboard/resetKeyboard |
| dontStopAppOnReset / skipDeviceInitialization 与 noReset 混淆 | noReset 管"数据重置"，这两个管"是否停止 App / 是否跳过初始化安装"，职责不同 |

【我的理解】

> （appPackage 和 appActivity 组合起来解决什么问题？只给包名不给 Activity 行不行，为什么？）

---

## 五、iOS 独有参数

### 知识点 5：bundleId / autoAcceptAlerts 等

【课程原话/定义】

| 键 | 描述 | 值 |
|------|------|------|
| appium:bundleId | 被测应用的 bundle ID，真机启动用；用 bundleId 在真机测试时可省 app 关键字，但必须给 udid | io.appium.TestApp |
| appium:autoAcceptAlerts | iOS 个人信息访问警告（位置/联系人/图片）出现时自动点接受，默认 false | true/false |
| appium:showIOSLog | 是否在 Appium 日志显示设备捕获的日志，默认 false | true/false |

【为什么？】

1. bundleId 是 iOS 里等价于 Android appPackage 的概念——唯一定位一个 App（App Store 里每个 App 有唯一 bundle ID）。
2. iOS 首次访问位置/相册/通讯录会弹系统授权框，`autoAcceptAlerts=true` 自动点"接受"，否则弹窗会挡住自动化流程导致用例卡死。
3. showIOSLog 把设备日志拉到 Appium 日志里，方便排查崩溃原因。

【必须掌握】

- bundleId 是 iOS 定位 App 的 ID（对应 Android 的 appPackage）
- autoAcceptAlerts 解决 iOS 系统授权弹窗

【企业场景】

你在企业里，iOS 真机测试 bundleId 配合 udid 使用（bundleId 指定 App、udid 指定设备）；iOS 用例几乎必开 autoAcceptAlerts，否则第一次跑用例会卡在"是否允许访问位置"的弹窗上。Android 没有这套（权限在安装/首次调用时处理，处理机制不同）。

【面试考察】

面试官："iOS 测试里常见的两个特有 capability 是什么，解决什么问题？"

参考回答框架：bundleId（唯一定位被测 App，配合 udid 指定真机）和 autoAcceptAlerts（自动接受系统授权弹窗，避免用例被系统弹窗卡住）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 用 bundleId 真机测试不给 udid | 真机必须同时给 udid 指定设备，模拟器才可省 |
| Android 也用 autoAcceptAlerts | 那是 iOS 独有，Android 权限机制不同 |

【我的理解】

> （iOS 的 bundleId 和 Android 的 appPackage 是什么对应关系？autoAcceptAlerts 解决的是 iOS 特有的什么现象？）

---

## 六、完整示例与推荐优化参数

### 知识点 6：Desired Capabilities 示例 + 稳定性参数

【课程原话/定义】

API Demo 启动页配置：

```json
{
  "platformName": "android",
  "deviceName": "emulator-5554",
  "appium:appPackage": "io.appium.android.apis",
  "appium:appActivity": ".ApiDemos"
}
```

推荐配置优化参数（提高用例稳定性）：

```json
{
  "appium:noReset": true,
  "appium:dontStopAppOnReset": true,
  "appium:skipDeviceInitialization": true,
  "appium:unicodeKeyboard": true
}
```

【为什么？】

1. 基础配置只保证"能启动"；优化参数保证"跑得稳"：noReset 不清数据、dontStopAppOnReset 首启不停 App、skipDeviceInitialization 跳过重复安装/授权、unicodeKeyboard 支持中文输入。
2. 这些参数组合起来解决的是真实回归里的痛点：每次重装 App 慢、登录态丢失、中文输入失败。

【必须掌握】

- 一个能启动 + 一个能稳定回归的 capability 字典长什么样
- 优化参数各自解决什么问题

【企业场景】

你在企业里，标准 capability 模板通常是"基础参数 + 稳定性参数"两段式：基础段定位（platformName/automationName/appPackage/appActivity），稳定段提速（noReset/dontStopAppOnReset/skipDeviceInitialization）。新人接手先改基础段，遇到不稳定再加稳定段。

【面试考察】

面试官："说出几个能提高 App 用例稳定性的 capability，并说明原因。"

参考回答框架：noReset（不清数据，用例连续跑）、dontStopAppOnReset（首启不停 App，避免冷启动耗时/状态丢失）、skipDeviceInitialization（跳过重复安装授权，提速）、unicodeKeyboard（中文输入不乱码）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 原文优化参数 JSON 用了 `True` 和 `//` 注释 | JSON 里布尔是小写 `true`，且 JSON 不支持 `//` 注释——原文混入了 Python 语法，直接复制会解析失败 |
| 原文 "unicodeKeyBoard" 大小写不一致 | 正确键名是 **unicodeKeyboard**（正文表格），推荐配置里写成 unicodeKeyBoard 是笔误 |

【我的理解】

> （"基础参数"和"稳定性参数"各自回答什么问题？如果把 noReset 设成 true 但用例又依赖"每次都是全新数据"，会发生什么？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Desired Capabilities 与 Session | 键值对 + 创建 session 流程 | ★★★☆☆ |
| W3C 标准 + appium: 前缀 | browserName/platformName + 扩展前缀 | ★★★★☆ |
| 公共 capability | automationName / noReset / fullReset / newCommandTimeout | ★★★★★ |
| Android 特有 | appPackage / appActivity / unicodeKeyboard | ★★★★★ |
| iOS 独有 | bundleId / autoAcceptAlerts | ★★★☆☆ |
| 稳定性优化参数 | noReset / dontStopAppOnReset / skipDeviceInitialization | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch10-自动化测试用例结构分析]]（知识点3 已先讲了 5 个核心 capability，本章是完整参数展开）
- [[Ch12-App应用启动与关闭]]（capability 最终喂给 webdriver.Remote 启动会话）
- [[Ch09-Appium原理解析]]（Desired Capabilities 通过 POST /session 发给 Server）
