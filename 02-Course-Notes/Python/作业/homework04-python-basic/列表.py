"""
•统计当前学生总人数。
•添加两名新学生："Mark"（87分）和"Eva"（80分)。
• 删除第2位学生的记录。
"""

students = [["Anna", 90], ["Tom", 78], ["Jerry", 85], ["Lucy", 92]]

print(len(students))
students.extend([["Mark", 87],["Eva", 80]])
print(students)
students.remove(students[1])
print(students)