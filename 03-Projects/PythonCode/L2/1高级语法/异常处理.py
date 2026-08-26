file = open("data.txt","r")
try:
    # 写入数据时可能会有问题
    file.write("写入的数据")
except IOError as err:
    print("文件不能写入", err)

file.close()


# file = open("data.txt","r")
# try:
#     # 写入数据时可能会有问题
#     # file.write("写入的数据")
#     # print(a)
#     print(3 / 0)
#     # print([][10])
#     print("hello" + 100)
# except IOError as err:
#     print("文件不能写入", err)
# except NameError:
#     print("标识符没有定义")
# except ZeroDivisionError:
#     print("除数不能为0")
# except IndexError:
#     print("下标越界了")
# except Exception:
#     print("程序运行出错，请检查代码")

# Python 使用 else 在处理在代码无异常时的后续操作
try:
    n = input("请输入一个数字:")
    num = int(n)
except Exception:
    print("元素无法转换为数字")
else:
    print("转换后成功", num)    # 只有转换成功才执行



