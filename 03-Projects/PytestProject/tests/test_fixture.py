import pytest

# @pytest.fixture()
# def login():
#      print("完成登录操作")

def test_search():
    print("搜索")


# 该测试用例执行之前，会自动执行 fixture
def test_cart(login):
    print("购物车")


# 该测试用例执行之前，会自动执行 fixture
def test_order(login):
    print("下单功能")
