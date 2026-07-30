"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
import allure
import pytest

from script.student_management import StudentManagement

@allure.feature("学生管理系统")
class TestStudentManagement:

    def setup_class(self):
        # 获取管理系统的实例
        self.sm = StudentManagement()

    @pytest.mark.P0
    @pytest.mark.order(1)
    @allure.story("添加学生")
    @allure.title("添加学生冒烟用例")
    def test_add_student(self):
        '''
        测试添加学生方法
        '''
        # 测试步骤
        result = self.sm.add_student("s01", "lily", 21, "female")
        # 断言
        assert result == "添加成功"

    @pytest.mark.P0
    @pytest.mark.order(3)
    @allure.story("修改学生")
    @allure.title("修改学生冒烟用例")
    def test_modify_student_by_id(self):
        '''
        测试通过 id 修改学生函数
        '''
        # 原则：测试用例尽量不耦合
        # 先添加学生信息
        self.sm.add_student("s02", "tom", 22, "male")
        # 修改学生信息
        result = self.sm.modify_student_by_id("s02", "jack", 23, "male")
        # 断言
        assert result == "修改成功"

    @pytest.mark.P0
    @allure.story("查询学生")
    @allure.title("通过 id 查询学生冒烟用例")
    def test_query_student_by_id(self):
        '''
        测试通过 id 查询学生函数
        '''
        self.sm.add_student("s03", "marry", 23, "female")
        result = self.sm.query_student_by_id("s03")
        assert result == "查询成功"

    @pytest.mark.order(3)
    @allure.story("查询学生")
    @allure.title("通过姓名查询学生冒烟用例")
    def test_query_student_by_name(self):
        '''
        测试通过姓名查询学生函数
        '''
        self.sm.add_student("s04", "linda", 21, "female")
        result = self.sm.query_student_by_name("linda")
        assert result == "查询成功"

    @pytest.mark.P0
    @allure.story("删除学生")
    @allure.title("通过 id 删除学生冒烟用例")
    def test_delete_student_by_id(self):
        '''
        测试通过 id 删除学生函数
        '''
        self.sm.add_student("s05", "xiaobai", 24, "male")
        result = self.sm.delete_student_by_id("s05")
        assert result == "删除成功"

    @pytest.mark.P1
    @pytest.mark.order(2)
    @allure.story("删除学生")
    @allure.title("通过姓名删除学生冒烟用例")
    def test_delete_student_by_name(self):
        '''
        测试通过姓名删除学生函数
        '''
        self.sm.add_student("s06", "xiaolin", 21, "female")
        result = self.sm.delete_student_by_name("xiaolin")
        assert result == "删除成功"