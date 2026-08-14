---
tags: [Pytest, Python, 总结]
created: 2026-08-03
status: completed
---

# Python 类方法 + Pytest 测试总结

> 核心问题：实例方法/静态方法/类方法的区别，self 是什么，pytest 如何调用被测代码。

---

## 一、Python 中三种方法类型

### 1. 实例方法（instance method）

```python
class Calculator:
    def add(self, a, b):
        return a + b
```

| 特征 | 说明 |
|------|------|
| 第一个参数 | 必须是 `self`，表示当前对象 |
| 调用方式 | 先创建对象，再 `对象.方法()` |
| 背后实际 | `Calculator.add(对象, a, b)` |

```python
calculator = Calculator()
result = calculator.add(1, 2)   # self=calculator, a=1, b=2
```

### 2. 静态方法（staticmethod）

```python
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b
```

| 特征 | 说明 |
|------|------|
| 不需要 `self` | 不依赖对象数据 |
| 调用方式 | 直接 `类.方法()` |
| 适用场景 | 工具函数、无状态计算 |

```python
result = Calculator.add(1, 2)   # a=1, b=2
```

### 3. 类方法（classmethod）

```python
class Calculator:
    @classmethod
    def add(cls, a, b):
        return a + b
```

第一个参数是 `cls`（类本身），较少用于普通业务计算。

---

## 二、self 到底是什么？

> ❌ self 是参数  
> ✅ self 是对象本身

```python
class Student:
    def study(self):
        print("学习")

s = Student()
s.study()               # self = s
# 等价于：
Student.study(s)        # 显式传入对象
```

---

## 三、为什么计算器推荐静态方法？

如果方法里没有用到 `self.xxx`（没有访问对象属性），就说明对象没有保存状态，更适合 `@staticmethod`：

```python
# ❌ 没必要 — 没用到 self
class Calculator:
    def add(self, a, b):
        return a + b

# ✅ 更合理 — 无状态，直接调
class Calculator:
    @staticmethod
    def add(a, b):
        return a + b
```

测试时也更简洁：`Calculator.add(1, 2)` 而不是先 `c = Calculator()`。

---

## 四、Pytest 测试基本结构

```
输入 → 调用功能 → 获取结果 → assert 验证
```

```python
def test_add():
    result = Calculator.add(1, 2)
    assert result == 3
```

---

## 五、测试类为什么有 self？

```python
class TestCalculator:
    def test_add(self):
        result = Calculator.add(1, 2)
        assert result == 3
```

因为 `TestCalculator` 本身也是 Python 类，pytest 执行流程：

```python
test = TestCalculator()    # 创建对象
test.test_add()            # 调用方法，self = test
```

| | 测试函数 | 测试类 |
|---|---|---|
| 需要 self？ | 不需要 | 需要（必须） |
| 推荐场景 | 简单测试 | 需要 setup/teardown 时 |

---

## 六、导入类的方法

```
project/
├── calculator.py          ← def class Calculator
└── test_calculator.py     ← from calculator import Calculator
```

```python
from calculator import Calculator

def test_add():
    assert Calculator.add(1, 2) == 3
```

---

## 七、常见错误对照

| 错误写法 | 问题 | 正确写法 |
|----------|------|----------|
| `from operator import add` | 导入了 Python 内置，不是自己的类 | `from calculator import Calculator` |
| `subtract(1, 2)` | 方法是类里的，不能当独立函数调 | `Calculator.subtract(1, 2)` |
| `Calculator.subtract(1, 2, 1)` | 实例方法的第一个参数被当成 self | 静态方法：`Calculator.subtract(1,2)`；实例方法：`obj.subtract(1,2)` |

---

## 八、自动化测试思维

以后所有测试的本质都一样：

```
普通函数测试：   calculator.add()
      ↓
接口测试：       client.post("/login")
      ↓
UI 自动化：      page.login()
```

底层思维不变：**调用功能 → 获取结果 → 验证结果。**

拿到需求先拆：

| 步骤 | 做什么 |
|------|--------|
| 1. 功能点 | 加法、减法、乘法、除法 |
| 2. 输入 | a, b |
| 3. 输出 | 计算结果 |
| 4. 正向测试 | `1+2=3` |
| 5. 异常测试 | `10/0` → `pytest.raises(ZeroDivisionError)` |

---

## 九、速查表

| 方法类型 | 定义 | 调用 |
|----------|------|------|
| 实例方法 | `def add(self, a, b)` | `对象.add(a, b)` |
| 静态方法 | `@staticmethod` / `def add(a, b)` | `类.add(a, b)` |
| 测试函数 | `def test_xxx()` | pytest 自动发现 |
| 测试类方法 | `def test_xxx(self)` | pytest 自动创建对象 |
