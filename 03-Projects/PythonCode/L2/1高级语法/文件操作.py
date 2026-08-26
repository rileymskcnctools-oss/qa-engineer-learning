# # 打开文件
# file=open("data.txt","w")
#
# length=file.write("print('hello riley')\n")
# print(f"成功写入{length}个字节")
# datas=["aaaaa\n","bbbbb\n","ccccc\n"]
# file.writelines(datas)

# 打开文件
file=open("data.txt","r")
# content=file.write("eeeee")
# content=file.read(10)
# print(content,end="")
# content=file.read(100)
# print(content)
# content=file.readline(9)
# print(content)
# content=file.readline()
# print(content)

content=file.readlines()
print(content)
# 文件关闭
file.close()

# 上下文管理器 with
with open("data.txt","r") as f:
    content=f.read(20)
    print(content)


