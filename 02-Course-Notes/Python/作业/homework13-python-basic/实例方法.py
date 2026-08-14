"""
课程管理系统

功能：
1. Course类封装课程信息
2. 私有属性name和credit
3. 提供设置和获取方法
4. 实现课程添加、删除、查看
"""
# 创建课程类

class Course:

    def __init__(self, name, credit):

        # 私有属性
        self.__name = name
        self.__credit = credit

    # 设置课程名称
    def set_name(self, name):
        self.__name = name

    # 获取课程名称
    def get_name(self):
        return self.__name

    # 设置课程学分
    def set_credit(self, credit):
        self.__credit = credit

    # 获取课程学分
    def get_credit(self):
        return self.__credit

    # 显示课程信息
    def show_info(self):
        print(f"课程名称:{self.__name}, 学分:{self.__credit}")

# 课程管理系统
class CourseManager:
    def __init__(self):
        # 保存课程列表
        self.courses = []

    # 添加课程,course是课程对象
    def add_course(self, course):
        self.courses.append(course)
        print(f"{course.get_name()} 添加成功")

    # 删除课程
    def delete_course(self, name):
        for course in self.courses:
            if course.get_name() == name:
                self.courses.remove(course)
                print(f"{name} 删除成功")
                return
        print("课程不存在")

    # 查看所有课程
    def show_courses(self):
        print("当前课程列表:")
        for course in self.courses:
            course.show_info()

# 测试
manager = CourseManager()

# 创建课程对象
course1 = Course("Python程序设计", 3)
course2 = Course("软件测试", 2)
course3 = Course("数据库", 4)

# 添加课程
manager.add_course(course1)
manager.add_course(course2)
manager.add_course(course3)

print("----------------")

# 查看课程
manager.show_courses()
print("----------------")

# 修改课程信息
course1.set_credit(5)
print("修改后:")
course1.show_info()
print("----------------")

# 删除课程
manager.delete_course("数据库")
print("----------------")


# 再次查看
manager.show_courses()
