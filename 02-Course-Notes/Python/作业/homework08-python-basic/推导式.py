"""
学生成绩管理系统

功能：
1. 使用列表推导式筛选及格学生
2. 使用字典推导式生成学生成绩字典
"""

# 原始学生成绩数据
# 使用列表存储，每个学生是一个字典

students = [
    {"name": "Anna", "score": 90},
    {"name": "Tom", "score": 55},
    {"name": "Jerry", "score": 85},
    {"name": "Lucy", "score": 40},
    {"name": "Riley", "score": 75}
]
# 1. 使用列表推导式筛选及格学生
passed_students = [
    student
    for student in students
    if student["score"] >= 60
]
# print(passed_students)
print("及格学生：")
for student in passed_students:
    print(student)

# 2. 使用字典推导式生成学生成绩字典

student_scores = {
    student["name"]: student["score"]  # k , v
    for student in students
}
print("\n学生成绩字典：")
print(student_scores)