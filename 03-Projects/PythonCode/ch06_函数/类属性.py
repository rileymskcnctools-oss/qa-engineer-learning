# 定义一个饮水机类
# class WaterDispenser:
#     # 剩余水量
#     surplus_water = 1500
#     # 出水口
#     def water_outlet(self, n):
#         WaterDispenser.surplus_water -= n
#         print("剩余水量：", WaterDispenser.surplus_water)
#
# wd1 = WaterDispenser()
# wd2 = WaterDispenser()
#
# wd1.water_outlet(100)
# print(wd1.surplus_water)
# wd2.water_outlet(200)
# print(wd2.surplus_water)
# print(WaterDispenser.surplus_water)


# 定义一个饮水机类
class WaterDispenser:
    # 剩余水量
    surplus_water = 1500
    # 出水口
    def water_outlet(self, n):
        WaterDispenser.surplus_water -= n
        print("剩余水量：", WaterDispenser.surplus_water)

wd1 = WaterDispenser()
wd2 = WaterDispenser()

wd1.water_outlet(100)
print(wd1.surplus_water)
wd2.water_outlet(200)
print(wd2.surplus_water)
print(WaterDispenser.surplus_water)

