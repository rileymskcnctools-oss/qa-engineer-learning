
# for 循环嵌套遍历可迭代对象--- 二维列表
# data = [
#     [1,2,3,4,5,6,7,8,9],
#     ["A","B","C","D","E"],
#     ["Hello","World","Python","Hogwarts"]
# ]
# for item in data:
#     for el in item:
#         print(el)

# while 循环遍历二维列表
# data = [
#     [1,2,3,4,5,6,7,8,9],
#     ["A","B","C","D","E"],
#     ["Hello","World","Python","Hogwarts"]
# ]
# l1 = len(data)
# i = 0
# while i < l1:
#     item = data[i]
#     l2 = len(item)
#     j = 0
#     while(j < l2):
#         el = item[j]
#         print(el)
#         j += 1
#     i += 1

for i in range(1,10):
    for j in range(1,i+1):
        print(f"{i}*{j}={i*j}",end="\t")
    print()
