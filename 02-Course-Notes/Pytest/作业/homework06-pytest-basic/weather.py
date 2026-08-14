class Weather:

    def __init__(self):
        pass


    def get_current_weather(self, city):

        # 模拟调用天气接口
        if city == "北京":

            return {
                "city": "北京",
                "temperature":25,
                "humidity":60,
                "wind_speed":10
            }


        elif city == "上海":

            return {
                "city":"上海",
                "temperature":28,
                "humidity":70,
                "wind_speed":8
            }


        else:

            raise ValueError(
                "城市不存在"
            )



    def get_history_weather(
            self,
            city,
            date
    ):


        if city not in ["北京","上海"]:

            raise ValueError(
                "城市不存在"
            )


        return {

            "city":city,

            "date":date,

            "temperature":20,

            "humidity":50,

            "wind_speed":5
        }


