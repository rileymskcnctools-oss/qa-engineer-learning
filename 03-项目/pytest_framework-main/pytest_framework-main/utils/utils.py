"""
__author__ = '霍格沃兹测试开发学社'
__desc__ = '更多测试开发技术探讨，请访问：https://ceshiren.com/t/topic/15860'
"""
import yaml


class Utils:

    @classmethod
    def get_yaml_data(cls, file_path):
        '''
        获取 yaml 文件数据
        :return: yaml 数据
        '''
        with open(file_path, encoding='utf-8') as f:
            result = yaml.safe_load(f)
        print(f"yaml 文件读取结果为 {result}")
        return result


