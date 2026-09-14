
"""
编写程序，让用户输入两个整数start和end,然后输出这两个整数之间的一个随机数。
要求考虑用户输入不是整数的情况，以及start>end的情况。根据实际情况进行适当提示或输出。
"""


import random

try:
    # 提示用户输入起始值和结束值
    start = int(input("请输入一个整数作为起始值： "))
    end = int(input("请输入一个整数作为结束值： "))

    # 检查起始值和结束值的关系
    if start > end:
        raise ValueError("起始值不能大于结束值，请重新输入。")

    # 生成随机数并输出
    random_num = random.randint(start, end)
    print("随机数为：", random_num)

except ValueError as ve:
    # 捕获值错误异常并输出错误信息
    print(ve)

except Exception as e:
    # 捕获其他异常并输出通用的错误信息
    print("发生了一个错误：", e)
