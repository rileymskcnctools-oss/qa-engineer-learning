# def info(name, age, gender):
#     print(f"我叫{name}, 年龄{age}岁，性别{gender}")
#
# # "Tom", 22, "男" 为实参

# 位置参数
# def printMsg(n, msg):
#     for i in range(n):
#         print(f'第{i+1}次输出{msg}')
#
# printMsg(5, "HAHA")         # 正确
# # printMsg("Hogwarts", 5)         错误：字符串传给了 n，int 传给了 msg


# 关键字参数
# def printMsg(n, msg):
#     for i in range(n):
#         print(f'第{i+1}次输出{msg}')
#
# printMsg(n=5, msg="Hogwarts")        # 关键字参数
# printMsg(msg="Hogwarts", n=5)        # 顺序无所谓

# 在定义函数时，形参可以定义变量一样进行赋值，这个值就是默认该参数的默认值
# def my_power(m, n=2):
#     return m ** n
#
# print(my_power(2, 3))   # 8, n=3
# print(my_power(2))      # 4, n 用默认值 2



# 不确定个数数字求和
def my_sum(*args):
    print(args)
    print(*args)
    print(type(args))
    s = 0
    for i in args:
        s += i

    print(s)
    print("*" * 10)

my_sum(1,2,3)
my_sum(1,2,3,4)
my_sum(1,2,3,4,5)
my_sum(1,2,3,4,5,6)


# `**kwargs` 接收任意数量的**关键字参数**，打包成一个**字典**
def print_info(**kwargs):
    print(kwargs)       # {'Tom': 18, 'Jim': 20}
    print(type(kwargs)) # <class 'dict'>
    for k, v in kwargs.items():
        print(k, v)

print_info(Tom=18, Jim=20, Lily=12)
print_info(name="tom", age=22, gender="male", address="BeiJing")