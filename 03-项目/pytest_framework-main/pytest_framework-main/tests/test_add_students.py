"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
import allure
import pytest

from script.student_management import StudentManagement
from utils.utils import Utils

import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

yaml_path = os.path.join(
    BASE_PATH,
    "datas",
    "stu_info.yaml"
)

stu_info = Utils.get_yaml_data(yaml_path)

@allure.feature("学生管理系统")
class TestAddStudents:

    def setup_class(self):
        self.sm = StudentManagement()

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
    def test_add_student_by_params(self, sid, name, age, gender):
        # 测试步骤
        result = self.sm.add_student(sid, name, age, gender)
        # 断言
        assert result == "添加成功"

    @pytest.mark.parametrize(
        "sid, name, age, gender",
        stu_info.get("add").get("P1").get("data"),
        ids=stu_info.get("add").get("P1").get("ids")
    )
    def test_add_student_by_yaml(self, sid, name, age, gender):
        print()
        # 测试步骤
        result = self.sm.add_student(sid, name, age, gender)
        # 断言
        assert result == "添加成功"