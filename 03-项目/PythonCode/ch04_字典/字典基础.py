#  # 可哈希数据
# print(hash(123))     数字
# print(hash("abc"))   字符串
# print(hash((1,2,3)))  元组
#
# # 不可哈希数据
# print(hash([1,2,3]))
# print(hash((1,2,[3])))

# d1 = {}
# d2 = {"name": "Alice", "age": 25, "gender": "female"}

# stu = {"name":"Tom", "age": 23, "gender":"male"}
# print(stu["name"])
# print(stu["age"])
# k = "gender"
# print(stu[k])

# 构造方法定义字典
# d1 = dict(one=1, two=2, three=3)
# print(d1)
# d2 = dict([('two', 2), ('one', 1), ('three', 3)])
# print(d2)
# d3 = dict((('two', 2), ('one', 1), ('three', 3)))
# print(d3)
# d4 = dict([('two', 2), ['one', 1], ('three', 3)])
# print(d4)
# d5 = dict({'one': 1, 'two': 2, 'three': 3})
# print(d5)
# d6 = dict({'one': 1, 'three': 3}, two=2)
# print(d6)
# d7 = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
# print(d7)


# 字典元素添加与修改
stu = {"name":"Tom", "age": 23, "gender":"male"}
print(stu)
# 添加新元素
stu["address"] = "BeiJing"
print(stu)
# 修改数据
stu["name"] = "Jack"
stu["address"] = "ShangHai"
print(stu)
# # 删除元素
# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# print(stu)
# del stu['age']
# print(stu)
# del stu['address']
# print(stu)