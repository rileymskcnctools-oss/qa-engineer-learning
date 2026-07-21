"""
被测试的业务模块 — 计算器 + 字符串工具

（将原 test_demo.py 和 test_setup.py 中被测函数提取到这里）
"""


def inc(x):
    """自增 1"""
    return x + 1


def double(a):
    """两倍"""
    return a * 2


def is_even(n: int) -> bool:
    """判断偶数"""
    return n % 2 == 0


def safe_divide(a: float, b: float) -> float:
    """安全除法，除数为 0 时抛出 ValueError"""
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b
