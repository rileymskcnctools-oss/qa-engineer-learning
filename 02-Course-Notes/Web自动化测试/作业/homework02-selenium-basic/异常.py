import random

try:
    start = int(input("请输入start："))
    end = int(input("请输入end："))

    if start > end:
        print("输入错误：start不能大于end")
    else:
        random_num = random.randint(start, end)
        print(f"{start}和{end}之间的随机数是：{random_num}")

except ValueError:
    print("输入错误：请输入整数！")