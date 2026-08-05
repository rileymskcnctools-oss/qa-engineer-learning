---
tags: [Pytest, setup_class, 对象管理]
created: 2026-08-03
status: completed
---

# cls.calculator = Calculator() 与 self.calculator.subtract() 详解

> 核心：pytest 中如何提前创建被测对象，测试方法如何通过属性找到并调用它。

---

## 1. `cls.calculator = Calculator()` 做了什么？

```python
@classmethod
def setup_class(cls):
    cls.calculator = Calculator()
```

逐层拆解：

| 步骤 | 代码 | 含义 |
|------|------|------|
| ① | `Calculator()` | 创建一个 Calculator 实例对象 |
| ② | `cls` | 代表测试类 `TestCalculator` 本身 |
| ③ | `cls.calculator = ...` | 给测试类添加一个类属性，保存 Calculator 对象 |

结构：

```
TestCalculator 类
    └── calculator 属性（类属性）
            └── Calculator 实例对象
                ├── add()
                ├── subtract()
                └── divide()
```

---

## 2. `calculator` 是属性吗？

是。

```python
cls.calculator       # ✅ 类属性（cls 代表类）
self.calculator      # ✅ 实例属性（self 代表实例对象）
```

| | `cls.calculator` | `self.calculator` |
|---|---|---|
| 定义位置 | `setup_class(cls)` | `setup_method(self)` |
| 作用范围 | 整个测试类共享 | 每个测试方法独立 |
| 生命周期 | 类加载时创建一次 | 每个测试方法创建和销毁 |

---

## 3. 为什么后面用 `self.calculator`？

```python
def test_subtract(self):
    self.calculator.subtract(2, 1)
```

pytest 执行时：`test = TestCalculator()` → `test.test_subtract()`。此时 `self` 就是 `test` 这个实例。

Python 查找 `self.calculator` 的顺序：

```
1. test 实例本身有没有 calculator？ → 没有
2. TestCalculator 类有没有 calculator？ → 有！（setup_class 里创建的）
3. 找到了 → 返回 Calculator 对象
4. 调用 .subtract(2, 1)
```

---

## 4. 为什么不直接写？

```python
# ❌ self 是 TestCalculator 实例，没有 subtract 方法
self.subtract(2, 1)

# ✅ 通过 calculator 属性找到 Calculator 对象，再调方法
self.calculator.subtract(2, 1)
```

---

## 5. 为什么提前创建对象？

```python
# ❌ 每个测试都 new 一次，重复
def test_add(self):
    c = Calculator()
    c.add(1, 2)

def test_subtract(self):
    c = Calculator()
    c.subtract(2, 1)

# ✅ 一次创建，所有测试共用
@classmethod
def setup_class(cls):
    cls.calculator = Calculator()

def test_add(self):
    self.calculator.add(1, 2)

def test_subtract(self):
    self.calculator.subtract(2, 1)
```

---

## 6. 类属性 vs 实例属性

| | 类属性（`cls.xxx`） | 实例属性（`self.xxx`） |
|---|---|---|
| 创建次数 | 1 次 | 每个测试 1 次 |
| 数据共享 | 所有测试共用 | 测试之间隔离 |
| 适合场景 | 浏览器对象、API 客户端、数据库连接 | 需要每个测试独立环境的数据 |
| 定义方式 | `setup_class` | `setup_method` |

---

## 7. 完整流程图

```
pytest 启动
    ↓
setup_class()
    ↓
cls.calculator = Calculator()    ← 创建被测对象，挂到类上
    ↓
test_add(self)
    ↓
self.calculator.add(1, 2)        ← 通过类属性找到对象，调用方法
    ↓
assert result == 3
    ↓
test_subtract(self)
    ↓
self.calculator.subtract(2, 1)   ← 同一个对象，复用
    ↓
assert result == 1
```

---

## 8. 这个模式的未来应用

以后所有自动化测试都是同一模式：

```python
# Web 自动化
cls.driver = webdriver.Chrome()
self.driver.find_element(...)

# 接口测试
cls.session = requests.Session()
self.session.post("/login", ...)

# API 封装
cls.api = UserApi()
self.api.login("admin", "123456")
```

> **一句话：`setup_class` 创建资源 → 保存为类属性 → 测试方法通过 `self` 访问调用。**

---

## 9. 参数化 `@parametrize` 的参数传给了谁？

```python
@pytest.mark.parametrize(
    "balance,amount,expected",
    [(1000, 50, 1050), (0, 200, 200), (500, 100, 600)]
)
def test_deposit(self, balance, amount, expected):
```

这些参数**不是传给实例对象的**，是传给**测试方法的参数**。

pytest 做的事：

```
第一次执行：test_deposit(balance=1000, amount=50, expected=1050)
第二次执行：test_deposit(balance=0,    amount=200, expected=200)
第三次执行：test_deposit(balance=500,  amount=100, expected=600)
```

---

## 10. 什么时候传给对象？

在测试方法**内部**手动传：

```python
def test_deposit(self, balance, amount, expected):
    account = BankAccount("Tom", balance)   # ← 这里才传给构造方法
    account.deposit(amount)
    assert account.balance == expected
```

完整流程：

```
@parametrize 提供 balance=1000, amount=50, expected=1050
    ↓
test_deposit 收到参数
    ↓
BankAccount("Tom", 1000)    ← 构造方法接收 balance
    ↓
account.deposit(50)         ← 业务方法接收 amount
    ↓
assert balance == 1050      ← 用 expected 验证
```

---

## 11. 两条不同的参数路线

```python
# 路线 A：setup_class 创建固定对象
cls.account = BankAccount("Riley", 1000)
#            ↑ 参数直接进入 __init__

# 路线 B：@parametrize 提供多组数据
@pytest.mark.parametrize("balance,amount,expected", [...])
def test_deposit(self, balance, amount, expected):
    #             ↑ 参数进入测试方法
    account = BankAccount("Tom", balance)
    #                                ↑ 测试方法再传给构造方法
```

| | 构造方法参数 | 参数化参数 |
|---|---|---|
| 来源 | 代码里直接写 | `@parametrize` 装饰器 |
| 传入目标 | `__init__(self, owner, balance)` | 测试方法 `(self, balance, ...)` |
| 作用 | 控制对象初始状态 | 控制测试输入数据 |
| 适用 | 固定资源（driver、session） | 多组数据（边界值、等价类） |

---

## 12. 一张图看清两条路线

```
                    pytest 启动
                        |
            ┌───────────┴───────────┐
            ↓                       ↓
    setup_class()              @parametrize
            ↓                       ↓
    cls.account =              提供多组数据
    BankAccount(                 (1000,50,1050)
        "Riley",1000)            (0,200,200)
            ↓                       ↓
    固定对象，所有测试共用       每组数据执行一次测试
            ↓                       ↓
            └───────────┬───────────┘
                        ↓
              test 方法内部
                        ↓
            assert 验证结果
```

---

## 13. 速查

```
实例化参数：  BankAccount("Riley", 1000)
                    ↑ 创建对象时传入

参数化参数：  @pytest.mark.parametrize(...)
                    ↑ 测试执行时传入

一个控制对象状态，一个控制测试输入数据。
```

