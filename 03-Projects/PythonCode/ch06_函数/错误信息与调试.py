def getInputData():
    print("input run")
    n = input("请输入一个数字:")
    msg = input("请输入一个数据:")
    return n,msg

def outputData(n,msg):
    print("output run")
    for i in range(n):
        print("output forin run")
        print(msg)

if __name__ == '__main__':
    n,msg = getInputData()
    outputData(n, msg)
