import random

try:
    start = int(input("请输入start:"))
    end = int(input("请输入end:"))

    if start > end:
        print("start不能大于end")

    else:
        num = random.randint(start, end)
        print(f"随机数是:{num}")

except ValueError:
    print("输入错误，请输入整数：")