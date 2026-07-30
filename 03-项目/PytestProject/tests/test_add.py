# test_add.py 文件内容
import pytest
import yaml

from src.operation import my_add


import os

def get_yaml():
    '''
    读取 yaml 文件数据
    :return: python 对象数据
    '''
    yaml_path = os.path.join(os.path.dirname(__file__), "..", "data", "data.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

class TestWithYaml:

    @pytest.mark.parametrize('x,y,expected', get_yaml())
    def test_add(self, x, y, expected):
        assert my_add(int(x), int(y)) == int(expected)