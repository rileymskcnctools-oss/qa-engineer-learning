---
tags: [课程笔记, 功能测试]
course: "功能测试"
chapter: "Ch05-JavaScript基础"
date: 2026-07-10
status: in_progress
---

# Ch05 - JavaScript 基础

## 课程来源

- 学习日期：2026-07-10
- 章节：JavaScript 讲解

---

## 一、JavaScript 是什么

### 【课程定义】

> JavaScript 是一种轻量级的脚本语言，可插入 HTML 页面中，由浏览器直接执行。它不是 Java，两者除了名字相似外没有关系。

### 【为什么？】

HTML 是骨架，CSS 是皮肤，JS 是肌肉。JS 让页面"活起来"：

```
HTML  →  静态结构（"有什么"）
CSS   →  视觉样式（"长什么样"）
JS    →  动态行为（"能干什么"）
```

**测试工程师为什么必须懂 JS 基础？**

| 场景             | 需要 JS 知识的点                        |
| -------------- | --------------------------------- |
| F12 Console 调试 | console.log() 查看输出、检查变量值          |
| 自动化测试          | Selenium/Playwright 底层用 JS 操作 DOM |
| 前端 Bug 定位      | Console 报错看不懂 = 没法描述 Bug          |
| 接口测试           | 理解前端怎么调用后端接口                      |
| 性能测试           | JS 阻塞渲染、内存泄漏等概念                   |

### 【必须掌握】

- JS 的作用：改变内容、改变样式、验证输入、响应事件
- JS 运行在浏览器端（区别于后端语言如 Python/Java）
- JS 三件套中的角色：行为层

### 【面试考察】

> 面试官：HTML、CSS、JavaScript 在网页中分别起什么作用？

参考回答框架：
1. HTML：结构层，定义页面有什么元素
2. CSS：表现层，定义元素的样式和布局
3. JS：行为层，定义页面的交互逻辑
4. 类比：HTML=骨架，CSS=皮肤，JS=肌肉

### 【我的理解】

> 

---

## 二、JS 的使用方式

### 【课程定义】

```html
<!-- 方式1：内部脚本 -->
<script>
  alert("Hello World");
</script>

<!-- 方式2：外部脚本 -->
<script src="myScript.js"></script>
```

`<script>` 标签可放在 `<head>` 或 `<body>` 中。

### 【为什么？】

脚本位置影响页面加载行为：

| 位置          | 行为              | 问题              |
| ----------- | --------------- | --------------- |
| `<head>` 中  | 先加载执行 JS，再渲染页面  | JS 阻塞页面渲染，白屏时间长 |
| `<body>` 底部 | 先渲染页面，再执行 JS    | 用户体验好，推荐方式      |
| 加 `defer`   | 异步下载，DOM 解析完后执行 | 不阻塞渲染           |

### 【必须掌握】

- 内部和外部两种引用方式
- `<script>` 可以放在 head 或 body
- 外部脚本的好处：代码复用、缓存、可维护

### 【企业场景】

> 你打开一个页面发现白屏，F12 Console 显示 JS 报错。开发告诉你"因为 `<head>` 里的 JS 执行报错，阻塞了后面的页面渲染"。如果你不知道脚本位置和渲染顺序的关系，这个 Bug 你根本没法复述清楚。

### 【我的理解】

> 

---

## 三、JS 输出方式

### 【课程定义】

| 方法                 | 作用         | 谁看得到   |
| ------------------ | ---------- | ------ |
| `window.alert()`   | 弹出警告框      | 用户     |
| `document.write()` | 写入 HTML 文档 | 用户     |
| `console.log()`    | 写入浏览器控制台   | 开发者/测试 |

### 【为什么？】

**console.log() 是测试工程师最常用的 JS 方法。** 你用 F12 Console 可以直接执行 JS 来验证页面状态：

```javascript
// 测试时在 Console 里直接执行：
console.log(document.title);           // 看页面标题
console.log(document.cookie);          // 看 Cookie
console.log(document.getElementById("username").value);  // 看输入框的值
```

### 【必须掌握】

- 三种输出方法的区别和使用场景
- console.log 是调试的核心工具
- alert 会阻塞页面交互

### 【我的理解】

> 

---

## 四、JS 基础语法速查

### 4.1 字面量（数据类型）

| 类型  | 写法           | 示例                               |
| --- | ------------ | -------------------------------- |
| 数字  | 直接写          | `100`, `3.14`, `1e5`             |
| 字符串 | 单引号或双引号      | `"hello"`, `'world'`             |
| 数组  | 方括号          | `[1, 2, 3]`                      |
| 对象  | 花括号          | `{name: "tom", age: 20}`         |
| 函数  | function 关键字 | `function add(a,b){return a+b;}` |

### 4.2 变量

```javascript
var name = "张三";    // 旧方式（ES5）
let age = 25;         // 新方式（ES6），块级作用域
const PI = 3.14;      // 常量，不可重新赋值
```

| 关键字 | 可否重新赋值 | 作用域 | 测试关注点 |
|--------|------------|--------|-----------|
| var | 可以 | 函数级 | 有变量提升，容易出 Bug |
| let | 可以 | 块级 | 推荐使用 |
| const | 不可以 | 块级 | 定义配置/常量 |

### 4.3 运算符

| 类别 | 运算符 | 测试关注点 |
|------|--------|-----------|
| 算术 | `+ - * /` | 前端计算是否正确 |
| 赋值 | `= += -=` | — |
| 比较 | `> < == === !=` | **`==` vs `===` 是面试高频** |

### 【关键对比】== vs ===

```javascript
0 == "0"    // true   — 只比较值，会做类型转换
0 === "0"   // false  — 比较值和类型，不转换
```

| 运算符   | 含义            | 是否类型转换 | 推荐        |
| ----- | ------------- | ------ | --------- |
| `==`  | 等于（值相等）       | 是      | ❌ 容易出 Bug |
| `===` | 严格等于（值和类型都相等） | 否      | ✅ 推荐使用    |

### 4.4 函数

```javascript
function 函数名(参数1, 参数2) {
  return 返回值;
}
```

### 【易错点】

| 误区            | 正解                               |
| ------------- | -------------------------------- |
| var 和 let 没区别 | let 有块级作用域，var 没有，这会导致循环中的经典 Bug |
| == 和 === 差不多  | == 会隐式类型转换，测试中验证结果时建议用 ===       |
| JS 的函数必须有返回值  | 没有 return 时默认返回 undefined        |

### 【我的理解】

> 

---

## 五、操作 HTML DOM（核心）

### 【课程定义】

> DOM（Document Object Model，文档对象模型）是浏览器把 HTML 文档解析成一个树形结构的对象，JS 可以通过 DOM API 来查找、修改、添加、删除 HTML 元素。

### 【为什么？】

DOM 是连接 HTML 和 JS 的桥梁，也是自动化测试的基础：

```
HTML 页面
    ↓ 浏览器解析
  DOM 树
    ↓ JS 操作
  页面动态变化
```

**自动化测试的本质 = 通过 DOM 查找元素 + 模拟操作 + 验证结果。** Selenium 的 `find_element_by_id()`、Playwright 的 `page.locator()`，底层全是 DOM 操作。

### 【DOM 操作三件套】

#### ① 查找元素

| 方法   | 代码                                              | 返回    |
| ---- | ----------------------------------------------- | ----- |
| 按 id | `document.getElementById("username")`           | 单个元素  |
| 按标签名 | `document.getElementsByTagName("p")`            | 数组    |
| 按类名  | `document.getElementsByClassName("btn")`        | 数组    |
| 按选择器 | `document.querySelector(".btn.primary")`        | 第一个匹配 |
| 按选择器 | `document.querySelectorAll("input[type=text]")` | 所有匹配  |

> 在 F12 Console 里直接用这些方法验证元素存在性，是测试定位问题的捷径。

#### ② 改变内容

```javascript
// 改变元素的文本内容
document.getElementById("title").innerHTML = "新标题";

// 改变元素的属性
document.getElementById("logo").src = "new-logo.png";

// 改变样式
document.getElementById("box").style.color = "red";
```

#### ③ 读取值

```javascript
// 读取输入框的值
var username = document.getElementById("username").value;

// 读取 Cookie
var cookies = document.cookie;
```

### 【必须掌握】

- DOM 是什么：HTML 文档的树形对象表示
- 三种查找方法：id / 标签名 / 类名
- innerHTML（内容）vs value（输入框的值）vs attribute（属性）
- 能在 F12 Console 中手动执行 DOM 操作

### 【企业场景】

> 测试一个表单提交流程时，你想验证后端有没有对某个字段做校验。你打开 F12 Console，输入：
> ```js
> document.getElementById("phone").value = "123"
> ```
> 手动改了手机号的值再提交，发现后端没校验就通过了。这就是一个越权/校验缺失的 Bug。懂 JS DOM 操作 = 多了一种测试手段。

### 【面试考察】

> 面试官：在自动化测试中，怎么定位一个没有 id、没有 class 的元素？

参考回答框架：
1. 用 CSS Selector 或 XPath
2. 按层级关系定位（父元素→子元素）
3. 按属性定位（`input[name="username"]`）
4. 按文本内容定位（Playwright 的 `getByText()`）
5. 如果什么都没有，找开发加 `data-testid`

### 【我的理解】

> 

---

## 六、JS 事件

### 【课程定义】

> JS 可以在事件发生时执行代码，如用户点击、页面加载、输入改变等。

### 【事件速查】

| 事件          | 触发时机   | 对应的测试场景         |
| ----------- | ------ | --------------- |
| onclick     | 点击元素   | 按钮点击、链接点击       |
| onload      | 页面加载完成 | 验证页面初始化数据       |
| onunload    | 页面卸载   | 离开页面时的清理/保存     |
| onchange    | 输入字段改变 | 下拉框联动、实时校验      |
| onmouseover | 鼠标移入   | 悬停菜单、tooltip 显示 |
| onmouseout  | 鼠标移出   | 悬停菜单消失          |
| onkeydown   | 按下按键   | 快捷键、回车提交        |

### 【为什么？】

事件 = 测试用例的来源。每个事件属性都是一个需要验证的交互路径。

### 【企业场景】

> 需求文档写"用户输入身份证号后自动填充出生日期"。你怎么测？在身份证输入框输入 18 位号码（触发 onchange），然后检查出生日期字段是否自动填充。这个过程你不需要知道 JS 怎么写，但需要知道 onchange 事件是这个功能的触发器。

### 【我的理解】

> 

---

## 七、操作浏览器 BOM

### 【课程定义】

> BOM（Browser Object Model，浏览器对象模型）允许 JS 与浏览器窗口交互，包括 Window、Screen、Location、History 对象。

### 【BOM 核心对象速查】

| 对象            | 常用属性/方法                  | 测试场景              |
| ------------- | ------------------------ | ----------------- |
| **window**    | `innerWidth/innerHeight` | 响应式测试、多窗口测试       |
|               | `open()` / `close()`     | 弹窗广告、新窗口打开链接      |
| **screen**    | `availWidth/availHeight` | 不同屏幕分辨率下的显示       |
| **location**  | `hostname`               | 验证当前域名是否正确        |
|               | `pathname`               | 验证当前路径            |
|               | `protocol`               | 验证是 http 还是 https |
| **history**   | `back()` / `forward()`   | 浏览器后退/前进功能测试      |
| **navigator** | `userAgent`              | 浏览器类型和版本检测        |
|               | `cookieEnabled`          | Cookie 是否启用       |

### 【为什么？】

BOM 让你能从 JS 层面读取和操作浏览器状态。测试时常用：

```javascript
// 在 F12 Console 中快速验证：
console.log(location.hostname);     // 看当前域名
console.log(location.protocol);     // 看是 http 还是 https
console.log(window.innerWidth);     // 看当前窗口宽度
console.log(navigator.userAgent);   // 看浏览器标识
```

### 【必须掌握】

- BOM 和 DOM 的区别：DOM 操作页面内容，BOM 操作浏览器窗口
- 能在 Console 中读取 location、navigator、screen 信息
- window 是全局对象，所有全局变量都是 window 的属性

### 【企业场景】

> 测试一个 HTTPS 强制跳转功能：用户访问 `http://example.com` 应该自动跳转到 `https://example.com`。你在 F12 Console 里输入 `location.protocol`，如果结果是 `"http:"` 说明没跳转成功。这是最直接的验证方式。

### 【面试考察】

> 面试官：DOM 和 BOM 有什么区别？

参考回答框架：
1. DOM（文档对象模型）：操作 HTML 文档内容，如查找元素、改内容
2. BOM（浏览器对象模型）：操作浏览器窗口，如打开新窗口、获取屏幕尺寸、跳转 URL
3. DOM 是 BOM 的一部分（`window.document`）
4. DOM 有 W3C 标准，BOM 没有统一标准

### 【我的理解】

> 

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| JS 概念 | 脚本语言、三件套角色分工 | ★★☆ |
| 使用方式 | script 标签、内部/外部引用 | ★★☆ |
| 输出方式 | console.log 是测试核心工具 | ★★★ |
| 基础语法 | 变量 var/let/const、== vs === | ★★★ |
| DOM 操作 | 查找元素三方法、innerHTML vs value | ★★★ |
| JS 事件 | 每个事件 = 一个测试场景 | ★★★ |
| BOM 操作 | window/location/screen/history | ★★☆ |

---

## 今天没搞懂的问题

- 
- 
- 

## 关联笔记

- [[Ch04-HTML基础]]
- [[Ch03-Web基础知识]]
- [[Ch02-Web测试体系]]
