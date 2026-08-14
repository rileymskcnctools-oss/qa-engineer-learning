# s = "Hello Hogworts!"  遍历字符串
# for c in s:
#     print(f"字符【 {c} 】的ASCII码为：【 {ord(c)} 】")

# t = (1,2,3,4,5)  遍历元组
# for n in t:
#     print(f"数字【 {n} 】的立方值为：【 {n**2} 】")

# requestMethods = ["get", "post", "put", "delete", "patch", "header", "options", 'trace'] 遍历列表
# for method in requestMethods:
#     print(f"请求方式【 {method} 】转换为大写后：【 {method.upper()} 】")

# requestMethods = {
#                     "get": "用于获取服务器上的资源，通过在URL中传递参数来发送请求。",
#                     "post": "用于向服务器提交数据，一般用于创建新的资源或进行修改操作。",
#                     "put": "用于更新服务器上的资源，一般用于修改已存在的资源的全部内容。",
#                     "delete": "用于删除服务器上的资源。"
#                 }  遍历字典 可结合keys() values() 使用
# for method in requestMethods.values():
#     print(method)

# 解包操作
requestMethods = {
                    "get": "用于获取服务器上的资源，通过在URL中传递参数来发送请求。",
                    "post": "用于向服务器提交数据，一般用于创建新的资源或进行修改操作。",
                    "put": "用于更新服务器上的资源，一般用于修改已存在的资源的全部内容。",
                    "delete": "用于删除服务器上的资源。"
                }
for key, value in requestMethods.items():
    print(f"请求方式【 {key} 】的作用为：【 {value} 】")