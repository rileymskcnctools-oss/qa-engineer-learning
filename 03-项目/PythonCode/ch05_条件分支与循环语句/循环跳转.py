# 持续输入直到用户输入 bye
# data = []
# while True:
#     d = input("请输入数据：")
#     if d == "bye":
#         break
#     data.append(d)
#     print(data)
# print("程序执行结束！")
# print(data)


# for i in range(3):
#     for j in range(5):
#         print("Hello", j)
#         if j == 5:
#             break


# 使用 continue
for i in range(10):
    print("*" * 10)
    print("i=", i)
    if i % 3 == 0:
        continue      # 跳过 print("i*10=...")
    print("i*10= ", i * 10)

# 等价改写：用条件反转替代 continue
for i in range(10):
    print("*" * 10)
    print("i=", i)
    if i % 3 != 0:    # 条件取反
        print("i*10= ", i * 10)
