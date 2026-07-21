"""
测试 my_module.py 中的函数

覆盖：
- 基本 assert
- pytest.raises 异常断言
- setup/teardown（继承自 test_setup.py）
- fixture 使用
- @pytest.mark.parametrize 参数化（Ch03）
- 自定义 marker（Ch04）
"""

import pytest
from src.my_module import inc, double, is_even, safe_divide


# ============================================================
# inc 测试（从 test_demo.py 移植）
# ============================================================
def test_inc():
    """原始用例：inc(4) == 5"""
    assert inc(4) == 5


def test_inc_negative():
    """补充：负数"""
    assert inc(-1) == 0


# ============================================================
# double 测试
# ============================================================
class TestDouble:
    """用类组织 double 相关测试"""

    @pytest.mark.smoke
    def test_double_int(self):
        assert double(1) == 2

    @pytest.mark.smoke
    def test_double_zero(self):
        assert double(0) == 0

    def test_double_negative(self):
        assert double(-1) == -2

    def test_double_float(self):
        assert double(0.1) == pytest.approx(0.2)


# ============================================================
# is_even 测试（演示参数化 — Ch03 知识）
# ============================================================
@pytest.mark.parametrize(
    "n, expected",
    [(2, True), (4, True), (0, True), (1, False), (3, False), (-2, True)],
    ids=["2偶数", "4偶数", "0偶数", "1奇数", "3奇数", "-2偶数"],
)
def test_is_even(n, expected):
    """参数化：6 组数据覆盖正/负/零"""
    assert is_even(n) == expected


# ============================================================
# safe_divide 测试（演示异常断言）
# ============================================================
class TestSafeDivide:
    def test_normal(self, sample_numbers):
        """使用 fixture 提供的数据"""
        assert safe_divide(sample_numbers["a"], sample_numbers["b"]) == 5.0

    def test_zero_division(self):
        """除 0 抛异常"""
        with pytest.raises(ValueError, match="除数不能为0"):
            safe_divide(10, 0)

    def test_float_result(self):
        """浮点结果"""
        assert safe_divide(1, 3) == pytest.approx(0.333333, rel=1e-5)


# ============================================================
# setup/teardown 验证（从 test_setup.py 移植）
# ============================================================
class TestDemo:
    """用类演示 setup/teardown"""

    def setup_class(self):
        print("\n>>> TestDemo setup_class：类开始前")

    def teardown_class(self):
        print(">>> TestDemo teardown_class：类结束后")

    def setup_method(self):
        print("  > setup_method：每个方法前")

    def teardown_method(self):
        print("  > teardown_method：每个方法后")

    def test_method1(self):
        assert True

    def test_method2(self):
        assert True


# ============================================================
# fixture db_mock 演示
# ============================================================
def test_with_db_mock(db_mock):
    """使用 db_mock fixture — 自动 setup/teardown"""
    assert db_mock == "db_connection"
