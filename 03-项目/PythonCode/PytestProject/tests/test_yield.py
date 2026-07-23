import pytest

@pytest.fixture(scope="class")
def login():
     # setup 操作
     print("完成登录操作")
     token = "abcd"
     username = 'hogwarts'
     yield token,username # 相当于return
     # teardown 操作
     print("完成登出操作")

def test_search(login):
    token,username = login
    print(f"token: {token} , name : {username}")
    print("搜索")
