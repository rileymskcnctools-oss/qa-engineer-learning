---
tags:
  - 课程笔记
  - 软件测试基础
course: 软件测试基础
chapter: Ch18-测试框架体系（TDD/BDD/ATDD/DDT/MBT）
date: 2026-08-19
status: in_progress
---

# Ch18 - 测试框架体系（TDD/BDD/ATDD/DDT/MBT）

## 课程来源

- 学习日期：2026-08-19
- 章节：测试框架体系介绍

---

## 一、什么是测试框架

### 【课程原话/定义】

> A testing framework is a set of guidelines or rules used for creating and designing test cases. A framework is comprised of a combination of practices and tools that are designed to help QA professionals test more efficiently.

> 测试框架是一组用于创建和设计测试用例的指南或规则。框架由旨在帮助 QA 专业人员更有效测试的实践和工具的组合组成。这些指南可能包括编码标准、测试数据处理方法、对象存储库、存储测试结果的过程、或如何访问外部资源的信息。

### 【为什么需要测试框架？】

裸写测试脚本（一堆 assert + 硬编码 URL/数据）会很快失控：脚本重复、数据散落、结果难维护。框架提供的是一套**约定**——用例怎么写、数据怎么管、结果怎么存、外部资源怎么访问，让团队的自动化测试"可复用、可维护、可扩展"。

### 【必须掌握】测试框架的五大收益

| 收益 | 含义 |
|------|------|
| 提高测试效率 | Improved test efficiency |
| 降低维护成本 | Lower maintenance costs |
| 最少的人工干预 | Minimal manual intervention |
| 最大测试覆盖率 | Maximum test coverage |
| 代码可重用性 | Reusability of code |

### 【我的理解】

> 思考：框架带来的"收益"里，"降低维护成本"和"代码可重用性"是什么关系？为什么说没有框架的自动化脚本"维护成本会越来越高"？

---

## 二、常见测试框架类型总览

### 【必须掌握】五种框架风格

| 框架 | 说明 |
|------|------|
| TDD | 代码风格（测试驱动开发） |
| DDT | 数据驱动风格 |
| ATDD | 验收测试驱动开发 |
| BDD | 行为驱动开发 Behavior-driven development |
| MBT | 基于模型的测试 Model Based Testing |

### 【易错点】"框架类型"其实是不同维度

| 维度     | 类型               | 说明              |
| ------ | ---------------- | --------------- |
| 开发方法论  | TDD / BDD / ATDD | 先写测试还是先写代码？谁来写？ |
| 测试数据组织 | DDT              | 测试逻辑和数据分离，用表格驱动 |
| 测试生成方式 | MBT              | 用模型（图）自动生成测试路径  |

> 面试时别说"这五个都是测试框架"，它们是**不同维度**的实践，常组合使用（如"DDT + 单元测试框架 JUnit"）。

---

## 三、TDD 测试驱动开发

### 【课程原话/定义】

> Test-driven development (TDD) is a software development process relying on software requirements being converted to test cases before software is fully developed. 测试驱动开发（TDD）是一个软件开发过程，在软件完全开发之前将需求转换为测试用例，并通过对所有测试用例重复测试来跟踪开发——与"先开发后写测试"相反。

### 【必须掌握】TDD 流程与关键词

```
写失败的测试 → 写最少代码让测试通过 → 重构
```

| 关键词    | 含义          |
| ------ | ----------- |
| 单元测试   | 先写测试，驱动最小实现 |
| 重构     | 测试通过后优化代码结构 |
| 覆盖率    | 用覆盖率衡量测试充分性 |
| 可测性提升  | 为了可测试而改进设计  |
| 模型驱动设计 | 测试驱动领域建模    |

> TDD 来源于 XP（极限编程）。代表框架：Java 的 JUnit/TestNG，Python 的 pytest/unittest。

### 【必须掌握】TDD 代表框架代码示例

**JUnit 5**

```java
@Test
void standardAssertions() {
    assertEquals(2, calculator.add(1, 1));
    assertEquals(4, calculator.multiply(2, 2),
        "The optional failure message is now the last parameter");
    assertTrue('a' < 'b', () -> "Assertion messages can be lazily evaluated");
}
```

**TestNG（分组测试）**

```java
public class SimpleTest {
  @BeforeClass
  public void setUp() { /* 测试实例化前执行 */ }

  @Test(groups = { "fast" })
  public void aFastTest() { System.out.println("Fast test"); }

  @Test(groups = { "slow" })
  public void aSlowTest() { System.out.println("Slow test"); }
}
```

**pytest**

```python
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5
```

**unittest**

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)
```

### 【易错点】JUnit vs TestNG vs pytest vs unittest

| 框架       | 语言     | 特点                |
| -------- | ------ | ----------------- |
| JUnit    | Java   | 最流行，注解简洁          |
| TestNG   | Java   | 功能更强，支持分组/依赖/参数化  |
| pytest   | Python | 语法最简洁，插件丰富（面试最常提） |
| unittest | Python | 内建框架，类似 JUnit 风格  |

### 【面试考察】

> 面试官："说一下 TDD？你实际用过吗？"

**参考回答框架：** TDD 是"先写测试再写代码"的开发方法：先写一个失败的测试，写最少代码让它通过，再重构。核心价值是让测试驱动设计、提高可测性和覆盖率。用过的框架：Java 用 JUnit/TestNG，Python 用 pytest。诚实说明：真实项目里"纯 TDD"较难坚持，更多是"关键逻辑先写测试 + 事后补测试"的混合模式。

---

## 四、BDD 行为驱动开发

### 【课程原话/定义】

> behavior-driven development (BDD) is an agile software development process that encourages collaboration among developers, quality assurance experts, and customer representatives. It encourages teams to use conversation and concrete examples to formalize a shared understanding of how the application should behave. It emerged from test-driven development (TDD).

> 行为驱动开发（BDD）是鼓励开发、质量保证专家和客户代表之间协作的敏捷软件开发过程，用对话和具体示例形成对应用行为的共同理解。它源于 TDD，并结合了领域驱动设计（DDD）的思想。

### 【必须掌握】BDD vs TDD

| 维度 | TDD | BDD |
|------|-----|-----|
| 关注 | 代码怎么实现 | 系统怎么表现（行为） |
| 语言 | 代码层（assert） | 自然语言（Given/When/Then） |
| 参与者 | 开发 | 开发 + 测试 + 客户 |
| 用例 | 面向函数 | 面向业务场景 |

### 【必须掌握】BDD 相关框架

JBehave、Cucumber、Mspec、Specflow（其中 Cucumber 最主流）。

### 【必须掌握】Cucumber 示例

**Scenario（场景，用自然语言写）**

```gherkin
Scenario: Finding some cheese
   Given I am on the Google search page
   When I search for "Cheese!"
   Then the page title should start with "cheese"
```

**步骤定义（Step Definition，把自然语言映射到代码）**

```java
@Given("I am on the Google search page")
public void I_visit_google() {
    driver.get("https://www.google.com");
}

@When("I search for {string}")
public void search_for(String query) {
    WebElement element = driver.findElement(By.name("q"));
    element.sendKeys(query);
    element.submit();
}

@Then("the page title should start with {string}")
public void checkTitle(String titleStartsWith) {
    new WebDriverWait(driver, 10L).until(d ->
        d.getTitle().toLowerCase().startsWith(titleStartsWith));
}
```

### 【为什么 BDD 用 Given/When/Then？】

Given（前置条件）/ When（动作）/ Then（预期结果）把测试用例变成一句"业务语言"，让不懂代码的客户/产品也能看懂、能确认需求。这是 BDD 的核心价值——**用具体示例对齐各方对需求的理解**。

### 【面试考察】

> 面试官："TDD 和 BDD 的区别？"

**参考回答框架：** TDD 面向开发，用代码断言驱动实现；BDD 面向协作，用 Given/When/Then 自然语言描述行为，让开发、测试、客户共同理解需求。BDD 源于 TDD，但把"技术测试"提升到"业务行为描述"，工具如 Cucumber。

---

## 五、ATDD 验收测试驱动开发

### 【课程原话/定义】

> Acceptance test–driven development (ATDD) is a development methodology based on communication between the business customers, the developers, and the testers. 验收测试驱动开发（ATDD）是基于业务客户、开发人员和测试人员之间沟通的开发方法，让客户能用自己的领域语言交流。

### 【必须掌握】ATDD 相关工具

| 工具 | 说明 |
|------|------|
| FitNesse | 完全集成的独立 wiki 和验收测试框架 |
| Robot Framework | 基于 Python 的可扩展关键字驱动自动化框架，支持 ATDD/BDD/RPA |

### 【必须掌握】Robot Framework 示例

**基础结构（Settings / Test Cases / Keywords）**

```robotframework
*** Settings ***
Documentation     Simple example using SeleniumLibrary.
Library           SeleniumLibrary

*** Variables ***
${LOGIN URL}      http://localhost:7272
${BROWSER}        Chrome

*** Test Cases ***
Valid Login
    Open Browser To Login Page
    Input Username    demo
    Input Password    mode
    Submit Credentials
    Welcome Page Should Be Open
    [Teardown]    Close Browser

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Title Should Be    Login Page
```

**数据驱动风格（Test Template）**

```robotframework
*** Settings ***
Test Template    Login with invalid credentials should fail

*** Test Cases ***                USERNAME         PASSWORD
Invalid User Name                 invalid          ${VALID PASSWORD}
Invalid Password                  ${VALID USER}    invalid
Empty User Name                   ${EMPTY}         ${VALID PASSWORD}
```

**BDD 风格**

```robotframework
*** Test Cases ***
Valid Login
    Given login page is open
    When valid username and password are inserted
    and credentials are submitted
    Then welcome page should be open
```

### 【必须掌握】TDD / ATDD / BDD 三者对比

| 维度 | TDD | ATDD | BDD |
|------|-----|------|-----|
| 受众 | 开发 | 开发 + 测试 + 客户 | 开发 + 测试 + 客户 |
| 过程 | 代码 | DSL（领域语言） | 行为 |
| 目标 | 代码调用功能 | 验收测试、需求 | 需求 |

### 【我的理解】

> 思考：ATDD 和 BDD 的受众都是"开发+测试+客户"，那它们到底差在哪？试着从"验收"和"行为"两个关键词区分它们。
> 
> ATDD 更强调“验收”，从需求和验收标准出发，确保最终功能满足业务要求；BDD 更强调“行为”，通过具体场景描述用户行为和系统预期行为。两者都强调开发、测试和业务共同参与，而且实际项目中经常结合使用。

---

## 六、DDT 数据驱动测试

### 【课程原话/定义】

> Data-driven testing (DDT), also known as table-driven testing or parameterized testing, describes testing done using a table of conditions directly as test inputs and verifiable outputs, where test environment settings and control are not hard-coded.

> 数据驱动测试（DDT，也叫表驱动/参数化测试），用条件表直接作为测试输入和可验证输出，测试环境设置和控制不硬编码。

### 【必须掌握】DDT 是"实践"，可结合多种框架

- 单元测试 + DDT：JUnit4 / JUnit5 / TestNG
- RobotFramework 的 DDT（Test Template）
- YAML / JSON / CSV 驱动的 HttpRunner

### 【必须掌握】HttpRunner（数据驱动 + YAML 用例）

```yaml
config:
  name: "request methods testcase with functions"
  variables:
    foo1: config_bar1
    base_url: "https://postman-echo.com"
  verify: False

teststeps:
  - name: get with params
    variables:
      foo1: bar11
    request:
      method: GET
      url: /get
      params:
        foo1: $foo1
    extract:
      foo3: "body.args.foo2"
    validate:
      - eq: ["status_code", 200]
      - eq: ["body.args.foo1", "bar11"]
  - name: post raw text
    request:
      method: POST
      url: /post
      data: "This is expected to be sent back: $foo1"
    validate:
      - eq: ["status_code", 200]
```

### 【必须掌握】数据驱动应用案例

| 场景 | 说明 |
|------|------|
| HttpRunner | 根据代理抓包自动生成测试用例 |
| YAPI / Swagger | 根据数据（接口定义）自动生成测试用例代码 |
| JVM-Sandbox-Repeater / Gor | 录制请求保存为用例并重放，实现快速回归 |

### 【为什么数据驱动风格广受欢迎？】

| 原因 | 说明 |
|------|------|
| 维护成本最低 | 逻辑和数据分离，加用例只加一行数据 |
| 录制回放技术成熟 | 录制工具产出结构化数据，天然适配 DDT |
| 低代码/用例生成流行 | 让数据驱动风格更普及 |

### 【我的理解】

> 思考：DDT 的"逻辑与数据分离"为什么能"降低维护成本"？如果 100 条用例的数据写死在 100 个脚本里，改一个字段要动几处？

---

## 七、MBT 基于模型的测试

### 【课程原话/定义】

> Model-Based Testing (MBT) 用模型（图）描述被测系统，工具从模型中自动生成测试路径。代表工具 GraphWalker。

### 【必须掌握】GraphWalker 三个核心概念

| 概念 | 含义 |
|------|------|
| edge（边） | 代表一个动作/转移：API 调用、按钮点击、超时等，把系统推进到新状态（**边不做验证**） |
| vertex（顶点） | 代表验证/断言：在这里验证 API 返回值、按钮是否关闭对话框等 |
| graph（图） | 模型 = 一组顶点和边，GraphWalker 从模型生成路径 |

> 模型有起始元素（start element）、路径生成规则（generator）、停止条件（stop condition）。

### 【必须掌握】MBT 代码示例

```java
@GraphWalker(value = "random(edge_coverage(100))")
public class OwnerInformationTest extends ExecutionContext implements OwnerInformation {

    @Override
    public void v_OwnerInformation() {   // vertex：断言
        $(By.tagName("h2")).shouldHave(text("Owner Information"));
    }

    @Override
    public void e_UpdatePet() {          // edge：动作
        $("button[type=\"submit\"]").click();
    }
    // ... 其余 e_xxx 动作方法、v_xxx 断言方法
}
```

### 【易错点】MBT 的"边 vs 顶点"

| 概念 | 职责 | 别搞混 |
|------|------|--------|
| edge（边） | 动作、转移，**不做验证** | 点击/调用 API/超时 |
| vertex（顶点） | 断言、验证，**不做动作** | 校验返回值/对话框关闭 |

> 面试关键词："edge 是动作、vertex 是断言，GraphWalker 从图模型生成测试路径"。

---

## 八、五种框架横向对比

| 维度 | TDD | BDD | ATDD | DDT | MBT |
|------|-----|-----|------|-----|-----|
| 核心 | 先写测试再写代码 | 用行为描述需求 | 用验收标准驱动开发 | 数据与逻辑分离 | 用模型生成路径 |
| 语言 | 代码断言 | Given/When/Then | 领域语言 | 表格/数据文件 | 图模型 |
| 代表工具 | JUnit/pytest | Cucumber/JBehave | FitNesse/RobotFramework | HttpRunner/参数化 | GraphWalker |
| 谁参与 | 开发 | 开发+测试+客户 | 开发+测试+客户 | 测试 | 测试/开发 |

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| 测试框架定义与收益 | 五大收益（效率/维护/干预/覆盖/复用） | ⭐⭐⭐ |
| TDD | 先测后码、红绿重构、JUnit/pytest | ⭐⭐⭐⭐ |
| BDD | 行为驱动、Given/When/Then、Cucumber | ⭐⭐⭐⭐ |
| ATDD | 验收驱动、FitNesse/RobotFramework | ⭐⭐⭐ |
| DDT | 数据驱动、HttpRunner、维护成本最低 | ⭐⭐⭐⭐ |
| MBT | 模型生成路径、edge/vertex/graph | ⭐⭐⭐ |

---

## 今天没搞懂的问题

-
-
-

---

## 关联笔记

- [[Ch04-测试技术体系]] — 单元测试工具（pytest/JUnit）、测试金字塔
- [[Ch15-自动化测试策略]] — 接口测试框架（Requests/RestAssured）
- [[Ch14-分层测试策略]] — 分层测试是框架落地的理论基础
- [[../Pytest/README|Pytest]] — pytest 详细学习
