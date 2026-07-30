"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
# 定义一个学生类
class Student:

    # 使用构造函数，接收实例化类时需要传入的参数
    def __init__(self, sid, name, age, gender):
        # 使用实例属性接收传入的值
        self.sid = sid
        self.name = name
        self.age = age
        self.gender = gender

    # 重写对象的显示格式方法
    def __str__(self):
        return f"SID: {self.sid} --- Name: {self.name} --- Age: {self.age} --- Gender: {self.gender}"


# 封装管理类
class StudentManagement:

    def __init__(self):
        # 定义一个实例变量，用来保存学生的信息，方法各个方法之间进行访问
        # 把这个实例变量设置为私有，只能让类中方法对其进行操作
        self.__students = []

    def __menu(self):
        '''
        菜单函数：展示学生管理系统菜单信息，并获取用户输入
        :return:  用户输入的编号字符串
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
        select_op = input("输入编号选择操作：")
        return select_op

    def __get_sid(self):
        '''
        获取用户输入的学号
        :return: 返回学号字符串
        '''
        sid = input("请输入学生ID:")
        return sid

    def __get_name(self):
        '''
        获取用户输入的姓名
        :return: 返回姓名字符串
        '''
        name = input("请输入学生名称：")
        return name

    def __get_age(self):
        '''
        获取用户输入的年龄
        :return: 返回年龄字符串
        '''
        while True:
            age = input("请输入学生年龄：")
            if age.isdigit():
                return int(age)
            else:
                print("输入年龄不合法，请输入数字")

    def __get_gender(self):
        '''
        获取用户输入的性别
        :return: 返回性别字符串
        '''
        gender = input("请输入学生性别：")
        return gender

    def add_student(self, sid, name, age, gender):
        '''
        添加学生
        :param sid: 学生 id
        :param name: 学生姓名
        :param age: 学生年龄
        :param gender: 学生性别
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                print("学生编号已存在，添加失败")
                return "添加失败"
        else:
            student = Student(sid, name, age, gender)
            self.__students.append(student)
            print("添加学生信息成功")
            return '添加成功'

    def modify_student_by_id(self, sid, name, age, gender):
        '''
        通过学号修改学生信息
        :param sid: 学生学号
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                s.name = name
                s.age = age
                s.gender = gender
                print("修改成功")
                return "修改成功"
        else:
            print(f'没有 {sid} 对应的学生信息')
            return "修改失败"

    def delete_student_by_id(self, sid):
        '''
        通过ID删除学生信息
        :param sid: 学生学号
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                self.__students.remove(s)
                print("删除成功")
                return "删除成功"
        else:
            print(f'没有 {sid} 对应的学生信息')
            return "删除失败"

    def delete_student_by_name(self, name):
        '''
        通过学生姓名 删除所有符合的学生
        :param name: 学生姓名
        :return: 操作提示信息
        '''
        exist_s = []
        # 找出所有要删除的学生
        for s in self.__students:
            if s.name == name:
                exist_s.append(s)

        # 开始删除
        if len(exist_s) > 0:
            for s in exist_s:
                self.__students.remove(s)
                print(f"名称为 { name } 的学生删除成功")
            else:
                print(f"成功删除 {len(exist_s)} 个学生")
                return "删除成功"
        else:
            print(f"学生【{name}】不存在，无法删除")
            return "删除失败"

    def query_student_by_id(self, sid):
        '''
        通过学号查询学生信息
        :param sid: 学生学号
        :return: 操作提示信息
        '''
        for s in self.__students:
            if s.sid == sid:
                print(f"学生编号 {sid} 的学生信息如下：")
                print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")
                return "查询成功"
        else:
            print(f"学生编号 {sid} 的学生不存在")
            return "查询失败"

    def query_student_by_name(self, name):
        '''
        通过姓名查询学生信息
        :param name:
        :return: 操作提示信息
        '''
        exist_s = []
        for s in self.__students:
            if s.name == name:
                exist_s.append(s)

        if len(exist_s) > 0:
            print(f"名称为 {name} 的学生共 {len(exist_s)} 名，信息如下：")
            for s in exist_s:
                print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")
            return "查询成功"
        else:
            print(f"名称为 {name} 的学生不存在")
            return "查询失败"

    def show(self):
        '''
        显示所有学生信息
        :return: 格式化的学生信息
        '''
        print("所有学生信息如下：")
        for s in self.__students:
            print(f"学号：{s.sid}，姓名：{s.name}，年龄：{s.age}，性别：{s.gender}")

    def manager(self):
        '''
        管理方法
        :return:
        '''
        while True:
            select_op = self.__menu()
            if len(select_op) == 1 and select_op in "12345678":
                if select_op == "1":
                    sid = self.__get_sid()
                    name = self.__get_name()
                    age = self.__get_age()
                    gender = self.__get_gender()
                    self.add_student(sid, name, age, gender)
                elif select_op == "2":
                    sid = self.__get_sid()
                    name = self.__get_name()
                    age = self.__get_age()
                    gender = self.__get_gender()
                    self.modify_student_by_id(sid, name, age, gender)
                elif select_op == "3":
                    sid = self.__get_sid()
                    self.delete_student_by_id(sid)
                elif select_op == "4":
                    name = self.__get_name()
                    self.delete_student_by_name(name)
                elif select_op == "5":
                    sid = self.__get_sid()
                    self.query_student_by_id(sid)
                elif select_op == "6":
                    name = self.__get_name()
                    self.query_student_by_name(name)
                elif select_op == "7":
                    self.show()
                else:
                    break
            else:
                print("输入的数据不合法，请输入在合法范围内的操作编号！！！")