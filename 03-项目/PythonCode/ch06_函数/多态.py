class Father:
    def cure(self):
        print("使用中医方法治疗。。。")

class Son(Father):
    def cure(self):
        print("使用西医方法治疗。。。")

class Patient:
    def needDoctor(self, doctor):
        doctor.cure()               # 不管什么医生，都调 cure()

patient = Patient()
patient.needDoctor(Father())        # 使用中医方法治疗。。。
patient.needDoctor(Son())           # 使用西医方法治疗。。。