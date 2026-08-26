# len() 用来获取参数字符串的字符个数
# length = len("Hello")
# print(length)
# length = len("Hello World")
# print(length)

# count() 返回 str 在 string 里面出现的次数
# s = "hello world hello Python"
# n = s.count("o")
# print(n)
# n = s.count("O")
# print(n)
# n = s.count("or")
# print(n)
# n = s.count("o",10,50)
# print(n)

# index() 检测 sub 是否包含在 string 中，如果 start 和 end 指定范围，则检查是否包含在指定范围内，
# 如果是返回开始的索引值，否则抛出一个异常
# s = "Hello"
# print(s.index("l"))
# print(s.index("l",0,3)) # 区间使用下标位置，左闭右开区间
# print(s.index("k"))


# s = "Hello"
# print(s.rindex("l"))
# print(s.rindex("H",0,3))
# print(s.rindex("k"))

# s = "Hello World"
# print(s.find("ll"))
# print(s.find("lll",0,10))
# s = "Hello World"
# print(s.rfind("l"))
# print(s.rfind("l",0,3))
# print(s.rfind("k"))

s = "Hello Hello Hello"
print(s.replace("ll","LL"))
print(s.replace("l","L",4))