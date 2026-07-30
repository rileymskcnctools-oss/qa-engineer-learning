# conftest.py — 根级 conftest（预留扩展点）
# 所有 tests/ 下的测试文件都可以使用这里定义的 fixture
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')
# conftest.py
import pytest


@pytest.fixture(scope="function", autouse=True)
def login():
     # setup 操作
     print("完成登录操作")
     token = "abcd"
     username = 'hogwarts'
     yield token,username # 相当于return
     # teardown 操作
     print("完成登出操作")

@pytest.fixture()
def connectDB():
     print("连接数据库")
     yield
     print("断开数据库")

# test_fixture_conftestdemo.py
def test_get_product(login, connectDB):
    print("验证获取单品信息")
