class Calc:
    @staticmethod
    def add(n1, n2):
        return n1 + n2

    @staticmethod
    def sub(n1, n2):
        return n1 - n2

    @staticmethod
    def mul(n1, n2):
        return n1 * n2

    @staticmethod
    def div(n1, n2):
        return n1 / n2


print(Calc.add(10, 20))
print(Calc.sub(10, 20))
print(Calc.mul(10, 20))
print(Calc.div(10, 20))
