# 保存结果的变量
result = 1
# 循环控制变量
n = 2
# 开始循环
while n <= 10:
    # 计算乘积
    result *= n
    # 改变循环变量向结束条件趋近
    n += 1

# 输出结果
print("1~10的乘积为：", result)



password = "password" # 设置正确的密码
input_password = ""

while input_password != password:
    input_password = input("请输入密码: ")

print("密码正确，登录成功！")


# 循环变量实始化
n = 1
# 循环条件
while n<=100:
    # 数字对7求模为0，则表示该数字是7的倍数
    # 将数字转换为字符串类型，使用成员运算符判断字符7是否在字符串中，检查包含关系
    if n % 7 == 0 or "7" in str(n): # 强制类型转换
        # 输出满足条件的数字
        print(n)
    # 改变循环变量趋近于结束条件
    n += 1
