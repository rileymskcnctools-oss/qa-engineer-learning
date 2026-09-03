---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 环境搭建
course: APP自动化测试
chapter: Ch08-Appium环境安装与使用
created: 2026-09-03
status: draft
---

# Ch08 - Appium 环境安装与使用

## 课程来源
- 学习日期：

---

## 一、环境全景：七大组件

### 知识点 1：七件套各自职责

【课程原话/定义】

Appium 服务安装及代码测试需要的基本环境：JDK、Android SDK、Node.js、Appium 服务、Appium Inspector、Appium 客户端、移动设备平台工具。

【为什么？】

1. JDK：UiAutomator2 用 Java 编写、与 Android App 交互，所以要 JDK。
2. Android SDK：Appium 通过 SDK 与设备通信、管理模拟器、执行测试（adb 就在 SDK 的 platform-tools 里）。
3. Node.js：命令行版 Appium Server 是 Node.js 写的，要用 npm 安装。
4. Appium 服务：核心，接收脚本命令并转发给设备。
5. Inspector：辅助定位元素。
6. 客户端：你写脚本所用的语言库。
7. 设备工具：真机/模拟器 + 对应平台工具（Android 的 SDK、iOS 的 Xcode）。

【必须掌握】

- 七个组件各解决什么问题
- 核心依赖链：Node.js（装 Server）→ JDK + Android SDK（跑 Android）→ 客户端（写脚本）

【企业场景】

你在企业里，新电脑装 Appium 环境，报错基本都能用"缺哪一环"定位：Server 起不来查 Node，连不上设备查 adb/SDK，元素定位不了查 Inspector。所以先把七件套的职责记牢，排错快一倍。

【面试考察】

面试官："Appium 测试需要哪些环境？各自作用？"

参考回答框架：JDK（UiAutomator2 是 Java 写的）、Android SDK（adb 通信）、Node.js（npm 装 Server）、Appium Server（核心）、Inspector（定位）、客户端库（写脚本）、设备工具（真机/模拟器）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 只装 Appium Server 就能跑 | 没有 JDK/SDK/adb，Server 起得来也连不上 Android 设备 |
| 漏装 Node.js | Appium 2.x 只有命令行版，必须用 npm 装，Node.js 是前提 |

【我的理解】

> （如果命令行报 adb "command not found"，是七件套里哪一环缺了？如果 appium 命令不存在呢？）

---

## 二、Android SDK 与 JDK

### 知识点 2：SDK 安装与环境变量

【课程原话/定义】

- JDK：参考安装教程安装（UiAutomator2 需要）。
- Android SDK：用 Android Studio 安装（推荐），或下载独立 SDK。装好后在 Android Studio 欢迎界面的 SDK Manager 里，SDK Tools 目录下勾选安装需要的工具。
- Windows 环境变量：新增系统变量 ANDROID_HOME（值 = SDK 根目录），Path 加 `%ANDROID_HOME%\emulator`、`%ANDROID_HOME%\platform-tools`、`%ANDROID_HOME%\tools`、`%ANDROID_HOME%\tools\bin`。
- MacOS：在 .bash_profile 里 export ANDROID_HOME 和 PATH。
- 验证：命令行输入 `adb --version`，输出版本号即成功。

【为什么？】

1. 用 Android Studio 装 SDK 是推荐方式，因为它顺带装好 JDK、SDK Manager、AVD 模拟器管理，一站式。
2. ANDROID_HOME 是 Appium/adb 找 SDK 的"路标"——没配它，Appium 找不到 adb 和 build-tools。
3. platform-tools 里有 adb（连设备），emulator 里有模拟器命令，tools / tools\bin 里有 sdkmanager/avdmanager。

【必须掌握】

- ANDROID_HOME 指向 SDK 根目录
- Path 加哪几个子目录（emulator / platform-tools / tools / tools\bin）
- adb --version 验证

【企业场景】

你在企业里，最常踩的坑是"配了 ANDROID_HOME 但忘了把 platform-tools 加进 Path"，结果命令行 adb 能用但 Appium 找不到。记牢：ANDROID_HOME 是给程序找 SDK 用的，Path 是给你在命令行直接敲 adb 用的，两个都要配。

【面试考察】

面试官："Android 环境怎么配置和验证？"

参考回答框架：ANDROID_HOME 指向 SDK 根目录 → Path 加 emulator/platform-tools/tools/tools\bin → 命令行 adb --version 验证。

【易错点】

| 误区 | 纠正 |
|------|------|
| 只配 ANDROID_HOME 不配 Path | 命令行敲不了 adb；两个都要配 |
| 变量值写成某个具体工具路径 | ANDROID_HOME 是 SDK 根目录，不是 platform-tools 目录 |

【我的理解】

> （ANDROID_HOME 和 Path 各服务谁？为什么"程序找 SDK"和"你敲 adb"是两件不同的事？）

---

## 三、Node.js

### 知识点 3：Node.js 安装与验证

【课程原话/定义】

命令行版 Appium Server 需要 Node.js，建议 14.17.0、16.13.0 或不小于 18.0.0。安装时勾选 "Add to PATH"（选中会自动配置环境变量）。验证：`node -v`、`npm -v` 输出版本号。

【为什么？】

1. Appium Server 2.x 是 Node.js 项目，用 npm 安装（npm install -g appium），所以 Node.js 是硬前提。
2. "Add to PATH" 勾上后，node/npm 命令全局可用，否则要在安装目录下才能执行。
3. 版本有下限：太低版本跑不了新版 Appium。

【必须掌握】

- 版本要求（>=18 最稳）
- 安装时勾 Add to PATH
- node -v / npm -v 验证

【企业场景】

你在企业里，node -v 输出版本号就说明 Node 装好了；如果 npm install -g appium 报权限/路径错，多半是没勾 Add to PATH 或没有管理员权限。

【面试考察】

面试官："为什么装 Appium 要先装 Node.js？"

参考回答框架：Appium 2.x 是 Node.js 项目，靠 npm 安装，Node.js 是运行前提。

【易错点】

| 误区 | 纠正 |
|------|------|
| 版本任意 | 太低版本跑不了 Appium 2.x，建议 >=18 |
| 装完 Node 就直接跑 appium | Node 只是前提，还要再装 Appium 本体（npm install -g appium） |

【我的理解】

> （"Node.js 是前提，Appium 才是本体"——装好 Node 后 node -v 能输出版本号，但这时 appium 命令能用吗？为什么？）

---

## 四、Appium Server 2.x

### 知识点 4：Server 安装与驱动安装

【课程原话/定义】

- GUI 版：对应 Appium 1.x，官方已停止更新。
- 命令行版：Appium 2.x，`npm install -g appium` 安装，输入 `appium` 启动，出现 "Welcome to Appium v2.0.0" 即成功。
- 2.x 必须单独装驱动：`appium driver install uiautomator2`。
- 可选 appium-doctor：`npm install -g appium-doctor`，`appium-doctor` 验证环境，所需环境前方为 "√" 即安装成功。

【为什么？】

1. 2.x 把驱动拆出 Server 本体，Server 更轻量，按需装驱动（这是 1.x→2.x 最大的架构变化）。
2. 2.x 装完 Server 只是"空壳"，必须 appium driver install uiautomator2 装上 Android 引擎才能跑 Android。
3. appium-doctor 把环境检查自动化，缺 JDK/SDK/adb 一眼看出。

【必须掌握】

- npm install -g appium
- appium driver install uiautomator2（2.x 必须单独装）
- appium-doctor 验证

【企业场景】

你在企业里，装完 appium 直接跑脚本会报 "driver not installed"，因为 2.x 忘了装 uiautomator2 驱动——这是 2.x 最常见的坑。环境出问题先 appium-doctor，看哪个项不是 √。

【面试考察】

面试官："Appium 2.x 装完 Server 就能测 Android 了吗？"

参考回答框架：不能。2.x 把驱动拆出本体，必须再 appium driver install uiautomator2 装 Android 引擎。

【易错点】

| 误区 | 纠正 |
|------|------|
| 装完 appium 就能测 | 2.x 必须单独装驱动 |
| GUI 和命令行一起装 | 二选一；GUI 对应 1.x 已停更，建议用 2.x 命令行 |

【我的理解】

> （2.x 为什么要把驱动拆出来？"轻量 Server + 按需装驱动"相比 1.x 的"全家桶"，好处是什么？）

---

## 五、Appium 1.x vs 2.x 差异

### 知识点 5：四大差异

【课程原话/定义】

1. 默认服务器基本路径：Appium 1 默认接受 http://localhost:4723/wd/hub；Appium 2 的默认基本路径改为 /。
2. 单独安装驱动：1.x 驱动随主服务一起装；2.x 拆出，可分开装（appium driver install ...）或一起装（`npm i -g appium --drivers=xcuitest,uiautomator2`）。
3. capability 需加前缀：任何非标准功能都要供应商前缀，如 appium:app、appium:noReset、appium:deviceName；W3C 标准功能（browserName、platformName）不加。
4. 图像分析功能移到插件：appium plugin install images，运行 appium --use-plugins=images。
5. 支持配置文件：JSON/JS/YAML，appium --config-file /path/to/config/file 指定。

【为什么？】

1. /wd/hub 是 Selenium1→2 迁移的历史遗留约定，2.x 不再和 Selenium 强绑定，默认路径改为 /。
2. 驱动拆出 = Server 轻量化 + 用户按需装。
3. capability 前缀：W3C 标准功能不加前缀，非标准功能加 appium:，避免各家 vendor 命名冲突。
4. 图像功能拆到插件，保持 Server 核心精简。
5. 配置文件让"一堆命令行参数"落成文件，便于版本管理和复用。

【必须掌握】

- 路径差异（/wd/hub vs /）
- 驱动拆分 + capability 前缀 + 图像插件

【企业场景】

你在企业里，从 Appium 1.x 脚本迁移到 2.x，最常见的三处改动：①URL 去掉 /wd/hub；②capability 加 appium: 前缀；③驱动单独装。这三点就是 1.x→2.x 迁移清单。

【面试考察】

面试官："Appium 1.x 和 2.x 有什么区别？"

参考回答框架：默认路径（/wd/hub→/）、驱动拆分（单独装）、capability 加 appium: 前缀、图像功能拆到插件、支持配置文件。

【易错点】

| 误区 | 纠正 |
|------|------|
| 脚本 1.x 直接跑 2.x | URL 要去掉 /wd/hub，capability 要加 appium: 前缀 |
| "标准 capability 也要加前缀" | 只有非标准功能加 appium:，browserName/platformName 等 W3C 标准不加 |
| 照抄原文 `--dirvers=xuitest` | 原文有两处笔误，正确应为 `--drivers=xcuitest`（dirvers→drivers、xuitest→xcuitest） |

【我的理解】

> （为什么 W3C 标准功能不加前缀，非标准功能要加？加前缀解决的是什么冲突？）

---

## 六、客户端库与设备工具

### 知识点 6：Python/Java 客户端 + mumu 模拟器

【课程原话/定义】

- Python 客户端：`pip install Appium-Python-Client`
- Java 客户端：maven 依赖 io.appium:java-client:8.0.0-beta
- 移动设备平台工具：Android 装 SDK + 平台版本/工具；iOS 装 Xcode + 模拟器/真机。
- mumu 模拟器：官网 https://mumu.163.com/ 下载安装；设置中心把界面调成 1280*720 手机大小，保存后重启。

【为什么？】

1. 客户端库是"脚本 → Server"的桥梁，语言不同库不同。
2. Android 用 SDK 管设备，iOS 必须用 Xcode（iOS 测试的硬门槛是 Mac 环境）。
3. mumu 是 Android 模拟器的一种，调成 1280*720 是模拟手机屏幕比例，避免元素因分辨率错位。

【必须掌握】

- pip install Appium-Python-Client
- iOS 测试需要 Xcode（Mac 环境）
- mumu 设置 1280*720

【企业场景】

你在企业里，iOS 自动化测试的隐性成本是"必须有一台 Mac + Xcode"，这是 iOS 比 Android 难上自动化的根本原因。Android 端用 mumu/Genymotion/真机都行，成本低很多。

【面试考察】

面试官："iOS 和 Android 自动化环境最大的差别是什么？"

参考回答框架：iOS 必须有 Mac + Xcode + 签名证书，门槛高；Android 用 SDK + 任意模拟器/真机，成本低。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 iOS 也能在 Windows 上随便测 | iOS 自动化基本依赖 Mac + Xcode |
| 客户端库版本随意 | Java 客户端示例是 8.0.0-beta，注意与 Appium 2.x 匹配 |

【我的理解】

> （为什么 iOS 自动化是 Mac 生态的"绑定"？客户端库在整条链路里扮演什么角色？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 七大环境 | JDK/SDK/Node/Server/Inspector/客户端/设备 | ★★★★☆ |
| Android SDK | ANDROID_HOME + Path + adb 验证 | ★★★★☆ |
| Node.js | Add to PATH + node -v/npm -v | ★★☆☆☆ |
| Appium Server 2.x | npm 安装 + 单独装驱动 + doctor | ★★★★★ |
| 1.x vs 2.x | 路径/驱动/capability 前缀/插件/配置 | ★★★★★ |
| 客户端与设备 | Python/Java 库 + mumu + Xcode | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch07-Appium基本介绍]]（先认识 Appium 是什么、Drivers 是什么，再装它）
- [[Ch09-Appium原理解析]]（装完之后，理解 Client/Server/设备是怎么通信的）
