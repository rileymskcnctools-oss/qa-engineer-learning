---
tags:
  - 课程笔记
  - Web自动化测试
  - Selenium
  - 日志
  - 截图
  - page_source
course: Web自动化测试
chapter: Ch13-Web自动化关键数据记录
created: 2026-08-29
status: draft
---

# Ch13 - Web 自动化关键数据记录

## 课程来源
- 学习日期：

---

## 一、关键数据记录概述

### 知识点 1：为什么需要"关键数据记录"

【课程原话/定义】
关键数据记录是 Web 自动化测试中的关键部分，它们提供了关于系统行为和执行过程的详细信息，有助于**验证用例的正确性、排查问题和确保应用程序的质量**。

三大类关键数据：
1. **行为日志**（logging）：记录操作和事件，用于审计、故障排查
2. **步骤截图**（screenshot）：捕捉关键执行步骤，验证正确性 + 可视化执行过程
3. **页面源代码**（page source）：捕获当前网页的 DOM 结构，排查元素查找问题

【为什么？】
这三样东西解决同一个根本问题：**用例失败了，你怎么知道"为什么失败"？**

一条自动化用例只有两种状态——"过"或"挂"。但"挂"只是一个结果，排查需要**证据链**：

```
失败断言 ← 当时的页面长什么样？（截图）
         ← 执行到了哪一步？（日志）
         ← 页面 DOM 是不是变了、元素到底在不在？（page_source）
```

Ch06 知识点1 的面试回答里就提过"失败自动截图 + 保存 page_source"——本章把这句话展开成具体技术。**没有记录能力的自动化框架，等于"出了事故没有监控录像"**。

【必须掌握】
- 三大记录：行为日志 / 步骤截图 / page source
- 三者构成"失败证据链"：日志回答"做到哪"、截图回答"长什么样"、page_source 回答"元素在哪"
- 记录的核心目的：验证正确性 + 排查问题

【企业场景】
你早上到公司看到 CI 里 3 条用例红了，报错都是 `NoSuchElementException`。如果框架没有记录能力，你得手动重跑复现；如果框架在失败时自动留了日志 + 截图 + page_source，你打开截图就能看到"页面停在了登录页没进去"，打开日志看到"第 5 步点击登录失败"——几分钟定位，而不是半天。

【面试考察】
面试官："你的自动化用例失败时，怎么快速定位问题？"

参考回答框架：
1. 三大记录：行为日志（做到哪一步）+ 截图（页面当时的样子）+ page_source（DOM 结构）
2. 集成方式：fixture teardown 里判断用例失败就自动截图 + 存 page_source
3. 日志用 logging，分级别（INFO 记录步骤、ERROR 记录异常）
4. 最终落到 Allure 报告里，失败用例附截图和日志

【易错点】

| 误区 | 纠正 |
|------|------|
| 用例失败只靠报错信息排查 | 报错信息有限，要配截图 + 日志 + page_source |
| 记录代码散落在用例里 | 抽到 fixture / 公共方法里，失败自动触发 |

【我的理解】
> （"失败证据链"三件套各回答什么问题？如果只能留一样，你会留哪个？为什么？）

---

## 二、行为日志

### 知识点 2：logging 行为日志

【课程原话/定义】
行为日志用于记录系统或应用程序的操作和事件，目的是跟踪执行过程，以便审计、故障排查。日志通常包括：

- **时间戳**（Timestamp）：每个操作发生的精确时间点
- **操作描述**（Action Description）：对操作的详细描述
- **事件级别**（Log Level）：重要性级别（信息/警告/错误等）
- **相关信息**（Additional Information）：参数、输入值等

Python 实现（需要先导入 logging 模块）：

```python
import logging

def test_logging():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.baidu.com")
    logging.info("打开百度首页")                       # 记录操作
    driver.find_element(By.CSS_SELECTOR, "#kw").send_keys("霍格沃兹测试学院")
    logging.info("输入霍格沃兹测试学院")
    driver.find_element(By.CSS_SELECTOR, "#su").click()
    logging.info("点击搜索")
    time.sleep(3)
    driver.quit()
```

Java 实现（SLF4J + Logback）：

```java
private static final Logger logger = LoggerFactory.getLogger(demoTest.class);

logger.info("打开百度首页");
logger.info("输入霍格沃兹测试学院");
logger.info("点击搜索");
```

【为什么？】
日志的核心价值是**还原执行轨迹**：每个关键步骤打一行 `info`，失败时一看最后一行日志就知道"死在哪一步"，不用逐行 debug。

但有一个**新手必踩的坑**：Python 的 `logging` **默认级别是 WARNING**，直接 `logging.info(...)` **默认不输出**！课程说"运行之后可以看到打印了日志"，实际要先配置级别：

```python
import logging
logging.basicConfig(level=logging.INFO)   # 关键：把级别降到 INFO
```

四个级别从低到高：`DEBUG < INFO < WARNING < ERROR`，只输出"级别 ≥ 设定级别"的日志。所以：
- 设 `INFO` → 输出 INFO/WARNING/ERROR（日常用这个）
- 设 `DEBUG` → 额外输出调试细节
- 设 `ERROR` → 只输出错误

【必须掌握】
- 日志四要素：时间戳 / 操作描述 / 级别 / 相关信息
- Python `logging.info(...)`，**默认级别 WARNING，INFO 需先 `basicConfig(level=logging.INFO)`**
- 四级：DEBUG < INFO < WARNING < ERROR
- Java：SLF4J + Logback，`logger.info(...)`

【企业场景】
你在框架里定了规范："每个用例的关键步骤（打开页面、输入、点击、断言）各打一行 `logging.info`"。CI 上某条用例失败，你打开日志文件，看到最后一行是"输入用户名"，立刻知道死在了"点击登录"——排查范围从整条用例缩小到一步。

【面试考察】
面试官："你怎么在自动化脚本里加日志？日志分几个级别？"

参考回答框架：
1. Python 用 `logging`，关键步骤 `logging.info("...")`
2. 四级：DEBUG / INFO / WARNING / ERROR，越往后越严重
3. 注意坑：logging 默认级别 WARNING，INFO 要 `basicConfig(level=logging.INFO)` 才输出
4. 用途：失败时靠"最后一行日志"定位到具体步骤

【易错点】

| 误区 | 纠正 |
|------|------|
| `logging.info()` 不输出就以为代码错 | 默认级别 WARNING，先 `basicConfig(level=logging.INFO)` |
| 课程 Python 示例漏 `import logging` | 用了 logging 却没 import（课程笔误，同 Ch10 的 time） |
| 每步打日志嫌麻烦就省略 | 日志是"失败定位"的命根子，关键步骤必须打 |

【扩展知识】
Java 侧日志体系：SLF4J 是门面（接口），Logback 是实现。`LoggerFactory.getLogger(Class.class)` 拿到 logger，`logger.info/warn/error` 分级输出。对比 Python 的 `logging`，思想完全一致：**分级别 + 记录步骤**。

【我的理解】
> （为什么 Python 的 `logging.info()` 默认不输出，而 `logging.warning()` 默认能输出？这和"级别过滤"机制是什么关系？）

---

## 三、步骤截图

### 知识点 3：get_screenshot_as_file 步骤截图

【课程原话/定义】
步骤截图用于捕捉 Web 自动化测试中的关键执行步骤，以便验证正确性和可视化执行过程。包括：
- **屏幕截图**：整个浏览器窗口的屏幕图像
- **元素状态截图**：特定元素的状态（悬停、点击后的变化）
- **控制台日志截图**：浏览器控制台的日志信息

Python 实现（`get_screenshot_as_file`，需提前创建保存目录）：

```python
def test_screenshot():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.baidu.com")
    driver.get_screenshot_as_file("./screenshot/打开百度首页.png")          # 截图
    driver.find_element(By.CSS_SELECTOR, "#kw").send_keys("霍格沃兹测试学院")
    driver.get_screenshot_as_file("./screenshot/输入霍格沃兹测试学院.png")
    driver.find_element(By.CSS_SELECTOR, "#su").click()
    driver.get_screenshot_as_file("./screenshot/点击搜索.png")
    time.sleep(3)
    driver.quit()
```

Java 实现（**元素截图**，`element.getScreenshotAs`）：

```java
File eleScreen = element.getScreenshotAs(OutputType.FILE);
FileUtils.copyFile(eleScreen, new File("./image2.png"));   // 依赖 Apache Commons IO
```

【为什么？】
截图让"失败"变得**可见**。相比日志只告诉你"做到哪"，截图直接展示"页面当时长什么样"——很多 flaky 问题（遮罩没消失、弹窗挡着、页面停在登录页）一眼就能看出。

三种截图的用途分工：

| 类型      | 方法                                         | 用途          |
| ------- | ------------------------------------------ | ----------- |
| 整页/窗口截图 | `driver.get_screenshot_as_file(path)`      | 看页面整体状态     |
| 元素截图    | `element.getScreenshotAs(OutputType.FILE)` | 只截某个元素（更聚焦） |
| 控制台日志截图 | 手动/工具截 Console 面板                          | 结合 JS 报错分析  |

⚠️ 关键坑：`get_screenshot_as_file` 要求**保存目录必须已存在**，目录没建会报 `FileNotFoundError`。所以要么先 `os.makedirs("screenshot", exist_ok=True)`，要么在框架初始化时统一建好目录。

【必须掌握】
- 整页截图：`driver.get_screenshot_as_file(路径)`（目录需提前建）
- 元素截图：`element.getScreenshotAs(OutputType.FILE)`（Java，需 FileUtils）
- 三种截图：屏幕 / 元素状态 / 控制台日志
- 最有价值的是"**失败时**"的截图，不是每步都截

【企业场景】
你在 pytest 的 fixture teardown 里写：`if 用例失败: driver.get_screenshot_as_file(f"截图/{用例名}.png")`。这样只有失败才截图，既省空间，又保证每条红用例都留了"案发现场"。结合日志 + page_source，CI 上的失败几乎不用重跑就能定位。

【面试考察】
面试官："截图怎么加？失败时怎么自动留证？"

参考回答框架：
1. 整页 `get_screenshot_as_file`、元素 `getScreenshotAs`
2. 不是每步都截，而是**失败时**截（teardown 里判断用例结果）
3. 截图 + 日志 + page_source 三件套一起留证
4. 目录用 `os.makedirs(exist_ok=True)` 提前建，文件名带用例名/时间戳
5. 最终集成进 Allure 报告，失败用例附截图

【易错点】

| 误区 | 纠正 |
|------|------|
| 目录没建就截图 | 报 FileNotFoundError，先 `os.makedirs` 或框架统一建 |
| 每步都截图 | 文件爆炸、拖慢执行；只截关键步骤或失败时 |
| 截图文件名不带用例名 | 多个失败混在一起，无法对应到用例 |

【扩展知识】
Python 里除了 `get_screenshot_as_file`，还有 `driver.get_screenshot_as_png()`（返回字节流，可直接塞进 Allure 的 attachment）和 `driver.save_screenshot(path)`（等价于 file 版）。Allure 集成时常用 `get_screenshot_as_png` 而不是落盘文件。

【我的理解】
> （为什么"失败时截图"比"每步截图"更好？从磁盘空间、执行速度、排查效率三个角度想。）

---

## 四、页面源代码 page source

### 知识点 4：driver.page_source 页面源代码

【课程原话/定义】
page source 用于捕获当前网页的 DOM 结构，用于排查元素查找问题、验证页面结构和属性。包括：HTML 结构、CSS 样式、元素属性、JavaScript 代码。

Python 实现：

```python
def test_page_source():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get("https://www.baidu.com")
    print(driver.page_source)     # 获取并打印整个页面 HTML
    ...
```

Java 实现：

```java
String pageSource = driver.getPageSource();          // 获取 HTML 字符串
logger.debug(pageSource);                            // 打到日志

FileWriter pageSourceFile = new FileWriter("./pageSource.html");
pageSourceFile.write(pageSource);                    // 落盘保存
pageSourceFile.close();                              // 记得关闭
```

【为什么？】
page_source 回答的是截图和日志都回答不了的深层问题：**"元素到底在不在 DOM 里、属性长什么样"**。

`NoSuchElementException` 有两个完全不同的根因：
1. **元素确实还没加载**（等待问题）→ page_source 里搜不到这个元素
2. **定位器写错了**（定位问题）→ page_source 里有这个元素，但你的 selector 不匹配

把 page_source 存下来，用文本搜索元素的关键属性/文本，立刻能区分是哪种。这直接对应 Ch07 讲的"先区分没出现（等待）还是找错了（定位）"。

注意：`page_source` 是"**当前时刻**"的 DOM 快照，页面还在异步渲染时拿到的可能是"半成品"，所以排查时通常配合"失败那一刻"抓取，而不是事后手动打开页面。

【必须掌握】
- `driver.page_source`（Python）/ `getPageSource()`（Java）取当前页面 HTML
- 用途：区分"元素没加载"和"定位器写错"
- 是"当前时刻"的 DOM 快照，要抓"失败那一刻"
- Java 落盘后记得 close（或 try-with-resources）

【企业场景】
某条用例报 `NoSuchElementException`，你打开失败时保存的 page_source.html，Ctrl+F 搜元素的 id——搜到了，说明是定位器写错；没搜到，说明页面当时根本没渲染出这个元素（等待问题）。这个判断直接决定了修复方向：改定位器 or 加等待。

【面试考察】
面试官："page_source 有什么用？什么时候抓它？"

参考回答框架：
1. 拿当前页面的 HTML/DOM 快照
2. 核心用途：排查元素查找问题——区分"元素没加载"vs"定位器写错"
3. 时机：失败那一刻抓（配合截图 + 日志），不是事后手动开页面
4. 落盘保存 + 文本搜索验证元素是否存在、属性是否正确

【易错点】

| 误区 | 纠正 |
|------|------|
| page_source 当"当前页面实时镜像" | 是"抓取那一刻"的快照，异步渲染中可能是半成品 |
| Java FileWriter 不 close | 文件内容可能没刷盘，用 try-with-resources |
| 只 print 不落盘 | 排查要可搜索/可对比，落盘成 .html 更好 |

【扩展知识】
page_source 与"元素是否可交互"的关系：元素在 page_source 里存在，只说明"DOM 里有它"，不代表"可点击"（Ch07 的"元素在 DOM ≠ 可交互"）。所以 page_source 用于"定位诊断"，交互问题还要看截图和等待策略。

【我的理解】
> （一个 `NoSuchElementException`，你查 page_source 发现元素其实在——这说明了什么？修复方向是改定位器还是加等待？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 关键数据概述 | 日志 + 截图 + page_source 构成"失败证据链" | ★★★★☆ |
| 行为日志 | logging 四级；默认 WARNING，INFO 需 basicConfig | ★★★★☆ |
| 步骤截图 | get_screenshot_as_file / 元素截图；失败时截图 | ★★★★☆ |
| page source | 取 DOM 快照，区分"没加载 vs 定位错" | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch06-八大元素定位方式]]（失败自动截图 + page_source 的思路首次提出）
- [[Ch07-强制等待与隐式等待]]（page_source 用于区分"等待问题 vs 定位问题"）
- [[Ch10-测试人论坛搜索功能自动化测试]]（综合实战里可加日志/截图留证）
- [[Pytest/README|Pytest]]（fixture teardown 里做失败自动截图，后续 Allure 报告集成）
- [[Ch14-电子商务产品实战-litemall优惠券管理]]（日志/截图/Allure 在 litemall 完整项目中的工程化落地）
- [[Ch16-异常自动截图]]（用装饰器把"失败留证"自动化，三件套的落地实现）
