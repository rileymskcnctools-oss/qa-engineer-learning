"""
练习代码：
模块化
"""

# 定义学生类
class Student:

    # 使用构造函数，接收实例化类的时候需要传入的参数
    def __init__(self, sid, name, age, gender):
        self.sid = sid
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"SID: {self.sid}, Name: {self.name}, Age: {self.age}, Gender: {self.gender}"

class StudentManage:
    def __init__(self):
        # 定义一个实例变量，用来保存学生信息
        # 设为私有，只能让类内部的方法进行访问和操作
        self.__students = []

    def __menu(self):
        '''
        菜单函数
        :return: 用户输入的编号
        '''
        print("****************************************")
        print("*                学生管理系统             *")
        print("*        1. 添加新学生信息                 *")
        print("*        2. 通过学号修改学生信息              *")
        print("*        3. 通过学号删除学生信息              *")
        print("*        4. 通过姓名删除学生信息              *")
        print("*        5. 通过学号查询学生信息              *")
        print("*        6. 通过姓名查询学生信息              *")
        print("*        7. 显示所有学生信息               *")
        print("*        8. 退出系统                    *")
        print("****************************************")
        # 接收用户的输入
        select_op = input("输入编号选择操作：")
        return select_op

    def __get_sid(self):
        '''
        获取用户输入的学号
        :return:
        '''
        sid = input("请输入学生的 ID：")
        return sid

    def __get_name(self):
        '''
        获取用户输入的姓名
        :return:
        '''
        name = input("请输入学生姓名：")
        return name

    def __get_age(self):
        '''
        获取用户输入的年龄
        :return:
        '''
        while True:
            age = input("请输入学生年龄：")
            if age.isdigit():
                return int(age)
            else:
                print("输入的年龄不合法，请输入数字！")

    def __get_gender(self):
        '''
        获取用户输入的性别
        :return:
        '''
        gender = input("请输入学生的性别：")
        return gender

    def add_student(self, sid, name, age, gender):
        '''
        添加学生
        :param sid: 学生 ID
        :param name: 学生姓名
        :param age: 学生年龄
        :param gender: 学生性别
        :return: 操作提示信息
        '''
        # 遍历学生管理系统列表，判断学生 ID 是否已经存在
        for s in self.__students:
            if s.sid == sid:
                print("学号已经存在，添加失败！")
                return "添加失败"
        # 拼接学生信息，和原来不一样，不能拼接成字典，拼接实例
        student = Student(sid, name, age, gender)
        # 把学生信息存入列表
        self.__students.append(student)
        print("添加学生信息成功")
        return "添加成功"

    def modify_student_by_id(self, sid):
        '''
        通过学号修改学生信息
        :param sid: 学生 ID
        :return: 操作提示信息
        '''
        # 遍历学生列表
        for s in self.__students:   #私有变量访问用self.
            # 如果对应 ID 的学生存在
            if s.sid == sid:   # 实例化属性访问方式 实例对象.属性名称
                # 接收用户输入的学生信息
                name = self.__get_name()  #私有方法访问用self.
                age = self.__get_age()   #私有方法访问用self.
                gender = self.__get_gender() #私有方法访问用self.
                # 给当前学生信息重新赋值
                s.name = name
                s.age = age
                s.gender = gender
                print(f"学生 ID 为 {sid} 的信息修改成功！")
                return "修改成功"
        print(f"没有 ID 为 {sid} 对应的学生信息！")
        return "修改失败"

    def delete_student_by_id(self, sid):
        '''
        通过学生 ID 删除学生信息
        :param sid: 学生 ID
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                self.__students.remove(s)
                print(f"ID 为 {sid} 的学生删除成功！")
                return "删除成功"
        print(f"没有 ID 为 {sid} 对应的学生信息！")
        return "删除失败"

    def delete_student_by_name(self, name):
        '''
        通过学生姓名，删除所有符合的学生
        :param name: 学生姓名
        :return: 操作提示信息
        '''
        # 准备删除的学生列表
        exist_s = []
        for s in self.__students:
            # 传入的学生姓名存在
            if s.name == name:
                exist_s.append(s)
        # 如果准备要删除的学生列表中有数据
        if len(exist_s) > 0:
            for s in exist_s:
                self.__students.remove(s)
                print(f"ID 为 {s.sid}，姓名为 {name} 的学生删除成功！")
            print(f"成功删除了 {len(exist_s)} 个学生！")
            return "删除成功"
        else:
            print(f"姓名 {name} 不存在，无法删除！")
            return "删除失败"

    def query_student_by_id(self, sid):
        '''
        通过学号查询学生信息
        :param sid: 学生 ID
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                print(f"学号为 {sid} 的学生信息如下：")
                print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")
                return "查询成功"
        print(f"学号 {sid} 的学生不存在！")
        return "查询失败"

    def query_student_by_name(self, name):
        '''
        通过学生姓名查询学生信息
        :param name: 学生姓名
        :return: 操作提示信息
        '''
        # 查询到的学生列表
        exist_s = []
        for s in self.__students:
            # 传入的学生姓名存在
            if s.name == name:
                exist_s.append(s)
        # 如果查询到的学生列表中有数据
        exist_s_num = len(exist_s)
        if exist_s_num > 0:
            print(f"姓名为 {name} 的学生共有 {exist_s_num} 名，信息如下：")
            for s in exist_s:
                print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")
            return "查询成功"
        else:
            print(f"姓名为 {name} 的学生不存在！")
            return "查询失败"

    def __show(self):
        '''
        查询所有学生的信息
        '''
        if self.__students:
            print("所有学生信息如下：")
            for s in self.__students:
                print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")
        else:
            print("当前系统没有学生，请尽快添加！")

    def manager(self):
        '''
        学生管理系统
        '''
        # 使用死循环展示系统菜单，并且根据用户的选择完成对应的操作
        while True:
            # 展示菜单，并获取用户选择的数字
            select_op = self.__menu()
            # 如果用户选择的是 1-8 之间的单个数字，那么完成对应的操作
            if len(select_op) == 1 and select_op in "12345678":
                # 输入 1 完成添加学生的操作
                if select_op == "1":
                    # 接收用户输入的学生信息
                    sid = self.__get_sid()
                    name = self.__get_name()
                    age = self.__get_age()
                    gender = self.__get_gender()
                    # 调用添加学生函数
                    self.add_student(sid, name, age, gender)
                elif select_op == "2":
                    # 接收用户输入的学生编号
                    sid = self.__get_sid()
                    # 调用通过学号修改学生信息的函数
                    self.modify_student_by_id(sid)
                elif select_op == "3":
                    # 接收用户输入的学生编号
                    sid = self.__get_sid()
                    # 调用通过学号删除学生信息的函数
                    self.delete_student_by_id(sid)
                elif select_op == "4":
                    # 接收用户输入的学生姓名
                    name = self.__get_name()
                    # 调用通过姓名删除学生信息的函数
                    self.delete_student_by_name(name)
                elif select_op == "5":
                    # 接收用户输入的学生编号
                    sid = self.__get_sid()
                    # 调用通过学号查询学生信息的函数
                    self.query_student_by_id(sid)
                elif select_op == "6":
                    # 接收用户输入的学生姓名
                    name = self.__get_name()
                    # 调用通过姓名查询学生信息的函数
                    self.query_student_by_name(name)
                elif select_op == "7":
                    # 调用查询全部学生信息的函数
                    self.__show()
                else:
                    # 完成退出系统的操作
                    break
            else:
                print("输入的数据不合法，请输入 1-8 之间的操作编号！")

if __name__ == '__main__':

    # s1 = Student("s011", "tom", 23, "male")
    # print(type(s1))
    # print(s1)


    # 获取学生管理系统的实例
    sm = StudentManager()
    # 通过实例调用实例方法
    sm.manager()