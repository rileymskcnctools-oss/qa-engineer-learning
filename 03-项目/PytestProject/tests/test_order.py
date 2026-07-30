import pytest


@pytest.mark.order(3)
def test_pay():
    print("支付订单")
    assert True


@pytest.mark.order(1)
def test_login():
    print("用户登录")
    assert True


@pytest.mark.order(2)
def test_create_order():
    print("创建订单")
    assert True
