class BankAccount:

    def __init__(self, owner, balance=0):
        """
        初始化账户

        owner: 用户名
        balance: 初始余额
        """

        self.owner = owner
        self.balance = balance

    # 存款
    def deposit(self, amount):

        if amount <= 0:
            raise ValueError("存款金额必须大于0")

        self.balance += amount

        return self.balance

    # 取款
    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError("取款金额必须大于0")


        if amount > self.balance:
            raise ValueError("余额不足")


        self.balance -= amount

        return self.balance


    # 转账
    def transfer(self, other_account, amount):

        if amount <= 0:
            raise ValueError("转账金额必须大于0")


        if amount > self.balance:
            raise ValueError("余额不足")


        self.balance -= amount

        other_account.balance += amount

    # 查询余额
    def get_balance(self):

        return self.balance