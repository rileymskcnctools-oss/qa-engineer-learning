import allure
import requests,pytest

from L1_beginner.utils.log_util import logger

@allure.feature("宠物搜索接口")
class TestPetstorePetSearch:
    '''
    宠物商店宠物查询单接口测试
    '''

    def setup_class(self):
        # 定义请求 URL
        self.base_url="https://petstore.swagger.io/v2/pet"
        # 拼接宠物查询接口 URL
        self.search_url=self.base_url+"/findByStatus"

    @allure.story("冒烟用例")
    def test_search_pet(self):
        #宠物查询接口请求参数
        pet_stats={
            "status":"available",
        }
        # 发出查询接口请求
        r=requests.get(self.search_url,params=pet_stats)
        # 查看接口响应
        logger.info(r.text)
        # 状态断言
        assert r.status_code == 200
        # 业务断言
        assert r.json() != []
        # 响应返回的是一个列表，判断列表中第一个元素中是否包含 id 这个 key
        assert "id" in r.json()[0]

    @pytest.mark.parametrize("status", ["available", "pending", "sold"],
                             ids=["available_pets", "pending_pets", "sold_pets"])
    @allure.story("status 正常参数化传参")
    def test_search_pet_by_params(self,status):
        # 宠物查询接口请求参数
        pet_stats = {
            "status": status
        }
        # 发出查询接口请求
        r = requests.get(self.search_url, params=pet_stats)
        # 查看接口响应
        logger.info(r.text)
        # 状态断言
        assert r.status_code == 200
        # 业务断言
        assert r.json() != []
        # 响应返回的是一个列表，判断列表中第一个元素中是否包含 id 这个 key
        assert "id" in r.json()[0]


    @pytest.mark.parametrize("status",
                             ["petstatus","", 12345],
                             ids=["wrong_value", "none_str", "number"]
                             )
    @allure.story("status 异常参数化传参")
    def test_search_pet_by_ex(self,status):
        # 宠物查询接口请求参数
        pet_stats = {
            "status": status
        }
        # 发出查询接口请求
        r = requests.get(self.search_url, params=pet_stats)
        # 查看接口响应
        logger.info(r.text)
        # 状态断言
        assert r.status_code == 200
        # 业务断言
        assert r.json() == []

    @allure.story("不传 status 参数")
    def test_search_pet_none_param(self):
        # 发出查询接口请求
        r = requests.get(self.search_url)
        # 查看接口响应
        logger.info(r.text)
        # 状态断言
        assert r.status_code == 200
        # 业务断言
        assert r.json() == []

    @allure.story("传入非 status 参数")
    def test_search_pet_wrong_param(self):
        # 宠物查询接口错误的请求参数
        pet_stats = {
            "key": "available"
        }
        # 发出查询接口请求
        r = requests.get(self.search_url, params=pet_stats)
        # 查看接口响应
        logger.info(r.text)
        # 状态断言
        assert r.status_code == 200
        # 业务断言
        assert r.json() == []







