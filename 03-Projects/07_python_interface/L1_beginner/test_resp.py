import requests


def test_res():
    r=requests.get("https://httpbin.ceshiren.com/get")
    r.status_code == 200   # 判断返回状态码是否为 200
    # r.headers
    # print("==========字典，响应头的所有信息=============")
    # print(r.headers)
    # print("==========编码后的请求 URL=============")
    # print(r.url)
    # print("==========HTTP 响应状态码=============")
    # print(r.status_code)
    # print("==========响应内容（字节流）=============")
    # print(r.content)
    # print("==========响应内容（字符串）=============")
    # print(r.text)