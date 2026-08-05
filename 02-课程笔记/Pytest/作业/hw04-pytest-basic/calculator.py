class Calculator:

    # 加法
    def add(self, a, b):
        return a + b


    # 减法
    def subtract(self, a, b):
        return a - b


    # 乘法
    def multiply(self, a, b):
        return a * b


    # 除法
    def divide(self, a, b):

        if b == 0:
            raise ValueError("除数不能为0")

        return a / b