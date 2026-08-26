# 字典数据获取类操作

# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# ks = stu.keys()
# print(ks)
#
# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# ks = stu.values()
# print(ks)
#
# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# ks = stu.items()
# print(ks)


# get(key, default) 用来获取 key 对应的值，如果指定的 key 不存在，则返回默认值
# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# # print(stu["name"])
# # print(stu["hobby"])
# print(stu.get("name"))
# print(stu.get("hobby"))
# print(stu.get("hobby","无数据"))

# 字典添加更新类操作
# setdefault(key,default) 给一个不存在的 key 添加一个默认值并将该键值对保存到字典中。
# stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
# stu.setdefault("hobby1")
# print(stu)
# stu.setdefault("hobby2", "无")
# print(stu)

#key准备好，值还没有，很少用
# ks = ("name", "age", "gender")
# s1 = dict.fromkeys(ks)
# print(s1)
#
# s2 = dict.fromkeys(ks,"无")
# print(s2)

# update(dict | iterable) 使用参数中的数据更新当前字典
# 更新目标数据是一个字典
stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
newStu = {"name":"Jack","hobby":"eat"}
stu.update(newStu)
print(stu)
# 更新目标数据是一个可迭代对象
stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
newStu = (("name","Rose"),["hobby","play"])
stu.update(newStu)
print(stu)

# popitem() 用来获取并删除字典中的最后一个键值对，返回一个元组
stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
v = stu.popitem()
print(v)
print(stu)
print({}.popitem())
# pop(key) 用于获取并删除字典中指定 key 对应的键值对
stu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}
v = stu.pop("name")
print(v)
print(stu)
# clear() 清空字典中所有的键值对元素
tu = {'name': 'Tom', 'age': 23, 'gender': 'male', 'address': 'BeiJing'}

print(stu)
stu.clear()
print(stu)