"""
员工管理系统

功能：
1. 创建 Employee 基类
2. 创建 Manager 子类
3. 创建 Developer 子类
4. 实现员工分类管理和信息展示
"""


# 员工基类
class Employee:
    # 初始化员工信息
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    # 通用工作方法
    def work(self):
        print(f"{self.name} 正在工作")

    # 展示员工信息

    def show_info(self):
        print(
            f"姓名:{self.name}, 年龄:{self.age}, 工资:{self.salary}"
        )

# 管理者类，继承Employee
class Manager(Employee):
    def __init__( self, name, age,salary,team_size):
    # 调用父类初始化方法
     super().__init__(name,age,salary)
    # Manager自己的属性
     self.team_size = team_size

    # Manager专属方法
    def manage_team(self):
        print(  f"{self.name} 正在管理 {self.team_size} 人团队")

# 开发者类，继承Employee
class Developer(Employee):
    def __init__(self,name,age, salary,language):
        # 调用父类初始化
        super().__init__( name,age,salary)
        # Developer自己的属性
        self.language = language

    # Developer专属方法
    def show_language(self):
        print( f"{self.name} 使用编程语言:{self.language}"
)


# 员工管理
def employee_manage():

    employees = [
        Manager(
            "李经理",
            35,
            15000,
            18
        ),

        Developer(
            "宋然",
            25,
            10000,
            "Python"
        ),

        Developer(
            "王丽",
            28,
            12000,
            "Java"
        )

    ]

    # 遍历员工

    for employee in employees:
        employee.show_info()
        employee.work()

        # 判断员工类型
        if isinstance(employee, Manager):
            employee.manage_team()
        elif isinstance(employee, Developer):
            employee.show_language()
        print("----------------")
employee_manage()