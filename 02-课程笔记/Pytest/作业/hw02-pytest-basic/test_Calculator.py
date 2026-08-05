from calculator import Calculator

class TestCalculator:

    def test_add(self):
        result = Calculator.add(1,2)
        assert result == 3

    def test_sub(self):
        result= Calculator.subtract(1,2)
        assert result == -1

    def test_multiply(self):
        result = Calculator.multiply(1,2)
        assert result == 2

    def test_divide(self):
        result = Calculator.divide(2,1)
        assert result == 2
