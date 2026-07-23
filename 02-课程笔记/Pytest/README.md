# Pytest 课程笔记

> 测试开发核心技能 — Python 主流测试框架

## 课程清单

| 章节 | 标题 | 状态 | 学习日期 |
|------|------|------|----------|
| [[Ch01-Pytest入门]] | 简介/安装/命名规则/PyCharm配置/用例结构 | draft | |
| [[Ch02-Pytest断言与框架结构]] | assert断言/项目结构/setup与teardown | draft | |
| [[Ch03-Pytest参数化用例]] | 单参数/多参数/笛卡尔积/ids重命名 | draft | |
| [[Ch04-Pytest标记测试用例]] | 自定义marker/注册/-m筛选/内置标记 | draft | |
| [[Ch05-Pytest运行用例]] | 界面化运行/命令行运行/常见运行结果 | draft | 2026-07-23 |
| [[Ch06-Pytest结合数据驱动-YAML]] | DDT概念/YAML语法/PyYAML/数据驱动实战 | draft | 2026-07-23 |
| [[Ch07-Pytest测试用例生命周期管理-fixture]] | 生命周期/fixture定义/作用域/fixture vs setup | draft | 2026-07-23 |
| [[Ch08-Pytest测试用例生命周期管理-yield]] | yield三段式/异常安全/返回值传递 | draft | 2026-07-23 |
| [[Ch09-Pytest测试用例生命周期管理-自动注册]] | conftest.py/自动加载/层级叠加/团队共享 | draft | 2026-07-23 |
| [[Ch10-Pytest测试用例生命周期管理-自动生效]] | autouse=True/显式vs隐式/适用场景 | draft | 2026-07-23 |
| [[Ch11-Pytest插件]] | 插件架构/10个常用插件/内置vs外部vs本地 | draft | 2026-07-23 |
| [[Ch12-Pytest测试用例执行顺序自定义]] | pytest-order/@pytest.mark.order/first/last | draft | 2026-07-23 |
| [[Ch13-Pytest测试用例并行运行与分布式运行]] | pytest-xdist/-n auto/--dist loadscope | draft | 2026-07-23 |

## 核心技能矩阵

| 技能 | 掌握程度 | 面试权重 |
|------|----------|----------|
| Pytest 命名规则 | ⬜ | ⭐⭐⭐⭐⭐ |
| assert 断言六种用法 | ⬜ | ⭐⭐⭐⭐⭐ |
| setup/teardown 四种作用域 | ⬜ | ⭐⭐⭐⭐⭐ |
| @parametrize 参数化（单/多/笛卡尔积） | ⬜ | ⭐⭐⭐⭐⭐ |
| 自定义 marker + -m 筛选 | ⬜ | ⭐⭐⭐⭐⭐ |
| 测试用例三段式结构 | ⬜ | ⭐⭐⭐⭐ |
| ids 用例重命名 + 中文修复 | ⬜ | ⭐⭐⭐ |
| 内置标记（skip/skipif/xfail） | ⬜ | ⭐⭐⭐ |
| PyCharm 配置 Pytest | ⬜ | ⭐⭐ |
| 项目结构组织 | ⬜ | ⭐⭐⭐ |
| 命令行运行（四种粒度 + `::` 语法） | ⬜ | ⭐⭐⭐⭐⭐ |
| 运行结果区分（fail/error/pass/warning/deselect） | ⬜ | ⭐⭐⭐⭐⭐ |
| YAML 数据驱动（safe_load/safe_dump + parametrize） | ⬜ | ⭐⭐⭐⭐⭐ |
| fixture 定义与依赖注入 | ⬜ | ⭐⭐⭐⭐⭐ |
| fixture 五种作用域（function/class/module/package/session） | ⬜ | ⭐⭐⭐⭐⭐ |
| fixture vs setup/teardown 对比 | ⬜ | ⭐⭐⭐⭐⭐ |
| fixture + yield 资源清理 | ⬜ | ⭐⭐⭐⭐⭐ |
| conftest.py 自动注册与层级叠加 | ⬜ | ⭐⭐⭐⭐⭐ |
| autouse 自动生效与取舍原则 | ⬜ | ⭐⭐⭐⭐ |
| 常用插件（order/xdist/html/allure/timeout） | ⬜ | ⭐⭐⭐⭐⭐ |
| 插件分类（内置/外部/本地） | ⬜ | ⭐⭐⭐⭐ |
| pytest-order 执行顺序控制 | ⬜ | ⭐⭐⭐⭐⭐ |
| pytest-xdist 并行/分布式执行 | ⬜ | ⭐⭐⭐⭐⭐ |
