import pytest

def double(a):
    return a * 2

@pytest.mark.int
def test_double_int():
    assert 2 == double(1)

@pytest.mark.minus
def test_double1_minus():
    assert -2 == double(-1)

@pytest.mark.float
def test_double_float():
    assert 0.2 == double(0.1)


@pytest.mark.minus
def test_double2_minus():
    assert -0.2 == double(-0.1)


@pytest.mark.zero
def test_double_0():
    assert 0 == double(0)

@pytest.mark.bignum
def test_double_bignum():
    assert 200 == double(100)


@pytest.mark.str
def test_double_str():
    assert 'aa' == double('a')


@pytest.mark.str
def test_double_str1():
    assert 'a$a$' == double('a$')
