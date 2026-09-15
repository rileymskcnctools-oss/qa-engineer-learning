---
tags: [课程笔记, 接口测试]
course: "接口测试"
chapter: "Ch11-抓包工具Charles"
created: 2026-09-15
status: draft
---

# Ch11 - 抓包工具 Charles

## 课程来源
- 学习日期：

---

## 一、Charles 是什么

### 知识点 1：Charles 简介与主要功能

【课程原话/定义】
Charles 是一款**跨平台**的代理工具，Mac、Windows、Linux 都可以使用。它通过**将自己设置成系统的网络访问代理服务器**，使得所有网络访问请求都通过它来完成，从而实现了网络数据包的截取和分析。

Charles 的主要功能：
- 支持 SSL 代理（抓 HTTPS 包）
- 支持流量控制（弱网模拟）
- 支持重发网络请求，方便后端调试
- 支持修改网络请求参数
- 支持网络请求的截获并动态修改
- 可以自动将 json 或 xml 数据格式化，方便查看

【为什么？】
Charles 的核心原理是**中间人代理（MITM）**：它把自己插在"客户端 ↔ 服务器"之间，客户端的请求先发给 Charles、Charles 再转发给服务器，服务器的响应也先经过 Charles 再回到客户端。因为流量"路过"它，所以它能看、能改、能重发。这也是为什么它能抓 HTTPS——它向客户端冒充服务器、向服务器冒充客户端，两边都用它自己的证书完成加密（所以需要安装并信任它的根证书，见 [[Ch12-抓包工具证书配置]]）。

【必须掌握】
- Charles 是跨平台（Mac/Windows/Linux）HTTP/HTTPS 代理抓包工具
- 原理：中间人代理，流量经过 Charles 被截获
- 六大功能：SSL 代理、流量控制、重发请求、修改参数、动态修改、json/xml 格式化
- 与 Fiddler 的区别：Charles 全平台，Fiddler 仅 Windows

【企业场景】
你在公司测一个 App，后端的接口文档不全或者和线上对不上。你把 Charles 打开、手机连上代理，在 App 里点几个操作，就能在 Charles 里看到 App 实际请求了哪些接口、传了什么参数、返回了什么数据——这是"还原接口真相"的最快手段，也是接口测试用例设计的前置动作。

【面试考察】
面试官："Charles 的抓包原理是什么？为什么能抓到 HTTPS 的明文？"

参考回答框架：
1. Charles 是中间人代理，客户端请求先发到 Charles，再由它转发给服务器
2. HTTPS 本身是加密的，但 Charles 用自己的证书"冒充"双方
3. 客户端信任了 Charles 的根证书，才会把 Charles 当作可信服务器
4. 所以 HTTPS 抓包的前提是"安装并信任 Charles 证书"

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| Charles 只能抓 HTTP | 装证书后也能抓 HTTPS（SSL Proxying） |
| Charles 是"黑客工具" | 是合法测试手段，用于还原接口协议、排查问题 |
| 抓包 = 只看看 | Charles 还能改请求、重发、断点、限速、做 mock |

【我的理解】
> （用自己的话说说"中间人代理"：Charles 站在客户端和服务器之间，它是怎么同时"骗过"两边的？这和安全里的"中间人攻击"是不是同一个机制？）

---

### 知识点 2：Charles 安装

【课程原话/定义】
Charles 官网：https://www.charlesproxy.com/ ，另有学社下载地址。

【为什么？】
为什么要提"安装"？因为 Charles 是商业软件，分**免费试用版和付费版**：免费版每次只能运行 30 分钟，到时间会自动关闭，需要重启（开发调试会反复被打断）。了解这一点，测试人员在公司里通常会申请付费 License，或者用 30 分钟版应付临时抓包。安装本身只是第一步，真正关键的是后续的证书配置（Ch12）。

【必须掌握】
- 官网下载：charlesproxy.com，跨平台（Mac/Windows/Linux）
- 免费版限制：每次运行约 30 分钟自动关闭
- 安装后需完成两件事才能正常抓 HTTPS：装证书 + 开启 SSL Proxying

【企业场景】
你在公司装好 Charles 后，第一件事不是立刻抓包，而是先完成两件配置：① 电脑装好并信任 Charles 根证书；② 在 Proxy → SSL Proxying Settings 里勾选要抓的域名。否则只能看到一堆 `CONNECT xxx:443` 的握手请求，看不到 HTTPS 的明文内容。

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 装完 Charles 直接就能抓 HTTPS | 还必须装证书 + 开启 SSL Proxying，否则只看到握手 |
| 免费版和付费版功能一样 | 免费版 30 分钟自动关，付费版无此限制 |
| 只在 Mac 上能用 | Charles 跨 Mac/Windows/Linux 三平台 |

【我的理解】
> （如果免费版 30 分钟就自动关闭，会对你的抓包工作造成什么影响？公司里一般怎么解决这个问题？）

---

## 二、Charles 界面介绍

### 知识点 3：界面布局（菜单栏 + 主导航栏）

【课程原话/定义】
菜单栏：
- File：session 相关操作
- Edit：基础复制粘贴等操作
- View：选择要查看的界面
- proxy（菜单）：抓包 recording / 抓 https 包 ssl proxying / 网络限速 throttling / 断点 breakpoint / 系统代理功能 macOS·Windows
- tools：map remote（请求转发、修改响应）/ map local（请求映射到本地数据）/ rewrite（重写修改请求与响应）

主导航栏：
- 左侧：Structure（按访问域名分类）/ Sequence（按访问时间排序）
- 右侧：某接口的请求内容，可切换导航查看详细情况（请求响应时间、请求头、请求详细内容、请求体等）
  - Overview：请求大体情况（请求头、起止时间、notes 等）
  - Content：请求具体内容和服务器响应（配合下方 header/cookies/form/raw 查看）
  - Summary：资源分布（服务器响应时长、host 等）
  - Chart：响应时间分布（表格）
  - Notes：给该请求记录备注

【为什么？】
为什么要分清 Structure 和 Sequence？因为这是两种"找请求"的视角：Structure 按**域名**分组（适合"我要看某个服务的所有接口"），Sequence 按**时间**排序（适合"我刚才那个操作发了什么请求"）。右侧的 Overview/Content/Summary 则是三个层次——Overview 看"是什么请求"、Content 看"具体数据"、Summary 看"性能概况"。分清这些，抓包时才能快速定位目标请求。

【必须掌握】
- Structure 按域名分类，Sequence 按时间排序
- proxy 菜单四大能力：recording（抓包）、ssl proxying（抓 https）、throttling（限速）、breakpoint（断点）
- tools 三大能力：map remote（转发）、map local（本地映射）、rewrite（重写）
- 右侧 Content 配合下方 header/cookies/form/raw 查看请求详情
- Overview/Summary/Chart 分别看概览/资源/耗时分布

【企业场景】
你在公司抓一个 App 的登录请求：先切到 Sequence 视图，按时间找到刚点的"登录"操作对应的请求；点开后切 Content → Headers 看请求头和 URL，切 Cookies 看登录态。如果想看这个登录接口的响应速度，切 Summary 看服务器响应时长、切 Chart 看耗时分布。Structure 视图则用于"只看某个域名（如 api.xxx.com）下的所有请求"。

【面试考察】
面试官："Charles 里 Structure 和 Sequence 视图有什么区别？"

参考回答框架：
1. Structure：按访问的域名分组展示请求，适合看某个服务的所有接口
2. Sequence：按访问时间排序展示请求，适合定位"刚才这个操作发的请求"
3. 两个视图互补：找操作对应请求用 Sequence，梳理某服务接口用 Structure

【易错点】

| 常见错误 | 正确理解 |
|----------|----------|
| 抓包太多找不到目标请求 | 用 Filter/Focus 过滤，或切 Sequence 按时间定位 |
| 把 map remote 和 map local 混淆 | map remote 转发到另一服务器；map local 映射到本地文件/数据 |
| rewrite 和断点混为一谈 | rewrite 是自动重写规则，断点是手动拦截修改 |

【我的理解】
> （Structure 和 Sequence 分别解决"找请求"的什么问题？如果我想看"刚才点登录按钮发了什么"，应该用哪个视图？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| Charles 简介 | 跨平台代理工具，中间人代理原理 | ★★★★☆ |
| 六大功能 | SSL 代理/流量控制/重发/改参/动态修改/格式化 | ★★★☆☆ |
| 安装 | 官网 + 免费版 30 分钟限制 | ★★☆☆☆ |
| 界面布局 | Structure/Sequence + proxy/tools 菜单 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch12-抓包工具证书配置]]
- [[Ch13-App抓包实战练习]]
- [[Ch08-接口测试用例设计]]
