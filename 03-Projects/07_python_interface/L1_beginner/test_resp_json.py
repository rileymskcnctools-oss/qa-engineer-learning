import requests
def test_res_json():
    # 响应体断言 = 验证返回数据是否符合预期
    r = requests.get("https://httpbin.ceshiren.com/get")
    print(type(r.json()))
    assert r.status_code == 200
    # r.json()转成对象，再取字段
    assert r.json()["url"] == "https://httpbin.ceshiren.com/get"   # 断言顶层字段
    assert r.json()["headers"]["Host"] == "httpbin.ceshiren.com"   # 断言嵌套字段

def test_res_json_fail():
    r = requests.get("https://www.baidu.com/")
    # print(r.text)
    # print(r.json()) 如果响应体是非JSON 不能用r.json()转成对象，用r.text即可
    assert r.status_code == 200