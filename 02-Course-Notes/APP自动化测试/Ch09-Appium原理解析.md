---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 原理
course: APP自动化测试
chapter: Ch09-Appium原理解析
created: 2026-09-03
status: draft
---

# Ch09 - Appium 原理解析

## 课程来源
- 学习日期：

---

## 一、为什么要懂原理

### 知识点 1：四大应用价值

【课程原话/定义】

了解原理的价值：应对面试、分析与解决问题能力、二次开发与定制开发能力、提升架构能力。

【为什么？】

1. 面试：大厂爱问原理性知识，测候选人的研究能力。
2. 排障：Appium 架构复杂，安装使用常出问题，懂原理能定位是 Client、Server 还是设备端的问题。
3. 二次开发：懂设计才能按 Appium 的设计写插件。
4. 架构能力：每学一个框架的设计，都能提升设计模式与架构能力。

【必须掌握】

- 四大价值：面试 / 排障 / 二开 / 架构

【企业场景】

你在企业里，脚本报错时，懂原理能让你快速判断"是脚本写错了（Client）、还是 Server 没起来、还是设备上 adb 连不上"，而不是无头苍蝇式地全查一遍。

【面试考察】

面试官："为什么要研究 Appium 的原理？"

参考回答框架：排障能力（定位问题在哪一层）+ 面试 + 二次开发插件 + 提升架构能力。

【易错点】

| 误区 | 纠正 |
|------|------|
| 只会用 API 不碰原理 | 出问题只能靠猜，无法定位问题层级 |

【我的理解】

> （"懂原理"对排障最直接的价值是什么？举一个脚本报错时能靠原理缩小排查范围的例子。）

---

## 二、三大模块架构

### 知识点 2：Client / Server / 移动端

【课程原话/定义】

Appium 设计分三大模块，各司其职，符合设计模式的单一职责（这也是可拓展性强的原因）：

- Client 端：把与 Appium 的各种交互封装为可被调用的 API/工具，使用者通过 Inspector 或 Java/Python 客户端库调用 Server。
- Server 端：信息中转。启动 HTTP 服务接收 Client 请求，并把所有控制命令（adb 命令、自动化控制命令等）转发到被测 App 的移动端。
- 移动端：真正执行自动化测试的地方。

【为什么？】

1. 单一职责：三模块各管一段（发起 / 中转 / 执行），职责清晰，任何一层可替换、可扩展。
2. Server 是"中转站"：Client 不直接碰设备，统一通过 HTTP 请求发给 Server，Server 再翻译成设备命令——这就是"跨语言"能成立的原因（Client 只需要会说 HTTP，不用会说 adb）。
3. 移动端执行：真正的自动化动作（点击、输入）最终发生在设备上的 Appium 相关组件。

【必须掌握】

- 三模块职责 + 单一职责设计
- Server 的"中转"作用（HTTP 进、设备命令出）

【企业场景】

你在企业里，理解三模块后，看日志就能分清：请求发没发出去（Client 层）、Server 收没收到、命令转没转发到设备（Server 层）、设备上执行成没成功（移动端）。排查定位到具体层，问题就解决一半了。

【面试考察】

面试官："Appium 的架构分哪几层？各自职责？"

参考回答框架：Client（封装 API 发起请求）、Server（HTTP 服务，中转命令）、移动端（真正执行）；单一职责设计，可扩展。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 Client 直接操作设备 | Client 只发 HTTP 请求，操作设备的是 Server 转发 + 设备端执行 |
| 以为 Server 只是"转发"没别的事 | Server 还负责匹配 driver、转发 adb、端口映射、安装依赖等（见日志） |

【我的理解】

> （为什么"Server 做中转"是 Appium 跨语言、跨平台的关键？"Client 只要会说 HTTP"这句话怎么理解？）

---

## 三、通信过程与日志流转

### 知识点 3：一次 session 的完整流程

【课程原话/定义】

通过日志可以看到整个流转流程（关键信息）：

1. 环境检查：Appium 启动，加载 AndroidUiautomator2Driver。
2. 启动 4723 服务（电脑端）。
3. 发送 HTTP 请求 `POST /session`（含 capabilities 信息）。
4. 创建 session（AppiumDriver.createSession）。
5. 检查 driver 配置：按 automationName 'uiautomator2' 和 platformName 'Android' 匹配 driver。
6. 检查 ADB 环境，启动 adb server（adb -P 5037 start-server）。
7. 推送 settings apk（io.appium.settings）到设备。
8. 端口映射：本地 8200 → 设备 6790（adb forward tcp:8200 tcp:6790）。
9. 检查/安装 server apk（appium-uiautomator2-server）与 test apk。
10. 启动 UIAutomator2 server。
11. 用 adb 启动被测 App（adb shell am start ...）。

【为什么？】

1. POST /session 是 WebDriver 协议的核心：Client 用这一个请求把 capabilities 发给 Server，Server 据此决定用哪个 driver、连哪个设备。
2. 端口映射：Server 把本地端口（8200）转发到设备端口（6790），让 UIAutomator2 server 在设备上跑、被本地调用。
3. 两个 apk 是 Appium 的"内应"：io.appium.settings（设置类）+ appium-uiautomator2-server（执行类），Appium 靠它们在设备上执行自动化命令。
4. 最后 am start 才是真正拉起被测 App。

【必须掌握】

- POST /session + capabilities 的作用
- 端口映射（本地 8200 ↔ 设备 6790）
- 两个依赖 apk 的作用

【企业场景】

你在企业里，看 Server 日志排查时，卡在"端口映射"说明 Server 连到设备了但 UIAutomator2 没起来；卡在"Pushing settings apk"说明 adb 有问题。日志的每一段对应一个环节，是排障地图。

【面试考察】

面试官："描述一次 Appium 从创建 session 到启动 App 的完整流程。"

参考回答框架：Client 发 POST /session（带 caps）→ Server 匹配 driver → 检查/启动 adb → 推 settings apk → 端口映射 → 装/启动 UIAutomator2 server → am start 启动 App。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 App 直接由 Client 启动 | 是 Server 通过 adb am start 启动，Client 只发请求 |
| 忽略两个依赖 apk | io.appium.settings 和 appium-uiautomator2-server 是 Appium 在设备上的"执行器" |

【我的理解】

> （"端口映射 8200→6790"是为了解决什么问题？为什么不能直接让 Server 调用设备上的 UIAutomator2？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 原理价值 | 面试/排障/二开/架构 | ★★★☆☆ |
| 三大模块 | Client/Server/移动端 + 单一职责 | ★★★★★ |
| 通信流程 | POST /session → 匹配 driver → adb → 端口映射 → am start | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch08-Appium环境安装与使用]]（装好环境后，理解它怎么工作）
- [[Ch10-自动化测试用例结构分析]]（原理落地到脚本：capability → webdriver → 用例）
