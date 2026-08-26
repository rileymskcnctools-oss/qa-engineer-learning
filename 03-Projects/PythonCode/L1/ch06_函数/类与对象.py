# class Plane(object):
#     def flying(self, hour):
#         print(f"飞机已飞行{hour} 小时。。。")
#
# # 实例化两个对象
# airPlane1 = Plane()
# airPlane2 = Plane()

# # 不同对象调用同一个方法
# airPlane1.flying(3)    # 飞机已飞行3 小时。。。
# airPlane1.flying(5)    # 飞机已飞行5 小时。。。
# airPlane2.flying(3)    # 飞机已飞行3 小时。。。

class Student:
    pass
# 实例对象
s1 = Student()
s2 = Student()

# 为实例对象s1动态绑定属性
s1.name = "Tom"
s1.age = 22
# 访问实例对象s1的属性
print(s1.name)
print(s1.age)

# 输出什么？
print(s2.name)
print(s2.age)