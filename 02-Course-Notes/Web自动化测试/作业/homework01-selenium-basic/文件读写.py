# 1. 写入文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("文件第一行\n")
    f.write("写入文件第二行内容\n")
    f.write("文件写入结束")

# 2. 读取文件
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 3. 显示读取到的内容
print(content)


# with open("aaa.txt","w", encoding="utf-8") as f:
#     f.writelines("AAAAAAAAAAAAA\nBBBBBBBBBBBBBB\n")
# with open("aaa.txt","r", encoding="utf-8") as f:
#     print(f.readlines())