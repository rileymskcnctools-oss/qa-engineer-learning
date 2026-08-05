class Product:

    def __init__(self,name,price):

        self.name = name
        self.price = price

    def get_info(self):
        return f"name:{self.name},price:{self.price}"



class ShoppingCart:

    def __init__(self):
        self.items = []
        # items 是一个存放商品对象的列表

    def add_item(self,name,price):

        product = Product(name, price)
        self.items.append(product)

    def remove_item(self,name):
        for item in self.items:
            if item.name == name:
                self.items.remove(item)

    def calculate_total(self):
        total = 0
        # price 是商品的属性，访问方式--对象.属性名
        for item in self.items:
            total += item.price
        return total

    def clear_cart(self):
        self.items.clear()