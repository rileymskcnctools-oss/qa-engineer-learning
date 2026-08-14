# len(l) 获取列表中元素的个数
# l=[1,2,3,4,5,3,21,6,8,2]
# print(len(l))
#
# # count(value) 在列表中统计参数 value 出现的次数
# print(l.count(3))
#
# # index(value, start, stop) 在列表中查找参数 value 第一次出现的下标位置
# print(l.index(3))
# print(l.index(3,5,10))

# append(value) 向列表最后追加元素
# l = []
# l.append(1)
# print(l)
# l.append(1)
# print(l)
# l.append(2)
# print(l)
#
l1 = [1,2,3]
l2 = ["a","b","c"]

# extend(iterable) 将一个可迭代对象的元素依次添加到列表最后
l1.append(l2)
print(l1)
l1.extend(l2)
print(l1)
l1.extend("456")
print(l1)
l1.extend(("A","B","C"))
print(l1)

# l = [1,2,3,4,5]

# # insert(index, value) 向列表指定下标位置插入一个元素
# l.insert(0, "A")
# print(l)
# l.insert(3, "B")
# print(l)
# l.insert(10, "C")
# print(l)
# l.insert(9, "D")
# print(l)

# del 可以使用 del 关键字结合索引来删除指定位置的元素 按索引删除
# l = [1,2,3,4,5,1,2,3]
# del l[0]
# print(l)
# del l[10]

# remove(value) 在列表中删除第一个指定的数据  按值删
# l = [1,2,3,4,5,1,2,3]
# l.remove(3)
# print(l)
# l.remove(33)

# pop(index) 从列表中取出并删除指定下标位置的元素，默认取出并删除最后一个元素
# l = [1,2,3,4,5,1,2,3]
# print(l.pop())
# print(l)
# print(l.pop(3))
# print(l)
# print(l.pop(10))


# clear() 清空列表
# l = [1,2,3,4,5,1,2,3]
# l.clear()
# print(l)
# l = ["a","abc","ab","A"]
# l.sort()
# print(l)
# l = ["a","abc","ab","A"]
# l.sort(reverse=True)
# print(l)