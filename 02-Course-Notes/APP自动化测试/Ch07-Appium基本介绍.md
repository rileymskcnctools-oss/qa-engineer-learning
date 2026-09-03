---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
course: APP自动化测试
chapter: Ch07-Appium基本介绍
created: 2026-09-03
status: draft
---

# Ch07 - Appium 基本介绍

## 课程来源
- 学习日期：

---

## 一、Appium 是什么

### 知识点 1：Appium 的定位

【课程原话/定义】

Appium 是一款开源框架，拥有丰富的生态系统和强大的社区支持，一直受到开发者的积极维护。作为一种灵活的跨平台测试自动化工具，Appium 能在 iOS、Android、Windows 和 Mac 设备上执行移动应用的自动化测试，并支持用相同的 API 编写适用于多个平台的测试脚本。

Appium 与 Selenium 类似，是一个跨语言的自动化框架，可与任何测试框架结合使用。支持 Java、JavaScript、PHP、Ruby、Python、C# 等语言。

【为什么？】

1. "跨平台"和"跨语言"是 Appium 的两个核心卖点：一套 API 能写多个平台的脚本，团队用自己熟悉的语言写，不用学新语言。
2. "与 Selenium 类似"是理解 Appium 的钥匙：它复用了 WebDriver 协议（Selenium 的通信协议），所以熟悉 Selenium 的人上手 Appium 非常快。
3. 开源 + 社区强 → 踩坑有人答、更新有人维护，长期成本低。

【必须掌握】

- Appium = 开源 + 跨平台 + 跨语言 + WebDriver 协议
- 一句话定位：移动端的 Selenium

【企业场景】

你在企业里，团队会 Python 或 Java，产品同时有 Android 和 iOS 两端，Appium 让你一套脚本两端跑，维护成本最低——这是大多数测试团队选它的直接原因。

【面试考察】

面试官："介绍一下 Appium。"

参考回答框架：开源框架 → 跨平台（iOS/Android/Windows/Mac）→ 跨语言（Java/Python/JS...）→ 基于 WebDriver 协议 → 与 Selenium 同源，所以叫"移动端的 Selenium"。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 Appium 只能测手机 | 还能测 Windows、Mac 桌面应用（对应 Windows Driver / Mac2 Driver） |
| 以为 Appium 是"测试框架" | 它是"自动化框架/引擎"，用例组织还要靠 Pytest/JUnit 等测试框架配合 |

【我的理解】

> （"跨平台"和"跨语言"分别解决了企业里的什么痛点？为什么"与 Selenium 类似"能让 Selenium 老手上手更快？）

---

## 二、Appium 的优势

### 知识点 2：五大优势

【课程原话/定义】

1. 支持的应用类型（原生 / 混合 / 移动 Web）
2. 跨平台和跨设备支持
3. WebDriver 协议
4. 第三方工具和集成
5. Appium Drivers（引擎体系）

【为什么？】

1. 应用类型：原生 App、混合 App（内嵌 WebView）、移动 Web 都能测，覆盖面广。
2. 跨平台跨设备：Android/iOS/Windows/Mac + 真机/模拟器都能跑，一份脚本多处复用。
3. WebDriver 协议：这是"跨语言"的技术基础——协议统一了客户端和服务器之间的通信，任何语言只要有客户端库就能调。
4. 第三方工具/集成：能接 Jenkins 等 CI、能配 Allure 报告，能进流水线规模化。
5. Drivers 引擎：通过切换底层引擎适配不同平台/技术栈（见知识点 3）。

【必须掌握】

- 五大优势各能说一句
- WebDriver 协议是"跨语言"的技术根基

【企业场景】

你在企业里，Appium 五大优势里最常被用到的两条是"跨平台跨设备"（一套脚本测两端）和"第三方集成"（挂 Jenkins 每天回归）——前者省人力，后者让自动化从"本地跑"变成"流水线跑"。

【面试考察】

面试官："Appium 有哪些优势？"

参考回答框架：应用类型全覆盖 + 跨平台跨设备 + WebDriver 协议（跨语言基础）+ 第三方集成 + 多引擎可切换。

【易错点】

| 误区 | 纠正 |
|------|------|
| 把"优势"背成"性能强" | Appium 优势是"覆盖面广 + 灵活"，不是速度最快、稳定性最好 |
| 忽略 WebDriver 协议 | 它是"一套 API 多种语言"的技术前提，没有它谈不上跨语言 |

【我的理解】

> （五大优势里哪一条是"其它四条成立的技术前提"？为什么？）

---

## 三、Appium Drivers（引擎体系）

### 知识点 3：多平台引擎

【课程原话/定义】

Drivers 即 Appium 引擎，是框架核心组件，负责驱动和控制移动设备/模拟器以执行自动化脚本。Drivers 最初只是 Node.js 类，Appium 把它扩展为 BaseDriver，是对整个 WebDriver 协议的封装。

- iOS 引擎：XCUITest（默认引擎，测 iOS 原生）、WebDriverAgent（基于 XCUITest 的开源框架）
- Android 引擎：UiAutomator2（默认引擎，测 Android 原生）、Espresso（UI 自动化）、Selendroid（支持旧版 Android）
- 其他引擎：Chromium Driver（Chrome 浏览器）、Flutter Driver（Flutter 应用）、Windows Driver（Windows 桌面）、Mac2 Driver（Mac 桌面）

【为什么？】

1. "引擎可切换"是 Appium 灵活性的来源：同一套脚本，通过 automationName 切换底层引擎，就能适配不同平台。
2. UiAutomator2 是 Android 默认引擎，因为它基于 Android 官方 UiAutomator 框架，稳定、支持系统级操作；XCUITest 是 iOS 默认引擎，基于 Apple 官方 XCUITest 框架。
3. 默认引擎之外的（Espresso/Selendroid/Flutter 等）覆盖特殊场景：Espresso 更快更贴近 App 代码、Selendroid 支持老系统、Flutter Driver 测 Flutter 应用。

【必须掌握】

- UiAutomator2（Android 默认）/ XCUITest（iOS 默认）是两大主力引擎
- automationName 用来指定引擎
- 各引擎对应什么平台

【企业场景】

你在企业里，99% 的情况用两个默认引擎：Android 配 UiAutomator2、iOS 配 XCUITest。遇到 Flutter 应用才切 Flutter Driver。选引擎的决策点是"被测 App 用什么技术栈"，不是"哪个引擎名气大"。

【面试考察】

面试官："Appium 测 Android 和 iOS 分别用什么引擎？"

参考回答框架：Android 默认 UiAutomator2（基于官方 UiAutomator 框架）；iOS 默认 XCUITest（基于官方 XCUITest 框架，底层是 WebDriverAgent）。通过 automationName 指定。

【易错点】

| 误区 | 纠正 |
|------|------|
| 把 WebDriverAgent 和 XCUITest 当成两个独立引擎 | WDA 是基于 XCUITest 的开源实现，iOS 默认引擎就是 XCUITest，二者不是并列关系 |
| 把 Selendroid 当主力 | 它只用于旧版 Android（4.x），新项目直接用 UiAutomator2 |
| Espresso 和 UiAutomator2 混为一谈 | Espresso 是 Google 的 UI 测试框架（更快、更白盒），Appium 默认用 UiAutomator2 |

【我的理解】

> （"Drivers 是对 WebDriver 协议的封装（BaseDriver）"这句话怎么理解？为什么封装了协议就能跨平台？）

---

## 四、Appium 生态工具

### 知识点 4：Drivers / Clients / Plugins / Related-Tools

【课程原话/定义】

Appium 生态包含四个部分：

- Drivers（必需）：适用于多平台的驱动程序
- Clients（必需）：各语言的客户端封装库，用于连接 Appium Server
- Plugins（可选）：提供各种方式扩展 Appium 功能
- Related-Tools（辅助）：与测试无直接关系的辅助工具
  - Appium Inspector：用来做元素定位
  - Appium Doctor：检测 Appium 环境安装、检测常见问题

【为什么？】

1. Drivers 和 Clients 是必需的：没有 Driver 不能驱动设备，没有 Client 不能从代码连 Server。
2. Plugins 可选：把非核心功能（如图像识别）拆到插件，按需安装，让 Server 更轻量。
3. Related-Tools 是"周边"：Inspector 解决"元素怎么定位"（写脚本最大痛点），Doctor 解决"环境怎么排错"。

【必须掌握】

- 四件套各自的定位和必需/可选
- Inspector 定位元素、Doctor 检查环境

【企业场景】

你在企业里，日常最常用的是 Appium Inspector（定位元素、复制定位器代码），环境出问题先跑 appium-doctor 看缺什么。这两件工具一个服务"写脚本"，一个服务"排环境"。

【面试考察】

面试官："Appium 的生态包含哪些部分？"

参考回答框架：Drivers（必需，驱动设备）、Clients（必需，语言库连 Server）、Plugins（可选，扩展功能）、Related-Tools（Inspector 定位、Doctor 查环境）。

【易错点】

| 误区 | 纠正 |
|------|------|
| Clients 和 Drivers 分不清 | Clients 在"代码侧"（pip install Appium-Python-Client），Drivers 在"Server 侧"（appium driver install uiautomator2） |
| 以为 Inspector/Doctor 是必需 | 它们是辅助工具，可装可不装，但强烈建议装 |

【我的理解】

> （Clients 和 Drivers 一个在代码侧、一个在 Server 侧——画一条"脚本 → Client → Appium Server → Driver → 设备"的链路，标出每一环属于生态的哪个部分。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Appium 定位 | 开源 + 跨平台 + 跨语言 + WebDriver 协议 | ★★★★☆ |
| 五大优势 | 应用类型/跨平台/协议/集成/引擎 | ★★★☆☆ |
| Drivers 引擎 | UiAutomator2（Android）/ XCUITest（iOS） | ★★★★★ |
| 生态工具 | Drivers/Clients/Plugins/Related-Tools | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch06-App自动化测试价值与体系]]（本章之前：App 自动化价值与选型，Appium 是选型结论）
- [[Ch08-Appium环境安装与使用]]（本章之后：把 Appium 装上）
- [[Web自动化测试/README|Web自动化测试]]（同属 UI 自动化，Appium 是移动端这一层，Web 端对应 Selenium）
