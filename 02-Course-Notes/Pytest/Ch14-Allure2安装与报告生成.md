---
tags: [课程笔记, Pytest, Allure]
course: "Pytest"
chapter: "Ch14-Allure2安装与报告生成"
created: 2026-07-28
status: draft
---

# Ch14 - Allure2 安装与报告生成

## 课程来源
- 学习日期：

---

## 一、Allure2 简介

### 知识点1：Allure2 是什么

【课程原话/定义】
Allure 是一款灵活的测试报告工具，用 Java 语言开发。它可以生成详尽的测试报告，包括测试类别、步骤、日志、图片等，并生成高水准的统计报告。Allure 还能轻松集成到 Jenkins 中，生成在线趋势汇总报告。

【为什么？】
> 请用自己的话回答：为什么已经有 pytest-html 了，还需要 Allure？

【必须掌握】
- Allure 是 Java 开发的测试报告框架，不绑定任何语言
- 支持 Python、Java、JS、PHP、Ruby 等多语言

【企业场景】
> 你在 CI 流水线（Jenkins/GitLab CI/GitHub Actions）中配置 Allure 报告，每次提交代码自动跑测试并生成报告。开发同学和 PM 不用找你，直接在 Jenkins 上点"Allure Report"就能看到这次的测试结果，还能和昨天的结果做趋势对比。

【面试考察】
> 面试官：你们公司用什么工具生成测试报告？能说下 Allure 报告里有哪些信息吗？
> 
> 参考回答框架：先说 Allure 是什么，再说你们实际怎么用的（CI 集成），最后举例报告里展示的信息（步骤、日志、截图、分类、严重级别）

【易错点】

| 易混淆概念 | 辨析 |
|-----------|------|
| Allure vs pytest-html | Allure 有分类体系（epic/feature/story）、趋势图、步骤展示、重试记录；pytest-html 只是简单的 HTML 报告 |
| Allure 框架 vs allure-pytest 插件 | Allure 框架是 Java 程序（提供 CLI），allure-pytest 是 Python 插件（在 pytest 里生成中间 JSON 数据） |

【我的理解】
> （请用自己的话总结 Allure2 是什么，以及它解决了什么痛点）

---

## 二、Allure2 安装

### 知识点2：安装的三部分

【课程原话/定义】
安装 Allure 需要：1) Java 环境 2) Allure 服务（CLI 工具）3) Allure 插件（Python 用 allure-pytest）

【为什么？】
> 为什么需要 Java 环境？（提示：Allure CLI 本身是 Java 程序）

【必须掌握】
- Java 环境（JDK 8+）
- 下载 Allure CLI，解压后把 `bin/` 目录加到 PATH
- `pip install allure-pytest`

| 组件            | 作用                                 | 验证命令               |              |
| ------------- | ---------------------------------- | ------------------ | ------------ |
| Java          | 运行 Allure CLI                      | `java -version`    |              |
| Allure CLI    | 把 JSON 中间数据渲染成 HTML 报告             | `allure --version` |              |
| allure-pytest | pytest 插件，生成 `--alluredir` 指定的中间数据 | `pip list          | grep allure` |

【企业场景】
> 新同事入职，你需要帮他配好 Allure 环境。你在他的电脑上按顺序检查：Java 装了没→Allure CLI 配了没→Python 插件装了没，三步走，少了哪步补哪步。

【面试考察】
> 面试官：Allure 环境搭建需要哪些步骤？
> 
> 参考回答框架：三部分，分别说清楚每个的作用，以及怎么验证安装成功。

【易错点】

| 常见错误                           | 正确做法                                |
| ------------------------------ | ----------------------------------- |
| 只装 allure-pytest 不装 Allure CLI | 两个都要装：插件生成数据，CLI 渲染报告               |
| 解压后忘记把 bin/ 加到 PATH            | 加到 PATH 后重启终端，`allure --version` 验证 |
| 用 scoop/choco/brew 装 Allure    | 也可以，但要知道手动安装的流程（面试会问）               |

【扩展知识】
- Mac: `brew install allure`
- Windows: `scoop install allure`
- Linux: `sudo apt install allure`

【我的理解】
> （请用自己的话描述安装 Allure 的三个步骤，每一步的作用是什么）

---

## 三、Allure2 运行方式

### 知识点3：报告生成流程

【课程原话/定义】
两步流程：1) 运行测试生成中间数据（JSON） 2) 通过 CLI 解析中间数据生成报告

【为什么？】
> 为什么要分两步？为什么不一次性生成 HTML 报告？

【必须掌握】

```
pytest --alluredir=./result    # 第一步：生成中间 JSON 数据
allure serve ./result           # 第二步：在线查看
allure generate ./result -o ./report --clean   # 第二步：生成静态报告
```

【企业场景】
> 你在 CI 流水线里这样配置：先跑 `pytest --alluredir=./result`，然后 `allure generate ./result -o ./report`，最后 Jenkins 的 Allure Plugin 自动读取 `./report` 展示在线报告。**没有人会在服务器上用 `allure serve`，因为它会阻塞终端。**

【面试考察】
> 面试官：`allure serve` 和 `allure generate` 有什么区别？
> 
> 参考回答框架：serve 是临时在线预览，关终端就没了；generate 生成静态 HTML 文件，可以部署到 Web 服务器或 Jenkins。CI 流水线里必须用 generate。

【易错点】

| 易混淆 | 区别 | 使用场景 |
|--------|------|----------|
| `allure serve` | 启动临时 HTTP 服务，退出命令报告销毁 | 本地调试时快速看报告 |
| `allure generate` | 生成 HTML/CSS/JS 静态文件到磁盘 | CI/CD 流水线，持久化保存 |

| 参数 | 含义 |
|------|------|
| `--alluredir=./result` | 指定中间数据存放目录 |
| `--clean-alluredir` | 先清空上次的中间数据 |
| `-o ./report` | 指定静态报告输出目录 |
| `--clean` / `-c` | 清理上一次的报告再生成 |
| `-h 127.0.0.1` | 指定 open 时的主机 IP |
| `-p 8883` | 指定 open 时的端口 |

【我的理解】
> （请用自己的话画出 Allure 报告生成的完整流程图，标注每一步用到的命令）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Allure 简介 | Java 开发的多语言测试报告工具 | ⭐⭐⭐ |
| 安装配置 | Java + Allure CLI + allure-pytest 三步 | ⭐⭐⭐⭐ |
| 报告生成 | 两步流程：中间数据 → 渲染报告 | ⭐⭐⭐⭐⭐ |
| serve vs generate | 临时预览 vs 静态部署 | ⭐⭐⭐⭐⭐ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch13-Pytest测试用例并行运行与分布式运行]]
- [[Ch15-Allure2用例装饰器]]
