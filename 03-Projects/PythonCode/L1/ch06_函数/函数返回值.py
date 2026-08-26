# # return 结束函数
# def show():
#     print("循环前输出内容")
#     for i in range(10):
#         print(i)
#         if i == 2:
#             return
#     print("循环后输出内容")
#
# print("函数调用前输出内容")
# show()
# print("函数调用后输出内容")



# def getTwoNum():
#     a = int(input("请输入第一个数字："))
#     b = int(input("请输入第二个数字："))
#     return a, b
#
# m, n = getTwoNum()
# print(m, n)



# def getTwoNum():
#     a = int(input("请输入第一个数字："))
#     b = int(input("请输入第二个数字："))
#     return a, b
#
# result = getTwoNum()
# print(result)
# print(type(result))


def getTwoNum():
    a = int(input("请输入第一个数字："))
    b = int(input("请输入第二个数字："))
    return a, b        # 自动组包为 (a, b) 元组

result = getTwoNum()
print(result)          # (3, 5)  一个元组
print(type(result))    # <class 'tuple'>