import pytest
from bank_account import BankAccount

def setup_module():

    print("\n银行账户模块测试开始")

def teardown_module():

    print("\n银行账户模块测试结束")


class TestBankAccount:

    @classmethod
    def setup_class(cls):

        print("\n创建银行账户对象")

        cls.account = BankAccount(
            "Riley",
            1000
        )


    @classmethod
    def teardown_class(cls):
        print("\n银行账户测试结束")

    def setup_method(self):
        print("\n测试方法开始")

    def teardown_method(self):
        print("\n测试方法结束")

    # ========================
    # 测试存款
    # ========================

    @pytest.mark.parametrize(
        "balance,amount,expected",
        [
            (1000,50,1050),
            (0,200,200),
            (500,100,600)
        ]
    )
    def test_deposit(self,balance,amount,expected):

        account = BankAccount(
            "Tom",
            balance
        )

        result = account.deposit(amount)
        assert result == expected

    # ========================
    # 测试取款
    # ========================

    @pytest.mark.parametrize(
        "balance,amount,expected",
        [
            (100,50,50),
            (500,200,300),
            (1000,800,200)
        ]
    )
    def test_withdraw(self,balance,amount,expected):

        account = BankAccount(
            "Tom",
            balance
        )

        result = account.withdraw(amount)

        assert result == expected

    # ========================
    # 测试转账
    # ========================

    def test_transfer(self):

        account1 = BankAccount(
            "Tom",
            1000
        )

        account2 = BankAccount(
            "Jack",
            500
        )

        account1.transfer(
            account2,
            300
        )

        assert account1.balance == 700
        assert account2.balance == 800


    # ========================
    # 查询余额
    # ========================

    @pytest.mark.parametrize(
        "balance,expected",
        [
            (100,100),
            (500,500),
            (1000,1000)
        ]
    )
    def test_get_balance(self,balance,expected):
        account = BankAccount(
            "Tom",
            balance
        )

        result = account.get_balance()

        assert result == expected

    # ========================
    # 异常测试
    # ========================

    def test_withdraw_not_enough_money(self):
        account = BankAccount(
            "Tom",
            100
        )


        with pytest.raises(ValueError):

            account.withdraw(200)

