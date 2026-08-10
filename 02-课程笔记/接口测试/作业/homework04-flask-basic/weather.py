from flask import Flask, jsonify

app = Flask(__name__)

# 解决中文JSON转义
app.json.ensure_ascii = False
@app.route("/")
def index():
    return "霍格沃兹天气查询平台"


@app.route("/weather")
def show_weather():

    data = {
        "city": "济南",
  "date": "2022-05-05",
  "week": "星期四",
  "update_time": "22:38",
  "wea": "多云",
  "wea_img": "yun",
  "tem": "25",
  "tem_day": "30",
  "tem_night": "23",
  "win": "南风",
  "win_speed": "3级",
  "win_meter": "19km/h",
  "air": "53",
  "pressure": "987",
  "humidity": "27%"
    }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True,port=5050)