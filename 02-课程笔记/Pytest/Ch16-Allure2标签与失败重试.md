---
tags: [课程笔记, Pytest, Allure]
course: "Pytest"
chapter: "Ch16-Allure2标签与失败重试"
created: 2026-07-28
status: draft
---

# Ch16 - Allure2 标签与失败重试

## 课程来源
- 学习日期：

---

## 一、Pytest 标签在 Allure 中的展示

### 知识点1：xfail 标签

【课程原话/定义】
使用 `@pytest.mark.xfail` 标记预期失败的用例。Allure 会区分 xfail（预期失败，实际失败）和 xpass（预期失败，实际通过）两种状态。

【为什么？】
> 已知 Bug 的用例天天报警，你烦不烦？用 xfail 标记后，领导问"为什么这条用例总是失败"，你直接回答"这是已知 Bug BUG-123，已标记预期失败"。

【必须掌握】

```python
# xfail：预期失败，实际失败 → 报告显示为 expected failure ✓
@pytest.mark.xfail(reason='BUG-123: 验证码不刷新')
def test_captcha():
    assert False

# xpass：预期失败，实际通过 → 报告显示为 unexpected success ⚠
@pytest.mark.xfail(reason='BUG-456: 已修复但用例未更新')
def test_fixed_bug():
    assert True
```

| Allure 展示 | 含义 | 实际结果 |
|-------------|------|----------|
| Expected Failure | 预期失败 | 用例失败了（符合预期） |
| Unexpected Success (xpass) | 意外通过 | 用例通过了（Bug 可能已修复） |

【企业场景】
> 你们团队有个登录页验证码的 Bug，开发说"下个迭代再修"。你用 `@pytest.mark.xfail(reason='BUG-234')` 标记相关用例。3 周后 CI 报告突然出现一条 "Unexpected Success"——Bug 被悄悄修好了！你去 Allure 里点链接确认，然后移除 xfail 标记。

【面试考察】
> 面试官：Allure 报告里的 xfail 和 xpass 分别代表什么？你们怎么用？
> 
> 参考回答框架：xfail = expected failure（标记了会失败，确实失败了），xpass = unexpected success（标记了会失败，结果通过了，说明 Bug 可能已经修复）

【易错点】

| 常见错误 | 正确做法 |
|----------|----------|
| 所有不稳定用例都标 xfail | xfail 是标记"已知 Bug"，不是"偶发不稳定"。偶发不稳定用 rerun |
| Bug 修复后忘记移除 xfail | xpass 就是提醒机制——定期检查 xpass 用例，确认 Bug 已修复就移除标记 |

【我的理解】
> （请用自己的话说说：一条用例挂了，你什么时候用 xfail 标记，什么时候直接提 Bug？）

---

### 知识点2：skipif 标签

【课程原话/定义】
`@pytest.mark.skipif(condition, reason)` 根据条件跳过用例。Allure 报告中展示为 Skipped 状态。

【为什么？】
> Windows 上能跑的用例在 Mac 上跑不了怎么办？直接跳过，别让 CI 报红。

【必须掌握】

```python
import sys

@pytest.mark.skipif(sys.platform == 'darwin', reason='仅支持 Windows 环境')
def test_windows_only():
    pass

@pytest.mark.skipif(True, reason='功能未开发完成')
def test_not_ready():
    pass
```

【企业场景】
> 你们的测试环境分 Windows 和 Linux 两套。某些用例依赖 Windows 特有的浏览器驱动，在 Linux CI 上跑会直接报错。你用 `skipif(sys.platform != 'win32')` 让这些用例在 Linux 上自动跳过。Allure 报告里显示 Skipped，不是 Failed，不影响通过率统计。

【面试考察】
> 面试官：skipif 在 Allure 报告里怎么展示？会影响测试通过率吗？
> 
> 参考回答框架：展示为 Skipped 状态，不影响通过率。通常用于环境不兼容或功能未完成的场景。

【我的理解】
> （请写一个 skipif 的例子：只在 Python 3.10+ 版本才执行的用例）

---

### 知识点3：fixture 在 Allure 中的展示

【课程原话/定义】
Allure 自动追踪每个 fixture 的调用，展示 fixture 的执行顺序和参数，保持正确的前后置顺序。

【为什么？】
> 你的用例 setUp 了 3 个 fixture，结果测试失败，你怎么知道是哪个 fixture 出问题了？

【必须掌握】

```python
@pytest.fixture()
def db_connection():
    print("连接数据库")
    yield
    print("断开数据库")

@pytest.fixture()
def login_session(db_connection):   # fixture 依赖另一个 fixture
    print("登录获取 token")
    yield
    print("登出清除 token")

def test_query(login_session):
    print("执行查询")
    assert True
```

Allure 报告中 fixture 展示顺序：`db_connection (setup) → login_session (setup) → test_query → login_session (teardown) → db_connection (teardown)`

【企业场景】
> 你的用例依赖 4 层 fixture：config → db → redis → api_client。某天用例挂在了 redis 连接上，Allure 报告的 fixture 时间线一眼定位到 redis 的 setup 耗时 30 秒后超时——你直接去找运维修复 Redis，不用逐层排查。

【面试考察】
> 面试官：Allure 能展示 fixture 的执行顺序吗？这对排查问题有什么用？
> 
> 参考回答框架：能，Allure 自动追踪 fixture 调用链，报告中按时间线展示每个 fixture 的 setup 和 teardown。排查 fixture 依赖问题时直接看哪个 fixture setup 失败或超时。

【我的理解】
> （请画一个 fixture 依赖链：A → B → C → 用例，说明 Allure 中的展示顺序）

---

## 二、失败重试功能

### 知识点4：pytest-rerunfailures + Allure

【课程原话/定义】
配合 `pytest-rerunfailures` 插件，Allure 可以记录失败重试的历史，在报告详情的 Retries 选项卡中展示每次重试的结果。

【为什么？】
> 用例因为网络抖动失败一次，就判定为 Bug？太冤了。重试机制能帮你区分"偶发失败"和"真 Bug"。

【必须掌握】

```bash
pip install pytest-rerunfailures
```

```python
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_flaky_network():
    import random
    assert random.choice([True, False])  # 模拟不稳定
```

| 参数 | 含义 |
|------|------|
| `reruns` | 失败后重试次数 |
| `reruns_delay` | 每次重试间隔（秒） |

Allure 报告中的展示：
- 第一次失败 → Retries 显示 Attempt 1: Failed
- 第二次失败 → Retries 显示 Attempt 2: Failed
- 第三次通过 → 最终状态 Passed，Retries 记录完整历史

【企业场景】
> 你们的 UI 自动化每天跑 200 条用例，总有 3~5 条因为页面加载慢偶发失败。你给所有用例加上 `reruns=1, reruns_delay=3`。每天早上看 Allure 报告：Retries 里有一次重试就通过的 → 环境抖动，忽略。重试 3 次全部失败 → 真 Bug，提单。从"每天早上排查 5 个误报"变成"每天早上看 0~1 个真 Bug"。

【面试考察】
> 面试官：一条用例重试了 3 次才通过，你怎么判断是环境问题还是代码 Bug？
> 
> 参考回答框架：看 Allure 的 Retries 选项卡。如果每次失败的错误信息不一样（如第 1 次超时、第 2 次通过了），大概率是环境问题。如果每次都是同一个断言失败，大概率是代码 Bug。结合趋势统计，如果该用例历史上很少失败，这次连续失败，优先排查环境。

【易错点】

| 错误 | 正确 |
|------|------|
| `reruns` 设置太高（如 10 次） | 合理设 1~3 次，重试太多拖慢 CI 且掩盖真 Bug |
| 不稳定用例只加重试不排查根因 | 重试是最后防线，先排查为什么不稳定（等待时间不够？数据冲突？） |
| 混淆 flaky 和 xfail | flaky = 偶发失败（重试能过），xfail = 已知 Bug（预期失败） |

【我的理解】
> （请设计一个场景：哪些情况适合加重试，哪些情况不适合？至少各举一个例子）

---

## 今日课程总结

| 模块 | 核心内容 | 面试权重 |
|------|----------|----------|
| xfail | 预期失败（xfail）vs 意外通过（xpass） | ⭐⭐⭐⭐ |
| skipif | 条件跳过，不影响通过率 | ⭐⭐⭐ |
| fixture 展示 | Allure 自动追踪 fixture 调用链 | ⭐⭐⭐⭐ |
| 失败重试 | rerun + Retries 选项卡排查偶发失败 | ⭐⭐⭐⭐⭐ |

---

## 今天没搞懂的问题
-
-
-

## 关联笔记
- [[Ch14-Allure2安装与报告生成]]
- [[Ch15-Allure2用例装饰器]]
- [[Ch07-Pytest测试用例生命周期管理-fixture]]
