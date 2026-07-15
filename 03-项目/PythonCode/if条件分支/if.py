# student = "测试工程师"
# school = "hogwarts"
# # if else
# if school == "hogwarts":
#     print("霍格沃兹测试开发")
# else:
#     print("测试开发")

# food = input("请输入水果的类型:\n")

# if elif elif else  多条件选一
# if food == "apple":
#     print("你输入的是苹果")
# elif food == "banana":
#     print("你输入的是香蕉")
# elif food == "orange":
#     print("你输入的是橘子")
# else:
#     print("你触及了我翻译的盲区了:(")
#
name = input("请输入你的名字：\n")
hobby = int(input("请选择你擅长/喜欢的科目，文科选1，理科选2：\n"))
if hobby == 1:
    orientation_choose = int(input("请选择你想要的职业，历史选1，地理选2：\n"))
    if orientation_choose == 1:
        orientation = "历史"
    else:
        orientation = "地理"
else:
    orientation_choose = int(input("请选择你想从业的方向：数学选1，生物选2，编程选3\n"))
    if orientation_choose == 1:
        orientation = "数学"
    elif orientation_choose == 2:
        orientation = "生物"
    else:
        coder_choose = int(input("请选择你想从事的软件职业方向：测试选1，开发选2，产品选3，项目经理选4\n"))
        if coder_choose == 1:
            orientation = "测试"
        elif coder_choose == 2:
            orientation = "开发"
        elif coder_choose == 3:
            orientation = "产品"
        else:
            orientation = "项目经理"
print(f"{name} 同学，你意向的职业为: {orientation}")