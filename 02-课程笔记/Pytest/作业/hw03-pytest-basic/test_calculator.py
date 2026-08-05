from calculator import Calculator


# 模块级 setup
def setup_module():

    print("Calculator模块测试开始")


# 模块级 teardown
def teardown_module():

    print("Calculator模块测试结束")


class TestCalculator:


    # 类级setup
    @classmethod
    def setup_class(cls):

        print("创建Calculator实例")

        cls.calculator = Calculator()


    # 类级teardown
    @classmethod
    def teardown_class(cls):

        print("Calculator测试类结束")


    # 方法级setup
    def setup_method(self):

        print("测试方法开始")


    # 方法级teardown
    def teardown_method(self):

        print("测试方法结束")


    def test_add(self):

        result = self.calculator.add(1,2)

        assert result == 3


    def test_subtract(self):

        result = self.calculator.subtract(2,1)

        assert result == 1


    def test_multiply(self):

        result = self.calculator.multiply(2,3)

        assert result == 6


    def test_divide(self):

        result = self.calculator.divide(6,2)

        assert result == 3