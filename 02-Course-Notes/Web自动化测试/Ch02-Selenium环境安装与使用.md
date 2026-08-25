---
tags: [课程笔记, Web自动化测试, Selenium, 环境搭建]
course: "Web自动化测试"
chapter: "Ch02-Selenium环境安装与使用"
created: 2026-08-25
status: draft
---

# Ch02 - Selenium 环境安装与使用

## 课程来源
- 学习日期：

---

## 一、环境准备

### 知识点 1：四件套环境要求

【课程原话/定义】

- Python 3.10 或以上
- PyCharm
- Google Chrome
- Selenium 4.x

推荐安装最新版。

【为什么？】
四件套里每一项都有明确的"为什么是它"：

| 组件 | 为什么需要 | 版本为什么有要求 |
|------|-----------|----------------|
| Python 3.10+ | 写脚本的语言 | Selenium 4 新版本已放弃对 3.7/3.8 的支持；3.10+ 才能装上最新 selenium |
| PyCharm | 写代码、调试（断点看元素对象） | 非必须，但 debug 体验最好 |
| Chrome | 被自动化控制的目标浏览器 | 浏览器版本必须和 driver 匹配（见知识点 4） |
| Selenium 4.x | 驱动浏览器的 Python 库 | **4.x 才有 Selenium Manager**，3.x 需要手动下载配置 driver |

最关键的一条是 **Selenium 必须 4.x**。3.x 时代最折磨新人的就是"下载 chromedriver → 放到 PATH → 版本不匹配 → 重新下载"这个循环，4.x 的 Selenium Manager 直接把它消灭了。所以看到网上教程让你手动下 chromedriver，那是老教程。

Riley 环境提示（本机约定）：项目 venv 统一用 **Python 3.12.13（uv 管理）**，作业目录用 `pyproject.toml` + `uv sync` 恢复环境，不手动 venv + pip。3.12 满足 3.10+ 要求。

【必须掌握】
- 四件套：Python 3.10+ / PyCharm / Chrome / Selenium 4.x
- Selenium 4.x 是硬要求（Selenium Manager 只在 4.x 有）
- Chrome 与 chromedriver 的版本必须匹配（4.x 自动处理）

【企业场景】
新同事入职第一天配环境，装了 `pip install selenium==3.141.0`（网上老教程的版本），跑脚本报 `WebDriverException: 'chromedriver' executable needs to be in PATH`。你让他 `pip install -U selenium` 升到 4.x，代码一行没改就跑起来了——因为 4.x 自动管理 driver。这是团队里最高频的新人问题之一。

【面试考察】
面试官："搭建 Selenium 环境需要哪些东西？Selenium 3 和 4 在环境上最大的区别是什么？"

参考回答框架：
1. Python + Selenium 库 + 浏览器 + 浏览器驱动（driver）
2. Selenium 3：driver 必须手动下载、版本对齐浏览器、放进 PATH
3. Selenium 4：内置 **Selenium Manager**，自动检测浏览器版本、自动下载并缓存 driver
4. 结论：4.x 极大降低了环境成本，新项目一律用 4.x

【易错点】

| 误区 | 后果 | 纠正 |
|------|------|------|
| 按老教程装 selenium 3.x | 必须手动配 driver，报 PATH 错误 | `pip install -U selenium` 用 4.x |
| 以为装了 Chrome 就有 driver | 浏览器 ≠ 驱动，是两个东西 | 4.x 由 Manager 自动下 driver |
| PyCharm 是必需品 | 不是，只是提升效率 | 命令行 + 任意编辑器也能跑 |
| 在系统 Python 里全局装包 | 项目间版本互相污染 | 每个项目独立虚拟环境（uv/venv） |

【我的理解】
> （浏览器、driver、selenium 库这三者是什么关系？谁在中间传话？）

---

### 知识点 2：Selenium 安装

【课程原话/定义】
- **方法一**：PyCharm 图形界面安装（Settings → Project Interpreter → `+` → 搜索 selenium → Install）
- **方法二（推荐）**：命令行安装 —— `pip install selenium`

> 📷 【截图占位】Selenium 安装流程 UML 图

【为什么？】
为什么推荐命令行而不是图形界面？三个原因：

1. **可复现**：命令行安装能写进 `requirements.txt` / `pyproject.toml`，别人一条命令还原环境；图形界面点出来的东西没法交给同事。
2. **可进 CI**：Jenkins/GitLab CI 里没有 PyCharm，只有命令行。你在本地怎么装的，CI 就得怎么装。
3. **看得见报错**：图形界面失败往往只给一句红字，命令行能看到完整报错（网络、权限、版本冲突）。

一句话：**图形界面是给个人用的，命令行是给团队和机器用的。**

【必须掌握】
- 安装命令：`pip install selenium`
- 指定版本：`pip install selenium==4.21.0`
- 本机 uv 项目写法：`uv add selenium`（写进 pyproject.toml）
- 安装到"哪个 Python"很关键——必须是项目虚拟环境那个解释器

【企业场景】
你的项目用 uv 管理依赖，加 Selenium 的正确做法：

```bash
cd 02-Course-Notes/Web自动化测试/作业/homework01-selenium-basic
uv add selenium            # 写入 pyproject.toml + 更新 lock
uv run python demo.py      # 用项目环境运行
```

换到另一台电脑（比如你另一台 Administrator 的机器）只需 `uv sync`，Selenium 版本完全一致。对比手动 `pip install`：换机器就得凭记忆重装，版本还可能不一样。

【面试考察】
面试官："你们项目的依赖怎么管理？"

参考回答框架：
1. 每个项目独立虚拟环境，避免全局污染
2. 依赖声明在 `requirements.txt` / `pyproject.toml`，进版本控制
3. 新环境一条命令还原（`pip install -r` / `uv sync`）
4. 为什么重要：本地能跑 CI 不能跑，90% 是依赖不一致

【易错点】

| 现象 | 原因 | 排查 |
|------|------|------|
| `pip install selenium` 成功但 import 报 ModuleNotFoundError | 装到了另一个 Python（系统 vs 虚拟环境） | `pip -V` 和 `python -V` 看是不是同一个解释器 |
| PyCharm 里能跑，命令行不能 | PyCharm 用的是项目解释器，命令行是系统 Python | 命令行先激活虚拟环境 |
| 装了但版本是 3.x | 老教程 pin 了旧版本 | `pip show selenium` 确认，`pip install -U selenium` |

【我的理解】
> （为什么"装到哪个 Python 里"比"装没装上"更容易出问题？想想你机器上有几个 Python）

---

### 知识点 3：版本验证与升级

【课程原话/定义】
- 查看版本：`pip show selenium`
- 升级：`pip install -U selenium`

【为什么？】
先验证再写代码，是排查思路的起点。因为 Selenium 报错有一个特点：**同一个报错在 3.x 和 4.x 下的原因完全不同**（比如找不到 driver：3.x 是正常现象需要手动配，4.x 是 Manager 出问题了）。不知道版本就无法判断该往哪个方向查。

`pip show` 除了版本，还会给出 `Location`（装在哪里）——这一行恰好能解决知识点 2 里"装到了别的 Python"的问题。

【必须掌握】
- `pip show selenium` 看版本 + 安装路径
- `pip install -U selenium` 升级到最新
- 代码里看版本：`import selenium; print(selenium.__version__)`
- 出问题第一步永远是**确认版本和路径**

【企业场景】
同事说"你的脚本我这跑不了"。你让他执行三条命令：`python -V`、`pip show selenium`、`chrome://version`（浏览器版本）。三条信息一贴出来，问题基本就定位了——90% 的"你能跑我不能跑"都是这三者之一不一致。把这三条做成团队排查模板，能省掉大量来回沟通。

【面试考察】
面试官："别人的环境跑不起来你的自动化脚本，怎么排查？"

参考回答框架：
1. 先对齐版本三要素：Python 版本、selenium 版本、浏览器版本
2. 再对齐依赖：是否用同一份 requirements/lock 文件安装
3. 再看环境差异：操作系统、是否有头/无头、网络能否访问被测站点
4. 根治：用虚拟环境 + 锁定依赖 + 在容器里跑（环境即代码）

【易错点】

| 误区 | 纠正 |
|------|------|
| `pip list \| grep selenium` 就够了 | `pip show` 还能看安装路径，更有用 |
| 遇到报错先搜索报错文本 | 先确认版本，很多老答案只适用于 3.x |
| 无脑升级到最新 | 团队项目要统一版本，升级前确认兼容 |

【我的理解】
> （`pip show selenium` 输出里的 Location 一行，什么时候会救你一命？）

---

## 二、Selenium Manager 与第一个脚本

### 知识点 4：Selenium Manager（4.x 的核心便利）

【课程原话/定义】
Selenium Manager 自动完成：

- 自动检测浏览器版本
- 自动下载对应 Driver
- 自动缓存 Driver
- 自动启动浏览器

> 📷 【截图占位】Selenium Manager 工作流程 UML 图

【为什么？】
要理解 Manager 的价值，先要理解 Selenium 的三层结构：

```
你的 Python 脚本
      ↓  （Selenium 库发送 W3C WebDriver 协议请求）
ChromeDriver（一个本地小型 HTTP 服务）
      ↓  （用 Chrome 的调试接口驱动浏览器）
Chrome 浏览器 → 打开页面、点击、输入
```

中间这层 **driver 是浏览器厂商提供的、和浏览器版本强绑定的可执行文件**。Chrome 自动升级到 128，driver 还是 127 → 直接报 `session not created: This version of ChromeDriver only supports Chrome version 127`。

Selenium 3 时代这件事必须人工维护（Chrome 静默升级一次就要重下一次 driver），Selenium 4 的 Manager 把"查浏览器版本 → 下匹配 driver → 缓存起来"自动化了。这就是为什么 4.x 的 `webdriver.Chrome()` 可以一个参数都不传。

【必须掌握】
- Selenium 4 内置 Manager，**不需要手动下载 chromedriver**
- 四个自动：检测浏览器版本 / 下载 driver / 缓存 driver / 启动浏览器
- driver 缓存位置（了解）：`~/.cache/selenium`（Windows：`C:\Users\<user>\.cache\selenium`）
- 首次运行需要联网下载 driver，之后走缓存

【企业场景】
公司内网 CI 机器无法访问外网，Selenium Manager 下载 driver 失败，构建全红。解决方案有两种：①在镜像里预置好 driver，并用 `Service(executable_path=...)` 显式指定；②在内网搭 driver 镜像源。这类问题的根因是"Manager 需要联网"这一前提在受限网络里不成立——知道原理才能想到解法。

【面试考察】
面试官："Selenium 里 driver 是干什么的？为什么会有版本不匹配的报错？"

参考回答框架：
1. 三层结构：脚本 → Selenium 库（W3C 协议）→ driver（本地 HTTP 服务）→ 浏览器
2. driver 是浏览器厂商提供的桥梁，与浏览器版本强绑定
3. 浏览器自动升级后 driver 没跟上 → `session not created ... only supports Chrome version XXX`
4. Selenium 4 用 Manager 自动检测+下载+缓存解决；受限网络下可显式指定 driver 路径

【易错点】

| 误区 | 说明 |
|------|------|
| driver 就是浏览器 | 是两个独立程序，driver 只是"翻译官" |
| 4.x 完全不需要网络 | 首次下载 driver 需要联网，之后用缓存 |
| 版本不匹配报错是代码写错了 | 是环境问题，看报错里的 "only supports Chrome version" |
| 手动下 driver 更靠谱 | 4.x 下反而多余，除非离线/内网环境 |

【扩展知识】
显式指定 driver（离线/内网时使用）：

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=r"D:\drivers\chromedriver.exe")
driver = webdriver.Chrome(service=service)
```

注意 4.x 里 `executable_path` 已从 `webdriver.Chrome()` 移到 `Service` 对象，老教程的 `webdriver.Chrome(executable_path=...)` 会报 TypeError。

【我的理解】
> （用"你 → 翻译 → 外国人"的比喻解释脚本、driver、浏览器三者关系，并说明为什么"翻译"要和"外国人"版本对齐）

---

### 知识点 5：第一个 Selenium 程序

【课程原话/定义】

```python
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://ceshiren.com")

print(driver.title)

driver.quit()
```

> 📷 【截图占位】程序执行流程 UML 图

【为什么？】
这 5 行是所有 Web 自动化脚本的骨架，每一行都对应一个概念：

| 代码 | 做了什么 | 深层含义 |
|------|---------|---------|
| `from selenium import webdriver` | 导入 webdriver 模块 | webdriver 是"浏览器遥控器"的工厂 |
| `driver = webdriver.Chrome()` | 启动 Chrome + 建立会话（session） | 这一行背后：Manager 找 driver → 启动 driver 服务 → driver 启动浏览器 → 返回 sessionId |
| `driver.get(url)` | 打开网址 | 会**等待页面 load 事件完成**才返回（但 Ajax 内容不保证已到） |
| `print(driver.title)` | 拿到页面标题 | 第一个"读取页面信息"的动作，是最简单的断言素材 |
| `driver.quit()` | 关闭浏览器并结束会话 | 释放 driver 进程；不写会残留进程 |

`driver` 这个变量是整个脚本的核心——后面所有操作（找元素、点击、截图、切窗口）都挂在它身上。理解它是"一个已建立的浏览器会话的句柄"，就理解了 Selenium 的编程模型。

【必须掌握】
- 五步骨架：导入 → 实例化 driver → get(url) → 操作/断言 → quit()
- `driver.title` 取标题，`driver.current_url` 取当前地址
- **`quit()` 与 `close()` 的区别**（面试高频，见易错点）
- 断言要用 assert，不能只 print

【企业场景】
把课程这段 demo 升级成一条**真正的测试用例**（有断言、能被 Pytest 收集、自动清理）：

```python
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.implicitly_wait(5)
    yield d              # 用例执行
    d.quit()             # 无论用例成功失败都关闭浏览器


def test_open_ceshiren(driver):
    driver.get("https://ceshiren.com")
    assert "测试人" in driver.title      # 断言：没有它就不是测试
```

区别在三点：fixture 保证浏览器一定被关闭（对应 [[Python/Ch25-文件操作|Ch25]] 里 `with` 的同一思想：资源必须被释放）、有断言、能被批量执行。

【面试考察】
面试官："`driver.quit()` 和 `driver.close()` 有什么区别？"

参考回答框架：
1. `close()`：关闭**当前窗口/标签页**；如果只剩一个窗口，效果接近关浏览器，但**session 未必正常结束**，driver 进程可能残留
2. `quit()`：关闭**所有窗口** + 结束 WebDriver 会话 + 退出 driver 进程
3. 实践：脚本结束一律用 `quit()`；多窗口场景中关掉某个标签用 `close()`
4. 加分：`quit()` 要放在 fixture 的 teardown（或 try/finally），保证用例失败时也执行，否则会攒一堆僵尸 Chrome 进程

【易错点】

| 错误写法/做法 | 后果 | 正确做法 |
|-------------|------|---------|
| 用 `close()` 收尾 | chromedriver 进程残留，跑多了机器卡死 | 用 `quit()` |
| `quit()` 写在用例最后一行 | 用例中途失败就不会执行 | 放 fixture teardown / try-finally |
| 只 `print(driver.title)` | 没有断言，永远"通过" | `assert` 断言 |
| `driver.get("ceshiren.com")` | 报 `InvalidArgumentException` | URL 必须带协议 `https://` |
| 忘了 Chrome 在跑就直接看结果 | 脚本秒开秒关，肉眼看不到 | 调试期加断点 / 或临时 `time.sleep()`，正式代码不留 sleep |

【扩展知识】
常用启动参数（后续章节展开，先知道存在）：

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")        # 无头模式，CI 上必备
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)
```

CI 服务器没有图形界面，必须用无头模式；本地调试则用有头模式方便观察。

【我的理解】
> （`webdriver.Chrome()` 这一行代码背后实际发生了哪几件事？按顺序写出来）

---

### 知识点 6：常见问题排查

【课程原话/定义】
浏览器没有启动？请依次检查：

1. Python 是否安装成功
2. Selenium 是否安装成功
3. Chrome 是否已安装
4. 是否能够联网
5. Selenium 是否为 4.0 以上版本

【为什么？】
这个清单的价值不在五个条目本身，而在"**依次**"这两个字——它是一条**从底层往上的排查链**：语言 → 库 → 浏览器 → 网络 → 版本。每一层都是上一层的前提，跳着查会浪费大量时间。

这正是 [[Python/Ch20-错误分析与调试|Ch20 错误分析与调试]] 里"分层排查"思想在环境问题上的复用：先确认地基，再查上层。

补一张更实用的报错对照表（面试和日常都用得上）：

| 报错关键字 | 真实原因 | 解决 |
|-----------|---------|------|
| `ModuleNotFoundError: No module named 'selenium'` | 没装，或装到了别的 Python | `pip show selenium` 看路径，在项目环境重装 |
| `'chromedriver' executable needs to be in PATH` | selenium 是 3.x | 升级到 4.x |
| `session not created: This version of ChromeDriver only supports Chrome version XXX` | driver 与浏览器版本不匹配 | 4.x 让 Manager 处理；或手动换匹配的 driver |
| `WebDriverException: unknown error: cannot find Chrome binary` | 没装 Chrome / 装在非默认路径 | 装 Chrome 或用 `options.binary_location` 指定 |
| `Timed out receiving message from renderer` | 页面加载慢/网络问题 | 检查网络、加超时与等待 |
| `InvalidArgumentException: invalid argument` | URL 没带 `https://` | 补全协议 |

【必须掌握】
- 排查顺序：Python → selenium 库 → 浏览器 → 网络 → 版本
- 认识上表五条高频报错及其含义（面试常问"遇到过什么环境问题"）
- 报错要**读英文关键句**，尤其 `only supports Chrome version` 这类明确提示

【企业场景】
早上夜间构建全红，报错都是 `session not created ... only supports Chrome version 127`。原因：CI 镜像里的 Chrome 昨晚自动升级到 128，而镜像里预置的 driver 还是 127。修法：镜像里锁定 Chrome 版本（禁止自动升级）+ driver 同步升级，二者版本作为镜像构建参数统一管理。这类"环境漂移"是自动化落地的经典坑。

【面试考察】
面试官："自动化脚本在 CI 上突然全部失败，本地却正常，你怎么定位？"

参考回答框架：
1. 先分类：全部失败通常是**环境/前置**问题，不是用例逻辑问题
2. 看第一条报错的英文关键句，判断层级（依赖 / driver / 浏览器 / 网络 / 被测服务）
3. 对比本地与 CI 的三要素：Python 版本、selenium 版本、浏览器与 driver 版本
4. 常见根因：浏览器自动升级导致 driver 不匹配、CI 无网/无头未开、被测环境挂了
5. 根治：环境容器化 + 版本锁定 + 构建前健康检查

【易错点】

| 做法 | 问题 |
|------|------|
| 报错就直接搜索整段 Traceback | 应先读最后一行的异常类型和关键句 |
| 跳过"是否联网"直接怀疑代码 | 首次运行需要联网下 driver，这条经常是根因 |
| 遇错就重装 Python | 成本极高且往往无效，先按层级排查 |
| 忽略 CI 与本地的环境差异 | "本地能跑"不是证据，环境不同结论不同 |

【我的理解】
> （把上面的排查清单改写成你自己的"三条命令自检法"，遇到问题先跑哪三条命令？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 环境四件套 | Python 3.10+ / PyCharm / Chrome / **Selenium 4.x** | ★★★☆☆ |
| 安装方式 | `pip install selenium`（推荐命令行，可复现、可进 CI） | ★★★☆☆ |
| 版本验证 | `pip show selenium` / `pip install -U selenium`；排查第一步是确认版本 | ★★★☆☆ |
| Selenium Manager | 自动检测浏览器版本 + 下载 + 缓存 driver + 启动浏览器；三层结构：脚本→driver→浏览器 | ★★★★★ |
| 第一个程序 | 五步骨架：导入 → `webdriver.Chrome()` → `get()` → 操作/断言 → `quit()` | ★★★★★ |
| quit vs close | `quit()` 关全部窗口+结束会话；`close()` 只关当前窗口 | ★★★★★ |
| 问题排查 | 分层排查：Python→库→浏览器→网络→版本；五条高频报错 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-Web自动化测试价值与体系]]
- [[Ch03-SeleniumIDE用例录制]]
- [[Python/Ch20-错误分析与调试|Python Ch20 错误分析与调试]]（分层排查思想）
- [[Python/Ch25-文件操作|Python Ch25 文件操作]]（资源必须释放：with / quit）
- [[Pytest/README|Pytest]]（fixture 管理 driver 生命周期）
