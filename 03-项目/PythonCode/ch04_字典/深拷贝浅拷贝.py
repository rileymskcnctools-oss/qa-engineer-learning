import copy

# 原始数据
originData = [[1,2],{"name":"Tom", "chars":["A","B"]}]

# 使用对象的copy()方法得到浅拷贝对象
copyData1 = originData.copy()
# 使用工厂方法获取浅拷贝对象
copyData2 = list(originData)
# 使用切片方式获取浅拷贝对象
copyData3 = originData[:]
# 使用 copy模块中的copy方法获取浅拷贝对象
copyData4 = copy.copy(originData)

# 拷贝成功的验证，内容相同，地址不同
# 查看所有对象内容
print(originData)
print(copyData1)
print(copyData2)
print(copyData3)
print(copyData4)
# 查看所有对象的址,
print(id(originData))
print(id(copyData1))
print(id(copyData2))
print(id(copyData3))
print(id(copyData4))

# 当修改任意对象时，其它对象都会受影响
copyData3[1]["chars"][1] = "BBB"

# 查看所有对象的数据
print(originData)
print(copyData1)
print(copyData2)
print(copyData3)
print(copyData4)
import copy

# 原始数据
originData = [[1,2],{"name":"Tom", "chars":["A","B"]}]

# 使用 copy模块中的deepcopy方法获取深拷贝对象
deepCopyData = copy.deepcopy(originData)

# 拷贝成功的验证，内容相同，地址不同
# 查看所有对象内容
print(originData)
print(deepCopyData)

# 查看所有对象的址,
print(id(originData))
print(id(deepCopyData))


# 当修改任意对象时，其它对象都不会受影响
originData[1]["chars"][1] = "BBB"

# 查看所有对象的数据
print(originData)
print(deepCopyData)
