# center() 返回一个原字符串居中,并使用空格填充至长度 width 的新字符串，
# 如果指定 fillchar 参数，则使用指定字符填充，fillchar 参数长度只能为 1
# print("|"+"hogworts".center(20) + "|")
# print("|"+"hogworts".center(5) + "|")
# print("|"+"hogworts".center(20, "-") + "|")
# print("*"*20)
# print("|"+"hogworts".ljust(20) + "|")
# print("|"+"hogworts".ljust(5) + "|")
# print("|"+"hogworts".ljust(20, "-") + "|")
# print("*"*20)
# print("|"+"hogworts".rjust(20) + "|")
# print("|"+"hogworts".rjust(5) + "|")
# print("|"+"hogworts".rjust(20, "-") + "|")

# strip() 删除 string 左右两侧的空白字符
# print("|" + "  hogworts  " + "|")
# print("|" + "  hogworts  ".strip() + "|")
# print("|" + "  hogworts".strip() + "|")
# print("|" + "hogworts  ".strip() + "|")
# print("|" + "  h o g w o r t s  ".strip() + "|")
# print("|" + "bachogwortsabc".strip("cba") + "|")

# split() 以 sep 为分隔符分割 string ，如果指定 maxsplit 参数，则仅分割 maxsplit 次
# print("a-b-c-d".split("-"))
# print("a-b-c-d".split("-", 2))
# print("a--b-c-d".split("-"))
# print("a-+b-c-d".split("-+"))
# print("a b\tc\nd\re".split())
# print("a b c d e".split(" ", 3))

# splitlines() 使用换行符\n分割 string，如果指定 keepends 参数，则结果中会保留\n符号
# print("a\nb\nc".splitlines())
# print("a\nb\nc".splitlines(True))
print("*"*20)
# 字符串分割 只分三段 partition()
# print("This is Hogworts".partition("is"))
# print("This is Hogworts".partition("iss"))
# print("*"*20)
# # 字符串分割 只分三段 从右侧分rpartition()
# print("This is Hogworts".rpartition("is"))
# print("This is Hogworts".rpartition("iss"))
# # 字符串连接方法join()
# print("".join(("a","b","c")))
# print("-".join("hello"))
# print("->".join(("a","b","c")))
# print("->".join(["a","b","c"]))
# print("->".join({"a","b","c"}))
# print("->".join({"a":"A","b":"B","c":"C"}))

# print("abc123".encode("gbk"))
# print("你好".encode("gbk"))
#
# print("abc123".encode("utf-8"))
# print("你好".encode("u8"))
#
# s1 = b'\xc4\xe3\xba\xc3'
# s2 = b'\xe4\xbd\xa0\xe5\xa5\xbd'
# print(s1.decode("gbk"))
# print(s2.decode("utf-8"))


s = "abcdefg"

# 普通切片
print(s[0: 2])
# 省略范围
print(s[0:])
print(s[: 2])
print(s[:])
# 指定步长
print(s[::1])
print(s[::2])
# 负下标
print(s[-3: -1])
# 负步长
print(s[-1: -3: -1])
# 逆序
print(s[::-1])
