class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        print(f"Name: {self.name}")
        if self.age >= 18:
            print("已成年")
        else:
            print("未成年")

