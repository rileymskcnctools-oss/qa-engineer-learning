import pytest


@pytest.mark.order("first")
def test_login():
    pass


@pytest.mark.order("last")
def test_logout():
    pass


def test_create_order():
    pass
