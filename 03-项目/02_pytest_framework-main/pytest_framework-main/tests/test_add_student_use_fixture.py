"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
import allure
import pytest

from script.student_management import StudentManagement


@allure.feature("学生管理系统")
class TestAddStudents:

    # 参数化使用场景：测试步骤完全一致，只有测试数据有变化的情况
    @pytest.mark.parametrize(
        "sid, name, age, gender",
        [
            ["s01", "lily", 21, "female"],
            ["s02", "tom", 22, "male"],
            ["s03", "jack", 23, "male"],
            ["s04", "ema", 22, "female"]
        ],
        # ids=["add 01", "add 02", "add 03", "add 04", "add 05"]
    )
    @allure.story("添加学生")
    @allure.title("参数化添加学生 {sid}, {name}, {age}, {gender}")
    # 使用 fixture的方法：1. 在参数列表 self 后的第一个位置传入 fixture 函数名
    def test_add_student_by_params(self, get_sm, sid, name, age, gender):
        # 测试步骤
        # 2. 使用 fixture 函数名完成调用
        result = get_sm.add_student(sid, name, age, gender)
        # 断言
        assert result == "添加成功"

    def test_1(self):
        # 不需要学生管理系统的实例
        assert True

    def test_2(self):
        assert True

    def test_modify_student_by_id(self, get_sm, add_for_test):
        '''
        测试通过 id 修改学生函数
        '''
        # 修改学生信息
        result = get_sm.modify_student_by_id(add_for_test, "jack", 23, "male")
        # 断言
        assert result == "修改成功"