---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - Inspector
  - 用例录制
course: APP自动化测试
chapter: Ch16-Appium Inspector与用例录制
created: 2026-09-07
status: draft
---

# Ch16 - Appium Inspector 与用例录制

## 课程来源
- 学习日期：

---

## 一、Appium Inspector 简介

### 知识点 1：Inspector 是什么 + 四大功能

【课程原话/定义】

Appium Inspector 是 Appium 的一个工具，用于帮助开发和测试人员分析和调试移动应用。它提供图形界面和交互式功能，能轻松检查 UI 元素、获取元素属性、执行操作、生成自动化测试脚本。

四大主要功能：

1. **元素定位和查看**：直接点击界面元素，Inspector 显示其属性（ID、类名、文本等），用于确定定位策略。
2. **执行操作**：提供操作按钮（点击、输入文本、滑动屏幕），验证应用的交互和功能。
3. **自动化脚本生成**：根据操作生成相应的测试脚本，作为起点再定制扩展。
4. **元素搜索和筛选**：按属性值、文本内容等条件搜索筛选，快速定位目标元素。

【为什么？】

1. Inspector 解决"盲定位"问题：不靠猜，直接点一下元素就能看到它真实的属性（resource-id、text 等），定位器就是这么拿到的。
2. "执行操作"和"脚本生成"让 Inspector 既是调试器又是生成器——先手动点一遍验证交互，再一键生成脚本起点。
3. 搜索筛选解决"页面元素太多找不到目标"的问题，比肉眼在源码树里翻快得多。

【必须掌握】

- Inspector 的四大功能：元素定位查看 / 执行操作 / 脚本生成 / 元素搜索筛选
- Inspector 的核心价值：可视化拿定位器 + 生成脚本起点

【企业场景】

你在企业里，Inspector 是"拿定位器"的第一工具：新页面要写用例，先开 Inspector 点一遍，把每个元素的 resource-id/accessibility-id 抄下来，比看代码猜准确一百倍。它也是排查"为什么定位不到"的现场——在 Inspector 里能不能点到那个元素，直接定位是定位器问题还是页面没加载。

【面试考察】

面试官："Appium Inspector 是干什么的？主要功能有哪些？"

参考回答框架：可视化检查和调试 App UI 的工具，四大功能：元素定位查看（点元素看属性）、执行操作（模拟点击/输入/滑动）、脚本生成（按操作生成脚本起点）、元素搜索筛选（按属性/文本定位）。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 Inspector 生成的脚本能直接用 | 录制脚本只是"起点"，缺 capability/setup/teardown/断言，要优化（呼应 Ch10） |
| Inspector 只能看不能操作 | 它能模拟点击/输入/滑动，既是查看器也是调试器 |

【我的理解】

> （Inspector 的"脚本生成"和"元素定位查看"是什么关系？为什么说录制脚本是"起点"而不是"终点"？）

---

## 二、配置启动（上）

### 知识点 2：安装 apk + 启动 Appium 服务

【课程原话/定义】

测试对象：Appium 官方 Demo apk（ApiDemos-debug.apk）。

安装 apk：拖拽到模拟器安装；或进入 apk 下载目录执行 `adb install ApiDemos-debug.apk`。

启动 Appium 服务：命令行输入 `appium`，成功启动服务。

【为什么？】

1. 练习需要一个真实可用的 App，ApiDemos 是官方 Demo，控件全（OS/Morse Code/滑动条等），是 Appium 的标准练习对象。
2. adb install 是命令行装 apk 的标准方式，拖拽只是图形化的等价操作——自动化/远程场景只能靠 adb。
3. Inspector 本身不启动 Appium，它只是客户端，必须先有 `appium` 服务在跑（呼应 Ch09 的 Client/Server 架构）。

【必须掌握】

- adb install xxx.apk 安装
- 命令行 appium 启动服务（Inspector 依赖它）

【企业场景】

你在企业里，真机/模拟器上装被测包是跑自动化的第一步；Appium Server 起不来，Inspector 连不上、脚本也起不来。记住"先起服务，再连 Inspector"这个顺序。

【面试考察】

面试官："用 Inspector 之前需要准备什么？"

参考回答框架：装好被测 apk（adb install）、启动 Appium 服务（appium 命令）、准备好设备的包名和启动 Activity。

【易错点】

| 误区 | 纠正 |
|------|------|
| 直接开 Inspector 就能用 | Inspector 是客户端，必须先在命令行起 appium 服务 |
| adb install 路径不对 | 要先 cd 到 apk 所在目录，或用绝对路径 |

【我的理解】

> （Inspector 和 Appium Server 是什么关系？"先起服务再连 Inspector"这个顺序如果反过来会怎样？）

---

## 三、配置启动（中）：获取被测 App 信息

### 知识点 3：获取包名与启动 Activity 的两种方法

【课程原话/定义】

配置 Desired Capabilities 需要被测 App 的包名和启动 Activity 名，两种获取方法：

**方法一（monkey）**：

```bash
# 一：找到当前设备所有软件
adb shell pm list packages

# 二：按关键词筛选包名
# mac
adb shell pm list packages | grep "软件名"
# windows
adb shell pm list packages | findstr "软件名"
# package:io.appium.android.apis

# 三：对指定应用执行一个 Monkey 测试事件，输出详细日志
adb shell monkey -p "包名" -vvv 1
# 日志里可见：cmp=io.appium.android.apis/.ApiDemos
```

**方法二（logcat）**：

```bash
# Mac
adb logcat ActivityManager:I | grep "START"
# Windows
adb logcat ActivityManager:I | findstr "START"
```

打印并筛选 adb 日志，重新打开被测 App，即可从日志得到 package 和 activity。

【为什么？】

1. 包名（package）和启动 Activity 是 Desired Capabilities 里 appPackage/appActivity 的必填值，拿错了会话起不来。
2. 方法一的精髓在第三步 monkey：`-p 包名` 指定应用、`-vvv` 详细日志、`1` 一个事件——日志里会打出 `cmp=包名/Activity`，直接抄。
3. 方法二 logcat 抓的是"Activity 启动"系统日志（ActivityManager 的 START），重开 App 时最新一条就是启动入口。

【必须掌握】

- 方法一：pm list packages → grep/findstr 筛包名 → monkey -p 包名 -vvv 1 拿 cmp
- 方法二：adb logcat ActivityManager:I | grep/findstr "START"
- Windows 用 findstr、Mac/Linux 用 grep

【企业场景】

你在企业里，接手一个没文档的 App 要写自动化，第一步就是这两条命令拿到 package 和 activity。这比找开发要"包名和入口"更快，也是测试自给自足的基本功。

【面试考察】

面试官："怎么获取一个 Android App 的包名和启动 Activity？"

参考回答框架：两种方法——① pm list packages 列出所有包 → 按关键词筛出包名 → monkey -p 包名 -vvv 1 看日志里的 cmp=包名/Activity；② adb logcat ActivityManager:I 抓 START 日志，重开 App 得到最新启动的 package 和 activity。

【易错点】

| 误区 | 纠正 |
|------|------|
| 原文 "Monkecy" | 正确拼写是 **Monkey**（猴子测试工具），原文笔误 |
| Windows 下还用 grep | Windows cmd 用 **findstr**，Mac/Linux 才用 grep |
| 只看包名不拿 Activity | appPackage 和 appActivity 两个都要，缺 Activity 起不来 |

【我的理解】

> （方法一 monkey 日志里的 `cmp=io.appium.android.apis/.ApiDemos` 拆成两部分看，分别对应哪个 capability？）

---

## 四、配置启动（下）：验证 Activity + Remote Path + Capability

### 知识点 4：am start 验证 + Remote Path + Desired Capability

【课程原话/定义】

验证 Activity（能启动就代表包名和 Activity 正确）：

```bash
adb shell am start -W -S -n io.appium.android.apis/.ApiDemos
# Stopping: io.appium.android.apis
# Starting: Intent { cmp=io.appium.android.apis/.ApiDemos }
# Status: ok
```

`-S` 代表先停止目标应用再启动；`-W` 代表展示启动时间信息。

配置 Remote Path：

- Remote Path：`/`
- 本机调试：Remote Host 127.0.0.1、Remote Port 4723

跟 Appium Server GUI 配置对应（IP、端口、地址）。IP 本机就配 127.0.0.1；Server 和 Inspector 不在同一台机器时，配 Server 所在机器 IP（Server GUI 的 HOST 也要配本机 IP，不能 0.0.0.0）。

配置 Desired Capability（最基本的）：

```json
{
   "platformName": "android",
   "appium:automationName": "uiautomator2",
   "appium:deviceName": "emulator-5554",
   "appium:appPackage": "io.appium.android.apis",
   "appium:appActivity": "io.appium.android.apis.ApiDemos"
}
```

保存：点 Save as 输入名字，重启后直接选，无需重输。Attach to Session：若 Appium 已连手机有 session，直接选 Session ID 加入，免配置。启动：点 Start Session 进入 Inspector 页面。

【为什么？】

1. `am start -W -S -n` 是"先验证再填配置"的好习惯：用 adb 独立验证包名+Activity 能启动，排除"配置写对但 App 本身起不来"的干扰。
2. Remote Path 是 Appium 2.x 的关键差异点：2.x 用 `/`，1.x 才用 `/wd/hub`——填错连不上。
3. appActivity 在这里写全限定名 `io.appium.android.apis.ApiDemos`，和前面例子的 `.ApiDemos`（前导点简写）等价，两者都能启动。

【必须掌握】

- am start -W -S -n 包名/Activity 验证（-S 先停、-W 显示启动时间）
- Remote Path：Appium 2.x 填 `/`
- Desired Capability 五个参数 + Save as + Attach to Session

【企业场景】

你在企业里，新 App 上线要接自动化，流程是：adb 拿包名和 Activity → am start 验证能启动 → 填 Inspector 的 Capability → 保存配置复用。Server 部署在远程机器时，Remote Host 填那台机器的 IP，本机调试才填 127.0.0.1。

【面试考察】

面试官："Appium 2.x 的 Remote Path 填什么？为什么 1.x 是 /wd/hub？"

参考回答框架：2.x 默认路径是 `/`（去掉了 /wd/hub）；1.x 兼容旧 WebDriver 客户端保留了 /wd/hub。这是 1.x→2.x 的迁移点之一。

【易错点】

| 误区 | 纠正 |
|------|------|
| 原文说"地址默认配置 /wd/hub" | 前面正文明确 Remote Path 填 `/`，/wd/hub 是 **1.x** 的写法，2.x 应填 `/`，原文两处矛盾（教程混写了新旧版本） |
| appActivity 前导点写错 | `.ApiDemos`（简写）和 `io.appium.android.apis.ApiDemos`（全限定名）都合法，但简写必须带点 |
| 远程调试 Remote Host 填 127.0.0.1 | Server 在别的机器要填那台机器 IP，本机才填 127.0.0.1 |

【我的理解】

> （Remote Path 的 `/` 和 `/wd/hub` 分别对应 Appium 哪个版本？为什么教程里会同时出现这两种写法？）

---

## 五、Inspector 基础功能

### 知识点 5：模式与操作按钮

【课程原话/定义】

启动 Session 进入 Inspector 页面后，基础功能按钮：

- **Native App Mode**：原生态 App 模式。
- **Web/Hybrid App Mode**：Web 和混合模式移动应用。
- **Select Elements**：选择元素。
- **Swipe By Coordinates**：通过坐标点滑动。
- **Tap By Coordinates**：通过坐标点点击。
- **Back**：返回按键。
- **Refresh Source & Screenshot**：刷新，同步移动端页面。
- **Start Recording**：录制按钮。
- **Search for element**：搜索定位表达式。
- **Quit Session & Close Inspector**：退出当前 Session。

【为什么？】

1. 两个 Mode 决定 Inspector 解析哪套页面结构：Native 解析原生控件树，Web/Hybrid 解析 H5 的 DOM——测混合 App 要切对模式。
2. Select Elements 是核心：进入"点谁看谁"模式；Swipe/Tap By Coordinates 是坐标手势（呼应 Ch15 的 tap 坐标）。
3. Start Recording 是录制入口，Refresh 是"手机页面变了重新同步"，两者配合完成"操作→同步→录制"的循环。

【必须掌握】

- Native App Mode vs Web/Hybrid App Mode 的区别
- Select Elements / Refresh / Start Recording 三个核心按钮

【企业场景】

你在企业里，测原生 App 用 Native 模式；测内嵌 H5 页面（如 App 里的活动页）要切 Web/Hybrid 模式才能定位到 H5 元素。Refresh 用得最频繁——手机页面切换后先刷新，源码树才跟得上。

【面试考察】

面试官："Native App Mode 和 Web/Hybrid App Mode 有什么区别？"

参考回答框架：Native 模式解析原生控件树（UIAutomator2/XCUITest），Web/Hybrid 模式解析内嵌 WebView 的 DOM，测混合 App 的 H5 部分要切 Web/Hybrid 模式。

【易错点】

| 误区 | 纠正 |
|------|------|
| 切页面后不 Refresh | 源码树还是旧页面的，要先 Refresh 同步 |
| 测 H5 还用 Native 模式 | 内嵌 H5 元素要切 Web/Hybrid 模式才能定位 |

【我的理解】

> （"Select Elements"和"Refresh Source & Screenshot"这两个按钮，在"定位元素"这个流程里分别扮演什么角色？）

---

## 六、元素定位与查看

### 知识点 6：Select Elements / 页面源码 / 元素属性 / 元素操作

【课程原话/定义】

同步到移动端页面后，点 Select Elements 进入选择元素模式，点页面元素即可查看元素源码和属性信息。

**查看页面源码**（App Source）：以 XML 树展示控件布局，可复制页面源码、下载页面源码。

**查看元素属性**（Selected Element）：查看选中元素的详细属性，定位元素就用这些属性。

**对选中元素的操作**：

- 点击（Tap）：发命令给 Appium 执行，成功后左侧生成新截图，失败显示错误消息。
- 输入文本（Send Keys）：前提是 EditText 输入框。
- 清空文本（Clear）：前提是 EditText 输入框。
- 复制元素属性：以 JSON 格式保存到粘贴板。

【为什么？】

1. Select Elements 是"点谁看谁"——选中后，右侧 App Source 定位到它在 XML 树的位置，Selected Element 面板列出它的属性，定位器就是这么确定的。
2. 源码树展示层级关系，是理解 XPath（父子/层级）的直观入口（呼应 Ch13 的页面结构）。
3. "复制元素属性"把属性以 JSON 存剪贴板，方便贴进脚本；点击/输入/清空是"边看边验证"——先手动确认元素能交互，再写进脚本。

【必须掌握】

- Select Elements 选中元素 → 看源码树 + 属性面板
- 页面源码可复制/下载；元素可点击/输入/清空/复制属性

【企业场景】

你在企业里，标准定位流程是：Select Elements 点目标元素 → Selected Element 面板抄 resource-id/content-desc → 用"点击/输入"按钮手动验证能操作 → 把定位器和操作写进脚本。这套"先验证再编码"能少踩很多"定位到了但点不动"的坑。

【面试考察】

面试官："在 Inspector 里怎么确定一个元素的定位策略？"

参考回答框架：Select Elements 模式点中元素，在 Selected Element 面板看它的属性（resource-id、content-desc、text、class），挑一个稳定唯一的属性作为定位器；还可以在 App Source 源码树里看层级辅助 XPath。

【易错点】

| 误区 | 纠正 |
|------|------|
| 只看 text 不核对 resource-id | text 易变，优先 resource-id/content-desc（呼应 Ch13） |
| 不手动点一遍就直接写脚本 | 先在 Inspector 里点击/输入验证元素可交互，再写脚本，避免"定位到但点不动" |

【我的理解】

> （Inspector 里"复制元素属性"得到的是 JSON——它和写脚本时的 find_element(AppiumBy.ID, "...") 之间是怎么衔接的？）

---

## 七、自动化用例录制

### 知识点 7：录制步骤 + 示例

【课程原话/定义】

录制步骤：

1. 点 Start Recording 进入录制状态。
2. 在同步过来的界面中选择元素。
3. 在 Selected Elements 界面进行操作。
4. 操作结束点 Pause Recording 结束录制。
5. 在 Recorder 界面展示录制脚本。

用例录制示例（测试步骤）：

1. 打开 API Demo 应用。
2. 点击 OS，进入下个界面。
3. 点击【Morse Code】。
4. 输入内容【ceshiren.com】。
5. 返回上一个页面。
6. 返回上一个页面。

【为什么？】

1. 录制的本质是"记录你点过的元素和操作"：Inspector 把每一步（点哪个元素、输什么）转成 find_element + click/send_keys 代码。
2. 录制产出的就是 Ch10 知识点2 里那个"原始版脚本"——只有定位 + 操作，缺 capability、setup/teardown、断言。
3. 课程自己也强调：录制功能主要适合初学者学习阶段，进入编码阶段后要靠更高级的框架（PO 等）维护。

【必须掌握】

- 录制五步：Start Recording → 选元素 → 操作 → Pause Recording → Recorder 看脚本
- 录制脚本是"起点"，不是"终点"

【企业场景】

你在企业里，录制只用于"快速拿某段交互的定位器代码"，很少直接把录制结果上生产。真正的用例还是手写进 pytest + PO 框架。录制的价值是"省去手写定位器"，不是"省去设计用例"。

【面试考察】

面试官："Inspector 录制的脚本能直接用于回归吗？"

参考回答框架：不能。录制脚本只有定位+操作，缺 capability、setup/teardown、断言，且是面条代码不可维护；它只是脚本起点，需要放进框架（pytest/PO）里重构后才能回归。

【易错点】

| 误区 | 纠正 |
|------|------|
| 录制脚本直接上生产 | 缺断言、缺清理、不可维护，只当起点 |
| 依赖录制替代写框架 | 录制是"省手写定位器"，框架（PO/数据驱动）还是要自己搭 |

【我的理解】

> （录制的每一步操作，最终会对应成哪几行代码？"返回上一个页面"对应 driver 的什么方法？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Inspector 简介 | 四大功能 | ★★★☆☆ |
| 配置启动 | adb install + appium 服务 | ★★★★☆ |
| 获取包名/Activity | monkey / logcat 两方法 | ★★★★★ |
| 验证 + Remote Path + Capability | am start / `/` vs /wd/hub | ★★★★★ |
| 基础功能 | Native vs Web/Hybrid + 按钮 | ★★★★☆ |
| 元素定位与查看 | Select Elements / 源码 / 属性 | ★★★★☆ |
| 用例录制 | 录制步骤 + 脚本是起点 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch10-自动化测试用例结构分析]]（知识点2 录制脚本输出，本章是完整的 Inspector 工具用法）
- [[Ch11-Capability配置参数解析]]（Desired Capability 的完整参数，本章讲怎么在 Inspector 里填）
- [[Ch13-常见控件定位方法]]（Inspector 拿到的属性就是定位策略的来源）
- [[Ch09-Appium原理解析]]（Inspector 是 Client，连的是 Appium Server）
