"""
共享 fixture — 所有测试文件自动发现

（原 test_setup.py 的 setup/teardown 移植到这里）
"""
import pytest


# ============================================================
# setup/teardown — 四种作用域（从 test_setup.py 移植）
# ============================================================
def setup_module():
    print("\n===== setup_module：整个模块开始前执行一次 =====")


def teardown_module():
    print("\n===== teardown_module：整个模块结束后执行一次 =====")


def setup_function():
    print("\n----- setup_function：每个函数用例前 -----")


def teardown_function():
    print("----- teardown_function：每个函数用例后 -----")


# ============================================================
# fixture 方式（推荐：比 setup_function 更灵活）
# ============================================================
@pytest.fixture
def sample_numbers():
    """提供一组测试数据"""
    return {"a": 10, "b": 2}


@pytest.fixture(autouse=False)
def db_mock():
    """模拟数据库连接（演示 fixture 的 setup/teardown）"""
    print("\n[DB] 连接数据库...")
    yield "db_connection"
    print("[DB] 关闭数据库...")
