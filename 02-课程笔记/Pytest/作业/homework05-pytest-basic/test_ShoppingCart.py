import pytest
from shopping import ShoppingCart, Product



# ===========================
# 模块级 setup teardown
# ===========================

def setup_module():

    print("\n购物车模块测试开始")


def teardown_module():

    print("\n购物车模块测试结束")



# ===========================
# 测试类
# ===========================

class TestShoppingCart:


    # 类级setup
    @classmethod
    def setup_class(cls):

        print("\n创建购物车测试环境")


    @classmethod
    def teardown_class(cls):

        print("\n购物车测试类结束")



    # 方法级setup
    def setup_method(self):

        print("\n创建新的购物车")
        self.cart = ShoppingCart()


    # 方法级teardown
    def teardown_method(self):

        print("\n清理购物车")
        self.cart.items.clear()
        # 变量.属性



    # ===========================
    # 添加商品测试
    # ===========================

    @pytest.mark.parametrize(
        "name,price,expected_count",
        [
            ("手机",5999,1),
            ("耳机",299,1),
            ("电脑",6999,1)
        ]
    )
    def test_add_item(
            self,
            name,
            price,
            expected_count
    ):


        self.cart.add_item(
            name,
            price
        )


        assert len(self.cart.items) == expected_count



    # ===========================
    # 删除商品测试
    # ===========================

    @pytest.mark.parametrize(
        "name,price,remove_name,expected_count",
        [
            ("手机",5999,"手机",0),
            ("耳机",299,"耳机",0),
            ("电脑",6999,"电脑",0)
        ]
    )
    def test_remove_item(
            self,
            name,
            price,
            remove_name,
            expected_count
    ):


        # 添加商品
        self.cart.add_item(
            name,
            price
        )


        # 删除商品
        self.cart.remove_item(
            remove_name
        )


        # 断言
        assert len(self.cart.items) == expected_count



    # ===========================
    # 计算总价测试
    # ===========================

    def test_calculate_total(self):

        self.cart.add_item(
            "手机",
            5999
        )

        self.cart.add_item(
            "耳机",
            299
        )
        result = self.cart.calculate_total()
        assert result == 6298