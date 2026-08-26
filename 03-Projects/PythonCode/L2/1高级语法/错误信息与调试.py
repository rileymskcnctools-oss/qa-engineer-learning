def getInputData():
    print("input run")
    n = int(input("请输入一个数字:"))  #在根源解决错误
    msg = input("请输入一个字符串信息:")
    return n,msg

def outputData(n,msg):
    print("output run")
    for i in range(n):
        print("output forin run")
        print(msg)

if __name__ == '__main__':
    # print("main1")
    n,msg = getInputData()
    # print("main3")
    outputData(n, msg)
    # print("main2")
    # print 辅助找出错代码范围