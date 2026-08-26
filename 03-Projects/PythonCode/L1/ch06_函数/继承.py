# class A(object):
#     # A 继承自 object 根类
#     def show(self):
#         print("父类A的方法")
#
# class B(A):
#     # B类 继承自 A类
#     def display(self):
#         print("子类B的方法")
#
# b = B()
# # 子类对象使用自己的方法
# b.display()
# # 子类对象使用父类的方法，如果父类有没有该方法则继续向上查找，直到根类
# b.show()

# 方法重写
# class A:
#     def show(self):
#         print("父类A的方法")
#
# class B(A):
#     def show(self):              # 重写父类方法
#         super().show()           # 调用父类的 show()
#         print("子类B的方法")
#
# b = B()
# b.show()
# # 父类A的方法
# # 子类B的方法

# class FA:
#     def fa_show(self):
#         print("FA Show")
#
# class FB:
#     def fb_show(self):
#         print("FB Show")
#
# class S(FA, FB):            # 同时继承 FA 和 FB
#     def s_show(self):
#         print("S Show")
#
# s = S()
# s.fa_show()   # ✅
# s.fb_show()   # ✅

class FA:
    def show(self):
        print("FA")

class FB:
    def show(self):
        print("FB")

class S(FB, FA):     # FB 在左，优先查找
    pass

s = S()
s.show()             # "FB" —— 按书写顺序，FB 优先
