# # a = 10
# # b = 20
# # c = a + b
# # print("a + b 的值为：", c)
# # print(9%2)
# # s1 = "hello"
# # s2 = "hogwarts"
# # res = s1 + s2
# # print("字符串拼接结果为：", res)
#
# # print(2 ** 10)
# # print("hello" * 3) 乘法运算符也可用作字符串拼接
# # print(100//11)
# # print(200//3)
# a, b, c = 1, 2, 3
# print(a, b, c)
#
# a = 10
# a += 20 # 相当于表达式  a = a + 20
# print(a)
#
# a = 10
# a *= 20 # 相当于表达式  a = a * 20
# print(a)
#
# a = 10
# a /= 20 # 相当于表达式  a = a / 20
# print(a)
#
# a = 10
# a //= 20 # 相当于表达式  a = a // 20
# print(a)
#
# a = 10
# a %= 20 # 相当于表达式  a = a % 20
# print(a)
#
# a = 10
# a **= 20 # 相当于表达式  a = a ** 20
# print(a)
#
# n = 2
# # 该表达式结果为 14， 并不是10
# # 如果一定要展开，可以理解展开后为 n = n * ( 3 + 4)
# n *= 3 + 4
# print(n)

# print(3 > 2 and 2 > 1)
# print(3 < 2 and 2 > 1)
# print(3 < 2 and 2 < 1)
# print(1 < 2 and "H" + "W")

result = True and print("Hello, World!1")  # 第一个操作数为True，不能确定后续都为真，所以print语句会执行
print(result)   # 输出 None，print语句的返回值为None

result = False or print("Hello, World!2")  # 第一个操作数为False，不能确定后续都为假，所以print语句会执行
print(result)  # 输出 None，print语句的返回值为None

result = False and 1/0  # 第一个操作数为False，已经可以确认整个表达式的结果，虽然表达式有除0错误，但并不会执行
print(result)  # 结果为False

result = True or 1/0  # 第一个操作数为True，已经可以确认整个表达式的结果，虽然表达式有除0错误，但并不会执行
print(result)  # 结果为True
