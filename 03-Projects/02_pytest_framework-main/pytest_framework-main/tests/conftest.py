"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
import pytest

from script.student_management import StudentManagement

@pytest.fixture(scope="class", autouse=True)
def get_sm():
    # 测试用例执行之前执行的
    sm = StudentManagement()
    print("测试用例执行前准备工作")
    yield sm
    # 测试用例执行之后执行的
    print("测试类执行完毕")


@pytest.fixture()
def add_for_test(get_sm):
    sid = "for_test1"
    get_sm.add_student(sid, "for_test", 22, "male")
    yield sid
    get_sm.delete_student_by_id(sid)