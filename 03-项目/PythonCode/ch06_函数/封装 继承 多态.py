class A(object):
    def __init__(self):
        # 公有属性
        self.a = 10
        # 保护属性
        self._b = 20
        # 私有属性
        self.__c = 30

    # 公有方法
    def show(self):
        # 在类中使用公有属性
        print(f"A: {self.a}")
        # 在类中使用保护属性
        print(f"B: {self._b}")
        # 在类中使用私有属性
        print(f"C: {self.__c}")
        # 在类中使用保护权限的方法
        self._display()
        # 在类中使用私有方法
        self.__info()


    # 保护权限的方法
    def _display(self):
        print(f"B: {self._b}")

    # 私有权限的方法
    def __info(self):
        # 在类中使用私有属性
        print(self.__c)
obj = A()
# 在类外使用公有属性
print(obj.a)
# 在类外无法使用保护仅限的属性（不建议这样使用）
print(obj._b)
# 在类外使用私有属性，访问失败
# print(obj.__c)
# 在类外使用公有方法
obj.show()
# 在类外无法使用保护权限的方法（不建议这样使用）
obj._display()
# 在类外访问私有方法，访问失败
# obj.__info()
