---
tags:
  - 课程笔记
  - APP自动化测试
  - Python
  - sys模块
  - 标准库
course: APP自动化测试
chapter: Ch03-sys模块
created: 2026-08-31
status: draft
---

# Ch03 - sys 模块

## 课程来源
- 学习日期：

---

## 一、sys 模块简介与常用属性

### 知识点 1：sys 是与 Python 解释器交互的标准库

【课程原话/定义】

`sys` 是 Python 的内置标准库模块，提供访问与 Python 解释器相关的变量和函数的功能，主要用途：系统交互、解释器配置、命令行参数处理、标准输入输出、异常处理等。

【为什么？】

1. `sys` 管的是"解释器这一层"，`os` 管的是"操作系统这一层"——两者分工不同：`sys.argv` 拿脚本启动参数，`sys.path` 管模块搜索路径，这些都是"Python 运行时"自己的信息。
2. 内置标准库**无需安装**，`import sys` 即可用；但也要注意它和第三方库不同——它跟着解释器版本走。
3. 自动化里最常用的两个：`sys.argv`（命令行传参，如传入测试环境/设备号）和 `sys.path`（排查 `ModuleNotFoundError` 时的模块搜索路径）。

【必须掌握】

- `sys` = 解释器层信息；`os` = 操作系统层信息（下一章）
- 内置标准库，无需安装
- 最常用：`sys.argv`、`sys.path`

【企业场景】

你在企业里跑 App 自动化，常常要"同一个脚本跑不同环境"——比如 `python run.py staging` 或 `python run.py device1`。这个 `staging`/`device1` 就是通过 `sys.argv` 传给脚本的。另外，当你在 CI 上跑用例报 `ModuleNotFoundError` 时，第一件事就是打印 `sys.path` 看解释器到底在哪些目录找模块。

【面试考察】

面试官："sys 和 os 模块分别管什么？"

参考回答框架：
1. `sys`：Python 解释器相关（命令行参数 argv、模块路径 path、版本 version、解释器退出 exit）。
2. `os`：操作系统相关（文件/目录、路径、环境变量、进程）。
3. 一句话：sys 面向"解释器"，os 面向"操作系统"。

【易错点】

| 误区 | 纠正 |
|------|------|
| 把 sys 和 os 混为一谈 | sys 管解释器（argv/path/version），os 管操作系统（文件/目录/路径） |
| 以为 sys 需要 pip 安装 | 内置标准库，import 即可 |
| `sys.argv[0]` 当第一个参数用 | argv[0] 是脚本名本身，真正的参数从 argv[1] 开始 |

【我的理解】
> （`sys.argv[0]` 是"脚本名"而不是"第一个参数"。如果命令行是 `python run.py a b c`，argv 里各元素分别是什么？）

---

## 二、sys 常用属性

### 知识点 2：argv / version / platform / modules / path

【课程原话/定义】

```python
import sys
# 1. sys.argv：命令行参数列表，第一个元素是脚本名，后续是参数
script_name = sys.argv[0]
arguments = sys.argv[1:]

# 2. sys.version：解释器版本信息（字符串）
print("Python 解释器版本：", sys.version)

# 3. sys.version_info：版本信息（元组，可逐项比较，如 version_info >= (3, 8)）
print("Python 解释器版本信息：", sys.version_info)

# 4. sys.platform：操作系统平台名称（win32 / linux / darwin）
print("当前操作系统平台：", sys.platform)

# 5. sys.modules：已导入的模块信息（字典）
for module_name, module in sys.modules.items():
    print(f"模块名：{module_name}")

# 6. sys.path：模块搜索路径列表，解释器按此顺序找模块
print(sys.path)
```

【为什么？】

1. **`version` vs `version_info`**：`version` 是给人看的字符串；`version_info` 是元组（如 `(3, 12, 13, ...)`），可以**做版本比较**（`if sys.version_info >= (3, 8)`），这是写"兼容不同 Python 版本"代码的标准做法。
2. **`platform` 用于跨平台判断**：Windows 返回 `win32`，Linux 返回 `linux`，macOS 返回 `darwin`。自动化里常用于"不同系统走不同路径分隔符/驱动"的分支。
3. **`modules` 是"已加载模块的字典"**：`sys.modules['selenium']` 能拿到已导入的 selenium 模块对象，常被框架用来"判断某模块是否已加载"或"动态拿模块"。
4. **`path` 是"模块搜索顺序"**：`import xxx` 报 `ModuleNotFoundError` 时，本质是 xxx 不在 `sys.path` 的任何目录里——排查导入问题的第一入口。

【必须掌握】

- `argv[0]` 是脚本名，参数从 `argv[1]` 开始
- `version_info` 是元组，可做版本比较
- `platform` 判断操作系统（win32/linux/darwin）
- `path` 是模块搜索路径，排查 import 报错

【企业场景】

你在企业里写 App 自动化，`sys.platform` 常用来做跨平台兼容：比如本地 Windows 开发、CI 跑 Linux，日志/驱动路径的分隔符和驱动名都不同，代码里 `if sys.platform == "win32": ... else: ...` 分支处理。`sys.path` 则是在"测试文件 import 不到 conftest 或公共模块"时，用来确认根目录有没有进搜索路径。

【面试考察】

面试官："import 一个模块报 ModuleNotFoundError，你从 sys 的角度怎么排查？"

参考回答框架：
1. 打印 `sys.path`，确认目标模块所在目录是否在搜索路径里。
2. 不在就加：`sys.path.append(路径)` 或配置 `PYTHONPATH`。
3. 说明 `sys.path` 的顺序（脚本目录 → 环境变量 → 标准库 → site-packages）。

【易错点】

| 误区 | 纠正 |
|------|------|
| `sys.argv[0]` 当成第一个参数 | argv[0] 是脚本名，argv[1:] 才是参数 |
| 用 `version` 做版本判断 | version 是字符串无法直接比较，用 `version_info >= (3, 8)` |
| `platform` 返回值记错 | Windows=win32、Linux=linux、macOS=darwin |

【我的理解】
> （`sys.path` 是一个"列表"，import 时按列表顺序逐个目录找。那如果两个目录里都有同名模块，会 import 到哪个？这和列表顺序有什么关系？）

---

## 三、sys 常用方法

### 知识点 3：getdefaultencoding 与 exit

【课程原话/定义】

```python
import sys
# 获取系统当前默认编码
print(sys.getdefaultencoding())   # 通常为 utf-8

# 运行时退出，后面的代码不再执行
print("这一行会执行")
sys.exit()
print("这一行不会执行")
```

【为什么？】

1. **`getdefaultencoding()`**：返回解释器默认的字符串编码（Python 3 通常是 `utf-8`）。处理中文文件读写、跨平台编码问题时，先确认编码是排查乱码的第一步。
2. **`sys.exit()`**：立即终止程序，`exit()` 之后的代码不再执行。本质是抛出一个 `SystemExit` 异常——所以它其实**能被 `except SystemExit` 或 `finally` 捕获**，这也是它能被测试框架拦截的原因。
3. 自动化里 `sys.exit()` 常用于"环境检查不通过就直接退出"（比如检测到设备没连接、依赖缺失，直接终止而不是带着错误跑下去）。

【必须掌握】

- `getdefaultencoding()` 拿默认编码（Python 3 一般 utf-8）
- `sys.exit()` 立即终止，本质抛 SystemExit 异常
- `exit()` 后代码不执行

【企业场景】

你在企业里写 App 自动化入口脚本时，常在开头做环境自检：设备没连上、Appium 没启动、配置文件缺失——直接 `sys.exit("提示信息")` 终止，而不是让脚本带着错误继续跑、最后抛一堆难看的异常。这比"跑到一半崩溃"对 CI 更友好。

【面试考察】

面试官："sys.exit() 会执行 finally 块吗？"

参考回答框架：
1. 会。`sys.exit()` 本质是抛出 `SystemExit` 异常。
2. 异常会触发 finally 块（finally 的"无论成败都执行"对 SystemExit 也生效）。
3. 但 exit() 之后的普通代码不会执行。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 exit() 是"普通返回" | 它抛 SystemExit 异常，能被 finally/except 拦截 |
| 以为 exit() 后 finally 不执行 | finally 仍会执行 |
| 处理中文乱码时猜编码 | 先用 `sys.getdefaultencoding()` 确认默认编码 |

【我的理解】
> （`sys.exit()` 既然"抛异常"，那它和普通异常有什么不同？为什么说它是"能退出程序、又能被 finally 兜住"的特殊存在？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| sys 定位 | 解释器层信息（对比 os 操作系统层） | ★★★☆☆ |
| 常用属性 | argv / version_info / platform / modules / path | ★★★★☆ |
| 常用方法 | getdefaultencoding / exit（本质 SystemExit） | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch04-os模块]]（sys 管解释器、os 管操作系统，两者分工对照）
- [[Python/Ch25-文件操作]]（文件读写里的编码与路径，和 sys/os 配合）
- [[Web自动化测试/Ch02-Selenium环境安装与使用]]（sys.path 排查 import 报错的实际应用）
