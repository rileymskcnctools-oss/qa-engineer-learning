---
tags: [课程笔记, Python]
course: "Python"
chapter: "Ch01-PyCharm常用快捷键"
date: 2026-07-13
status: draft
---

# Ch01 - PyCharm 常用快捷键

## 1. 知识点理解

> 一句话解释：PyCharm 快捷键是用键盘组合键替代鼠标点击操作，让写代码和调试代码的速度翻倍。

| 维度 | 说明 |
|------|------|
| **一句话解释** | 键盘替代鼠标，减少手离开键盘的次数，保持编码流 |
| **为什么需要** | 你以后写自动化脚本，每天要在 PyCharm 里待 6 小时以上。快捷键省的不是"每次省 2 秒"，而是一天省几百次手从键盘移到鼠标再移回来的操作 |
| **在测试中的作用** | 写测试脚本时高频操作：注释/取消注释调试代码、格式化代码对齐、查找替换测试数据、快速跳转到报错行——全在快捷键上完成 |

## 2. 常用快捷键速查

> 此节替代通用模板的"Python 语法"（本节偏工具操作）。以下以 Windows 为准，macOS 将 `Ctrl` 替换为 `Command`。

### 核心快捷键（按使用频率排序）

| 快捷键                 | 作用        | 测试场景中什么时候用                    |
| ------------------- | --------- | ----------------------------- |
| `Ctrl + /`          | 注释/取消注释   | 调试时临时屏蔽某行断言 `# assert ...`    |
| `Ctrl + Alt + L`    | 代码格式化     | 从网页复制代码段后，一键对齐缩进              |
| `Ctrl + D`          | 复制当前行     | 写多个相似测试用例时，复制上一行改参数           |
| `Ctrl + F`          | 查找        | 在几百行脚本中找变量名、函数名               |
| `Ctrl + R`          | 替换        | 批量把测试数据中的 `url_a` 替换为 `url_b` |
| `Alt + Enter`       | 问题修复      | 红色波浪线提示导入缺失，一键 import         |
| `Ctrl + Shift + ↑↓` | 上下移动当前行   | 调整测试步骤顺序                      |
| `Ctrl + G`          | 跳转到指定行    | 报错信息说第 87 行出错，直接跳过去           |
| `Tab`               | 缩进 / 跳制表域 | 代码块缩进，或接受代码补全建议               |

### 记忆技巧

```
Ctrl + /      → / 像注释符号 //
Ctrl + D      → D = Duplicate（复制）
Ctrl + F/R    → F = Find, R = Replace
Alt + Enter   → Enter = 确认修复建议
Ctrl + G      → G = Go to line
```

### 示例：一段测试脚本中的快捷键运用

```python
# 1. 从别处复制了一段代码 →  Ctrl + Alt + L  格式化
# 2. 想临时跳过第 3 行    →  光标放第 3 行 → Ctrl + /  注释
# 3. 发现 all 拼错了       →  Ctrl + F  查找 "all"
# 4. 批量替换为 assert     →  Ctrl + R  全部替换
# 5. 第 10 行报错           →  Ctrl + G  输入 10  跳转

def test_login():
    result = login("admin", "123456")
    # allert(result["msg"] == "success")       # 临时注释掉
    assert result["code"] == 200               # 修复后
    assert result["msg"] == "success"
```

## 3. 测试应用场景

| 场景        | 怎么用                                              | 对应阶段 |
| --------- | ------------------------------------------------ | ---- |
| 测试用例      | 写测试函数时：`Ctrl+D` 复制上一个用例快速改参数，`Ctrl+/` 注释切换不同断言方式 | 目前   |
| 自动化脚本     | 脚本报错后：`Ctrl+G` 跳转报错行，`Alt+Enter` 自动导入缺失模块        | 后续   |
| Pytest 集成 | 运行测试后 PyCharm 底部面板显示失败用例，点击直接跳转，配合快捷键修 Bug       | 后续   |

> 说明：目前只需要关注「测试用例」列，自动化/Pytest 是后续学习内容，此处先建立印象。

## 4. 易错点

| 常见错误 | 错误原因 | 解决方法 |
|---------|---------|---------|
| 快捷键不生效 | 输入法是中文状态 | 切换到英文输入法再按快捷键 |
| `Ctrl + /` 没反应 | 按成了数字键盘的 `/` | 用主键盘区域的 `/`（在 `.` 右边） |
| `Ctrl + Shift + 方向键` 不移动行 | 输入法占用了 `Ctrl + Shift` 切换 | 在 PyCharm 设置中修改快捷键，或临时切输入法 |
| macOS 上按了 `Ctrl` 没反应 | macOS 多数快捷键用 `Command` | Windows `Ctrl` → macOS `Command` |
| 代码格式化反而更乱 | 代码有语法错误时会格式化失败 | 先修红色波浪线，再格式化 |

## 5. 实战练习

> 每个练习围绕测试场景设计，不写脱离测试的纯语法练习。

### 练习 1：快捷键肌肉记忆

在 PyCharm 中新建 `test_demo.py`，输入以下代码（故意不缩进、不格式化）：

```python
def test_user_login():
result = login("admin", "123")
assert result["code"] == 200
print("登录成功")
assert result["msg"] == "success"
```

依次完成：
1. `Ctrl + Alt + L` 格式化整个文件
2. `Ctrl + /` 注释掉 `print` 那行
3. `Ctrl + D` 复制 `assert result["msg"]` 这一行，改断言内容
4. `Ctrl + F` 查找所有 `assert` 确认断言数量

### 练习 2：模拟调试流程

```python
# 假设这段代码在第 42 行报错
# 1. Ctrl + G → 输入 42 → 跳转到第 42 行
# 2. Alt + Enter → 看有没有修复建议
# 3. Ctrl + / → 如果不确定怎么修，先注释掉这行

def test_calculator():
    a = 10
    b = 0
    result = a // b  # ← 这里报错 ZeroDivisionError
    assert result == 0
```

### 练习 3：批量替换测试数据

```python
def test_api_1():
    response = requests.get("http://old-server.com/api/user/1")
    assert response.status_code == 200

def test_api_2():
    response = requests.get("http://old-server.com/api/user/2")
    assert response.status_code == 200
```

用 `Ctrl + R` 把所有 `old-server.com` 替换为 `new-server.com`。

## 6. 自动化关联

| 关联框架 | 关系说明 | 学到时会怎么用 |
|---------|---------|--------------|
| **Pytest** | PyCharm 原生支持 Pytest，右键直接运行测试函数 | 写完 `test_xxx()` → 左侧出现绿色三角 → 点一下运行 |
| **Selenium** | 在 PyCharm 中写 Selenium 脚本，断点调试看浏览器操作步骤 | `Ctrl + F8` 打断点 → `Shift + F9` Debug |
| **Playwright** | Playwright 的 `--debug` 模式和 PyCharm 调试器无缝配合 | 单步执行看每一步浏览器操作 |

## 7. 面试输出

> 30 秒能说完的回答。

**问题：你平时用什么 IDE 写 Python？效率提升有哪些？**

**回答：** 我用 PyCharm，几个高频快捷键能省大量操作——`Ctrl+Alt+L` 一键格式化，`Ctrl+D` 复制行快速写相似测试用例，`Ctrl+/` 注释切换调试断言，`Ctrl+G` 根据报错行号直接跳转。另外 PyCharm 对 Pytest 原生支持，写完 `test_` 开头的函数左侧就有运行按钮，不用命令行手动跑。

## 8. 我的疑问

-
-
-

---

## 关联笔记

- [[Ch02-Web测试体系|功能测试/Ch02-Web测试体系]]
- [[Pytest/README|Pytest]]
