---
tags:
  - 课程笔记
  - Web自动化测试
  - Selenium
  - 综合实战
  - litemall
  - 商品类目
  - PageObject
  - BasePage
  - POM
course: Web自动化测试
chapter: Ch18-电子商务产品实战进阶-商品类目管理与POM改造
created: 2026-08-30
status: draft
---

# Ch18 - 电子商务产品实战进阶（商品类目管理 POM 改造）

## 课程来源
- 学习日期：

---

## 一、产品与用例分析

### 知识点 1：商品类目管理 + 新增/删除两条用例流程

【课程原话/定义】

- **产品**：Litemall 商城系统
- **功能**：商品类目管理
- **被测地址**：`http://litemall.hogwarts.ceshiren.com`
- **账户**：用户名 `manage` / 密码 `manage123`

**测试用例 - 新增类目**：用户登录 → 进入商品类目菜单 → 点击添加 → 创建商品类目 → 获取操作结果 → 断言测试结果

> 📷 【截图占位】新增类目用例流程

**测试用例 - 删除类目**：用户登录 → 进入商品类目菜单 → 点击添加 → 创建商品类目 → 点击删除 → 获取操作结果 → 断言测试结果

> 📷 【截图占位】删除类目用例流程

【为什么？】
本章是 Ch14（优惠券实战）+ Ch15（PO 模式）的**进阶融合**，换了一个新功能"商品类目管理"，并升级了三个难度：

1. **双语言对照**：Python + Java 各写一遍线性脚本，最后都改造成 POM。目的不是"两种语言都要会写"，而是通过对照看透"PO 的分层思想是语言无关的"——同样的套路，Python 用 `setup_class`，Java 用 `@BeforeAll`，本质一样。
2. **BasePage 基类封装**：Ch15 只在单个页面类里藏定位器，本章进一步抽出**所有页面共用的 driver 和 selenium API**，放进一个 `BasePage` 基类，页面类继承它。这是 PO 的"第二层抽象"。
3. **新增/删除两条用例的数据依赖**：删除类目要先"造一个类目"再删（和 Ch14 优惠券的"先增后删"同构），考验数据准备与清理的编排。

新增和删除两条用例的步骤几乎一样，只差"删除"一步——这正是后面"梳理业务流程"能提炼出公共页面类的依据。

【必须掌握】
- 实战信息：产品 / 功能 / 地址 / 账号（manage / manage123）
- 两条用例的完整步骤，能看出"删除用例 = 新增用例 + 一步删除"
- 本章的三个升级点：双语言 / BasePage / 数据依赖

【企业场景】
你在企业里做 POM 改造，通常不是从零写，而是"手上已经有一份线性脚本，把它重构成 PO"——本章就是这种真实场景的完整演练。先看清"现在有什么脚本"（线性 Python/Java 版），再一步步把它拆成页面类 + 基类，最后验证改造后的用例可读性。这个"线性 → PO"的改造能力，比"从零写 PO"更贴近实际工作。

【面试考察】
面试官："这个实战里，删除类目和新增类目两条用例有什么关系？"

参考回答框架：
1. 删除用例 = 新增用例 + 一步删除（都要先造数据）
2. 这是典型的数据依赖：删除的前提是"先有一个类目"
3. 应对：造数据步骤复用（公共方法/前置），清理放断言之后
4. 这也解释了为什么能提炼出公共页面类——两条用例共享"登录 → 进菜单 → 添加"的前半段

【易错点】

| 误区 | 纠正 |
|------|------|
| 把"新增"和"删除"写成两条完全独立的脚本 | 后半段不同，但"登录/进菜单/添加"前半段是共享的，正是 PO 提炼的依据 |
| 以为"双语言"要同时精通 Python 和 Java | 重点是看懂"PO 思想语言无关"，套路一致只是语法不同 |

【我的理解】
> （删除用例为什么一定要"先创建再删除"？如果直接删一个不存在的类目，用例还成立吗？这暴露了自动化测试里"造数据"的什么本质？）

---

## 二、传统线性脚本（Python 版）

### 知识点 2：Python 线性脚本的四个关键点

【课程原话/定义】

```python
class TestLitemall:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.driver.get("http://litemall.hogwarts.ceshiren.com/")
        # 问题：输入框内有默认值，此时 send_keys 不会清空只会追加
        # 解决方案：在输入信息之前，先对输入框完成清空
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys("manage")
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys("manage123")
        self.driver.find_element(By.CSS_SELECTOR, ".el-button--primary").click()

    def teardown_class(self):
        self.driver.quit()

    def test_add_type(self):
        # 进菜单 → 点添加 → 输入类目名
        self.driver.find_element(By.XPATH, "//*[text()='添加']").click()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input__inner").send_keys("新增商品测试")
        # 自定义显式等待：重试点击
        WebDriverWait(self.driver, 10).until(
            click_exception(By.CSS_SELECTOR, ".dialog-footer .el-button--primary"))
        res = self.driver.find_elements(By.XPATH, "//*[text()='新增商品测试']")
        self.get_screen()
        # 数据的清理一定要放在断言操作之后，否则会影响断言结果
        self.driver.find_element(By.XPATH, "//*[text()='新增商品测试']/../..//*[text()='删除']").click()
        assert res != []

    def test_delete_type(self):
        # 造数据：添加"删除商品测试" ...
        WebDriverWait(self.driver, 10).until_not(
            expected_conditions.visibility_of_any_elements_located(
                (By.XPATH, "//*[text()='删除商品测试']")))
        # 问题：代码执行速度过快，元素还未消失就捕获了
        # 解决：确认该元素不存在后，再捕获
        res = self.driver.find_elements(By.XPATH, "//*[text()='删除商品测试']")
        assert res == []
```

【为什么？】
这段线性脚本里有四个"看似能跑、实则暗藏坑"的关键点，都是实战必踩的：

1. **登录输入框要先 `clear()` 再 `send_keys()`**：`send_keys` 是"追加"不是"覆盖"。如果输入框有默认值（如预填的账号），直接 send_keys 会拼成 `默认值manage`。所以输入前先 clear。这个坑在后台表单里极常见。

2. **`click_exception` 自定义显式等待**：弹窗"确定"按钮有时第一次点不到（遮罩/动画/加载中），直接 `click()` 会抛 `ElementClickInterceptedException`。封装一个"重试点击"的自定义等待条件，在 `WebDriverWait(...).until(...)` 里最多重试 5 次——这是 Ch14 讲过的 `click_exception` 在本章的复用。

3. **数据清理放在断言之后**：`test_add_type` 里先 `find_elements` 拿到 `res`，再点删除清理，最后才 `assert res != []`。顺序不能反——如果先删再断言，删完元素就找不到了，断言会错误地失败。**"先取证、后清理"**是数据清理的铁律。

4. **删除后要"等元素消失"再断言**：`test_delete_type` 点删除后，代码可能跑得比页面动画快，元素还没消失就 `find_elements`，会错误地抓到"还没删干净"的元素。所以用 `until_not(visibility_of_any_elements_located(...))` 先确认元素**不存在**，再捕获断言。

【必须掌握】
- `send_keys` 是追加不是覆盖 → 输入前先 `clear()`
- 自定义显式等待 `click_exception`（重试点击，Ch14 复用）
- 数据清理放断言之后（先取证后清理）
- 删除后 `until_not` 等元素消失再断言（防"跑太快"）

【企业场景】
你在 review 一个新人写的脚本，发现登录那行 `send_keys("manage")` 但登录老失败——一查是输入框有默认值，`manage` 被追加成了 `默认值manage`。你会让他补 `clear()`。同样，他写的删除用例偶发失败，是因为删除后没等元素消失就断言。这四个点就是"脚本能跑"和"脚本稳定"之间的差距。

【面试考察】
面试官："`send_keys` 输入前为什么要 `clear()`？"

参考回答框架：
1. `send_keys` 是追加到输入框，不是覆盖
2. 输入框有默认值时会拼成"默认值+新值"
3. 所以输入前先 `clear()` 清空，再 `send_keys`
4. 同类坑：数据清理要在断言后做、删除要等元素消失再断言

【易错点】

| 误区 | 纠正 |
|------|------|
| 直接 send_keys，不管输入框默认值 | 先 clear() 再 send_keys，否则是追加 |
| 先删数据再断言 | 数据清理放断言后，"先取证后清理" |
| 删除后立即 find_elements 断言 | 用 until_not 等元素消失，防代码快于页面动画 |

【扩展知识】
`click_exception` 的自定义等待条件是 Ch14 的复用，完整结构：外层函数接收 `(by, element, max_attempts)` 返回 `_inner(driver)`；`_inner` 里 while 循环重试点击，成功 `return True`，超次数抛异常。注意课程里 `return _inner()`（带括号）是错误写法——应该 `return _inner`（返回函数本身，让 WebDriverWait 去调用它）。

【我的理解】
> （"数据清理放断言后"和"删除后等元素消失"这两个坑，本质是不是同一个问题——"动作和观察之间的时序"？用一个统一的说法解释它们。）

---

## 三、传统线性脚本（Java 版）

### 知识点 3：Java 线性脚本（JUnit5 + FluentWait）+ 双版本对比

【课程原话/定义】

```java
public class LitemallPlusTest {
    private static WebDriver driver;
    private static FluentWait<WebDriver> fluentWait;

    @BeforeAll
    static void setUpClass() {
        driver = new ChromeDriver();
        fluentWait = new FluentWait<WebDriver>(driver).
                withTimeout(Duration.ofSeconds(10)).
                pollingEvery(Duration.ofMillis(500)).
                ignoring(ElementClickInterceptedException.class);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(3));
        // 登录是所有用例执行前的准备，放 @BeforeAll
        driver.get("http://litemall.hogwarts.ceshiren.com/#/login");
        driver.findElement(By.name("username")).clear();
        driver.findElement(By.name("username")).sendKeys("manage");
        // ... 密码 + 点登录 + 进商品类目菜单
    }

    @AfterAll
    static void tearDownClass() { driver.quit(); }

    @Test
    void addProductType() {
        driver.findElement(By.cssSelector(".el-icon-edit")).click();
        fluentWait.until(driver1 -> {
            driver1.findElement(By.cssSelector(".el-dialog__footer .el-button--primary")).click();
            return driver.findElement(By.cssSelector(".el-notification__title"));
        });
        List<WebElement> eles = driver.findElements(By.xpath("//*[text()='测试添加商品']"));
        driver.findElement(By.xpath("//*[text()='测试添加商品']/../..//*[text()='删除']")).click();
        assertEquals(1, eles.size());   // 注意：JUnit 是 (期望, 实际)
    }
}
```

【为什么？】
Java 版和 Python 版是**同一个业务、同一套逻辑**，只是语法和框架不同。对照着看能加深两个理解：

1. **PO 思想语言无关**：Python 的 `setup_class` ↔ Java 的 `@BeforeAll`（都是"类级前置，整个类跑一次"）；`teardown_class` ↔ `@AfterAll`；`test_` 前缀 ↔ `@Test`；`assert x != []` ↔ `assertEquals(1, eles.size())`。这是 Ch17 知识点4 生命周期钩子对照的**落地验证**。

2. **FluentWait 是 WebDriverWait 的"增强版"**：Python 版用 `WebDriverWait(...).until(click_exception)` 重试点击；Java 版直接用 `FluentWait`，可以配置：
   - `withTimeout`（最长等待）
   - `pollingEvery`（轮询间隔 500ms，默认 WebDriverWait 是 500ms 但 FluentWait 可自定义）
   - `ignoring`（忽略哪些异常，如 `ElementClickInterceptedException`——点不到就重试，不中断）
   
   Java 版里 `fluentWait.until(driver1 -> {...})` 传一个 lambda，在 lambda 里点"确定"并返回"通知标题元素"作为成功标志，等价于 Python 的 `click_exception` 重试逻辑。

另外 Java 版有几个语言特有差异：登录走 `#/login` 路由、`assertEquals(期望, 实际)` 参数顺序和 Python `assert 实际 == 期望` 相反、`@BeforeAll/@AfterAll` 方法必须是 `static`。

【必须掌握】
- Python/Java 钩子对照的落地：setup_class↔@BeforeAll、teardown_class↔@AfterAll、test_↔@Test
- FluentWait 三配置：withTimeout / pollingEvery / ignoring
- Java `assertEquals(期望, 实际)` 参数顺序（和 Python 相反）
- 登录放 @BeforeAll（所有用例的前置准备）

【企业场景】
你所在团队 UI 自动化用的是 Java（很多后端团队顺带用 Java 写 UI 自动化），你从 Python 转过去时，最容易踩的坑就是 `assertEquals` 的参数顺序——写反了报错信息会误导排查。看懂"Python 和 Java 是同一套 PO 思想、不同语法"，切换语言就只是换皮，不是重学。

【面试考察】
面试官："FluentWait 和 WebDriverWait 有什么区别？"

参考回答框架：
1. 都是显式等待，FluentWait 是 WebDriverWait 的增强版（WebDriverWait 内部就是 FluentWait 的封装）
2. FluentWait 可配置：超时时间、轮询间隔（pollingEvery）、忽略的异常（ignoring）
3. 典型用法：ignoring(ElementClickInterceptedException) + 重试点击，处理"点不到"的闪烁
4. 场景：需要"忽略特定异常继续等"时用 FluentWait，普通条件等待用 WebDriverWait 即可

【易错点】

| 误区 | 纠正 |
|------|------|
| Java `assertEquals(实际, 期望)` | JUnit 是 `assertEquals(期望, 实际)`，和 Python 的 `assert 实际 == 期望` 相反 |
| @BeforeAll 方法没加 static | JUnit5 的 @BeforeAll/@AfterAll 方法必须是 static |
| 登录写进某一条用例里 | 登录是所有用例的前置准备，放 @BeforeAll / setup_class |

【我的理解】
> （FluentWait 的 `ignoring(ElementClickInterceptedException)` 和 Python 的 `click_exception` 重试，是不是在解决同一个问题？"点不到就重试"的本质是对付什么？）

---

## 四、PO 模式改造

### 知识点 4：从线性脚本到 POM 的四步改造法

【课程原话/定义】

> 📷 【截图占位】PO 模式改造示意

**第一步：梳理业务操作流程**（按页面切分）

> 📷 【截图占位】梳理业务操作流程

```python
"""登录页面：用户登录"""        # 访问登录页 → 输用户名 → 输密码 → 点登录 → 首页
"""系统首页：进入商品类目"""    # 点"商场管理" → 点"商品类目" → 类目列表页
"""类目列表页面：点击添加"""    # 点"添加" → 创建类目页面
"""创建类目页面：创建类目"""    # 输"类目名称" → 点"确定" → 类目列表页
"""类目列表页面：获取操作结果""" # 获取冒泡消息文本 → 返回消息文本
```

**第二步：梳理前置和后置**

```python
class TestLitemall:
    def setup_class(self):   # 初始化开始页面
    def teardown_class(self): # 退出浏览器
```

```java
@BeforeAll  public static void setUpClass(){ /* 初始化开始页面 */ }
@AfterAll   public static void tearDownClass(){ /* 退出浏览器 */ }
```

**第三步：构造 PO 模型**（创建页面类 + 定义页面方法）

> 📷 【截图占位】构造 PO 模型

**第四步：编写测试用例**（链式调用）

```python
def test_add_type(self):
    res = self.home.go_to_category().click_add().create_category().get_res()
```

```java
@Test
void addType() {
    String res = liteMall.goToMainPage().goToCategoryPage()
                         .createCategory("添加商品").get_res();
}
```

【为什么？】
PO 改造不是"凭感觉把代码搬进类里"，而是有一套可复用的四步法：

1. **梳理业务操作流程（按页面切分）**：把一个完整业务流程（登录 → 进菜单 → 添加 → 创建 → 取结果）按"页面"切成 5 段，每一段对应一个页面类、每一步对应一个方法。这是 PO 建模的**输入**——先有清晰的流程，才能决定"建几个类、每个类几个方法"。

2. **梳理前后置**：确认哪些是"类级一次性"（初始化开始页面、退出浏览器），哪些是"方法级每次"（复位状态）——承接 Ch17 的粒度权衡。

3. **构造 PO 模型**：每个页面一个类，页面元素定位器私有属性 + 业务方法。登录页 → `LoginPage`，首页 → `HomePage`，类目列表 → `CategoryPage`……

4. **编写用例（链式调用）**：用例层一行链式调用串起整个流程。`self.home.go_to_category().click_add().create_category().get_res()` 之所以能链起来，靠的是**原则 4——每个方法返回下一个 PageObject**（`go_to_category()` 返回类目列表页，`click_add()` 返回创建页……），最后 `get_res()` 返回断言用的文本。

这一步的本质，就是把 Ch15 的六大原则**应用到真实后台流程**上，尤其原则 3（方法=业务动作）和原则 4（返回 PageObject 支持链式）。

【必须掌握】
- 四步改造法：梳理流程（按页面切）→ 梳理前后置 → 构造页面类 → 链式调用
- 流程切分粒度 = 页面粒度，一个页面一个类
- 链式调用靠"方法返回下一个 PageObject"（原则 4）

【企业场景】
你拿到一份 200 行的 litemall 线性脚本要改造成 PO，不会直接开写，而是先在纸上/注释里把业务流程按页面切成几段（登录页、首页、类目列表页、创建页），确定要建哪几个类、每个类的公共方法叫什么。切完这张"流程 → 类 → 方法"的映射表，写代码就是照表填空。这个"先梳理后动手"的步骤，是 PO 改造不返工的关键。

【面试考察】
面试官："给你一份线性脚本，你怎么把它改造成 PO？"

参考回答框架：
1. 第一步：梳理业务流程，按页面切分（登录页/首页/列表页/创建页…）
2. 第二步：梳理前后置（类级初始化 vs 方法级复位）
3. 第三步：构造页面类（定位器私有 + 业务方法），可抽 BasePage 基类
4. 第四步：用例层链式调用（方法返回 PageObject）
5. 核心：先切流程再写代码，不是把代码搬进类里

【易错点】

| 误区 | 纠正 |
|------|------|
| 直接把线性代码搬进一个类里 | 要先按页面切分，确定"几个类、几个方法"，再动手 |
| 链式调用为什么能连起来搞不清 | 靠原则 4：方法返回下一个 PageObject |
| 流程切分按"步骤"不按"页面" | 切分粒度是页面，一个页面一个类 |

【我的理解】
> （"梳理业务操作流程"这一步，为什么切分粒度是"页面"而不是"步骤"？如果把每一步都建成一个类，会有什么问题？）

---

## 五、BasePage 封装

### 知识点 5：BasePage 基类——PO 的第二层抽象

【课程原话/定义】

```python
class BasePage:
    _BASE_URL = ""

    def __init__(self, base_driver=None):
        if base_driver:
            self.driver = base_driver          # 有传入 driver 就用传入的
        else:
            self.driver = webdriver.Chrome()    # 否则自己 new 一个
            self.driver.implicitly_wait(5)
            self.driver.maximize_window()
        if not self.driver.current_url.startswith("http"):
            self.driver.get(self._BASE_URL)

    def do_find(self, by, locator=None):
        """获取单个元素（两种传参：do_find(by, loc) 或 do_find((by, loc))）"""
        if locator:
            return self.driver.find_element(by, locator)
        else:
            return self.driver.find_element(*by)

    def do_finds(self, by, locator=None): ...
    def do_send_keys(self, value, by, locator=None):
        ele = self.do_find(by, locator)
        ele.clear()
        ele.send_keys(value)
    def do_quit(self): self.driver.quit()
    def wait_element_until_visible(self, locator: tuple):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(locator))
```

```java
public class BasePage {
    public WebDriver driver;
    public BasePage() {}
    public BasePage(WebDriver baseDriver) { driver = baseDriver; }
    public BasePage(String url) { baseURL = url; driver = new ChromeDriver(); ... }
    public WebDriverWait waitFor() { return new WebDriverWait(driver, Duration.ofSeconds(10)); }
    public FluentWait<WebDriver> fluentWaitFor() { ... }
    public WebElement find(By by) { return driver.findElement(by); }
    public List<WebElement> finds(By by) { return driver.findElements(by); }
    public void quitDriver() { driver.quit(); }
}
```

【为什么？】
Ch15 的页面类各自 `webdriver.Chrome()`、各自 `find_element(...).click()`，会导致**每个页面类重复写同样的 driver 创建和 selenium 调用**——这就是"样板代码"在页面类层的再次出现。BasePage 是**第二层抽象**，把"所有页面共用的东西"抽到基类：

1. **封装 driver**：`__init__(base_driver=None)` 是精髓——如果外部传入了 driver（`LoginPage(driver)`），就复用同一个；没传就自己 new 一个。这样**多个页面对象共享同一个浏览器实例**（链式调用时从首页跳到列表页，还是同一个 driver），而不是每个页面类开一个浏览器。这是链式调用能工作的底层前提。

2. **封装 selenium API**：`do_find` / `do_send_keys` / `wait_element_until_visible` 等。好处是统一了操作方式——比如 `do_send_keys` 内部先 `clear()` 再 `send_keys()`，把知识点 2 那个"先 clear"的坑**一次性在基类里解决**，所有页面类自动继承这个正确行为。

3. **统一等待、截图、日志**：`wait_element_until_visible`、`saveScreen`（Java）也放基类，页面类调用即可。

于是页面类变薄了：页面类只关心"本页面的定位器和业务方法"，共性的 driver/API/等待都下沉到 BasePage。这就是"**基类管共性，页面类管个性**"的分层。

【必须掌握】
- BasePage 封装两件事：driver（创建/复用）+ selenium API（find/send_keys/wait）
- `base_driver` 参数让多个页面类共享同一个 driver（链式调用的前提）
- 页面类继承 BasePage，只写本页面的定位器 + 业务方法
- `do_find` 两种传参：`(by, locator)` 分开传，或 `(by, locator)` 元组传

【企业场景】
你在搭框架时，先把 `BasePage` 写好：driver 复用逻辑、`do_find`/`do_send_keys`/`wait_element_until_visible` 这些每个页面都要用的方法。之后新人写 `LoginPage` 只要继承 `BasePage`、声明自己的定位器、写 `login()` 方法即可，不用再碰 driver 创建和等待的细节。`do_send_keys` 里内置的 `clear()` 也顺带统一了"输入前清空"的规范，不会再有新人踩"追加"的坑。

【面试考察】
面试官："PO 里为什么要抽一个 BasePage 基类？"

参考回答框架：
1. 解决页面类之间的样板代码重复（driver 创建、find/click 每次重写）
2. 封装两类：driver（创建 + base_driver 复用）+ selenium API（find/send_keys/wait）
3. base_driver 参数让多个页面共享同一个浏览器，链式调用才能串起来
4. 统一规范：如 do_send_keys 内置 clear()，把"输入前清空"一次固化
5. 分层：基类管共性，页面类管个性（本页定位器 + 业务方法）

【易错点】

| 误区 | 纠正 |
|------|------|
| 每个页面类都 new 一个 driver | 用 base_driver 传入复用，否则链式调用会开多个浏览器 |
| 页面类里重复写 find_element(...).click() | 下沉到 BasePage 的 do_find 等，页面类只调基类方法 |
| `do_find(*by)` 忘了解包 | `do_find((By.NAME, "x"))` 时元组要 `*` 解包，基类内部已处理 |

【扩展知识】
`do_find(self, by, locator=None)` 的 `if locator: ... else: find_element(*by)` 是"两种调用方式兼容"的写法：调用方既可以 `do_find(By.NAME, "username")`（两个参数），也可以 `do_find((By.NAME, "username"))`（一个元组）。后者更适合配合 PO 里"定位器声明成元组私有属性"的习惯（见 Ch15 知识点 6）。

【我的理解】
> （`base_driver` 这个参数为什么是链式调用的"底层前提"？如果没有它，`home.go_to_category()` 返回的列表页对象会怎样？和"共享同一个浏览器会话"有什么关系？）

---

## 六、脚本优化五件套

### 知识点 6：测试断言 / 数据清理 / 参数化 / 日志 / 报告

【课程原话/定义】

脚本优化五个方向：

1. **测试断言**：用断言验证"操作结果"，而不是只打印
2. **数据清理**：清理放在断言之后（先取证后清理，承接知识点 2）
3. **参数化**：同一套步骤用多组数据跑（`@pytest.mark.parametrize`）
4. **添加日志**：关键步骤打日志，配合报告定位问题
5. **测试报告**：截图 + 日志挂进 Allure

【为什么？】
改造完 PO 只是"结构对了"，但"用例质量"还要靠这五件套补齐——它们分别解决不同类型的问题：

1. **断言**：没有断言 = 用例永远"绿" = 零覆盖。断言是自动化的"眼睛"，`assert res != []`、`assertEquals(1, eles.size())` 都是把"操作结果"变成"可判定"。
2. **数据清理**：脏数据不清理会污染后续用例和环境。位置有讲究——**放断言之后**，因为清理动作（删元素）会改变"被断言的现场"。
3. **参数化**：`test_add_type("新增商品A")` 和 `test_add_type("新增商品B")` 是复制粘贴，用 `parametrize` 变成一条用例 + 多组数据（承接 Ch17 知识点2 的"参数化测试"要素）。
4. **日志**：`logger.info(f"断言获取到的实际结果为{res}")` 记录"实际拿到了什么"，失败时不用重新跑就能看到现场。
5. **报告**：`get_screen()` 截图 + `allure.attach` 挂进 Allure，失败现场直接进报告（承接 Ch13/Ch16）。

这五件套和 Ch17 的"可维护性 + 稳定性两把尺子"正好对应：断言/数据清理/日志/报告 → 稳定性（跑得稳、失败可查）；参数化 → 可维护性（少复制粘贴）。

【必须掌握】
- 五件套各自解决什么问题
- 数据清理放断言后（承接知识点 2）
- 参数化把"复制粘贴用例"变"一条用例 + 多组数据"
- 截图 + 日志挂 Allure（承接 Ch13/Ch16）

【企业场景】
你交付一个 POM 改造后的用例给团队，leader 追问三件事："有断言吗？脏数据清了吗？失败有截图和日志吗？"——这三问就是五件套里的核心。缺了断言，改造得再漂亮也是空转；缺了截图日志，CI 上红了只能重跑复现。五件套是"能交付"的最低门槛，不是加分项。

【面试考察】
面试官："PO 改造完之后，用例还要做哪些优化？"

参考回答框架：
1. 五件套：断言 / 数据清理 / 参数化 / 日志 / 报告
2. 断言：没有断言 = 零覆盖
3. 数据清理放断言后，先取证后清理
4. 参数化：复制粘贴用例变一条 + 多组数据
5. 日志 + 截图挂 Allure，失败可查现场（Ch13/Ch16）

【易错点】

| 误区 | 纠正 |
|------|------|
| 改造完 PO 就认为"完事了" | 还要补五件套，缺断言/清理/日志等于没交付 |
| 数据清理放断言前 | 清理会改变现场导致断言误判，放断言后 |
| 参数化 = 简单加个循环 | 用 pytest 的 parametrize，让每组数据独立报告、独立失败 |

【我的理解】
> （五件套里，"断言"和"日志/报告"都是"让失败可被发现"，但它们的作用对象一样吗？断言管"判对错"，日志报告管"失败后看现场"——把这两类分开想。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 产品与用例 | 商品类目管理 + 新增/删除数据依赖 | ★★★☆☆ |
| Python 线性脚本 | clear 坑 / click_exception / 先取证后清理 / until_not | ★★★★★ |
| Java 线性脚本 | @BeforeAll + FluentWait + assertEquals 顺序 | ★★★★☆ |
| PO 四步改造 | 切流程 → 前后置 → 页面类 → 链式调用 | ★★★★★ |
| BasePage | driver 复用 + selenium API 下沉 | ★★★★★ |
| 脚本优化五件套 | 断言/清理/参数化/日志/报告 | ★★★★☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch14-电子商务产品实战-litemall优惠券管理]]（同款实战，本章是"优惠券 → 商品类目"的进阶复刻）
- [[Ch15-PageObject设计模式]]（六大原则是本章 PO 改造的理论基础，尤其原则 3/4）
- [[Ch17-测试用例流程设计]]（生命周期钩子对照 + 粒度权衡，在本章 @BeforeAll/setup_class 落地）
- [[Ch13-Web自动化关键数据记录]]（截图/日志/报告五件套的失败留证来源）
- [[Ch16-异常自动截图]]（get_screen + allure.attach 的承接）
- [[Python/README|Python]]（面向对象继承，BasePage 基类的语言基础）
