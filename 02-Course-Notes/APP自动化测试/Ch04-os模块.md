---
tags:
  - 课程笔记
  - APP自动化测试
  - Python
  - os模块
  - 标准库
course: APP自动化测试
chapter: Ch04-os模块
created: 2026-08-31
status: draft
---

# Ch04 - os 模块

## 课程来源
- 学习日期：

---

## 一、os 模块简介与路径操作

### 知识点 1：os 是与操作系统交互的标准库

【课程原话/定义】

`os`（Operating System Interface）是 Python 的内置库，提供与操作系统交互的函数：文件和目录操作、环境变量访问、进程管理等。使用 os 可以编写跨平台代码，因为它对操作系统底层功能做了抽象，不用关心特定系统的细节。

【为什么？】

1. `os` 管"操作系统这一层"，和上一章的 `sys`（解释器层）互补：操作文件/目录/路径/进程找 os，操作命令行参数/模块路径/解释器版本找 sys。
2. **跨平台**是 os 的核心价值：Windows 的路径分隔符是 `\`，Linux/macOS 是 `/`——用 `os.path.join()` 拼接，就不用手写分隔符，代码一套跑遍三个平台。
3. 自动化里 os 几乎必用：日志目录、截图目录、配置文件路径、动态创建结果目录，全都要靠 os 的路径/目录操作。

【必须掌握】

- `os` = 操作系统层（文件/目录/路径/进程），对比 `sys` = 解释器层
- os 的核心价值是跨平台路径抽象
- 自动化里 os 用于日志/截图/配置路径管理

【企业场景】

你在企业里写 App 自动化，跑完一批用例要生成"按日期分目录的日志/截图/报告"——`os.makedirs()` 建目录、`os.path.join()` 拼路径、`os.path.exists()` 判断目录是否已存在。这些是每个测试框架 utils 里几乎必有的工具函数。

【面试考察】

面试官："os 和 sys 有什么区别？为什么说 os 能写跨平台代码？"

参考回答框架：
1. os 面向操作系统（文件/目录/路径/进程），sys 面向解释器（argv/path/version）。
2. os 把路径分隔符、系统名等平台差异抽象掉（如 os.sep、os.path.join），一套代码跨平台。
3. 举例：手写 `"a\\b"` 只在 Windows 对，`os.path.join("a","b")` 三平台都对。

【易错点】

| 误区 | 纠正 |
|------|------|
| os 和 sys 分不清 | os=操作系统（文件/目录/路径），sys=解释器（argv/path/version） |
| 手写路径分隔符 | Windows `\`、Linux `/` 不同，用 os.path.join / os.sep 跨平台 |
| 路径字符串里的反斜杠不转义 | `'\home\user'` 中 `\u` 会被当 Unicode 转义报错，见知识点 3 详解 |

【我的理解】
> （"跨平台"到底跨的是什么？举一个你在 Windows 上写、拿到 Linux 上会坏的路径写法，再用 os 重写一遍。）

---

## 二、os.path 路径方法

### 知识点 2：abspath / basename / dirname / split / join / exists / isdir / isfile / getsize

【课程原话/定义】

```python
import os
os.path.abspath('relative/path')      # 相对路径 → 绝对路径
os.path.basename('/path/to/file.txt') # 取文件名 file.txt
os.path.dirname('/path/to/file.txt')  # 取父目录 /path/to
os.path.split('/home/user/file.txt')  # 拆成 (目录, 文件名)
os.path.join('a', 'b', 'file.txt')    # 跨平台拼接路径
os.path.exists('/path')               # 路径是否存在（文件或目录都算）
os.path.isdir('/path/to/dir')         # 是否目录
os.path.isfile('/path/to/file')       # 是否文件
os.path.getsize('main.py')            # 文件大小（字节）
```

【为什么？】

1. **abspath vs 相对路径**：脚本的"当前工作目录"会变（在哪启动脚本，相对路径就指向哪），所以关键文件一律转成绝对路径，避免"换个目录跑就找不到文件"。
2. **basename / dirname / split 是"路径解析三件套"**：从完整路径里拆出"文件名"和"目录"，日志、报告、截图命名时经常用。
3. **join 是跨平台拼接的唯一正确姿势**：它自动用当前系统的分隔符，且能处理多余分隔符，比字符串 `+` 拼接安全。
4. **exists / isdir / isfile 是"先判断再操作"**：建目录前先 `exists` 判断、删文件前先 `isfile` 判断，避免"目录已存在"或"文件不存在"抛异常。

【必须掌握】

- abspath 转绝对路径（避免相对路径随 cwd 漂移）
- join 跨平台拼接（唯一正确姿势）
- exists/isdir/isfile 先判断再操作
- basename/dirname/split 拆分路径

【企业场景】

你在企业里，日志/截图工具函数几乎长这样：`log_dir = os.path.join(项目根目录, "logs", 日期)`；`if not os.path.exists(log_dir): os.makedirs(log_dir)`；`os.path.join(log_dir, f"{case_name}.png")`。这套"join + exists + makedirs"是每个测试框架的标配。

【面试考察】

面试官："为什么推荐用 os.path.join 拼接路径，而不是字符串相加？"

参考回答框架：
1. join 自动用当前系统的分隔符，跨平台（Windows `\` vs Linux `/`）。
2. 能规范处理多余/缺失的分隔符。
3. 手写 `"a\\b"` 只在 Windows 对，换 Linux 就坏。

【易错点】

| 误区 | 纠正 |
|------|------|
| `"a" + "\\" + "b"` 手拼路径 | 跨平台坏，用 os.path.join |
| 相对路径当绝对路径用 | 相对路径随启动目录变，关键路径用 abspath |
| 不判断就 mkdir | 目录已存在会抛 FileExistsError，先 exists 判断 |
| exists 能区分文件/目录 | exists 两者都返回 True，区分要用 isfile/isdir |

【我的理解】
> （`os.path.exists()` 对"文件"和"目录"都返回 True。那要精确判断"是文件还是目录"，该用什么？为什么自动化里"先判断再操作"能避免用例偶发失败？）

---

## 三、目录/文件操作与其它

### 知识点 3：listdir / mkdir / makedirs / rmdir / rename / remove + name / chmod / sep

【课程原话/定义】

```python
import os
os.listdir('/path')            # 列出目录内容
os.mkdir('/path/new')          # 创建单个目录（父目录必须已存在）
os.makedirs('/a/b/c')          # 递归创建多级目录（父目录不存在也会一起建）
os.rmdir('/path/empty')        # 删除空目录
os.rename(old, new)            # 重命名文件/目录
os.remove('/path/file.txt')    # 删除文件（只能删文件，不能删目录）

os.name          # 系统名：Windows=nt，Linux/macOS=posix
os.chmod(p, 0o755)  # 更改文件权限（八进制）
os.sep           # 路径分隔符：Windows=\ ，Linux/macOS=/
```

【为什么？】

1. **mkdir vs makedirs**：`mkdir` 只能建一层且父目录必须存在；`makedirs` 能递归建多级目录（`/a/b/c` 的 a、b 不存在也能一次建好）。自动化里"按日期建日志目录"几乎都用 `makedirs`（配合 `exist_ok=True` 更稳）。
2. **rmdir vs remove**：`rmdir` 只删**空目录**，`remove` 只删**文件**——搞反了会报错。删非空目录要用 `shutil.rmtree`。
3. **os.sep / os.name 是"平台信息"**：`os.sep` 返回当前系统分隔符，`os.name` 返回 `nt`（Windows）或 `posix`（Linux/macOS），跨平台分支判断时用。
4. **注意路径转义坑**：`path1 = '\home\user'` 这种写法里，`\u` 会被 Python 当成 Unicode 转义（`\u` 后面要跟 4 位十六进制），直接报 SyntaxError；Windows 路径要么用原始字符串 `r'C:\Users\x'`，要么用正斜杠 `'C:/Users/x'`，要么转义成 `'C:\\Users\\x'`。

【必须掌握】

- mkdir 建一层（父目录须存在）；makedirs 递归建多级（更常用）
- rmdir 删空目录；remove 删文件；删非空目录用 shutil.rmtree
- os.sep（分隔符）、os.name（nt/posix）跨平台判断
- Windows 路径反斜杠要转义或用 raw string / 正斜杠

【企业场景】

你在企业里，用例跑完要按"项目/日期/用例名"建日志目录：`os.makedirs(f"logs/{date}", exist_ok=True)`——`makedirs` 的递归 + `exist_ok=True` 避免"目录已存在"报错。而"Windows 路径反斜杠"是新人最常踩的坑：写 `'C:\Users\x'` 报 Unicode 转义错误，改 `r'C:\Users\x'` 就好。

【面试考察】

面试官："mkdir 和 makedirs 有什么区别？删除非空目录用什么？"

参考回答框架：
1. mkdir 只建单层目录，父目录必须存在；makedirs 递归建多级。
2. rmdir 只删空目录、remove 只删文件。
3. 删非空目录要用 shutil.rmtree（os 模块本身删不了）。

【易错点】

| 误区 | 纠正 |
|------|------|
| `'\home\user'` 直接写 | `\u` 被当 Unicode 转义报错；用 r'...' / 正斜杠 / 双反斜杠 |
| 用 mkdir 建多级目录 | 父目录不存在会报错，用 makedirs |
| 用 rmdir 删非空目录 | 只删空目录；非空用 shutil.rmtree |
| 用 remove 删目录 | remove 只删文件，删目录会报错 |

【我的理解】
> （`'C:\test'` 和 `r'C:\test'` 和 `'C:/test'` 三者有什么区别？为什么自动化代码里更推荐后两种写法？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| os 定位 | 操作系统层（对比 sys 解释器层），跨平台抽象 | ★★★☆☆ |
| os.path | join/abspath/exists/isdir/isfile/basename/dirname | ★★★★☆ |
| 目录文件操作 | mkdir vs makedirs、rmdir vs remove | ★★★★☆ |
| 其它 | os.sep / os.name / chmod + 路径反斜杠转义坑 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch03-sys模块]]（sys 管解释器、os 管操作系统，分工对照）
- [[Python/Ch25-文件操作]]（文件读写 open/with，与 os 的目录/路径操作互补）
- [[Web自动化测试/Ch13-Web自动化关键数据记录]]（日志/截图目录的 os 路径管理实际应用）
