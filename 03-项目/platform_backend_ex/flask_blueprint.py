from flask import Blueprint, Flask

app = Flask(__name__)


# 蓝图声明
goods_router = Blueprint(
    name="goods",
    import_name=__name__
)

user_router = Blueprint(
    name="user",
    import_name=__name__,
    url_prefix="/user"
)


# 商品接口
@goods_router.route("/")
def index():
    return {
        "code": 0,
        "msg": "get success",
        "data": []
    }


@goods_router.route("/add", methods=["POST"])
def add_goods():
    return {
        "code": 0,
        "msg": "add success"
    }


# 用户接口
@user_router.route("")
def user_index():
    return {
        "code": 0,
        "msg": "user_get success",
        "data": [111]
    }


@user_router.route("/login", methods=["POST"])
def login():
    return {
        "code": 0,
        "msg": "login success"
    }


if __name__ == "__main__":
    app.register_blueprint(goods_router)
    app.register_blueprint(user_router)

    app.run(
        port=5055,
        debug=True
    )