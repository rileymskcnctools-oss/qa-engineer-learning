import datetime
class Utils:
    now = datetime.datetime.now()

    @classmethod
    def current_date_time(cls):
        return cls.now

    @classmethod
    def current_date(cls):
        return cls.now.strftime("%Y-%m-%d")

    @classmethod
    def current_time(cls):
        return cls.now.strftime("%H-%M-%S")

    @classmethod
    def getYear(cls):
        return cls.now.year

    @classmethod
    def getMonth(cls):
        return cls.now.month

    @classmethod
    def getDay(cls):
        return cls.now.day


print(Utils.current_date_time())
print(Utils.current_date())
print(Utils.current_time())
print(Utils.getYear())
print(Utils.getMonth())
print(Utils.getDay())
