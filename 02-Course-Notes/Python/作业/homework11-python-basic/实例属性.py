"""
简单动物园系统

功能：
1. 创建动物基类
2. 创建狗、猫、鸟子类
3. 使用继承和多态实现不同叫声
"""


# 动物基类

class Animal:

    # 构造方法
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 发声方法
    def make_sound(self):
        print("动物发出声音")
    # 展示动物信息
    def show_info(self):
        print(f"名字:{self.name}, 年龄:{self.age}")

# 狗类，继承Animal
class Dog(Animal):
    def make_sound(self):
        print("小狗：汪汪汪")


# 猫类，继承Animal
class Cat(Animal):

    def make_sound(self):
        print("小猫：喵喵喵")



# 鸟类，继承Animal

class Bird(Animal):
    def make_sound(self):
        print("小鸟：叽叽喳喳")

# 创建动物并调用方法

def animal_test():
    animals = [

        Dog("旺财",3),

        Cat("咪咪",2),

        Bird("小黄",1)

    ]


    for animal in animals:

        animal.show_info()

        animal.make_sound()

        print("----------------")

animal_test()