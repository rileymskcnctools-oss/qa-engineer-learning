# class Student:
#     def __init__(self):
#         print("Init Run ...")
#         self.name = "Tom"
#         self.age = 22
#
# s1 = Student()  # 输出: Init Run ...
# s2 = Student()  # 输出: Init Run ...

class Student:
    def __init__(self, name, age):
        self.name = name    # 左边的 self.name 是属性名，右边的 name 是参数
        self.age = age

s1 = Student("Tom", 22)
s2 = Student("Jack", 23)

print(s1.name)  # Tom
print(s2.name)  # Jack

print(s1)  # 类型 对象 地址
print(s2)  # 类型 对象 地址