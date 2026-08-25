---
tags: [课程笔记, Web自动化测试, Selenium, SeleniumIDE, 录制回放]
course: "Web自动化测试"
chapter: "Ch03-SeleniumIDE用例录制"
created: 2026-08-25
status: draft
---

# Ch03 - Selenium IDE 自动化用例录制

## 课程来源
- 学习日期：

---

## 一、Selenium IDE 是什么

### 知识点 1：定义、优势与局限

【课程原话/定义】
Selenium IDE 是一个**浏览器扩展**，用于记录和回放用户的操作。

Selenium 的集成开发环境（Selenium IDE）是一个易于使用的浏览器扩展，使用现有的 Selenium 命令记录用户在浏览器中的操作，参数由每个元素的上下文定义。它提供了**学习 Selenium 语法的绝佳方式**。适用于 Google Chrome、Mozilla Firefox 和 Microsoft Edge。

缺点也很明显：

- 录制回放方式的**稳定性和可靠性有限**
- 只支持 Firefox、Chrome（及 Edge）
- 对于**复杂的页面逻辑处理能力有限**

【为什么？】
录制回放为什么天生不稳？因为录制器只能"看到你点了哪个 DOM 节点"，它**不知道你的业务意图**，于是只能自动生成一个能唯一命中该节点的定位表达式，通常是这种：

```
css=#ember18-header .name
xpath=//*[@id="ember77"]
```

`ember18`、`ember77` 是前端框架（Ember/React/Vue）**运行时动态生成的 ID**，刷新页面就变。人写脚本会选 `text()="类别"` 或 `data-test-id` 这类稳定属性，机器不会——它不知道哪个属性稳定。

第二个原因是**时序**：录制时你是"看到页面出来了才点"，人眼天然做了等待；录制器不会记录"我等了 2 秒"，只会记录"点击"。回放速度比人快得多，元素还没渲染出来就点 → `NoSuchElementException`。这就是为什么导出的代码里到处是 `time.sleep(2)`。

所以 IDE 的正确定位是：**学习工具和脚手架**，不是生产工具。

【必须掌握】
- Selenium IDE = 浏览器扩展，录制 + 回放 + 导出代码
- 核心价值：快速上手、学习 Selenium 语法、辅助获取元素定位表达式
- 三大局限：定位不稳（动态 ID）、无等待策略（时序脆弱）、复杂逻辑（条件/循环/参数化）搞不定
- 生产环境用 WebDriver 手写代码，不用录制脚本

【企业场景】
你所在团队的功能测试同学不会写代码，但想参与自动化。可行的分工：让他们用 IDE 录制核心业务的操作路径，你把录制结果当作"操作步骤说明书"，然后手写成 PO + Pytest 的正式脚本。IDE 在这里的作用是**沟通媒介 + 定位器来源**，不是最终交付物。

【面试考察】
面试官："你用过 Selenium IDE 吗？为什么企业里不用录制回放做自动化？"

参考回答框架：
1. 用过，入门阶段用它理解 Selenium 命令、快速拿元素定位表达式
2. 不用于生产的原因：①录制生成的定位器依赖动态属性，页面一变就失效 ②没有等待策略，回放比人快导致时序失败 ③无法做参数化、条件判断、循环、断言组织 ④不能分层复用，页面改动要重录而不是改一处
4. 正确做法：手写 WebDriver + PO 分层 + 显式等待 + Pytest 参数化
5. 一句话总结：**录制解决"怎么点"，工程化解决"怎么维护"**

【易错点】

| 误区 | 纠正 |
|------|------|
| 录制回放就是自动化测试 | 只是自动化的入门形态，缺断言组织、参数化、可维护性 |
| IDE 导出的代码可以直接用 | 必须改造：换稳定定位器、sleep 换显式等待、加断言 |
| IDE 不稳定所以完全没用 | 拿定位表达式、验证操作可行性仍然很省时间 |
| 学会 IDE 就算学会 Selenium | IDE 会随技术成长贬值，WebDriver + 设计能力才是资产 |

【我的理解】
> （录制出来的定位器是 `#ember77`，你会怎么把它换成一个"页面改版也不容易坏"的定位器？想想有哪些稳定属性可选）

---

### 知识点 2：使用场景与技术价值周期

【课程原话/定义】
使用场景：

- 刚开始入门 UI 自动化测试
- 团队代码基础较差
- **技术成长之后学习价值不高**

注意：Selenium IDE 更适合简单的自动化测试任务，对于复杂的测试需求和更高级的自动化任务，需要使用 **WebDriver** 或其他自动化工具。

【为什么？】
"技术成长之后学习价值不高"这句话，是课程里最诚实也最重要的一句。它说明了一类工具的共同规律：**降低入门门槛的工具，往往同时封住了上限。**

| 阶段 | IDE 的价值 | 原因 |
|------|-----------|------|
| 第 1 周（零基础） | 高 | 立刻看到"浏览器自己动起来了"，建立正反馈；直观理解命令-目标-值模型 |
| 第 2-4 周（学 WebDriver） | 中 | 当"元素定位表达式的取值器"用，比手动扒 DOM 快 |
| 之后（能写框架） | 低 | 手写更快更稳，且需要参数化/分层/等待，IDE 全给不了 |

所以正确的用法是：**用它建立直觉，然后果断放下。** 面试时如果只会 IDE，反而是减分项——它意味着你没有代码能力。

【必须掌握】
- 适用：入门期、演示、快速验证某个操作路径可行、快速取定位表达式
- 不适用：需要参数化/数据驱动、复杂断言、条件与循环、长期维护的项目
- 复杂需求一律用 WebDriver 手写
- 本章的复习优先级：⭐（了解即可）；真正要精通的是元素定位与 WebDriver API

【企业场景】
产品经理临时要一个"演示自动化能力"的 5 分钟 demo，明天上午就要。这时用 IDE 录一段核心流程回放，成本 10 分钟；手写脚本要 2 小时。**演示场景是 IDE 的最佳战场**——一次性、不需维护、要的是视觉效果。但如果领导接着说"那把这个纳入每晚回归"，就必须换成手写脚本，因为它要活很久。

【面试考察】
面试官："什么情况下你会选择录制工具，什么情况下坚持手写？"

参考回答框架：
1. 录制：一次性演示、快速验证路径、拿定位表达式、非技术同学参与
2. 手写：需要长期维护、需要参数化和数据驱动、需要分层复用、要进 CI
3. 判断依据：这段脚本**要活多久、要被改多少次**
4. 加分：两者可结合——录制产出"步骤 + 定位器"，人工重构成 PO 脚本

【易错点】

| 误区 | 纠正 |
|------|------|
| 团队代码差就长期用 IDE | 短期救急可以，长期会把技术债滚大；应同步提升代码能力 |
| 认为录制能省掉写脚本的工作 | 省的是"打字"，省不了"设计"；设计才是主要成本 |
| 在简历上重点写 Selenium IDE | 会被认为无代码能力，重点应是 WebDriver + Pytest + PO |

【我的理解】
> （"这段脚本要活多久"为什么能作为选录制还是手写的判断标准？用维护成本解释）

---

## 二、安装与项目创建

### 知识点 3：环境准备与安装

【课程原话/定义】

- 官网：https://www.selenium.dev/
- Chrome 插件：https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd
- Firefox 插件：https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/
- GitHub Release：https://github.com/SeleniumHQ/selenium-ide/releases
- 其它版本：https://addons.mozilla.org/en-GB/firefox/addon/selenium-ide/versions/

**注意：Chrome 插件在国内无法下载，Firefox 可以直接下载。**

安装完成后，通过在浏览器的菜单栏中点击图标启动。如果没看到图标，先确认是否安装了 Selenium IDE 扩展，可以通过点击菜单栏扩展程序按钮，找到并启动 Selenium IDE。

> 📷 【截图占位】浏览器菜单栏中的 Selenium IDE 图标

【为什么？】
国内下不了 Chrome 插件的根因是 Chrome 应用商店域名被墙。三条可行路径，优先级从高到低：

1. **用 Firefox**（课程推荐）：addons.mozilla.org 可直连，最省事
2. **GitHub Release 下载 .crx/.zip**，Chrome 打开 `chrome://extensions` → 开启"开发者模式" → 加载已解压的扩展程序
3. 走代理访问 Chrome 商店（本机有 Clash 代理，端口 10808）

【必须掌握】
- Selenium IDE 是**浏览器扩展**，装在浏览器里，不是 Python 库（和 `pip install selenium` 完全无关）
- Chrome 商店国内不可达 → 优先用 Firefox 或 GitHub Release 离线安装
- 装完从浏览器扩展栏点击图标启动

【企业场景】
公司电脑装了安全管控软件，禁止安装未审批的浏览器扩展。这时候你连 IDE 都用不上——只能手写 WebDriver。这也从侧面说明为什么正式项目不能依赖 IDE：**它对环境有额外要求，而 Python 脚本只要有解释器就能跑，在任何 CI 容器里都行。**

【面试考察】
（工具安装类内容面试基本不问，重点在知识点 1、2 的"为什么不用它"以及知识点 6 的定位表达式）

面试官可能顺口问："IDE 和 Selenium 库是一个东西吗？"

参考回答：不是。IDE 是浏览器扩展，做录制回放；`selenium` 是 Python 库，通过 WebDriver 协议驱动浏览器。IDE 能把录制结果导出成用 selenium 库写的代码，二者是"生成器"和"运行库"的关系。

【易错点】

| 误区 | 纠正 |
|------|------|
| `pip install selenium` 就装好了 IDE | 完全无关，IDE 是浏览器扩展 |
| 一直卡在 Chrome 商店打不开 | 直接换 Firefox 或 GitHub Release 离线装 |
| 装完找不到入口 | 在扩展程序列表里找并固定到工具栏 |

【我的理解】
> （IDE 是浏览器扩展、selenium 是 Python 库——这个区别为什么会影响"能不能在 CI 上跑"？）

---

### 知识点 4：创建项目与界面功能

【课程原话/定义】
安装完成后点击图标启动 → 创建一个新项目 → 输入项目名称 → 进入界面。

> 📷 【截图占位】点击 Selenium IDE 图标
> 📷 【截图占位】创建新项目对话框
> 📷 【截图占位】输入项目名称
> 📷 【截图占位】Selenium IDE 主界面

常用功能（对应界面编号）：

1. 新建、保存、打开
2. 开始和停止录制
3. 运行 8 中所有的实例（运行全部用例）
4. 运行单个实例（运行单条用例）
5. 调试模式
6. 调整案例的运行速度
7. 要录制的网址
8. 实例列表（用例列表）
9. 动作、目标、值（Command / Target / Value）
10. 对单条命令的解释
11. 运行日志

> 📷 【截图占位】Selenium IDE 常用功能界面标注图

【为什么？】
界面里最值得理解的是第 9 项 —— **Command / Target / Value 三元组**，它是 Selenium 的核心抽象：

| 列 | 含义 | 对应 WebDriver 代码 |
|----|------|-------------------|
| **Command**（动作） | 做什么 | `click()` / `send_keys()` / `get()` |
| **Target**（目标） | 对谁做（定位表达式） | `find_element(By.XXX, "...")` |
| **Value**（值） | 用什么数据做 | `send_keys("hogwarts")` 里的参数 |

也就是说，一条 UI 自动化操作永远是 **"在哪个元素上、做什么动作、用什么数据"**。想清楚这一点，后面手写 WebDriver 时就不会迷路——`driver.find_element(By.ID, "kw").send_keys("测试")` 正是 Target + Command + Value 的组合。

第 6 项"运行速度"也很有信息量：**需要调慢速度才能跑通，恰恰暴露了录制回放没有等待机制**——它靠"整体放慢"来碰运气，而 WebDriver 用显式等待精确等待某个条件成立。这是玩具与工程的分界线。

【必须掌握】
- 三元组：Command（动作）/ Target（目标定位）/ Value（数据）
- 运行粒度：全部用例 / 单条用例（对应 Pytest 的"跑目录 / 跑单个用例"）
- 调速功能存在的原因 = 没有等待机制（工程化要用显式等待替代）
- 运行日志用来看每条命令的执行结果与失败原因

【企业场景】
你带一个刚转自动化的同事，他总记不住 `find_element` 的参数顺序。你让他打开 IDE 看 Command/Target/Value 三列，再对照导出的 Python 代码看一遍——五分钟就理解了"定位 + 动作 + 数据"的模型。**IDE 最大的价值就在这种概念可视化。**

【面试考察】
面试官："一条 UI 自动化操作由哪几部分组成？"

参考回答框架：
1. 定位元素（Target）→ 2. 执行动作（Command）→ 3. 传入数据（Value）→ 4. 断言结果
2. 对应代码：`driver.find_element(By.ID, "kw").send_keys("测试")` + `assert`
3. 强调：**没有第 4 步（断言）就不是测试用例**
4. 加分：稳定的自动化还需要第 0 步——等待元素可交互（显式等待）

【易错点】

| 误区 | 纠正 |
|------|------|
| 靠调慢运行速度解决失败 | 治标不治本，工程化要用显式等待 |
| 只关注 Command，不关注 Target 质量 | Target（定位器）质量决定脚本寿命 |
| 忘了断言 | Selenium IDE 里也有 assert/verify 命令，必须加 |

【扩展知识】
IDE 里的 `assert` 与 `verify` 区别（等价于测试框架里的硬断言/软断言）：`assert` 失败立即终止该用例；`verify` 失败记录错误但继续执行后面的命令。对应到 Pytest：`assert` = 硬断言，软断言需要用 `pytest-check` 等插件。

【我的理解】
> （用 Command/Target/Value 三元组描述"在搜索框输入 hogwarts 并点击搜索"这个操作，写出三行对应的三元组内容）

---

## 三、实战：录制、导出、回放

### 知识点 5：录制第一个用例与导出代码分析

【课程原话/定义】
创建新项目取名 `hogwarts_demo1` → 点击录制按钮 → 填写要录制的 URL（这里用 `https://ceshiren.com/`）→ 浏览器打开新窗口开始录制，页面上的操作都会记录到 IDE → 操作完成后切回 IDE 点击停止录制 → 为用例取名 `ceshiren_demo1`。

> 📷 【截图占位】录制过程与用例命名

导出为 Python pytest 格式的代码：

```python
# Generated by Selenium IDE
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestCeshirendemo1():
    # 每个测试方法执行前运行
    def setup_method(self, method):
        # 初始化 webdriver
        self.driver = webdriver.Chrome()
        self.vars = {}

    # 每个测试方法执行后运行
    def teardown_method(self, method):
        # 关闭浏览器并结束 ChromeDriver 进程
        self.driver.quit()

    def test_ceshirendemo1(self):
        self.driver.get("https://ceshiren.com/")          # 访问网址
        self.driver.set_window_size(1382, 744)            # 设置窗口大小
        self.driver.find_element(By.LINK_TEXT, "类别").click()   # 点击操作
        time.sleep(2)                                     # 等待 2 秒
        self.driver.close()                               # 关闭当前窗口
```

Java 版本（JUnit）结构对照：`@Before setUp()` 创建 driver → `@Test` 方法写操作 → `@After tearDown()` 调 `driver.quit()`，与 Python 版一一对应。

【为什么？】
这段导出代码**值得逐行批判**，因为它同时展示了"框架结构"和"典型坏味道"：

| 代码 | 好/坏 | 原因 |
|------|-------|------|
| `setup_method` / `teardown_method` | ✅ 好 | 这是 Pytest 的前后置钩子，保证每条用例独立、浏览器必被关闭 |
| `self.driver` 存实例属性 | ✅ 好 | 用例方法之间共享 driver 的标准做法 |
| `By.LINK_TEXT, "类别"` | 🟡 一般 | 文本定位比动态 ID 稳，但多语言/文案改动会失效 |
| `By.CSS_SELECTOR, "#ember18-header .name"`（另一例） | ❌ 坏 | `ember18` 是前端动态生成的 ID，刷新就变 |
| `time.sleep(2)` | ❌ 坏 | 固定等待：快了会失败，慢了浪费时间。应换显式等待 |
| `self.driver.close()` | ❌ 坏 | 用例里关窗口，与 teardown 的 `quit()` 冲突且语义混乱 |
| **没有任何 assert** | ❌❌ 最致命 | 只有操作没有验证 → 这不是测试用例，是点击器 |

所以"导出的代码能直接用吗？"答案是不能。它是**脚手架**：结构可以留（setup/teardown），定位器要换稳定的，sleep 要换显式等待，断言必须自己加。

改造后的样子（这才是能进仓库的代码）：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCeshiren:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self):
        self.driver.quit()                      # 只在 teardown 收尾，不用 close

    def test_open_category(self):
        self.driver.get("https://ceshiren.com/")
        # 显式等待：等元素可点击再点，替代 sleep(2)
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "类别"))).click()
        # 断言：验证结果，而不是只做操作
        assert "类别" in self.driver.title or "category" in self.driver.current_url
```

【必须掌握】
- 导出代码的可复用部分：`setup_method` / `teardown_method` 结构、`self.driver`
- 必须改造的三处：**动态定位器 → 稳定定位器**、**`time.sleep` → 显式等待**、**补断言**
- `setup_method`/`teardown_method` 是每个用例前后各执行一次（不是整个类一次，类级别是 `setup_class`）
- 录制代码里 `close()` 与 teardown 的 `quit()` 混用是坏味道

【企业场景】
新人交上来一个 PR，内容是 IDE 导出的代码原样提交，跑起来还挺绿。你在 code review 里要提三条意见：①没有断言，脚本永远通过，等于零覆盖 ②`#ember77` 这类定位器下次发版必失效 ③`time.sleep(2)` 在慢环境仍会失败、在快环境白等。这三条正是录制脚本进入工程环境时的固定问题清单。

【面试考察】
面试官："Selenium IDE 导出的代码能直接用于项目吗？为什么？"

参考回答框架：
1. 不能直接用，但结构可以借鉴（setup/teardown 的前后置管理）
2. 三个必须改造点：定位器（动态 ID → 稳定属性/文本/data-* 属性）、等待（固定 sleep → 显式等待）、断言（补 assert）
3. 更进一步：抽 PO 层（定位器与用例解耦）、参数化（数据外置到 yaml/csv）、加日志与失败截图
4. 一句话：**录制解决"能跑"，工程化解决"能长期跑"**

【易错点】

| 坏味道 | 后果 | 修法 |
|--------|------|------|
| 无断言 | 永远绿灯，覆盖为零 | 每条用例至少一个 assert |
| `time.sleep(n)` | 慢环境仍失败、快环境白等 | `WebDriverWait` + `expected_conditions` |
| 动态 ID 定位（`#ember77`） | 刷新/发版即失效 | 稳定属性、文本、相对定位、`data-test-id` |
| `close()` + `quit()` 混用 | 会话状态混乱 | 收尾只用 `quit()`，多窗口才用 `close()` |
| 定位器散落在用例里 | 页面一改要改几十处 | 抽到 PO 层，改一处 |

【我的理解】
> （把上面那份导出代码的 7 处逐行点评，按"影响脚本寿命的严重程度"重新排个序，最该先改哪一处？）

---

### 知识点 6：保存、回放与控件定位

【课程原话/定义】
**保存**：单击 IDE 右上角的 save 图标，输入项目的保存名称和地址。

**回放**：选择想要回放的测试用例，单击 play 按钮，在 IDE 中回放测试。

> 📷 【截图占位】回放测试用例界面

**控件定位**：如果想定位其他的控件，只需要点击界面中的箭头（Select target in page），点击后会跳转到浏览器，然后点击想要定位的控件，**Target 的值就会出现相应的定位表达式**。

> 📷 【截图占位】控件定位（Select target in page）界面（图 3-8）

【为什么？】
"点箭头 → 点页面元素 → 自动得到定位表达式"是 IDE 在你成为熟手后**唯一还值得留着的功能**。它比 F12 手动扒 DOM 快，而且会一次给出多个候选表达式（id / css / xpath / linkText），你可以从里面挑最稳的那个。

但要建立一个判断标准 —— **定位器优先级（越靠前越稳）**：

| 优先级 | 定位方式 | 例子 | 说明 |
|--------|---------|------|------|
| 1️⃣ | 语义化 id / `data-test-id` | `#login-btn` | 前端专为测试留的属性，最稳 |
| 2️⃣ | name / 稳定 class | `[name="username"]` | 表单元素常用 |
| 3️⃣ | 文本定位 | `//button[text()="登录"]` | 直观，但文案/多语言改动会失效 |
| 4️⃣ | 相对结构 CSS | `.login-form input:first-child` | 结构变动会失效 |
| ❌ | 动态生成 id / 绝对 XPath | `#ember77`、`/html/body/div[3]/div[2]/a` | **刷新或发版必失效，绝对不用** |

IDE 生成的往往是第 4 类甚至第 ❌ 类。所以正确用法是：**用 IDE 拿候选，用你的判断力做选择。** 这个"选定位器"的能力，正是下一章元素定位的核心，也是面试最爱问的地方。

【必须掌握】
- 保存的是 `.side` 项目文件（JSON 格式），只能被 IDE 打开，不是可执行代码
- 回放：选用例 → play；调试模式可逐步执行看哪一步失败
- Select target in page：点元素自动生成定位表达式（IDE 最保值的功能）
- 定位器优先级：语义 id/data-* > name > 文本 > 相对结构 > ❌ 动态 id/绝对 XPath

【企业场景】
你要给一个陌生的后台系统写自动化，页面元素没有任何 id，class 全是 `el-input__inner` 这种组件库通用类名（一个页面十几个一样的）。这时你的做法：①用 IDE 点几个关键元素看候选表达式，判断有没有可用的稳定属性 ②没有的话，去找前端同学要求补 `data-test-id`——**"要求前端加测试属性"是测试开发的正当诉求，也是面试的加分回答**，说明你懂治本而不是靠 XPath 硬扛。

【面试考察】
面试官："你怎么保证元素定位的稳定性？"

参考回答框架：
1. 定位器选择有优先级：优先语义化 id / `data-test-id`，其次 name，再考虑文本
2. 坚决避免：前端动态生成的 id（`ember77`、`react-select-3-input`）、绝对 XPath
3. 工程手段：定位器统一放 PO 层（改一处生效全局）+ 显式等待避免时序误判
4. 治本手段：推动前端为关键元素补 `data-test-id`，把定位契约化
5. 兜底：失败自动截图 + 保存页面源码，便于快速判断是元素变了还是真 bug

【易错点】

| 误区 | 问题 | 正确做法 |
|------|------|---------|
| 直接用 IDE 给的表达式 | 常是动态 id / 长 XPath | 挑稳定的，或自己改写 |
| 复制浏览器 F12 的 "Copy full XPath" | 绝对路径，结构一变就废 | 用相对 XPath / CSS |
| 认为 `.side` 文件就是自动化脚本 | 它只是 IDE 项目文件 | 要导出为代码才能被 Pytest 执行 |
| 定位不到就无脑加 sleep | 掩盖真实原因（frame、动态加载、元素不可见） | 先判断原因，再用显式等待/切 frame |

【扩展知识】
录制回放的失败自查顺序（比盲目重录高效得多）：

1. 元素定位表达式是否用了动态 id？→ 换稳定定位
2. 元素是否在 iframe 里？→ 需要先切 frame（IDE 里是 `select frame` 命令）
3. 元素是否需要滚动才可见/被遮挡？→ 滚动到元素或处理遮挡层
4. 是否页面还没加载完就操作？→ 显式等待
5. 是否上一步操作改变了页面（弹窗、跳转）？→ 检查步骤衔接

这套顺序在手写 WebDriver 时同样适用，是后续章节"元素定位与等待"的预备知识。

【我的理解】
> （为什么"推动前端加 data-test-id"比"写更复杂的 XPath"更值得做？从维护成本和责任划分两个角度想）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| IDE 定义与局限 | 浏览器扩展，录制回放；定位不稳、无等待、复杂逻辑无力 | ★★★☆☆ |
| 使用场景 | 入门期、演示、取定位表达式；成长后价值下降，复杂需求用 WebDriver | ★★★☆☆ |
| 安装 | 浏览器扩展（≠ pip install selenium）；Chrome 商店国内不可达 → Firefox / GitHub Release | ★☆☆☆☆ |
| 界面与三元组 | **Command（动作）/ Target（定位）/ Value（数据）**；调速功能暴露了无等待机制 | ★★★★☆ |
| 导出代码分析 | setup/teardown 可留；必改三处：动态定位器、`time.sleep`、**缺断言** | ★★★★★ |
| 控件定位 | Select target in page 取候选；定位器优先级：语义 id/data-* > name > 文本 > ❌ 动态 id/绝对 XPath | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-Web自动化测试价值与体系]]
- [[Ch02-Selenium环境安装与使用]]
- [[Python/Ch22-面向对象入门|Python Ch22 面向对象入门]]（导出代码的 class + self.driver 结构）
- [[Pytest/README|Pytest]]（setup_method/teardown_method 与 fixture 的关系）
