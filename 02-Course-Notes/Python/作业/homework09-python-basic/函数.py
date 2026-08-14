def func2():

    # 输入字符序列
    data = input("请输入字符序列：")

    # 创建统计字典
    count = {
        "大写字母": 0,
        "小写字母": 0,
        "数字": 0,
        "其他字符": 0
    }

    # 遍历每个字符
    for c in list(data):
        # 判断是否大写字母

        if c.isupper():

            count["大写字母"] += 1

        # 判断是否小写字母

        elif c.islower():
            count["小写字母"] += 1

        # 判断是否数字

        elif c.isdigit():
            count["数字"] += 1

        # 其他字符

        else:
            count["其他字符"] += 1

    # 输出统计结果
    print(count)

# 调用函数
func2()