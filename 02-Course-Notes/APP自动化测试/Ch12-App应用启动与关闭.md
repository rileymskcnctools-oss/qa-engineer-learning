---
tags:
  - 课程笔记
  - APP自动化测试
  - Appium
  - 应用控制
course: APP自动化测试
chapter: Ch12-App应用启动与关闭
created: 2026-09-07
status: draft
---

# Ch12 - App 应用启动与关闭

## 课程来源
- 学习日期：

---

## 一、启动应用

### 知识点 1：两种启动方式

【课程原话/定义】

启动应用有两种方式：

1. **正常启动**：创建 WebDriver 实例，与 Appium 服务器建立连接并传 Desired Capabilities。通过把 URL 和 capabilities 传给启动方法，客户端与服务器建立连接并启动会话，返回可交互的 WebDriver 实例。
2. **在脚本中启动其他应用**：在设备上激活给定应用，传入的 app_id 为指定应用的包名。

主要两个参数：url（Appium 服务器地址，如 http://localhost:4723）、capability（配置字典）。

Python 示例：

```python
# 启动应用：
appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(
    appium_server_url,
    options=UiAutomator2Options().load_capabilities(caps)
)

# 在脚本中启动其他应用：
driver.activate_app("com.xx.xx")
```

Java 示例：

```java
// 启动应用：
AndroidDriver driver = new AndroidDriver(new URL("http://127.0.0.1:4723"), uiAutomator2Options);
// 启动其他应用
driver.activateApp("com.xx.xx");
```

【为什么？】

1. `webdriver.Remote(url, options)` 是"创建会话"，会话绑定的是 capability 里指定的那个 App；一次会话通常只测一个 App。
2. `activate_app`（Python）/`activateApp`（Java）是"切换前台"，把另一个已安装的 App 拉到前台，不新建会话——适合测"App 间跳转/分享/唤起"场景。
3. 两者本质区别：Remote 建会话（新 driver），activate_app 在**同一个会话里**切换 App 上下文。

【必须掌握】

- webdriver.Remote(url, options) 启动被测 App（建会话）
- driver.activate_app("包名") 激活其他 App（同会话切前台）

【企业场景】

你在企业里，主用例用 Remote 启动被测 App；测"调起支付/唤起浏览器/分享到微信"这类跨 App 流程时，用 activate_app 切到目标 App 验证交互，再切回来。注意 activate_app 的前提是目标 App 已安装。

【面试考察】

面试官："启动一个 App 有哪些方式？它们的区别是什么？"

参考回答框架：Remote(url, caps) 建新会话启动被测 App；activate_app 在已有会话里把其他已安装 App 切到前台，不新建会话。前者是初始化，后者是上下文切换。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 activate_app 能启动未安装的 App | activate_app 只是"激活已安装应用"，目标 App 必须先装好 |
| Python 写 activateApp（驼峰） | Python 方法是 **activate_app**（下划线），Java 才是 activateApp |

【我的理解】

> （什么业务场景必须用 activate_app 而不是再 Remote 一个 driver？再 Remote 一个 driver 会带来什么副作用？）

---

## 二、关闭应用

### 知识点 2：terminate_app 与 quit

【课程原话/定义】

关闭指定 app：关闭当前操作的 App，不会关闭驱动对象。
关闭驱动对象：关闭当前所有关联的 App，并关闭驱动对象。

Python 示例：

```python
# 关闭指定 app
driver.terminate_app("com.xx.xx")
# 关闭当前所有关联的 app，并关闭驱动对象
driver.quit()
```

Java 示例：

```java
// 关闭指定 app
driver.terminateApp("包名");
// 关闭驱动对象
driver.quit();
```

【为什么？】

1. `terminate_app`（Python）/`terminateApp`（Java）结束指定 App 的**进程**，但 driver 还活着，可以继续操作别的 App 或再启动它。
2. `quit()` 结束**整个会话**：关闭所有关联 App、释放设备连接、销毁 driver。quit 之后不能再用这个 driver。
3. 区分"关 App"和"关会话"：terminate_app 关的是 App 进程，quit 关的是 Appium 会话本身。

【必须掌握】

- driver.terminate_app("包名") 关指定 App 进程（driver 仍在）
- driver.quit() 关会话 + 关 driver

【企业场景】

你在企业里，teardown 里标准写法是 `driver.quit()` 释放会话，避免设备被占、会话堆积。terminate_app 用于用例中间"主动杀掉 App 再重启验证冷启动"这种场景。忘记 quit 会导致设备上 session 不释放，连续跑多个用例报 "session already exists" 或设备被锁。

【面试考察】

面试官："terminate_app 和 quit 有什么区别？"

参考回答框架：terminate_app 结束指定 App 的进程、driver 仍可用；quit 结束整个会话、关闭所有关联 App 并销毁 driver，之后不能再用。一个关进程、一个关会话。

【易错点】

| 误区 | 纠正 |
|------|------|
| 原文 Java 注释 "terminateApp(app名称)" | 参数是**包名**（如 com.xx.xx），不是"app 名称"，原文注释笔误 |
| 以为 terminate_app 会关 driver | 它只结束 App 进程，driver 和会话还在 |
| teardown 漏写 quit | 会话不释放，设备被占、后续用例启动失败 |

【我的理解】

> （"结束 App 进程"和"结束会话"在设备上分别是什么表现？为什么 teardown 里一定是 quit 而不是 terminate_app？）

---

## 三、完整示例

### 知识点 3：启动/切换/关闭的完整流程

【课程原话/定义】

Python 完整示例：

```python
class TestApiDemo:
    def setup_class(self):
        caps = {}
        caps["platformName"] = "Android"
        caps["appium:appPackage"] = "io.appium.android.apis"
        caps["appium:appActivity"] = ".ApiDemos"
        caps["appium:noReset"] = True
        caps["appium:shouldTerminateApp"] = True
        appium_server_url = 'http://localhost:4723'
        self.driver = webdriver.Remote(appium_server_url,
                                       options=UiAutomator2Options().load_capabilities(caps))
        print('初始化driver')
        self.driver.implicitly_wait(10)

    def teardown_class(self):
        time.sleep(3)
        self.driver.activate_app("com.android.browser")
        print('打开浏览器')
        time.sleep(3)
        self.driver.terminate_app("com.android.browser")
        print('关闭浏览器')
        time.sleep(3)
        self.driver.quit()
        print('关闭driver')

    def test_control(self):
        print("执行成功")
```

Java 完整示例（关键流程）：

```java
@BeforeAll
public static void setUp() throws MalformedURLException {
    DesiredCapabilities caps = new DesiredCapabilities();
    caps.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
    caps.setCapability("appPackage", "io.appium.android.apis");
    caps.setCapability("appActivity", ".ApiDemos");
    caps.setCapability("appium:noReset", true);
    caps.setCapability("appium:shouldTerminateApp", true);
    URL remoteUrl = new URL("http://127.0.0.1:4723");
    driver = new AndroidDriver(remoteUrl, caps);
    driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
}

@AfterAll
public static void tearDown() throws InterruptedException {
    Thread.sleep(3000);
    driver.activateApp("com.android.browser");
    Thread.sleep(3000);
    driver.terminateApp("com.android.browser");
    Thread.sleep(3000);
    if (driver != null) {
        driver.quit();
    }
}
```

【为什么？】

1. setup/teardown 用 `setup_class`/`teardown_class`（类级别，只执行一次），和 Ch10 的 `setup_method`/`teardown_method`（方法级别，每个用例执行一次）不同——类级别适合"整个类共用一个 driver 会话"。
2. teardown 里 activate_app 打开浏览器 → terminate_app 关浏览器，是演示"切到别的 App 再关掉"的完整链路。
3. Java 侧 `if (driver != null)` 是防御性写法，防止 driver 没建成就 quit 抛空指针。

【必须掌握】

- 完整用例 = setup 建 driver（Remote + implicitly_wait）→ 用例操作 → teardown 关 driver（quit）
- Python setup_class/teardown_class 是类级别 fixture

【企业场景】

你在企业里，完整的自动化用例骨架就是这一节的内容：setup 初始化会话，teardown 释放会话，中间用例做业务。activate_app + terminate_app 这套"打开浏览器再关掉"的演示，对应真实场景里"App 跳转第三方（浏览器/地图/支付）后回收"的回归用例。

【面试考察】

面试官："setup_class 和 setup_method 有什么区别？什么时候用哪个？"

参考回答框架：setup_class/teardown_class 是类级别，整个类只执行一次，适合所有用例共用一个 driver；setup_method/teardown_method 是方法级别，每个用例都执行一次，适合每个用例都要独立初始化/清理的场景。

【易错点】

| 误区 | 纠正 |
|------|------|
| setup_class 和 setup_method 混用 | 类级别只跑一次（共享会话），方法级别每个用例跑一次（独立会话），按是否需要独立环境选 |
| shouldTerminateApp=true 但注释写"不重启" | shouldTerminateApp=true 是"会话结束终止 App"，与"不重启"是两回事（原文注释易误导） |
| 忘记 time.sleep 观察效果 | 示例里的 sleep 只是让人眼看清切换过程，生产脚本应少用 sleep |

【我的理解】

> （这个例子里 teardown 为什么是"打开浏览器 → 关浏览器 → quit"，而不是直接 quit？它想演示哪两个方法的区别？）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 启动方式 | Remote 建会话 / activate_app 切前台 | ★★★★★ |
| 关闭方式 | terminate_app 关进程 / quit 关会话 | ★★★★★ |
| 完整示例 | setup/teardown + 切换 + 关闭 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch11-Capability配置参数解析]]（caps 字典喂给 webdriver.Remote 启动）
- [[Ch10-自动化测试用例结构分析]]（setup/teardown 结构来源，setup_class vs setup_method 的进阶）
- [[Ch14-三种等待机制]]（implicitly_wait 属于隐式等待）
