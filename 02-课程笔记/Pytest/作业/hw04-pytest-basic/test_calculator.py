import pytest
from calculator import Calculator

# =========================
# 模块级 setup / teardown
# =========================

def setup_module():

    print("\nCalculator模块测试开始")


def teardown_module():

    print("\nCalculator模块测试结束")

# =========================
# 测试类
# =========================

class TestCalculator:

    # 类级setup
    @classmethod
    def setup_class(cls):

        print("\n创建Calculator实例")
        # 创建 TestCalculator类属性calculator，保存Calculator()实例对象
        cls.calculator = Calculator()


    # 类级teardown
    @classmethod
    def teardown_class(cls):

        print("\nCalculator测试类结束")


    # 方法级setup
    def setup_method(self):

        print("\n测试方法开始")


    # 方法级teardown
    def teardown_method(self):

        print("\n测试方法结束")


    # =========================
    # 加法参数化
    # =========================

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (1, 2, 3),
            (10, 20, 30),
            (-1, 5, 4)
        ]
    )
    def test_add(self, a, b, expected):
        # pytest 执行时test_add（），会创建当前类的实例对象test = TestCalculator(),这里的self--TestCalculator实例
        # 执行这句代码时，python 会先查看test对象有没有calculator属性，若无，再查看TestCalculator类有无calculator属性
        result = self.calculator.add(a, b)
        assert result == expected

    # =========================
    # 减法参数化
    # =========================

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (1, 2, -1),
            (10, 20, -10),
            (10, 5, 5)
        ]
    )
    def test_subtract(self, a, b, expected):

        result = self.calculator.subtract(a, b)

        assert result == expected


    # =========================
    # 乘法参数化
    # =========================

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (1, 2, 2),
            (10, 20, 200),
            (-1, 5, -5)
        ]
    )
    def test_multiply(self, a, b, expected):

        result = self.calculator.multiply(a, b)

        assert result == expected


    # =========================
    # 除法参数化
    # =========================

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (4, 2, 2),
            (20, 5, 4),
            (-9, -3, 3)
        ]
    )
    def test_divide(self, a, b, expected):

        result = self.calculator.divide(a, b)

        assert result == expected


    # =========================
    # 异常测试
    # =========================

    def test_divide_zero(self):

        with pytest.raises(ValueError):

            self.calculator.divide(10, 0)