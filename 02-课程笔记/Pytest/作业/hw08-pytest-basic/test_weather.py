import allure
import pytest
import yaml
from weather import Weather
import os



BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


yaml_path = os.path.join(
    BASE_DIR,
    "data",
    "weather.yaml"
)


with open(
    yaml_path,
    encoding="utf-8"
) as f:

    data = yaml.safe_load(f)

# yaml文件外层是字典，内层是列表

current_data = data["current_weather"]

history_data = data["history_weather"]


class TestWeather:


    @classmethod
    def setup_class(cls):

        cls.weather = Weather()

    # 当前天气测试
    # 第一执行
    @allure.title("查询城市当前天气")
    @allure.description("验证天气系统可以正确返回城市当前天气信息")
    @pytest.mark.current
    @pytest.mark.order(1)
    @pytest.mark.parametrize(
        "weather_data",
        current_data
    )
    def test_current_weather(
            self,
            weather_data
    ):
        with allure.step("输入城市名称"):
            city = weather_data["city"]

        with allure.step("调用当前天气接口"):
            result = self.weather.get_current_weather(
                city
            )

        with allure.step("校验温度信息"):
            assert result["temperature"] == weather_data["temperature"]

        with allure.step("校验湿度信息"):
            assert result["humidity"] == weather_data["humidity"]

        with allure.step("校验风速信息"):
            assert result["wind_speed"] == weather_data["wind_speed"]

    @allure.title("查询城市历史天气")
    @allure.description("验证天气系统可以根据日期返回历史天气")
    @pytest.mark.history
    @pytest.mark.order(2)
    @pytest.mark.parametrize(
        "weather_data",
        history_data
    )
    def test_history_weather(
            self,
            weather_data
    ):
        with allure.step("输入城市和日期"):
            city = weather_data["city"]
            date = weather_data["date"]

        with allure.step("调用历史天气接口"):
            result = self.weather.get_history_weather(
                city,
                date
            )

        with allure.step("校验历史温度"):
            assert result["temperature"] == weather_data["temperature"]


    @allure.title("查询不存在城市")
    @allure.description("验证输入非法城市时系统返回异常")
    @pytest.mark.exception
    @pytest.mark.order(3)
    def test_invalid_city(self):
        with allure.step("输入不存在城市"):
            city = "火星"

        with allure.step("验证系统抛出异常"):
            with pytest.raises(
                    ValueError,
                    match="城市不存在"
            ):
                self.weather.get_current_weather(
                    city
                )