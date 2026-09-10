---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 异常处理
  - 弹窗
course: APP自动化测试
chapter: Ch25-app弹窗异常处理
created: 2026-09-10
status: draft
---

# Ch25 - app 弹窗异常处理

## 课程来源
- 学习日期：

> 本章是工程化的第二块地基：**容错**。真实 App 会在运行时不定时弹广告/升级/新消息提示框，这些弹窗不是 BUG、也无法预知何时出现。用"黑名单 + 装饰器"把弹窗处理从业务代码里抽离，是框架稳定性的关键。

---

## 一、弹窗异常处理是什么

### 知识点 1：不定时弹窗的容错

【课程原话/定义】

弹窗异常处理：处理 App 中可能出现的各种弹窗、对话框、提示框等 UI 元素。可能是警告、确认、输入框，可能是正常行为，也可能是错误/异常指示。

使用场景：

- 运行过程中**不定时**弹框：广告弹窗、升级提示框、新消息提示框等。
- 弹框**不是 BUG**（UI 界面提示、警告的作用）。

【为什么？】

1. 弹窗是"不确定的干扰项"：不知道何时弹、弹什么，但它会挡在你正要操作的元素前面，导致 find_element 找到却被遮挡、或干脆找不到。
2. 传统做法是"每个操作前都 try 一下弹窗"，代码里到处散落 if-else，难以维护；黑名单把"处理弹窗"收敛到一个地方。
3. 关键认知：弹窗不是被测功能的 BUG，是 App 的正常行为——所以处理它的目的是"绕过它继续跑"，不是"报错"。

【必须掌握】

- 弹窗异常处理的场景：不定时弹框（广告/升级/新消息）
- 核心思路：把弹窗处理从业务代码抽离，统一容错

【企业场景】

你在企业里，雪球打开常弹"升级提示""新人礼包""消息提醒"，这些弹窗不处理，用例点击搜索框会失败。黑名单机制让"找到弹窗就点掉、再重试目标元素"，用例面对随机弹窗也能稳定跑完。

【面试考察】

面试官："App 自动化里遇到不定时弹窗，你怎么处理？"

参考回答框架：用黑名单机制——把常见弹窗的定位方式（如"确定""取消""关闭"）列成黑名单，二次封装 find 方法，找不到目标元素时先遍历黑名单点掉弹窗、再重试目标元素。这样把弹窗处理收敛到基类，业务代码不用管。

【易错点】

| 误区 | 纠正 |
|------|------|
| 弹窗出现就报错 | 弹窗不是 BUG，应"点掉它继续跑"，不是 fail |
| 每个操作前散落 if 处理弹窗 | 用黑名单统一处理，收敛到基类/装饰器 |

【我的理解】

> （为什么说"弹窗不是 BUG"？如果把它当 BUG 处理，用例会有什么问题？）

---

## 二、黑名单处理

### 知识点 2：二次封装 find 方法 + try/except

【课程原话/定义】

黑名单 + 二次封装查找元素方法：在原 find_element 基础上，用 try/except 捕捉异常，在异常处理逻辑里处理弹窗元素。

```python
black_list = [
    (AppiumBy.XPATH, "//*[@text='确定']"),
    (AppiumBy.XPATH, "//*[@text='取消']")
]

class BasePage:
    def __init__(self, driver: WebDriver=None):
        self.driver = driver

    def find(self, by, locator):
        try:
            return self.driver.find_element(by, locator)
        except Exception as e:
            for black in black_list:
                eles = self.driver.find_elements(*black)
                if len(eles) > 0:
                    eles[0].click()
                    return self.find(by, locator)
            raise e
```

【为什么？】

1. 核心逻辑：找目标元素失败 → 猜是弹窗挡道 → 遍历黑名单，看有没有弹窗 → 有就点掉、递归重试；没有才抛异常。
2. `find_elements`（复数）判空是"判断弹窗在不在"的标准姿势——找不到返回空列表，不抛异常（呼应 Ch13）。
3. 递归 `return self.find(by, locator)` 处理"点掉一个弹窗又弹一个"的连环弹窗；全部点完还找不到才 raise。

【必须掌握】

- 黑名单 = 弹窗定位方式的列表
- 二次封装 find：失败 → 遍历黑名单点掉 → 递归重试 → 还找不到才抛
- find_elements 判空判断弹窗是否存在

【企业场景】

你在企业里，黑名单里放"确定/取消/关闭/知道了/跳过"这类通用弹窗按钮，一次配置、全局生效。遇到新弹窗类型，往 black_list 加一行就行，业务代码零改动。

【面试考察】

面试官："黑名单处理弹窗的核心逻辑是什么？"

参考回答框架：二次封装 find 方法，find_element 抛异常时遍历黑名单（用 find_elements 判空），发现弹窗就点击关闭、再递归重试查找目标元素，直到找到或黑名单遍历完仍找不到才抛异常。

【易错点】

| 误区 | 纠正 |
|------|------|
| 源码 `return find(by, locator)` 缺 self | 应为 `return self.find(by, locator)`，否则 NameError（find 未定义） |
| 用 find_element 判断弹窗在不在 | find_element 找不到会抛异常，判断"在不在"要用 find_elements 判空 |
| 忘了递归重试 | 点掉弹窗后必须重新 find 目标元素，否则拿不到目标 |

【我的理解】

> （为什么黑名单里的弹窗要用 find_elements 而不是 find_element？如果点掉一个弹窗后又弹出一个，递归重试怎么保证最终能结束？）

---

## 三、装饰器处理异常

### 知识点 3：black_wrapper 装饰器

【课程原话/定义】

装饰器优势：增强原函数功能、不改变原函数逻辑、代码更简洁易维护。

```python
def black_wrapper(fun):
    def run(*args, **kwargs):
        basepage = args[0]  # 相当于 self
        try:
            logger.info(f"开始查找元素：{args[2]}")
            return fun(*args, **kwargs)
        except Exception as e:
            logger.warning("未找到元素，处理异常")
            image_path = basepage.screenshot()          # 截图留证
            pagesource_path = basepage.save_page_source()  # 源码留证
            for b in black_list:
                basepage.set_implicitly_wait()           # 降到 1s 快速探测
                eles = basepage.driver.find_elements(*b)
                if len(eles) > 0:
                    eles[0].click()
                    basepage.set_implicitly_wait(15)      # 恢复隐式等待
                    return fun(*args, **kwargs)
            logger.error(f"遍历黑名单，仍未找到元素，异常信息为 ====> {e}")
            raise e
    return run

class BasePage:
    @black_wrapper
    def find_ele(self, by, value):
        ele = self.driver.find_element(by, value)
        return ele
```

【为什么？】

1. 装饰器版和黑名单版（知识点 2）逻辑相同，但用 `@black_wrapper` 装饰 find 方法，把"异常处理"从"每个方法里 try"变成"一处定义、处处复用"，业务代码更干净。
2. 装饰器版还叠加了**留证**（截图 + page_source）和**隐式等待调优**（探测黑名单时降到 1s 快速试、找到弹窗后恢复 15s）——比知识点 2 更工程化。
3. `args[0]` 就是被装饰方法的 self（BasePage 实例），`args[2]` 是 value——装饰器通过 *args 拿到方法参数。

【必须掌握】

- black_wrapper 装饰器结构：try → 失败留证 → 遍历黑名单 → 点掉重试 → 还失败 raise
- 探测时降隐式等待、恢复时升回
- 装饰器"增强不改逻辑"的优势

【企业场景】

你在企业里，这套装饰器就是 PO 框架的 find 基座：所有页面类的 find_ele/find_eles 都挂 @black_wrapper，弹窗处理和失败留证自动生效，页面类只管写业务定位，不用重复写 try/except。这是"框架层能力下沉到基类"的典型体现。

【面试考察】

面试官："装饰器处理异常和直接 try/except 有什么区别？"

参考回答框架：装饰器把异常处理抽成公共逻辑，一处定义、装饰所有 find 方法，业务代码不写重复 try/except；同时统一叠加截图、page_source 留证和隐式等待调优，更简洁、易维护、不改变原方法逻辑。

【易错点】

| 误区 | 纠正 |
|------|------|
| 装饰器里 args[0] 是谁 | args[0] 是被装饰方法的 self（BasePage 实例），args[1]/args[2] 是 by/value |
| 探测黑名单不降隐式等待 | 降到 1s 快速试弹窗、找到后恢复 15s，否则每个黑名单项都等满 15s 会拖慢 |
| 找到弹窗后忘了恢复隐式等待 | 恢复 set_implicitly_wait(15)，否则后续查找都只有 1s 超时 |

【我的理解】

> （装饰器版相比知识点 2 的普通封装，多了哪两件"工程化"的事（留证 + 等待调优）？为什么"降到 1s 探测、恢复 15s"是必要的？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 弹窗异常场景 | 不定时弹框（广告/升级/新消息） | ★★★★☆ |
| 黑名单处理 | 二次封装 find + try/except + 递归重试 | ★★★★★ |
| 装饰器处理 | black_wrapper + 留证 + 等待调优 | ★★★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch01-闭包与装饰器]]（装饰器原理，本章是其工程化应用）
- [[Ch13-常见控件定位方法]]（find_element / find_elements 判空）
- [[Ch14-三种等待机制]]（implicitly_wait 的全局作用）
- [[Ch24-自动化关键数据记录]]（装饰器里的截图 + page_source 留证）
- [[Ch27-基于PO模式的测试框架优化实战]]（黑名单 + 装饰器在 PO 框架里落地）
