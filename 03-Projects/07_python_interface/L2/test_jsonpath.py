import requests
import jsonpath

def test_jsonpath():
    # 定义接口的 url
    url = "https://httpbin.ceshiren.com/post"
    # 定义一个变量，存放请求体信息
    req_body = {'teacher': 'ad','school':'hogwarts'}
    # 通过json 关键字传递请求体信息
    r = requests.post(url, json=req_body)
    # 打印接口响应的头信息，即返回的响应头信息
    # print(r.json()["headers"]["Content-Type"])

    # jsonpath返回值找不到返回 False
    assert jsonpath.jsonpath(r.json(),"$..Content-Type111")==False
    # jsonpath返回值找到返回列表
    assert jsonpath.jsonpath(r.json(), "$..Content-Type")


