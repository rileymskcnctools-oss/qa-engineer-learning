# conftest.py — 根级 conftest（预留扩展点）
# 所有 tests/ 下的测试文件都可以使用这里定义的 fixture
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode_escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode_escape')
