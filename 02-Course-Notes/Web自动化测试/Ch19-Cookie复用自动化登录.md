---
tags:
  - 课程笔记
  - Web自动化测试
  - Selenium
  - Cookie
  - 登录态
  - 企业微信
course: Web自动化测试
chapter: Ch19-Cookie复用自动化登录
created: 2026-08-31
status: draft
---

# Ch19 - Cookie 复用自动化登录

## 课程来源
- 学习日期：

---

## 一、为什么要用 Cookie 自动化登录

### 知识点 1：Cookie 复用的价值与适用场景

【课程原话/定义】

- **为什么用 Cookie 自动化登录**：登录（尤其扫码登录、验证码）是 UI 自动化最大的"人工卡点"。如果每个用例都重新走一遍登录，又慢又容易失败；把一次登录成功后的 Cookie 保存下来复用，之后就能直接跳过登录步骤。
- 流程示意：

> 📷 【截图占位】Cookie 复用流程图（课程源标注 uml diagram）

【为什么？】

1. **HTTP 是无状态的**：服务端不记得"上一次请求是你"，它靠浏览器每次请求自动携带的 Cookie 来识别"你是谁、是否已登录"。所以"登录"本质是服务端发给你一组凭证（Cookie），之后你每次带凭证来就不用再登录——这就是 Cookie 能"复用"的底层原因。
2. **扫码/验证码是自动化天敌**：它们设计出来就是为了"挡住机器人"，纯自动化脚本没法点验证码、没法扫二维码。唯一现实的做法是：人工登录一次 → 把登录态（Cookie）存下来 → 脚本以后直接"穿上"这套凭证。
3. **稳定性 + 速度**：登录是每个用例的前置，跳过它既省时间（少了扫码等待的 20 秒），也少了一个易失败环节。

【必须掌握】

- Cookie 是服务端识别登录态的凭证，浏览器每次请求自动携带
- 复用 Cookie = 复用登录凭证，跳过重复登录
- 适用场景：登录稳定、可先人工登录一次拿 Cookie
- 不适用场景：Cookie 有效期极短、服务端强绑定 IP/设备（换环境就失效）

【企业场景】

你在企业里做 UI 自动化，被测系统通常有三种登录方式：账密（好自动化，直接输）、验证码（难自动化）、扫码/SSO（基本无法自动化）。后两种的真实做法就是 Cookie 复用——你手动登录一次，把 Cookie 导出给自动化框架，CI 里每个用例直接注入。这也是为什么"登录态管理"是 UI 自动化框架里几乎必有的一个模块。

【面试考察】

面试官："UI 自动化里，遇到扫码登录或验证码，怎么处理？"

参考回答框架：
1. 先分类：账密登录可直接自动化；验证码要测试环境加"万能验证码"或屏蔽；扫码/SSO 无法自动化。
2. 扫码/SSO 用 **Cookie 复用**：人工登录一次 → `get_cookies()` 拿凭证 → 落盘 → 用例里 `add_cookie()` 注入。
3. 补充边界：Cookie 会过期，要做一个"失效检测 + 重新人工获取"的兜底；并发跑要避免同账号互踢。

【易错点】

| 误区 | 纠正 |
|------|------|
| 以为 Cookie 复用是"绕过登录的测试漏洞" | 它是**测试效率手段**：登录本身仍有专门的用例覆盖，复用只是让其他用例不重复登录 |
| 拿到 Cookie 就一劳永逸 | Cookie 有有效期，过期要重新人工获取；服务端改了会话策略也会失效 |
| 多机/并发共用同一账号 Cookie | 同账号新登录会踢掉旧会话（互踢），应每环境独立账号 |

【我的理解】
> （"登录"和"登录态"是两个东西——登录是"动作"，Cookie 是动作完成后留下的"结果"。为什么复用"结果"比重复"动作"更高效？用一句话说清，并举一个你自己会踩的坑。）

---

## 二、Cookie 的获取与持久化

### 知识点 2：get_cookies() 获取 + yaml 落盘

【课程原话/定义】

```python
class TestCookieLogin:
    def setup_class(self):
        self.drvier = webdriver.Chrome()

    def test_get_cookies(self):
        # 1. 访问企业微信主页/登录页面
        self.drvier.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        # 2. 等待20s，人工扫码操作
        time.sleep(20)
        # 3. 等成功登陆之后，再去获取cookie信息
        cookie = self.drvier.get_cookies()
        # 4. 将cookie存入一个可持久存储的地方，文件
        with open("cookie.yaml", "w") as f:
            yaml.safe_dump(cookie, f)
```

【为什么？】

1. `get_cookies()` 返回的是 `list[dict]`——不是单个 Cookie，而是当前域名下**一整组 Cookie**（可能有多个），所以用 `yaml.safe_dump(列表, f)` 整组落盘，读回来也是列表，遍历逐条 `add_cookie` 即可。
2. **先 get 再取 Cookie**：必须让浏览器先访问到目标域名，`get_cookies()` 才拿得到该域名下已种下的 Cookie；而且一定是在**登录成功之后**调，否则存进去的是"未登录态"。
3. `time.sleep(20)` 是给"人工扫码"留时间——这是少数几个合理保留强制等待的场景（等的是人，不是元素）。

【必须掌握】

- `get_cookies()` 返回 `list[dict]`，每个 dict 含 name/value/domain/path/expiry 等
- 取 Cookie 前必须先登录成功；`time.sleep(20)` 是等人工扫码
- `yaml.safe_dump(list, f)` 落盘、`yaml.safe_load(open(...))` 读回

【企业场景】

你在企业里一般不会在用例里写死 `time.sleep(20)` 等人工扫码——那是"获取 Cookie"的一次性脚本，单独跑一次、拿到 `cookie.yaml` 后就提交给团队，正式用例只读这份文件注入，不再走人工。这就是"获取"和"使用"解耦。

【面试考察】

面试官："`get_cookies()` 返回什么类型？为什么是列表而不是单个值？"

参考回答框架：
1. 返回 `list[dict]`，因为一个域名下通常种了多个 Cookie（登录态往往由多个 Cookie 组合构成，如 token + sessionid + 用户信息）。
2. 每个 dict 有 name/value/domain/path/expiry/httpOnly 等字段。
3. 所以复用时要**逐条** `add_cookie`，不能只注入一个。

【易错点】

| 误区 | 纠正 |
|------|------|
| `self.drvier` 拼写 | 课程源码笔误，应为 `self.driver`（`driver` 拼成了 `drvier`），运行会报 `AttributeError` |
| 还没登录成功就 `get_cookies()` | 存到的是未登录态，复用后依然是"未登录" |
| 在未访问目标域名前取 Cookie | 拿到的可能是空列表，因为 Cookie 是域名维度的 |

【我的理解】
> （`get_cookies()` 是"导出凭证"，`yaml.safe_dump` 是"凭证落盘"。为什么文件落盘比存内存变量更好？结合"获取脚本跑一次、用例长期复用"这个事实回答。）

---

## 三、Cookie 的植入与复用登录

### 知识点 3：add_cookie() 注入 + 刷新进入登录态

【课程原话/定义】

```python
    def test_add_cookie(self):
        # 1. 访问企业微信主页面
        self.drvier.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
        # 2. 定义cookie，cookie信息从已经写入的cookie文件中获取
        cookie = yaml.safe_load(open("cookie.yaml"))
        # 3. 植入cookie
        for c in cookie:
            self.drvier.add_cookie(c)
        time.sleep(3)
        # 4. 再次访问企业微信页面，发现无需扫码自动登录，而且可以多次使用
        self.drvier.get("https://work.weixin.qq.com/wework_admin/frame#contacts")
```

【为什么？】

1. **先 get 到目标域名再 add_cookie**：`add_cookie()` 要求 Cookie 的 `domain` 与当前页面域名匹配，否则抛 `InvalidCookieDomainException`。所以顺序必须是"先打开页面 → 再注入 → 再刷新/重新 get"。
2. **逐条注入**：Cookie 是一组（列表），得循环 `add_cookie(c)`；注入完成后重新访问页面，浏览器携带这些 Cookie 发请求，服务端识别为"已登录"，无需再扫码。
3. **复用多次**：这份 `cookie.yaml` 可以反复读、反复注入，直到 Cookie 过期或服务端踢下线。

【必须掌握】

- `add_cookie()` 前必须先 `get()` 到目标域名
- 逐条 `add_cookie`，注入后重新 `get()`/`refresh()` 进入登录态
- Cookie 可多次复用，但受有效期与互踢约束

【企业场景】

你在企业里的登录态管理模块，核心就是这个"注入"逻辑：把预先导出的 Cookie 读出来，在每个用例的 `setup` 里注入、再刷新一次页面，断言"登录后才会出现的元素"确认真的登上了。注入失败要有日志和截图（承接 Ch16 异常自动截图），否则 CI 里会静默出现"看着在跑、其实全是未登录态"的假绿灯。

【面试考察】

面试官："`add_cookie()` 前为什么要先访问一次页面？"

参考回答框架：
1. Cookie 的 `domain` 必须和当前页面域名匹配，否则抛 `InvalidCookieDomainException`。
2. 所以标准顺序：`get(目标域名)` → 循环 `add_cookie(c)` → `get()/refresh()`。
3. 这也是"注入后要再访问一次"的原因：让浏览器真正带上 Cookie 发请求，服务端才会返回已登录页面。

【易错点】

| 误区 | 纠正 |
|------|------|
| 先 add_cookie 再 get | Cookie domain 与空页面不匹配，抛 `InvalidCookieDomainException` |
| 只注入一个 Cookie | 登录态常由多个 Cookie 组成，要遍历整组逐条注入 |
| 注入完不刷新、直接断言 | 页面还是旧的，要 `get()`/`refresh()` 重新请求才进入登录态 |
| Cookie 的 `sameSite`/`expiry` 字段不兼容 | 直接 dump 再 load 可能带非法值导致 add_cookie 报错，必要时只保留 name/value/domain/path |

【我的理解】
> （`add_cookie` 的"先 get 再注入再 get"三步，分别解决了什么问题？如果调换前两步会怎样，这个报错你想在哪个环节拦住它？）

---

## 四、Java 版对照（JUnit5）

### 知识点 4：ObjectMapper + YAMLFactory 读写 Cookie

【课程原话/定义】

```java
@Slf4j
public class LoginTest {
    static ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
    static WebDriver driver;

    @BeforeAll
    static void setUp(){
        ChromeOptions options = new ChromeOptions();
        //防止连接报错
        options.addArguments("--remote-allow-origins=*");
        driver = new ChromeDriver(options);
    }

    @Test
    void dumpCookie() throws IOException {
        String url = "https://work.weixin.qq.com/wework_admin/frame";
        driver.get(url);
        WebDriverWait wait = new WebDriverWait(driver,
                Duration.ofSeconds(20),
                Duration.ofSeconds(1));
        wait.until(webDriver1 -> StringUtils.contains(webDriver1.getCurrentUrl(), "wework_admin/frame"));
        Set<Cookie> cookies = driver.manage().getCookies();
        log.info("登录cookies:", cookies);
        mapper.writeValue(new File("cookies.yaml"), cookies);
    }

    @Test
    void loadCookie() throws IOException {
        String url = "https://work.weixin.qq.com/wework_admin/frame";
        driver.get(url);
        TypeReference<List<HashMap<String, Object>>> typeReference = new TypeReference<>() {};
        List<HashMap<String, Object>> loadCookies =
                mapper.readValue(new File("cookies.yaml"), typeReference);
        loadCookies.stream()
                .filter(cookie -> cookie.get("domain").toString().contains("work.weixin.qq.com"))
                .forEach(cookie -> {
                    driver.manage().addCookie(
                            new Cookie(cookie.get("name").toString(),
                                    cookie.get("value").toString()));
                });
        driver.navigate().refresh();
    }
}
```

【为什么？】

1. **Python 与 Java 同一思路、两套写法**：Python 用 `yaml.safe_dump` 落盘，Java 用 Jackson 的 `ObjectMapper(new YAMLFactory())` 落盘；Python 用 `yaml.safe_load` 读回，Java 用 `mapper.readValue(file, typeReference)` 读回——本质都是"把 Cookie 序列化到文件、再反序列化注入"。
2. **`TypeReference` 泛型反序列化**：因为目标是 `List<HashMap<String,Object>>`，泛型在运行时会擦除，Jackson 需要 `new TypeReference<>() {}` 保留类型信息，否则反序列化成 `List<LinkedHashMap>` 会类型不匹配。
3. **`--remote-allow-origins=*`**：Chrome 111+ 加了跨域 Origin 校验，不加这个参数会报 `InvalidArgumentException: disconnected: not connected to DevTools`，Java 版必须加。
4. **`filter(domain contains ...)`**：把 Cookie 按 domain 过滤后再注入，只种"企业微信域名下"的 Cookie，避免无关域名干扰。

【必须掌握】

- Python/Java 都遵循"获取→落盘→读回→注入→刷新"五步
- Java 用 `ObjectMapper + YAMLFactory`、`TypeReference` 泛型读回 List
- `--remote-allow-origins=*` 解决 Chrome 111+ 的连接报错
- `@BeforeAll` ↔ Python `setup_class`（JUnit5 与 Pytest 生命周期对照）

【企业场景】

你在企业里技术栈可能是 Java 也可能是 Python，但"登录态管理"的思路完全一致。面试官看重的是你能讲出"这套流程语言无关"——Python 的 `yaml` 和 Java 的 Jackson 只是工具，核心是"凭证序列化 + 注入 + 验证"三步。混用两种语言写同一个功能，正好证明你掌握的是思想而非 API 记忆。

【面试考察】

面试官："Java 里 `new TypeReference<>() {}` 是干什么的？不写会怎样？"

参考回答框架：
1. 这是 Jackson 泛型反序列化用的"类型令牌"（Type Token）。
2. 因为 Java 泛型在运行时被擦除，`mapper.readValue(file, List.class)` 拿不到 `HashMap` 的泛型信息，会反序列化成错误的具体类型。
3. `TypeReference` 通过匿名子类在编译期捕获泛型类型，运行时才能正确还原 `List<HashMap<String,Object>>`。

【易错点】

| 误区 | 纠正 |
|------|------|
| `log.info("登录cookies:", cookies)` | 缺 `{}` 占位符，SLF4J 不会把 cookies 拼进去，日志里看不到值，应写 `log.info("登录cookies: {}", cookies)` |
| Java 版漏加 `--remote-allow-origins=*` | Chrome 111+ 报 `InvalidArgumentException` 连接断开 |
| `readValue` 不用 `TypeReference` | 泛型擦除导致类型不匹配 |
| `driver.manage().getCookies()` 返回 `Set` | 注意是 `Set<Cookie>`（Java）vs Python 的 `list[dict]`，类型形态不同 |

【我的理解】
> （Java 用 `Set<Cookie>`、Python 用 `list[dict]`，为什么同一份 Cookie 数据在两种语言里类型形态不同？这会影响你"跨语言迁移框架"时的哪些判断？）

---

## 五、常见问题与总结

### 知识点 5：企业微信互踢 / 获取时机 / 复用后验证

【课程原话/定义】

**常见问题：**
1. **企业微信等具有互踢机制** —— 同一个账号在新设备/新会话登录，会把旧会话踢下线，旧的 Cookie 立即失效。
2. **获取 Cookie 时为登录成功状态** —— 取 Cookie 的时机必须是"已登录"，否则存的是无效状态。
3. **复用 Cookie 之后的验证问题** —— 注入 Cookie 后不能默认"已经登录了"，要做验证。

【为什么？】

1. **互踢机制**：企业微信等系统服务端只允许一个账号同一时刻保持一个活跃会话，新登录触发"顶号"，旧会话的 Cookie 作废。自动化里"多个用例并发跑同一个账号"或"人工也在登录"时最容易踩。
2. **获取时机**：Cookie 是"登录成功的结果"，在登录过程中或登录失败时抓，等于存了个"没登录"的凭证，复用自然失败。
3. **复用后验证**：`add_cookie` 只是"种下" Cookie，服务端是否认可、会话是否有效，要由下一次请求的结果来证明——所以要断言"登录后才会出现的元素/URL"。

【必须掌握】

- 互踢机制：同账号新登录顶掉旧登录，旧 Cookie 失效，并发要用独立账号
- 取 Cookie 必须在登录成功状态
- 复用后必须验证登录态（断言登录后元素/URL），不能注入完就完事

【企业场景】

你在企业里的登录态管理要加两道保险：一是"Cookie 失效检测"——注入后断言登录态，失败就抛明确的错误 + 截图，而不是让用例带着未登录态往下跑；二是"账号隔离"——并发跑用例时给每个 worker 分独立账号，避免互踢导致一堆用例随机失败、且难以排查。

【面试考察】

面试官："你的自动化用例并发跑时，登录态怎么管理，会不会互相踢？"

参考回答框架：
1. 并发跑必须账号隔离：每个 worker/环境独立账号，避免互踢。
2. Cookie 注入后先断言登录态（登录后才出现的元素），失败即时报错 + 截图。
3. Cookie 有有效期，做失效检测，失效时走"重新人工获取"或"账号密码自动登录"兜底。

【易错点】

| 误区 | 纠正 |
|------|------|
| 并发用例共用同一账号 | 互踢导致 Cookie 随机失效，用例偶发失败难排查 |
| 注入 Cookie 后不做验证 | 带着"未登录态"往下跑，产生假绿灯 |
| Cookie 过期了不处理 | 有效期过了要重新获取，不能一直复用旧文件 |

【我的理解】
> （"注入 Cookie"和"验证已登录"为什么不能合并成一步？想想：服务端认可一个会话，和浏览器"有"这个 Cookie，是同一件事吗？）

---

### 知识点 6：Cookie 复用总结

【课程原话/定义】

在 Web 自动化测试中，掌握 Cookie 复用技巧至关重要。这不仅仅是关于复用 Cookie，更涉及到**复用登录凭证**，以减少繁琐的重复登录步骤，从而提高测试效率。这一技巧的核心在于有效地利用已有的登录状态，为测试过程增添便捷性和高效性。

【为什么？】

复用的本质是"把昂贵的一次性成本（人工登录/扫码）摊薄到所有用例上"：登录只发生一次，之后所有用例都复用它的结果。这背后是一个通用工程思想——**昂贵操作做一次、缓存结果、后续复用**，和"登录后发 token、请求带 token"是同一套逻辑。

【必须掌握】

- 一句话总结：Cookie 复用 = 复用登录凭证，减少重复登录
- 完整链路：人工登录 → get_cookies 落盘 → 用例 add_cookie 注入 → 刷新 → 验证登录态
- 边界：有效期、互踢、获取时机、复用后验证

【企业场景】

你在企业里搭建 UI 自动化框架时，"登录态管理"会作为基础设施沉淀下来：一个 `login.py`/`LoginUtil.java` 负责"获取凭证 + 注入 + 验证 + 失效兜底"，所有用例只调它、不关心细节。这正是从"单条脚本复用 Cookie"进化到"框架级登录态管理"的方向。

【面试考察】

面试官："请完整讲一遍 Cookie 复用的流程，以及每一步为什么这么做。"

参考回答框架：
1. 获取：人工登录成功 → `get_cookies()` 拿凭证 → 落盘（yaml/json）。
2. 注入：用例先 `get(目标域名)` → 循环 `add_cookie()` → `refresh()`。
3. 验证：断言登录后才出现的元素/URL，确认真的登上了。
4. 兜底：Cookie 过期/互踢时重新获取，并发用独立账号。

【易错点】

| 误区 | 纠正 |
|------|------|
| 把"复用 Cookie"理解成"跳过登录测试" | 登录功能本身有专门用例覆盖，复用只为其他用例提效 |
| 只记 API 不记链路顺序 | 顺序错了（先 add 后 get）直接报 `InvalidCookieDomainException` |
| 忽略失效场景 | 有效期/互踢/改会话策略都会让 Cookie 失效，要有兜底 |

【我的理解】
> （把"Cookie 复用"抽象成一句话的工程思想，你会怎么说？再想想这个思想在你学过的其它知识里（比如 token、缓存）是不是也出现过——找出它们的共同点。）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 为什么用 Cookie | HTTP 无状态 + 扫码/验证码无法自动化 | ★★★☆☆ |
| 获取与落盘 | get_cookies() 返回 list[dict] + yaml 持久化 | ★★★★☆ |
| 注入与复用 | 先 get 再 add_cookie 再刷新 + InvalidCookieDomainException | ★★★★★ |
| Java 对照 | ObjectMapper+YAMLFactory + TypeReference + remote-allow-origins | ★★★★☆ |
| 常见问题 | 互踢 / 获取时机 / 复用后验证 | ★★★★★ |
| 总结 | 复用登录凭证，减少重复登录 | ★★★☆☆ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch04-自动化测试用例结构分析]]（setup_class / @BeforeAll 生命周期钩子的来源，本章两版代码都用到）
- [[Ch07-强制等待与隐式等待]]（time.sleep(20) 等人工扫码，是"合理保留强制等待"的例外场景）
- [[Ch13-Web自动化关键数据记录]]（yaml 落盘持久化，与本章 Cookie 落盘同源）
- [[Ch16-异常自动截图]]（注入后验证登录态失败时，截图留证的下游承接）
- [[Ch17-测试用例流程设计]]（登录态作为前置/清理，用例流程设计的一环）
- [[Python/README|Python]]（yaml 读写、setup_class 的语法基础）
