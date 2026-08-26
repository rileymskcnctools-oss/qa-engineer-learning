# name = "Alice"
# age = 25
# message = "My name is {0}--, and I am {1}-- years old.".format(name, age)
# print(message)
# 输出：My name is Alice, and I am 25 years old.
#
# name = "Alice"
# age = 25
# message = "My name is {name}, and I am {age} years old.".format(name=name, age=age)
# print(message)
# # 输出：My name is Alice, and I am 25 years old.

# pi = 3.141592653589793
# formatted_pi = "The value of pi is approximately {:.7f}".format(pi)
# print(formatted_pi)
# 输出：The value of pi is approximately 3.14

# # 字符串对齐
# print("The value is ljust: |{:5}|".format("abc"))
# print("The value is ljust: |{:<5}|".format("abc"))
# print("The value is rjust: |{:>5}|".format("abc"))
# # 数字对齐
# print("The value is rjust: |{:5}|".format(11))
# print("The value is rjust: |{:>5}|".format(11))
# print("The value is ljust: |{:<5}|".format(11))

name = "Alice"
age = 25
greeting = f"{'Hello' if age < 30 else 'Hi'} {name.upper()}"
print(greeting)
# 输出：Hello ALICE

