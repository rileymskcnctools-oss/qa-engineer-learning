from time import sleep


def show():
    odds = []  # 用列表收集奇数
    for i in range(10):
        if i % 2 != 0:
            print(f"{i}是奇数")
            odds.append(i)
    print(f"奇数之和: {sum(odds)}")

show()
print(1+5)


