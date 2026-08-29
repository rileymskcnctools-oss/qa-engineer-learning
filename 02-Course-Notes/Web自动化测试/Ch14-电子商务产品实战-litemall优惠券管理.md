---
tags:
  - 课程笔记
  - Web自动化测试
  - Selenium
  - 综合实战
  - litemall
  - 优惠券
  - Allure
  - PO设计模式
course: Web自动化测试
chapter: Ch14-电子商务产品实战-litemall优惠券管理
created: 2026-08-29
status: draft
---

# Ch14 - 电子商务产品实战（litemall 优惠券管理）

## 课程来源
- 学习日期：

---

## 一、产品分析

### 知识点 1：实战项目——litemall 管理后台

【课程原话/定义】
- **产品**：litemall 管理后台（开源电商后台管理系统，基于 Vue + Element UI）
- **功能**：优惠券管理（新增 + 删除）
- **被测产品地址**：`https://litemall.hogwarts.ceshiren.com/`
- **使用账户**：用户名 `hogwarts` / 密码 `test12345`

【为什么？】
这是 Web 自动化模块第一个**真正"登录态 + 后台 CRUD"**的完整实战。相比 Ch10 的搜索功能（匿名、单表单），litemall 的优惠券管理覆盖了自动化测试最常遇到的四类复杂度：

1. **登录态前置**——所有操作都要先登录，登录放 setup，后面用例直接复用
2. **两级导航**——左侧边栏"推广管理"展开后才是"优惠券管理"，要先点一级再点二级
3. **多字段表单 + 下拉选择**——优惠券名称/介绍/标签/金额/限领/类型/数量/天数，其中"分发类型"是下拉框，不是简单输入
4. **列表断言**——新增完要验证"列表最顶部一行"，删除完要验证"不在列表里"

选"优惠券"作为实战对象，正是因为它是管理后台里最典型的"表单密集型"功能，能把前面所有章节（定位、等待、交互、断言、留证）串成一条完整链路。

【必须掌握】
- 实战项目的完整信息：产品 / 功能 / 地址 / 账号
- 管理后台自动化的四大复杂度：登录态 / 多级导航 / 复杂表单+下拉 / 列表断言
- "选择哪个功能做实战"的标准：能覆盖足够多的定位与交互技巧

【企业场景】
你在企业里被分配"把 XX 后台的 XX 模块做成自动化"，第一件事就是像本知识点一样做**产品分析**：被测地址、测试账号、需要哪些前置权限、模块的页面结构（几级菜单、几个表单、几个弹窗）。这一步没做清楚，后面写脚本会反复"找不到元素、进不去页面"。

【面试考察】
面试官："如果让你自动化一个管理后台的功能，你会选哪个功能？为什么？"

参考回答框架：
1. 选"表单密集 + 有增删改查 + 有登录态"的功能（如优惠券管理），因为能覆盖定位/等待/交互/断言的完整技能
2. 先产品分析：地址、账号、权限、页面结构
3. 再拆复杂度：登录态、多级导航、下拉/日期控件、列表断言
4. 最后才是写脚本

【易错点】

| 误区 | 纠正 |
|------|------|
| 拿"匿名、单表单"的功能当实战练 | 覆盖不了登录态、下拉、列表断言，练不到真实后台复杂度 |
| 直接开 IDE 写代码，跳过产品分析 | 地址/账号/权限没确认清楚，脚本会反复报错 |

【我的理解】
> （为什么选"优惠券管理"而不是"商品列表查看"这类只读功能做实战？"能覆盖足够多技巧"和"贴近真实后台复杂度"是什么关系？）

---

## 二、测试用例分析

### 知识点 2：添加 + 删除两条用例（数据依赖闭环）

【课程原话/定义】

| 用例标题 | 前提条件 | 用例步骤 | 预期结果 |
|----------|----------|----------|----------|
| 添加优惠券 | 1. 登录并进入用户管理后台<br>2. 登录账号有商场管理的权限 | 1. 点击增加<br>2. 输入优惠券名称等全部信息<br>3. 点击确定 | 1. 跳转优惠券列表，有成功提示信息<br>2. 新增优惠券在列表最顶部一行 |
| 删除优惠券 | 1. 进入用户管理后台<br>2. 商品列表里面有已存在的优惠券（新增） | 1. 点击删除按钮 | 1. 有删除成功提示信息<br>2. 被删除商品不在优惠券列表展示 |

【为什么？】
这两条用例暴露了自动化测试里一个核心概念：**数据依赖**。

删除用例的前提是"列表里已有优惠券"，而这个优惠券正是"添加用例"刚创建的。两条用例构成一个**闭环**：

```
添加用例 → 产生数据（新增的优惠券） → 删除用例消费这份数据（删掉它）
```

这带来两个工程问题：
1. **执行顺序**——删除依赖添加先跑。Pytest 默认按方法名字母序跑，`test_add_...` 恰好排在 `test_delete_...` 前，但这是"撞上的"，不可靠。
2. **数据污染/独立性**——如果添加失败，删除就没有可删的对象，跟着一起红。

再对比两条用例的**预期结果**，都是"提示信息 + 列表状态"两段式：提示信息（`成功` + 具体文案）是"过程断言"，列表状态（在最顶部 / 不在列表）是"结果断言"。这印证了 Ch10 的观点——预期结果必须落到"可断言的文本/列表元素"上。

【必须掌握】
- 两条用例的前置/步骤/预期，以及"数据依赖闭环"
- 预期结果的"两段式"：提示信息（过程）+ 列表状态（结果）
- 用例的前置条件（登录、权限）对应脚本里的 setup / 登录动作

【企业场景】
你在企业里设计自动化用例时，最怕"用例之间互相依赖"。理想是每条用例独立（自带数据、自清理），但后台 CRUD 天然有"先增后删"的依赖。做法是：**用 setup 统一造数据，用 teardown 统一清理**，把"删除"从"独立用例"变成"清理动作"，或者给数据加唯一标识（如时间戳）避免两条用例操作同一条数据。

【面试考察】
面试官："你的用例之间有数据依赖怎么办？怎么保证用例可重复执行？"

参考回答框架：
1. 先识别依赖：删除依赖添加产出的数据
2. 理想方案：用例独立化——每条用例自己造数据、自己清理（fixture 的 setup/teardown）
3. 数据唯一化：名称/ID 加时间戳或随机串，避免多次执行冲突
4. 清理动作：把"删"从断言用例里拆出来，放进 teardown 保证不留脏数据

【易错点】

| 误区 | 纠正 |
|------|------|
| 依赖 Pytest 方法名排序保证"先增后删" | 不可靠，应按数据依赖显式设计或用 fixture |
| 用例数据用固定名（"新人优惠券-test"） | 多次执行会冲突，应加时间戳/随机串 |
| 把"删除"只当独立用例 | 更稳的做法是删除兼做数据清理（teardown） |

【我的理解】
> （"删除用例依赖添加用例的数据"这个闭环，为什么会导致"添加一失败、删除跟着红"？如果要让两条用例互不依赖，你会怎么改？）

---

## 三、脚本编写思路与前置后置

### 知识点 3：setup_class / teardown_class + 隐式等待

【课程原话/定义】
> 📷 【截图占位】编写脚本思路的 UML 流程图（源文件里的 "uml diagram"）

```python
class TestLitemallDiscountCoupon:

    def setup_class(self):
        # 打开浏览器
        self.driver = webdriver.Chrome()
        # 添加隐式等待配置
        self.driver.implicitly_wait(15)

    def teardown_class(self):
        # 关闭浏览器进程
        self.driver.quit()
```

【为什么？】
这里用 `setup_class` / `teardown_class` 而不是 `setup_method` / `teardown_method`，是因为它是**类级（class）fixture，整个测试类只执行一次**。

对两条用例（添加 + 删除）来说，它们共享同一个浏览器和同一个登录态：
- 如果 driver 放 `setup_method`，每条用例都会开一个新浏览器 + 重新登录，慢一倍
- 放 `setup_class`，浏览器只开一次，登录只做一次，两条用例复用 → 快、且模拟"真实用户连续操作"

这正是 Ch04 讲的**粒度权衡**：driver 和登录态放类级（复用、快），数据清理放方法级（防污染）。

`implicitly_wait(15)` 是全局兜底：任何 `find_element` 找不到元素时，最多等 15 秒再抛异常。注意这里值偏大（15s），因为 litemall 是远程站点、网络慢；本地/内网项目通常 3-5s 就够（Ch07 结论）。

【必须掌握】
- `setup_class` / `teardown_class` 是类级，整个类执行一次；`setup_method` / `teardown_method` 是方法级，每条用例执行一次
- driver + 登录放类级（复用），数据清理放方法级
- `implicitly_wait` 全局兜底，值按网络环境调（本地小、远程大）
- `driver.quit()` 放 teardown，保证用例失败也能关浏览器（Ch05 结论）

【企业场景】
你在框架里定基线：`setup_class` 只做三件事——开浏览器、设隐式等待、最大化窗口；`teardown_class` 只做一件事——`driver.quit()`。登录可以放 `setup_class`（如果整个类都要登录）或抽成 fixture。这样每个测试类的生命周期是清晰的"开 → 用 → 关"，不会出现"用例失败后 chromedriver 僵尸进程堆积"。

【面试考察】
面试官："`setup_class` 和 `setup_method` 的区别？driver 应该放哪个？"

参考回答框架：
1. class 级执行一次，method 级每条用例执行一次
2. driver 放 class 级：多个用例共享一个浏览器，快且复用登录态
3. 但要注意：类级共享意味着用例之间会互相影响（数据、状态），需要时用 method 级隔离
4. 收尾 `quit()` 放 teardown，避免失败时残留进程

【易错点】

| 误区 | 纠正 |
|------|------|
| driver 放 `setup_method` | 每条用例重开浏览器 + 重登录，慢 |
| 隐式等待写 15s 到所有项目 | 本地/内网 3-5s 即可，15s 是远程站点妥协值 |
| teardown 只写 `quit()` 但写在用例最后一行 | 用例失败不执行，残留僵尸进程，必须放 teardown |

【扩展知识】
`setup_class` 对应 JUnit 的 `@BeforeAll`，`setup_method` 对应 `@BeforeEach`（Ch04 的 Pytest↔JUnit 对照表）。类级共享是"性能优先"，方法级隔离是"独立性优先"，团队里通常约定：**driver 类级，数据方法级**。

【我的理解】
> （为什么 driver 和登录放类级、数据清理放方法级？如果反过来——driver 方法级、数据类级——会出什么问题？）

---

## 四、初步实现功能（登录 + 新增 + 删除）

### 知识点 4：完整脚本与实战定位

【课程原话/定义】
完整脚本（登录 + 新增 + 删除）：

```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestLitemallDiscountCoupon:

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        # 登录
        self.driver.get("https://litemall.hogwarts.ceshiren.com/#/login?redirect=%2Fdashboard")
        username = self.driver.find_element(By.NAME, "username")
        username.clear()
        username.send_keys("hogwarts")
        password = self.driver.find_element(By.NAME, "password")
        password.clear()
        password.send_keys("test12345")
        self.driver.find_element(By.CSS_SELECTOR, '.el-button').click()
        # 准备测试数据
        self.coupon_name = "新人优惠券-test"

    def teardown_class(self):
        self.driver.quit()

    def test_add_discount_coupon(self):
        # 点击左侧边栏 推广管理
        self.driver.find_element(By.XPATH, "//span[text()='推广管理']").click()
        # 点击二级菜单 优惠券管理
        self.driver.find_element(By.XPATH, "//span[text()='优惠券管理']").click()
        # 点击 添加 按钮
        self.driver.find_element(By.XPATH, "//span[text()='添加']").click()
        # 输入优惠券名称
        self.driver.find_element(
            By.XPATH, "//label[text()='优惠券名称']/..//*[@class='el-input__inner']"
        ).send_keys(self.coupon_name)
        # 输入介绍
        self.driver.find_element(
            By.XPATH, "//label[text()='介绍']/..//*[@class='el-input__inner']"
        ).send_keys("测试优惠券")
        # 输入标签
        self.driver.find_element(
            By.XPATH, "//label[text()='标签']/..//*[@class='el-input__inner']"
        ).send_keys("测试")
        # 输入最低消费金额
        low_ele = self.driver.find_element(
            By.XPATH, "//label[text()='最低消费']/..//*[@class='el-input__inner']"
        )
        low_ele.clear()
        low_ele.send_keys("100")
        # 输入满减金额
        reduce_ele = self.driver.find_element(
            By.XPATH, "//label[text()='满减金额']/..//*[@class='el-input__inner']"
        )
        reduce_ele.clear()
        reduce_ele.send_keys("100")
        # 输入每人限领数量
        per_num_ele = self.driver.find_element(
            By.XPATH, "//label[text()='每人限领']/..//*[@class='el-input__inner']"
        )
        per_num_ele.clear()
        per_num_ele.send_keys("2")
        # 点击分发类型下拉按钮
        time.sleep(2)
        self.driver.find_element(
            By.XPATH, "//label[text()='分发类型']/..//span[@class='el-input__suffix-inner']"
        ).click()
        # 点击下拉列表中的 注册赠券
        time.sleep(2)
        eles = self.driver.find_elements(
            By.XPATH, "//div[@class='el-scrollbar']//span[text()='注册赠券']")
        eles[1].click()
        # 输入优惠券数量
        num_ele = self.driver.find_element(
            By.XPATH, "//label[text()='优惠券数量']/..//*[@class='el-input__inner']"
        )
        num_ele.clear()
        num_ele.send_keys("100")
        # 输入优惠券有效天数
        days_ele = self.driver.find_element(
            By.XPATH, "//div[text()='天']/..//*[@class='el-input__inner']"
        )
        days_ele.clear()
        days_ele.send_keys("15")
        # 点击确定按钮
        self.driver.find_element(By.XPATH, "//span[text()='确定']").click()
        time.sleep(1)
        result = self.driver.find_element(By.CSS_SELECTOR, ".el-notification__title").text
        result_msg = self.driver.find_element(
            By.CSS_SELECTOR, ".el-notification__content > p").text
        assert result == "成功"
        assert result_msg == "创建优惠券成功"
        # 验证新增的优惠券在列表中
        eles = self.driver.find_elements(
            By.CSS_SELECTOR, ".el-table_1_column_2.is-center.el-table__cell")
        counpun_names = [e.text for e in eles]
        assert self.coupon_name in counpun_names

    def test_delete_discount_coupon(self):
        time.sleep(5)
        # 点击新增优惠券的删除按钮
        self.driver.find_element(
            By.XPATH, f"//div[text()='{self.coupon_name}']/../..//*[text()='删除']"
        ).click()
        time.sleep(1)
        result = self.driver.find_element(By.CSS_SELECTOR, ".el-notification__title").text
        result_msg = self.driver.find_element(
            By.CSS_SELECTOR, ".el-notification__content > p").text
        assert result == "成功"
        assert result_msg == "删除优惠券成功"
        # 验证删除的优惠券不在列表中
        eles = self.driver.find_elements(
            By.CSS_SELECTOR, ".el-table_1_column_2.is-center.el-table__cell")
        counpun_names = [e.text for e in eles]
        assert self.coupon_name not in counpun_names
```

【为什么？】
这份脚本把前面所有章节串成了完整链路，同时暴露了**实战中真实的脆弱点**：

1. **结构定位**：`//label[text()='优惠券名称']/..//*[@class='el-input__inner']` 是"先按 label 文本找标签 → 回父节点 → 再找输入框"。这是 Element UI 表单的经典定位方式（input 没有语义 id，只能靠 label 文本关联）。但它依赖 `el-input__inner` 这个内部 class，前端换 UI 框架就崩。
2. **下拉选择用索引**：`find_elements(...注册赠券...)` 找到多个匹配，`eles[1].click()` 硬编码点第 2 个。这是**最脆弱的定位**——页面上"注册赠券"文本出现的位置一变，索引就错。
3. **动态表格 class**：`.el-table_1_column_2.is-center.el-table__cell` 里的 `el-table_1_column_2` 是 Element UI **自动生成**的序号类名，列顺序一变就失效。
4. **两段式断言**：先断 `el-notification__title == "成功"` + `content == "创建优惠券成功"`（过程），再断优惠券名在/不在列表（结果），正是知识点 2 说的两段式。

【必须掌握】
- 登录 → 两级导航 → 表单填写 → 下拉选择 → 确定 → 通知断言 → 列表断言，完整链路
- Element UI 表单定位：`//label[text()='X']/..//*[@class='el-input__inner']`
- 两段式断言：通知提示（过程）+ 列表状态（结果）
- 识别脚本里的脆弱点：动态 class、索引定位、内部 class 依赖

【企业场景】
你在企业里写的第一个后台自动化脚本，大概率就是长这样——能跑通，但满是 `time.sleep`、硬编码索引、动态 class。这不是"写错了"，而是"第一版脚本的正常状态"。关键是你**知道它哪里脆弱**：下次页面改版，`.el-table_1_column_2` 变成 `.el-table_2_column_2`，脚本就红，你要能立刻定位到"是动态 class 变了"，而不是从头查。

【面试考察】
面试官："这段脚本里有哪些地方不稳定？怎么改进？"

参考回答框架：
1. `time.sleep` → 显式等待（等元素/条件出现）
2. `eles[1]` 索引定位下拉 → 改语义化定位（data-test-id）或文本精确匹配
3. `.el-table_1_column_2` 动态 class → 用稳定属性或 `data-test-id`
4. 大量重复的 `find_element(By.XPATH, "//label[text()='X']/..//...")` → 抽公共方法，PO 模式解决

【易错点】

| 误区 | 纠正 |
|------|------|
| `.el-table_1_column_2` 当稳定定位 | Element UI 自动生成的序号 class，列一变就失效 |
| `eles[1]` 硬编码索引 | 依赖元素出现顺序，极脆弱 |
| `//label[text()='X']/..//*[@class='el-input__inner']` 到处复制 | 抽成"按 label 找输入框"的公共方法 |
| 变量名 `counpun_names`（课程笔误） | 应为 `coupon_names` |

【扩展知识】
Element UI 表单的三种定位思路对比：①label 文本关联（本脚本，最直观）②`data-test-id`（需前端配合，最稳）③`el-form-item` 的 `label` 属性。治本方案还是 Ch09 说的"推动前端补 `data-test-id`"，把定位契约化。

【我的理解】
> （脚本里 `eles[1].click()` 为什么是最脆弱的一行？如果前端在"注册赠券"前面又加了一个相同文本的元素，会发生什么？）

---

## 五、代码优化（强制等待 → 显式等待）

### 知识点 5：expected_conditions 与自定义显式等待条件

【课程原话/定义】

```python
# 使用 expected_conditions 提供的方法
WebDriverWait(self.driver, 10).until_not(
    expected_conditions.visibility_of_any_elements_located(
        (By.XPATH, "元素定位")))

# 自定义显式等待条件
def click_execption(by, element, attempts=5):
    def _inner(driver):
        """多次点击同个按钮"""
        count = 0           # 实际循环次数
        while count < attempts:
            try:
                count += 1
                driver.find_element(by, element).click()
                return True
            except Exception:
                print("出现异常啦")
        return False
    return _inner

# 使用自定义的显式等待条件
WebDriverWait(self.driver, 10).until(click_execption(By.CSS_SELECTOR, "元素定位"))
```

【为什么？】
这一步是"从能跑 → 能维护"的关键跃迁。核心动机还是 Ch07 那句话：**`time.sleep` 是死等固定时间，显式等待是"条件满足即返回"**。

两个新知识点：

1. **`expected_conditions`（EC）**：Selenium 提供的一组现成等待条件（元素可见、可点击、文本出现、元素消失……）。`until(条件)` 每 0.5s 轮询一次，条件满足就返回，超时抛 `TimeoutException`。`until_not(条件)` 反过来——**条件为假时才返回**（常用于"等某元素消失"）。

2. **自定义显式等待条件**：`until()` 接受的是"接收 driver 参数、返回布尔值的函数"。`click_execption` 就是自定义条件——它把"点击"包装成"可重试"的操作：循环尝试点击，成功返回 `True`，异常则再试，超过 `attempts` 次返回 `False`（触发超时）。

【必须掌握】
- `WebDriverWait(driver, 超时).until(EC.xxx((By.X, "locator")))` —— 显式等待标准写法
- `until` 等"条件为真"，`until_not` 等"条件为假"
- 自定义条件：传给 `until` 一个 `def fn(driver) -> bool`
- 常用 EC：`presence_of_element_located` / `visibility_of` / `element_to_be_clickable` / `text_to_be_present_in_element` / `invisibility_of_element_located`

【企业场景】
你在项目里定了规范：**正式代码里不允许出现 `time.sleep`**（只允许调试时临时用）。所有等待都走显式等待，理由是：①快——条件一满足立刻继续，不浪费固定秒数；②稳——等的是"业务条件"而不是"拍脑袋的秒数"；③可维护——超时报错信息清楚，能看出"在等什么没等到"。

【面试考察】
面试官："怎么把 `time.sleep` 换成显式等待？自定义等待条件怎么写？"

参考回答框架：
1. `WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "...")))`
2. EC 是一组现成条件，`until` 轮询到满足才返回
3. 自定义条件 = 写一个 `def fn(driver) -> bool` 传给 `until`
4. 举例：重试点击（点击失败再试 N 次）就是一种自定义条件
5. 对比：`until` 等为真，`until_not` 等为假（等元素消失）

【易错点】

| 误区 | 纠正 |
|------|------|
| `click_execption` 拼写（课程笔误） | 应为 `click_exception` |
| 以为 `click_execption` 是"等元素可点击" | 它本质是"点击失败重试 N 次"，不是可点击性判断；真正等可点击用 `EC.element_to_be_clickable` |
| 注释"多次点击同个按钮"（课程表述不准） | 实际是"重试点击直到成功"，不是无脑点多次 |
| `until_not(visibility_of_any_elements_located(...))` 写法别扭 | "等元素不可见"更直白用 `invisibility_of_element_located` |
| 以为"优化章节说全替换"就真的没 sleep 了 | 优化后的完整脚本里其实仍有 `time.sleep(1)` 残留，课程没替换干净 |

【扩展知识】
显式等待 + 隐式等待的混用风险（Ch07）：两者都用时超时可能叠加，因为不同 driver 实现里隐式等待会影响显式等待的轮询间隔。所以业界建议：**隐式等待设小值（3-5s）做兜底，显式等待做主力**，且尽量别在同一个 driver 上同时大规模依赖两者。

【我的理解】
> （`until_not(visibility_of_any_elements_located(...))` 和 `until(invisibility_of_element_located(...))` 语义一样吗？为什么说后者更直白？）

---

## 六、添加日志

### 知识点 6：RotatingFileHandler 滚动日志

【课程原话/定义】

```python
import logging
import os
from logging.handlers import RotatingFileHandler

# 绑定句柄到 logger 对象
logger = logging.getLogger(__name__)
# 获取当前工具文件所在的路径
root_path = os.path.dirname(os.path.abspath(__file__))
# 拼接当前要输出日志的路径
log_dir_path = os.sep.join([root_path, '..', f'/logs'])
if not os.path.isdir(log_dir_path):
    os.mkdir(log_dir_path)
# 创建日志记录器，指明日志保存路径、每个日志的大小、保存日志的上限
file_log_handler = RotatingFileHandler(os.sep.join([log_dir_path, 'log.txt']),
                                       maxBytes=1024 * 1024, backupCount=10, encoding="utf-8")
# 设置日志的格式
date_string = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(filename)s]/[line: %(lineno)d]/[%(funcName)s] %(message)s ',
    date_string)
# 日志输出到控制台的句柄
stream_handler = logging.StreamHandler()
file_log_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
# 为全局的日志工具对象添加日志记录器
logger.addHandler(stream_handler)
logger.addHandler(file_log_handler)
# 设置日志输出级别
logger.setLevel(level=logging.INFO)
```

【为什么？】
这是 Ch13 行为日志的**工程化升级**。Ch13 用的是 `logging.basicConfig`（简单、全局一次性配置），本章用 `RotatingFileHandler`（生产级）：

| 对比 | `basicConfig`（Ch13） | `RotatingFileHandler`（本章） |
|------|----------------------|------------------------------|
| 输出 | 默认控制台 | 文件 + 控制台（双句柄） |
| 文件大小 | 不管理 | 超过 `maxBytes`（1MB）自动滚动 |
| 历史备份 | 无 | 保留 `backupCount`（10）个备份 |

`RotatingFileHandler` 解决的实际问题是：**日志文件会无限膨胀**。长期运行的自动化框架，`log.txt` 会长到几个 G，既难打开又占磁盘。滚动机制让它"写满 1MB 就新开一个文件，最多留 10 个旧的"。

另外注意：这里同时加了两个 handler（文件 + 控制台），所以一条日志会**同时**写进文件、打印到控制台。格式里 `[%(funcName)s]` 记录函数名、`[line: %(lineno)d]` 记录行号——排查时能精确到"哪个函数第几行打的日志"。

【必须掌握】
- `RotatingFileHandler`：按大小滚动（`maxBytes`）+ 保留备份数（`backupCount`）
- 双句柄：文件 handler + 控制台 handler
- 日志格式六要素：时间 / 级别 / 文件名 / 行号 / 函数名 / 消息
- 与 Ch13 `basicConfig` 的定位区别：basicConfig 简单够用，RotatingFileHandler 是生产级

【企业场景】
你在框架里用 `RotatingFileHandler` 统一管日志：`maxBytes=1024*1024`（1MB）、`backupCount=10`，这样磁盘上最多 11 个日志文件，永远不会把 CI 机器磁盘写爆。格式里带 `funcName` + `lineno`，CI 上任何一条 ERROR 日志都能精确定位到代码行。

【面试考察】
面试官："日志文件越来越大怎么办？"

参考回答框架：
1. 用 `RotatingFileHandler` 做滚动：`maxBytes` 控制单文件大小，`backupCount` 控制备份数
2. 超过 `maxBytes` 自动新开文件，旧文件按 `backupCount` 滚动删除
3. 配合格式化（时间/级别/文件/行号/函数名）让日志可定位
4. 双句柄：控制台实时看 + 文件留档排查

【易错点】

| 误区 | 纠正 |
|------|------|
| `os.sep.join([root_path, '..', f'/logs'])` 混用 `'/'` 和 `os.sep`（课程笔误） | Windows 下会拼出怪路径，应统一用 `os.path.join` 或纯 `os.sep` |
| 只加文件 handler，不加控制台 handler | 调试时看不到实时输出 |
| `logger.setLevel(INFO)` 但 handler 没设级别 | 级别过滤是 logger 和 handler 两层，都要配 |
| 注释"绑定绑定句柄"（课程笔误，重复词） | 忽略即可 |

【扩展知识】
日志四大组件：`Logger`（记录器，入口）、`Handler`（处理器，决定输出到哪）、`Formatter`（格式化器，决定长什么样）、`Filter`（过滤器）。本脚本用到了前三者。`RotatingFileHandler` 是 Handler 的一种，此外还有 `TimedRotatingFileHandler`（按时间滚动，如每天一个文件）。

【我的理解】
> （为什么生产环境用 `RotatingFileHandler` 而不是 `basicConfig`？"日志无限膨胀"具体会造成什么后果？）

---

## 七、添加截图

### 知识点 7：save_screenshot + Allure 附件

【课程原话/定义】

```python
def get_step_screenshot(self):
    '''截图'''
    timestamp = int(time.time())
    # 前提：在当前路径需要有一个 images 文件夹
    # 获取当前文件所在的目录路径
    root_path = os.path.dirname(os.path.abspath(__file__))
    # 拼接截图保存路径，windows 系统的同学注意这里拼接 \\
    file_path = f"{root_path}/screenshot_{timestamp}.png"
    logger.info(f"截图保存路径为 {file_path}")
    self.driver.save_screenshot(file_path)
    allure.attach.file(
        file_path, name="pic",
        attachment_type=allure.attachment_type.PNG
    )
```

【为什么？】
这是 Ch13 截图三件套的**实战封装 + Allure 集成**。两个关键点：

1. **`save_screenshot(path)`**：等价于 Ch13 的 `get_screenshot_as_file`，整页/窗口截图。文件名带 `int(time.time())` 时间戳，保证多次截图不互相覆盖。
2. **`allure.attach.file(...)`**：把截图文件作为**附件**挂到 Allure 报告里，报告里每条用例/步骤旁边就能直接看到这张截图。这是"截图"从"躺在磁盘上"到"出现在报告里"的关键一步。

对比 Ch13：Ch13 讲"失败时截图 + 存 page_source"的思路，本章是把截图**封装成 `get_step_screenshot()` 方法 + 挂进 Allure**——从"会截图"升级到"截图能被人看到"。

【必须掌握】
- `driver.save_screenshot(path)` 整页截图，文件名带时间戳
- `allure.attach.file(path, name=..., attachment_type=allure.attachment_type.PNG)` 挂附件到报告
- 截图封装成方法（`get_step_screenshot`），用例里一行调用
- 与 Ch13 的关系：Ch13 讲思路，本章讲落地 + Allure 集成

【企业场景】
你在框架里封装 `get_step_screenshot()`，关键步骤（或失败时）调用一次。CI 上用例红了，你打开 Allure 报告，点开那条用例就能看到失败那一刻的截图——不用登录服务器去翻日志目录。这就是"截图"的价值闭环：**留证 → 进报告 → 被人看到**。

【面试考察】
面试官："截图怎么集成到测试报告里？"

参考回答框架：
1. `driver.save_screenshot(path)` 存文件，文件名带时间戳/用例名
2. `allure.attach.file(path, name=..., attachment_type=allure.attachment_type.PNG)` 挂进报告
3. 封装成公共方法，失败时（或关键步骤）调用
4. 最终效果：Allure 报告里每条用例能直接看截图

【易错点】

| 误区 | 纠正 |
|------|------|
| 截图目录（images）没提前建 | 报 FileNotFoundError，先 `os.makedirs(exist_ok=True)`（Ch13 同坑） |
| 文件名不带时间戳 | 多次截图互相覆盖，只剩最后一张 |
| 截图了但没 `allure.attach` | 截图躺在磁盘，报告里看不到 |
| 注释"注意这里拼接 \\"（课程 Windows 提示） | 用 `os.path.join` 或 `/` 更安全，手动拼 `\\` 易错 |

【扩展知识】
`save_screenshot` 与 `get_screenshot_as_png`（返回字节流，不落盘）的区别：落盘版适合归档，字节流版适合直接塞 Allure（`allure.attach(driver.get_screenshot_as_png(), ...)`）。工程上更推荐字节流版，省一次磁盘 IO、避免目录管理。

【我的理解】
> （为什么截图"存了文件"还不够，还要 `allure.attach`？从"排查效率"的角度，报告里能直接看图 vs 去翻目录，差在哪？）

---

## 八、生成测试报告

### 知识点 8：Allure 三步流程

【课程原话/定义】

```bash
# 1. 安装 Allure 程序（命令行工具）
# 2. 安装 allure-pytest 插件
pip install allure-pytest

# 3. 执行测试用例，生成测试报告数据
pytest 用例文件 --alluredir=报告路径

# 4. 生成测试报告在线地址
allure serve 报告路径
```

【为什么？】
这是自动化"最后一公里"——**把测试结果变成人能看的报告**。Allure 是业界最主流的测试报告框架，流程分三步，很多人会搞混"数据"和"报告"：

1. **装东西**：Allure 命令行程序（生成报告的引擎）+ `allure-pytest`（Python 插件，让 pytest 能输出 allure 格式的数据）
2. **生成数据**：`pytest --alluredir=路径` —— 这一步生成的**不是报告**，是一堆 JSON 中间数据（测试结果、附件、步骤）
3. **渲染报告**：`allure serve 路径` —— 把中间数据渲染成网页报告，并起本地服务打开

关键概念：`--alluredir` 生成的是**中间数据**（JSON），`allure serve` 才是**渲染成报告**。很多人只跑 `--alluredir` 就以为生成报告了，结果发现只有一堆 json 文件。

【必须掌握】
- 三步：装 Allure 程序 + 装 allure-pytest → `pytest --alluredir=路径` → `allure serve 路径`
- `--alluredir` 生成的是中间数据（JSON），不是报告
- `allure serve` 才渲染成网页报告
- 报告里能看到：用例结果、步骤、日志、截图附件（配合知识点 7 的 `allure.attach`）

【企业场景】
你在 CI 流水线里加一步"生成 Allure 报告"，让每次自动化回归的结果都有一份可视化报告：哪些用例红了、失败在哪一步、附了什么截图。产品/测试负责人不用看代码，打开报告链接就知道"这轮回归健不健康"。

【面试考察】
面试官："Allure 报告怎么生成的？"

参考回答框架：
1. 装 Allure 命令行程序 + `pip install allure-pytest`
2. `pytest --alluredir=结果目录` 生成中间数据
3. `allure serve 结果目录` 渲染成网页报告
4. 关键：`--alluredir` 出的是 JSON 数据，不是报告；`serve` 才渲染
5. 报告里集成日志、截图（`allure.attach`）形成完整证据链

【易错点】

| 误区 | 纠正 |
|------|------|
| 跑完 `--alluredir` 就以为有报告了 | 那只是 JSON 中间数据，还要 `allure serve` |
| 只装 `allure-pytest`，没装 Allure 程序 | `allure serve` 命令不存在，报 command not found |
| `allure serve` 生成的是静态文件？ | `serve` 起的是临时本地服务，要生成静态报告用 `allure generate` |

【扩展知识】
`allure serve`（起临时服务预览）vs `allure generate`（生成静态 HTML，可部署到 Jenkins/Nginx）。企业 CI 里通常是 `allure generate` 出静态报告再归档，`serve` 只用于本地开发调试。Allure 报告的能力：分类展示（失败/通过/跳过）、用例详情、步骤树、附件、历史趋势、重试。

【我的理解】
> （`--alluredir` 生成的"中间数据"和 `allure serve` 渲染出的"报告"是什么关系？为什么中间数据是 JSON 而不是 HTML？）

---

## 九、脚本存在的问题 → 引出 PO 设计模式

### 知识点 9：为什么需要 PO 设计模式

【课程原话/定义】
> 目前脚本存在的问题：
> - 很多重复代码，维护困难
> - 没有办法清晰地描述业务场景
>
> 学习 PO 设计模式之后解决这些问题。

【为什么？】
这是整章最重要的"承上启下"。脚本已经能跑通了，但存在两个结构性缺陷，它们不是"写得不好"，而是"没有分层的必然结果"：

1. **重复代码**：每一处 `find_element(By.XPATH, "//label[text()='X']/..//*[@class='el-input__inner']")` 都是复制粘贴改个文本。定位器散落在用例里，页面改版要改几十处。
2. **无法描述业务场景**：读脚本看到的是"找这个元素、点那个元素"，读不出"这是在给优惠券填名称"。**操作细节掩盖了业务意图**。

PO（Page Object）设计模式的解法，一句话：**把"页面"抽象成"对象"**。

```
现在（无分层）：        测试用例 = 元素定位 + 操作 + 断言（混在一起）
PO 模式：              测试用例 = 业务步骤（填名称 → 填金额 → 确定）
                      页面对象 = 元素定位 + 操作封装（隐藏细节）
```

好处直接对应上面两个问题：定位器集中在页面类里（改一处生效），用例只写"业务语言"（可读、可维护）。

【必须掌握】
- 当前脚本两大缺陷：重复代码 + 业务场景不清晰
- PO 模式核心思想：页面抽象成对象，定位/操作封装在页面类，用例只写业务步骤
- PO 三原则：页面对象封装定位与操作 / 用例只写业务 / 定位器只放一处

【企业场景】
你在企业里接手一个 200 条用例的 UI 自动化框架，如果每条用例里都硬编码 XPath，前端改一个按钮 class，你要改 200 处。引入 PO 后，按钮定位只在"优惠券页对象"里定义一次，改一处全部生效。这就是"为什么大厂 UI 自动化一定要分层"的原因——**不分层，用例越多，维护成本越爆炸**。

【面试考察】
面试官："为什么 UI 自动化要用 PO 设计模式？"

参考回答框架：
1. 解决两个问题：重复代码（定位器散落）+ 业务场景不清晰（操作细节掩盖意图）
2. PO 把页面抽象成对象，定位 + 操作封装在页面类里
3. 用例只写业务步骤（可读、像手工用例）
4. 好处：定位器集中一处改、用例可维护、可复用
5. 一句话：不 PO 的脚本，用例一多就维护爆炸

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为"能跑通"就够了 | 不分层，用例一多重复代码 + 维护成本爆炸 |
| 把 PO 理解成"只是把代码搬到另一个文件" | PO 是"页面对象封装定位+操作、用例只写业务"的分层思想 |
| 以为"重复代码"只是"复制粘贴"的字面问题 | 深层是"定位器散落在每条用例里"，页面一改要改几十处 |

【我的理解】
> （"重复代码"和"无法描述业务场景"是两个独立的问题，还是一个问题的两面？PO 模式是分别怎么解决它们的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 产品分析 | litemall 管理后台 + 优惠券管理 + 四大复杂度 | ★★★☆☆ |
| 测试用例分析 | 添加/删除用例 + 数据依赖闭环 + 两段式断言 | ★★★★☆ |
| 前置后置 | setup_class/teardown_class 类级 + 隐式等待兜底 | ★★★★☆ |
| 初步实现 | 登录→导航→表单→下拉→断言完整链路 + 脆弱点识别 | ★★★★☆ |
| 代码优化 | 强制等待→显式等待 + EC + 自定义等待条件 | ★★★★★ |
| 添加日志 | RotatingFileHandler 滚动日志（生产级） | ★★★☆☆ |
| 添加截图 | save_screenshot + allure.attach 挂进报告 | ★★★☆☆ |
| 生成报告 | Allure 三步（数据 vs 报告） | ★★★★☆ |
| PO 引出 | 重复代码 + 业务不清晰 → 页面对象分层 | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch10-测试人论坛搜索功能自动化测试]]（上一次综合实战，本章是"登录态 + 后台 CRUD"进阶版）
- [[Ch04-自动化测试用例结构分析]]（setup_class 类级 vs setup_method 方法级的粒度权衡）
- [[Ch07-强制等待与隐式等待]]（time.sleep → 显式等待的动机与"元素在 DOM ≠ 可交互"）
- [[Ch09-自动化测试定位策略]]（动态 class、索引定位的脆弱性 + 治本方案 data-test-id）
- [[Ch13-Web自动化关键数据记录]]（日志/截图/page_source 三件套，本章是其工程化落地 + Allure 集成）
- [[Pytest/README|Pytest]]（setup_class/teardown_class、--alluredir、后续 PO + Allure 报告）
- [[Ch15-PageObject设计模式]]（PO 六大原则 + 实战分层，本章结尾两个问题的"解药"）
