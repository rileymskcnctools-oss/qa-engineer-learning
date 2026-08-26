# def show():
#     a = 10          # 局部变量：show() 被调用时创建
#     print(a)        # 函数内部可以访问
#
# show()              # 输出 10
# # print(a)          # NameError: name 'a' is not defined


# m = 20          # 全局变量
#
# def show1():
#     print("show1:", m)   # 读取全局变量 ✓
#
# def show2():
#     print("show2:", m)   # 读取全局变量 ✓
#
# print(m)        # 20
# show1()         # show1: 20
# show2()         # show2: 20



# m = 10           # 全局变量
#
# def show():
#     m = "ABC"    # 创建局部变量 m，屏蔽全局 m
#     print("show:", m)  # 用局部 m
#
# print(m)          # 10（全局）
# show()            # show: ABC（局部屏蔽全局）
# print(m)          # 10（全局未被修改）


m = 10

def show():
    global m          # 声明 m 是全局变量
    m = "ABC"         # 修改全局 m
    print("show:", m)

print(m)              # 10
show()                # show: ABC
print(m)              # ABC（全局被修改了！）