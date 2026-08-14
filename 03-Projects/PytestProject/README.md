# PytestProject — Pytest 练习项目

## 快速开始（换电脑后三步跑通）

```bash
# 1. 创建虚拟环境（只需第一次）
cd 03-Projects/PythonCode
python -m venv .venv

# 2. 激活 + 装依赖
.venv\Scripts\activate        # Windows
pip install -r PytestProject/requirements.txt

# 3. 运行测试
cd PytestProject
pytest
```

## 项目结构

```
PytestProject/
├── src/
│   └── my_module.py          # 被测试的业务模块
├── tests/
│   ├── conftest.py           # 共享 fixture + setup/teardown
│   ├── test_my_module.py     # 主测试（参数化/异常/fixture/类组织）
│   └── test_another.py       # 高级标记（skip/smoke/slow/xfail）
├── conftest.py               # 根级 conftest（预留）
├── pytest.ini                # Pytest 配置（markers/addopts）
├── requirements.txt          # 依赖清单
└── README.md                 # 本文件
```

## 常用命令

```bash
pytest                  # 全跑（-v --tb=short 已配好）
pytest -m smoke         # 只跑冒烟
pytest -m "not slow"    # 跳过低速
pytest -k "double"      # 按名称筛选
pytest -s               # 显示 print（看 setup/teardown 日志）
pytest --lf             # 只跑上次失败的
```

## 测试技能覆盖

| 技能 | 位置 |
|------|------|
| 基本 assert | test_inc / test_double_int |
| pytest.raises 异常断言 | test_zero_division |
| pytest.approx 浮点比较 | test_double_float / test_float_result |
| @parametrize 参数化（Ch03） | test_is_even（6组数据 + ids） |
| setup/teardown 四种作用域 | conftest.py + TestDemo 类 |
| fixture（autouse/yield） | db_mock / sample_numbers |
| 自定义 marker + -m 筛选（Ch04） | @pytest.mark.smoke / slow |
| skip / skipif / xfail | test_another.py |
| 用类组织测试 | TestDouble / TestSafeDivide / TestDemo |
