"""
猜数字游戏

需求：
1. 随机生成1-100之间的目标数字
2. 玩家输入猜测数字
3. 根据结果提示猜大了或者猜小了
4. 猜中后显示猜测次数
"""

import random

# 随机生成目标数字
target_num = random.randint(1, 100)


# 记录猜测次数
count = 0

print("欢迎进入猜数字游戏！")
print("请输入1-100之间的数字")

while True:
    # 输入玩家猜测数字
    guess_num = int(input("请输入你猜的数字："))

    # 猜测次数+1
    count += 1

    # 判断大小
    if guess_num > target_num:
        print("猜大了，请继续猜")

    elif guess_num < target_num:
        print("猜小了，请继续猜")

    else:

        print("恭喜你，猜对了！")
        print(f"你一共猜了{count}次")

        break