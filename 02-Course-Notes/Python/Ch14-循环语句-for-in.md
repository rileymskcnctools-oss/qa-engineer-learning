---
tags: [课程笔记, Python]
course: "Python"
chapter: "Ch14-循环语句-for-in"
created: 2026-07-15
status: draft
---

# Ch14 - 循环语句 for-in

## 课程来源
- 学习日期：

---

## 一、for-in 是什么

### 知识点 1：for-in 的本质

【课程原话/定义】
Python 没有 C 语言那种传统 for 循环，而是提供了专门处理可迭代序列类型的增强型 for 循环 for-in。它会将可迭代对象中的元素依次取出，保存到迭代变量中，每取出一个元素便执行一次循环体。

【为什么？】
Python 的 for-in 设计哲学是"遍历对象本身，而不是遍历索引"。传统 for 循环 `for(i=0; i<len; i++)` 需要你手动管理索引、边界、步长——很容易写出差 1 错误。Python 的 for-in 让你直接说"把每个元素给我"，底层迭代器自动处理边界，更安全、更简洁。

这和 while 的本质区别：while 是"只要条件成立就一直做"，for-in 是"把集合里的每个元素都处理一遍"。测试中遍历用例列表、接口返回的数据数组，天然就是 for-in 的领地。

【必须掌握】
- 语法：`for 迭代变量 in 可迭代对象: 循环体`
- 可迭代对象包括：字符串、列表、元组、字典、集合、range()、文件对象等
- 不需要手动管理索引

【企业场景】
> 数据驱动测试的核心就是 for-in：`for case in test_cases: result = execute(case); assert result == case["expected"]`。这个模式在 Pytest 参数化、unittest DDT 中都存在，底层都是 for-in 循环遍历用例数据。

【面试考察】
> 面试官："Python 的 for-in 和 C 语言的 for(;;) 有什么不同？"
> 参考回答：C 的 for 是计数器循环（手动管理 i），Python 的 for-in 是迭代器循环（自动遍历可迭代对象）。Python 更安全——不会出现索引越界、不会因为差 1 错误漏掉或重复处理边界元素。

【我的理解】


---

## 二、遍历各种数据类型

### 知识点 2：遍历字符串

【课程原话/定义】
for-in 遍历字符串时，每次取出一个字符。

```python
s = "Hello"
for c in s:
    print(c)  # H, e, l, l, o
```

【为什么？】
字符串本质是字符序列，for-in 按序取出每个字符。测试中常用于字符级验证——比如验证生成的验证码是否全是数字、验证接口返回的 token 长度。

【企业场景】
> 验证随机生成的测试数据是否符合格式：`for ch in generated_code: assert ch in "0123456789"`——确保验证码全是数字。

【我的理解】


### 知识点 3：遍历元组

【课程原话/定义】
for-in 遍历元组时，依次取出每个元素。和列表遍历完全一致。

【企业场景】
> 测试中使用元组存储不可变的配置项序列，for-in 遍历检查：`for code in (200, 201, 204): assert_http_method_returns(method, code)`。

【我的理解】


### 知识点 4：遍历列表

【课程原话/定义】
for-in 遍历列表时，依次取出每个元素。这是 for-in 最常用的场景。

```python
methods = ["get", "post", "put", "delete"]
for method in methods:
    print(method.upper())  # GET, POST, PUT, DELETE
```

【为什么？】
列表是测试中最常见的数据容器（用例列表、结果列表、日志列表）——for-in 遍历列表就是测试脚本的"心跳"。Pytest 的 `@pytest.mark.parametrize` 背后的核心机制就是 for-in 遍历参数列表。

【企业场景】
> 批量执行接口测试：
> ```python
> endpoints = ["/api/users", "/api/orders", "/api/products"]
> for endpoint in endpoints:
>     response = requests.get(base_url + endpoint)
>     assert response.status_code == 200, f"{endpoint} 返回 {response.status_code}"
> ```

【易错点】

| 操作 | 会出现什么 | 怎么避免 |
|------|----------|---------|
| for 循环里 `l.append(x)` | 无限循环（每次迭代列表变长） | 遍历 `l[:]`（遍历副本） |
| for 循环里 `l.remove(x)` | 跳元素（索引错乱） | 列表推导式或遍历副本 |
| `for i in range(len(l))` | 手动管理索引，差 1 错误 | 直接用 `for item in l` |

【我的理解】


### 知识点 5：遍历字典

【课程原话/定义】
字典是特殊的——有 4 种遍历方式，每种取出的东西不同。

**方式一：默认遍历 → 遍历 key**

```python
for k in d:          # 等价于 for k in d.keys()
    print(k)         # 只拿到 key
```

**方式二：显式遍历 key**

```python
for k in d.keys():
    print(k)         # 和默认遍历一样，但更明确
```

**方式三：遍历 value**

```python
for v in d.values():
    print(v)         # 只拿到 value
```

**方式四：遍历 key-value（最常用）**

```python
for k, v in d.items():      # 解包：元组 (key, value) 拆成两个变量
    print(f"{k}: {v}")      # 同时拿到 key 和 value
```

也可以不拆包，手动取：

```python
for item in d.items():       # item 是元组 (key, value)
    print(f"{item[0]}: {item[1]}")
```

【为什么？】
字典默认遍历 key 是合理设计——大多数场景你只需要知道"有哪些 key"，然后通过 key 取值。`items()` + 解包是最 Pythonic 的写法，一行拿到 k 和 v，比手动 `item[0]` `item[1]` 可读性好太多。

【必须掌握】
- 4 种遍历方式，`for k,v in d.items()` 是最常用的
- 解包：`k, v = (key, value)` 等价于 `k = t[0]; v = t[1]`
- `d.keys()` / `d.values()` / `d.items()` 返回的是视图对象（不是列表副本）

【企业场景】
> 接口返回的 JSON 就是字典。遍历所有字段做验证：
> ```python
> response_data = {"code": 0, "message": "success", "data": {...}}
> required_fields = {"code", "message", "data"}
> for k in response_data:
>     assert k in required_fields, f"意外字段: {k}"
> ```
>
> 打印所有字段便于调试：
> ```python
> for key, value in response.items():
>     print(f"  {key}: {value}")
> ```

【面试考察】
> 面试官："遍历字典有哪几种方式？`for k in d` 和 `for k in d.keys()` 有区别吗？"
> 参考回答：四种——默认遍历 key、`keys()`、`values()`、`items()`。`for k in d` 和 `for k in d.keys()` 效果相同，但 `d.keys()` 可以用于集合运算（如 `d.keys() & other_keys`）。`items()` 配合解包是最常用的完整遍历方式。

【易错点】

| 遍历方式 | 迭代变量拿到什么 | 典型场景 |
|----------|---------------|---------|
| `for k in d` | key | 只需判断 key 是否存在 |
| `for k in d.keys()` | key | 同上，但可做集合运算 |
| `for v in d.values()` | value | 只关心值，不关心键（少见） |
| `for k, v in d.items()` | key 和 value | 需要同时用 key 和 value（最常见） |
| `for item in d.items()` | 元组 (k, v) | 需要用 item[0] item[1] 访问（不推荐） |

```python
# 动手验证 4 种遍历方式的区别：
d = {"get": "获取", "post": "提交", "put": "更新", "delete": "删除"}

print("=== 默认遍历 ===")
for x in d:
    print(f"  拿到: {x}")

print("=== keys() ===")
for x in d.keys():
    print(f"  拿到: {x}")

print("=== values() ===")
for x in d.values():
    print(f"  拿到: {x}")

print("=== items() 解包 ===")
for k, v in d.items():
    print(f"  拿到: {k} -> {v}")

print("=== items() 不解包 ===")
for item in d.items():
    print(f"  拿到: {item}, 类型: {type(item)}")
```

【我的理解】


---

## 三、while vs for-in 对比

### 知识点 6：什么时候用哪个

| 对比维度 | while | for-in |
|----------|-------|--------|
| 适用场景 | 不知道循环次数，知道结束条件 | 知道要遍历的集合 |
| 循环次数 | 由条件决定 | 由集合大小决定 |
| 是否需要索引 | 不直接提供索引 | 不直接提供（需要时用 `enumerate()`） |
| 死循环风险 | 高（忘记迭代） | 低（集合遍历完自动结束） |
| 测试中典型用法 | 轮询等待、重试 | 遍历用例、遍历结果 |
| Python 特性 | 支持 `while...else` | 支持 `for...else`（未 break 时执行 else） |

【面试考察】
> 面试官："while 和 for-in 怎么选？给一个具体例子说明你的选择逻辑。"
> 参考回答：知道要遍历什么集合→for-in（如遍历用例列表）；只知道结束条件但不知道要等多久→while（如轮询接口状态直到成功）。举例：跑 100 个用例用 for-in；提交异步任务后轮询结果用 while。

【我的理解】


---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| for-in 本质 | 迭代器遍历，不是计数器循环 | ★★★ |
| 遍历列表 | 最常用场景，注意遍历时不能增删 | ★★★ |
| 遍历字典 4 种方式 | 默认 key、keys()、values()、items()+解包 | ★★★ |
| 遍历字符串/元组 | 字符序列、元素序列 | ★☆☆ |
| while vs for-in | 条件循环 vs 计次循环的选择 | ★★★ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch13-循环语句-while]] — while vs for-in 对比选择
- [[Ch10-字典]] — `keys()` / `values()` / `items()` 方法
- [[Ch09-列表]] — 遍历时增删列表元素的陷阱
- [[Ch08-字符串]] — 字符串作为字符序列的遍历
