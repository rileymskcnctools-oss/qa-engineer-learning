"""
补充测试 — 演示高级标记用法（Ch04）

- skip / skipif
- 自定义 marker（smoke / slow）
- xfail
"""

import pytest
import sys


# ============================================================
# skip / skipif
# ============================================================
@pytest.mark.skip(reason="功能开发中，暂不测试")
def test_future_feature():
    assert False


@pytest.mark.skipif(sys.version_info < (3, 11), reason="Python 3.11+ 才支持")
def test_python311_plus():
    assert True


# ============================================================
# 自定义 marker
# ============================================================
@pytest.mark.smoke
def test_smoke_check():
    """冒烟：基本可用性"""
    from src.my_module import inc
    assert inc(0) == 1


@pytest.mark.slow
def test_slow_calculation():
    """标记为慢速 — CI 中可跳过"""
    import time
    time.sleep(0.1)
    assert True


# ============================================================
# xfail
# ============================================================
@pytest.mark.xfail(reason="已知 Bug #BUG-001：浮点精度问题", strict=False)
def test_float_precision_bug():
    """预期失败：浮点精度已知有问题"""
    from src.my_module import double
    assert double(0.15) == 0.30  # 浮点精度可能不精确匹配
