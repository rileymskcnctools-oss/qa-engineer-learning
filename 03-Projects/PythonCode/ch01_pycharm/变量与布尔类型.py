# 定义变量
# name = "霍格沃兹"       # str
# age = 18                # int
# score = 98.5            # float
# is_pass = True          # bool
#
# # 动态类型：同一变量可以换成不同类型
# name = "霍格沃兹"
# name = 123              # 现在 name 是 int 了
# print(type(name))       # <class 'int'>


# print(id("霍格沃兹"))
#
# name = "霍格沃兹"
# print(id(name))
#
# school = "霍格沃兹"
# print(id(school))

# 1. 条件判断产生布尔值
# x = 5
# y = 10
# print(x < y)    # True
# print(x > y)    # False
# print(x == 5)   # True
#
# # 2. 状态标记
# is_logged_in = False       # 初始未登录
# # ... 执行登录 ...
# is_logged_in = True        # 登录成功，更新状态
#
# # 3. 测试断言 = 就是在判断布尔值
# actual = 200
# expected = 200
# print(actual == expected)  # True → 测试通过

# 测试中常见：检查接口返回数据是否为空

response_data = []          # 接口返回了空列表

if response_data:
    print("有数据，开始验证")
else:
    print("无数据，跳过验证")   # ← 会走这里

# 等同于：
if len(response_data) > 0:  # 冗长
    ...
if response_data:           # 简洁（Python 风格）
    ...