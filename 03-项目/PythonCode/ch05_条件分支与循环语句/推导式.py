# 简单的元组推导式
# t1 = (x for x in range(1,10))
# for x in t1:
#     print(x)
# # 生成128位ASCII码元组
# t2 = (chr(x) for x in range(128))
# # 生成100以内能被7整除所有数字的元组
# t3 = (x for x in range(100) if x%7==0)
# # 生成99乘法表结果元组
# t4 = (x*y for x in range(1,10) for y in range(1, x+1))
# words = ["apple", "banana", "cherry"]
# upper_words = (word.upper() for word in words)

# 基本：生成 1~9
# L1=[x for x in range(1, 10)]
#
# # 带过滤：100 以内被 7 整除的数
# L2=[x for x in range(100) if x % 7 == 0]
# for i in L2:
#     print(i)
# # 带转换：字符串转大写
# words = ["apple", "banana", "cherry"]
# L3=[word.upper() for word in words]
# for word in L3:
#     print(word)
# 嵌套：九九乘法表所有结果
# L4=[x * y for x in range(1, 10) for y in range(1, x + 1)]
# for i in L4:
#     print(i)


names = ['Bob', 'Tom', 'Alice', 'Jerry', 'Wendy', 'Smith']
# 名字作键，长度作值
d1={name: len(name) for name in names}
# {'Bob': 3, 'Tom': 3, 'Alice': 5, 'Jerry': 5, 'Wendy': 5, 'Smith': 5}
for k,v in d1.items():
    print(k,v)

print("*"*20)
# 带过滤：只保留长度 > 3 的名字
d2={name: len(name) for name in names if len(name) > 3}
for k,v in d2.items():
    print(k,v)

print("=" * 20)
data = ['Bob', '123', 'Tom', 'ab123', 'alice', '123abc', 'Jerry', '456', 'Wendy', '554', 'Smith']
# 筛选列表中的纯数字字符串
newset = {n for n in data if n.isdigit()}
for i in newset:
    print(i)
# {'123', '456', '554'}

