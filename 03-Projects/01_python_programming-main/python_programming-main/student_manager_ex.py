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
    select_op = input("输入编号选择操作：")
    return select_op

def get_sid():
    sid=input("请输入学生的学号：")
    return sid


def get_name():
    name=input("请输入学生的姓名：")
    return name


def get_age():
    while True:
     age=input("请输入学生的年龄：")
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
    for stu in students:
        if stu["sid"] == sid:
            print("学号已存在，添加学生失败！")
            return "添加失败"
    students.append({"sid": sid, "name": name, "age": age, "gender": gender})
    print("添加学生信息成功")
    return "添加成功"

def modify_student_by_id(sid):
    '''
    通过学号修改学生信息
    :param sid: 学生 ID
    :return: 操作提示信息
    '''
    # 遍历学生列表
    for stu in students:
        if stu["sid"] == sid:
            # 接收用户输入信息
            name = get_name()
            age = get_age()
            gender = get_gender()
            # 给当前学生信息重新赋值
            stu["name"] = name
            stu["age"] = age
            stu["gender"] = gender
            print("学生ID为{sid} 对应信息修改成功")
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
    exist_s=[]
    for s in students:
        if s["name"] == name:
            exist_s.append(s)
    if len(exist_s)>0:
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
        if s["name"] == name:
            exist_s.append(s)

    exist_num=len(exist_s)
    if exist_num>0:
        print(f"姓名为 {name} 的学生共有 {exist_num} 名，信息如下：")
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

    while True:

        select_op = menu()

        if select_op in "12345678":

            if select_op=="1":

                sid=get_sid()
                name=get_name()
                age=get_age()
                gender=get_gender()

                add_student(
                    sid,
                    name,
                    age,
                    gender
                )


            elif select_op=="2":

                sid=get_sid()

                modify_student_by_id(sid)


            elif select_op=="3":

                sid=get_sid()

                delete_student_by_id(sid)


            elif select_op=="4":

                name=get_name()

                delete_student_by_name(name)


            elif select_op=="5":

                sid=get_sid()

                query_student_by_id(sid)


            elif select_op=="6":

                name=get_name()

                query_student_by_name(name)


            elif select_op=="7":

                show_all_info()


            elif select_op=="8":

                print("退出系统")

                break


        else:

            print("输入的数据不合法，请输入1-8")
if __name__ == "__main__":
    student_manager()