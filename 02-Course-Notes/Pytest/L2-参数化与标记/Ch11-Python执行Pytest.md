---
tags: [课程笔记, Pytest]
course: "Pytest"
chapter: "Ch11-Python执行Pytest"
created: 2026-09-17
status: in_progress
---

# Ch11 - Python 执行 Pytest

## 课程来源
- 学习日期：2026-09-17
- 课程源：霍格沃兹教程站 pytest_test_framework/v2/L2

---

## 一、用 Python 代码执行 pytest

### 知识点 1：pytest.main() 与 python -m pytest

【课程原话/定义】
除了命令行 pytest，还可以用 Python 方式执行：

1. **pytest.main()**（写在 if __name__ == '__main__' 里）：
```python
import pytest
if __name__ == '__main__':
    # 运行当前目录所有符合规则的用例
    pytest.main()
    # 运行指定模块的某条用例
    pytest.main(['test_mark1.py::test_dkej', '-vs'])
    # 运行某个标签
    pytest.main(['test_mark1.py', '-vs', '-m', 'dkej'])
```
运行：python test_*.py

2. **python -m pytest**（模块方式运行，保证用当前环境 pytest）：
```bash
python -m pytest test_demo.py
```

【为什么？】
为什么要用 Python 执行 pytest？因为自动化测试要"脚本化"——比如批量执行多个测试文件、自定义测试过程（设置环境、准备数据、处理结果）。pytest.main() 让你在 Python 代码里控制执行，方便和 CI、脚本集成。而 python -m pytest 的价值是"环境一致性"——保证用的是当前虚拟环境的 pytest（避免多版本/路径问题），在 Jenkins 等 CI 里推荐。两者都是"测试框架工程化"的一部分。

【必须掌握】
- pytest.main()：Python 代码里执行，参数传列表
- pytest.main(['文件::用例', '-vs'])：指定用例 + 参数
- pytest.main(['文件', '-m', '标签'])：按标签
- python -m pytest：保证当前环境 pytest，CI 推荐
- python 文件.py 直接执行（main 入口）

【企业场景】
你在公司写了个测试脚本，用 pytest.main() 批量执行多个测试文件 + 处理结果；CI（Jenkins）里用 python -m pytest 保证跑的是虚拟环境的 pytest。这两种方式让"跑测试"从手动命令变成"可脚本化、可 CI 化"。

【面试考察】
面试官：「怎么用 Python 执行 pytest？python -m pytest 有什么好处？」

参考回答框架：
1. pytest.main() 在代码里执行，参数传列表
2. python -m pytest 模块方式运行
3. python -m pytest 保证当前环境 pytest，避免多版本混淆
4. CI 里推荐 python -m pytest

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| pytest.main 参数忘加列表 | pytest.main(['-vs']) 参数是列表，不是字符串 |
| 多版本 pytest 直接 pytest | 用 python -m pytest 保证当前环境 |
| main 没写 if __name__ | 导入时也会执行，要包在 if __name__ == '__main__' |

【我的理解】
> （python -m pytest 和直接 pytest 有什么区别？为什么 CI 环境推荐前者？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Python 执行 | pytest.main / python -m pytest | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch10-Pytest运行用例]]
- [[Ch05-Pytest命令行常用参数]]
