"""
创建一个学生成绩管理系统，使用字典存储每个学生的名字和对应的成绩。
1. 输出所有学生姓名和成绩
2. 添加新学生及其成绩
3. 更新学生成绩
4. 删除学生记录
5. 查找某个学生成绩
"""


# 初始化学生成绩字典

student_scores = {
    "Anna": 90,
    "Tom": 78,
    "Jerry": 85,
    "Lucy": 92
}


# 1. 输出所有学生姓名和成绩

print("所有学生成绩:")

for name, score in student_scores.items():

    print(f"{name}: {score}")



# 2. 添加学生

student_scores["riley"] = 99

print("\n添加学生后:")

print(student_scores)



# 3. 更新学生成绩

student_scores.update({
    "Anna": 95
})

print("\n更新Anna成绩后:")

print(student_scores)



# 4. 删除学生

del student_scores["Tom"]

print("\n删除Tom后:")

print(student_scores)



# 5. 查询学生成绩

name = "Jerry"

score = student_scores.get(name)

print(f"\n{name}的成绩是:{score}")