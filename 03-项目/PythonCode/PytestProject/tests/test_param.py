import pytest

search_list = ['appium', 'selenium', 'pytest']

#单参数
@pytest.mark.parametrize('name', search_list)
def test_search(name):
    assert name in search_list

# 数据放在元组中，多参数
@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+5", 7), ("7+5", 12)],
    ids=['add_3+5=8', 'add_2+5=7', 'add_3+5=12']
)

def test_mark_more(test_input, expected):
    assert eval(test_input) == expected

# 笛卡尔积
@pytest.mark.parametrize("b", ["a", "b", "c"])   # 第二个装饰器 → 内层变量
@pytest.mark.parametrize("a", [1, 2, 3])          # 第一个装饰器 → 外层变量
def test_param(a, b):
    print(f"a={a}, b={b}")