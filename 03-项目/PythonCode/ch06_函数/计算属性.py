class Person:
    def __init__(self, name):
        self._name = name

    @property
    def username(self):              # getter —— 像属性一样读
        return self._name

    @username.setter
    def username(self, name):        # setter —— 像属性一样写
        if name.isalpha():
            self._name = name

tom = Person("tom")
print(tom.username)        # tom —— 像属性一样访问，实际调用了 getter
tom.username = "Tom"       # 像属性一样赋值，实际调用了 setter
print(tom.username)        # Tom