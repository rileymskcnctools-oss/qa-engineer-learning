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
    @pytest.mark.current
    @pytest.mark.order(1)
    @pytest.mark.parametrize(
        "weather_data", # 每次执行测试函数传入的变量名
        current_data    # 变量列表
    )
    def test_current_weather(
            self,
            weather_data
    ):


        result = self.weather.get_current_weather(
            weather_data["city"]
        )


        assert result["temperature"] == weather_data["temperature"]

        assert result["humidity"] == weather_data["humidity"]

        assert result["wind_speed"] == weather_data["wind_speed"]




    # 历史天气测试
    @pytest.mark.history
    @pytest.mark.order(2)
    @pytest.mark.parametrize(
        "weather_data",  # 每次执行测试函数传入的变量名
        history_data     # 变量列表
    )
    def test_history_weather(
            self,
            weather_data
    ):


        result = self.weather.get_history_weather(
            weather_data["city"],
            weather_data["date"]
        )


        assert result["temperature"] == weather_data["temperature"]




    # 异常测试
    @pytest.mark.exception
    @pytest.mark.order(3)
    def test_invalid_city(self):
        with pytest.raises(
                ValueError,
                match="城市不存在"
        ):
            self.weather.get_current_weather(
                "火星"
            )

