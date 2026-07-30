"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
# 保存学生的信息 {"sid": xxx, "name": xxx, "age":18, "gender": xxx}
# 定义为全局变量，方便各个函数进行访问
students = []

def menu():
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

def get_sid():
    '''
    获取用户输入的学号
    :return:
    '''
    sid = input("请输入学生的 ID：")
    return sid

def get_name():
    '''
    获取用户输入的姓名
    :return:
    '''
    name = input("请输入学生姓名：")
    return name

def get_age():
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

def get_gender():
    '''
    获取用户输入的性别
    :return:
    '''
    gender = input("请输入学生的性别：")
    return gender

def add_student(sid, name, age, gender):
    '''
    添加学生
    :param sid: 学生 ID
    :param name: 学生姓名
    :param age: 学生年龄
    :param gender: 学生性别
    :return: 操作提示信息
    '''
    # 遍历学生管理系统列表，判断学生 ID 是否已经存在
    for s in students:
        if s["sid"] == sid:
            print("学号已经存在，添加失败！")
            return "添加失败"
    # 拼接学生信息
    student = {
        "sid": sid,
        "name": name,
        "age": age,
        "gender": gender
    }
    # 把学生信息存入列表
    students.append(student)
    print("添加学生信息成功")
    return "添加成功"


def modify_student_by_id(sid):
    '''
    通过学号修改学生信息
    :param sid: 学生 ID
    :return: 操作提示信息
    '''
    # 遍历学生列表
    for s in students:
        # 如果对应 ID 的学生存在
        if s["sid"] == sid:
            # 接收用户输入的学生信息
            name = get_name()
            age = get_age()
            gender = get_gender()
            # 给当前学生信息重新赋值
            s["name"] = name
            s["age"] = age
            s["gender"] = gender
            print(f"学生 ID 为 {sid} 的信息修改成功！")
            return "修改成功"
    print(f"没有 ID 为 {sid} 对应的学生信息！")
    return "修改失败"

def delete_student_by_id(sid):
    '''
    通过学生 ID 删除学生信息
    :param sid: 学生 ID
    :return: 操作提示信息
    '''
    for s in students:
        if s["sid"] == sid:
            students.remove(s)
            print(f"ID 为 {sid} 的学生删除成功！")
            return "删除成功"
    print(f"没有 ID 为 {sid} 对应的学生信息！")
    return "删除失败"

def delete_student_by_name(name):
    '''
    通过学生姓名，删除所有符合的学生
    :param name: 学生姓名
    :return: 操作提示信息
    '''
    # 准备删除的学生列表
    exist_s = []
    for s in students:
        # 传入的学生姓名存在
        if s["name"] == name:
            exist_s.append(s)
    # 如果准备要删除的学生列表中有数据
    if len(exist_s) > 0:
        for s in exist_s:
            students.remove(s)
            print(f"ID 为 {s['sid']}，姓名为 {name} 的学生删除成功！")
        print(f"成功删除了 {len(exist_s)} 个学生！")
        return "删除成功"
    else:
        print(f"姓名 {name} 不存在，无法删除！")
        return "删除失败"

def query_student_by_id(sid):
    '''
    通过学号查询学生信息
    :param sid: 学生 ID
    :return: 操作提示信息
    '''
    for s in students:
        if s["sid"] == sid:
            print(f"学号为 {sid} 的学生信息如下：")
            print(f"学号：{s['sid']}，姓名：{s['name']}，年龄：{s['age']}，性别：{s['gender']}")
            return "查询成功"
    print(f"学号 {sid} 的学生不存在！")
    return "查询失败"

def query_student_by_name(name):
    '''
    通过学生姓名查询学生信息
    :param name: 学生姓名
    :return: 操作提示信息
    '''
    # 查询到的学生列表
    exist_s = []
    for s in students:
        # 传入的学生姓名存在
        if s["name"] == name:
            exist_s.append(s)
    # 如果查询到的学生列表中有数据
    exist_s_num = len(exist_s)
    if exist_s_num > 0:
        print(f"姓名为 {name} 的学生共有 {exist_s_num} 名，信息如下：")
        for s in exist_s:
            print(f"学号：{s['sid']}，姓名：{s['name']}，年龄：{s['age']}，性别：{s['gender']}")
        return "查询成功"
    else:
        print(f"姓名为 {name} 的学生不存在！")
        return "查询失败"

def show_all_info():
    '''
    查询所有学生的信息
    '''
    if students:
        print("所有学生信息如下：")
        for s in students:
            print(f"学号：{s['sid']}，姓名：{s['name']}，年龄：{s['age']}，性别：{s['gender']}")
    else:
        print("当前系统没有学生，请尽快添加！")


def student_manager():
    '''
    学生管理系统
    '''
    # 使用死循环展示系统菜单，并且根据用户的选择完成对应的操作
    while True:
        # 展示菜单，并获取用户选择的数字
        select_op = menu()
        # 如果用户选择的是 1-8 之间的单个数字，那么完成对应的操作
        if len(select_op) == 1 and select_op in "12345678":
            # 输入 1 完成添加学生的操作
            if select_op == "1":
                # 接收用户输入的学生信息
                # sid = get_sid()
                # name = get_name()
                # age = get_age()
                # gender = get_gender()
                # # 调用添加学生函数
                # add_student(sid, name, age, gender)
                add_student(get_sid(), get_name(), get_age(), get_gender())
            elif select_op == "2":
                # 接收用户输入的学生编号
                sid = get_sid()
                # 调用通过学号修改学生信息的函数
                modify_student_by_id(sid)
            elif select_op == "3":
                # 接收用户输入的学生编号
                sid = get_sid()
                # 调用通过学号删除学生信息的函数
                delete_student_by_id(sid)
            elif select_op == "4":
                # 接收用户输入的学生姓名
                name = get_name()
                # 调用通过姓名删除学生信息的函数
                delete_student_by_name(name)
            elif select_op == "5":
                # 接收用户输入的学生编号
                sid = get_sid()
                # 调用通过学号查询学生信息的函数
                query_student_by_id(sid)
            elif select_op == "6":
                # 接收用户输入的学生姓名
                name = get_name()
                # 调用通过姓名查询学生信息的函数
                query_student_by_name(name)
            elif select_op == "7":
                # 调用查询全部学生信息的函数
                show_all_info()
            else:
                # 完成退出系统的操作
                break
        else:
            print("输入的数据不合法，请输入 1-8 之间的操作编号！")

if __name__ == '__main__':
    student_manager()

