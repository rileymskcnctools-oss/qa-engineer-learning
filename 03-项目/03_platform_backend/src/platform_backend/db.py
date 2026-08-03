from pymysql import Connect
from pymysql.cursors import DictCursor


# 发起连接
def get_connect():
    return Connect(
        host="mysql.hogwarts.ceshiren.com",
        port=3306,
        user="stu",
        password="hogwarts_stu",
        database="hogwarts_stu",
        charset="utf8"
    )


# # 创建游标
# # cursor = db_connect.cursor() # 默认元祖游标
# cursor = db_connect.cursor(DictCursor)
# # 执行sql
# cursor.execute("select *  from student_0802;")
# # 获取所有数据
# datas = cursor.fetchall()
#
# cursor.close()
# db_connect.close()
# print(datas)
def query_all(sql: str, params=None):
    # 获取所有的数据
    conn = get_connect()
    try:
        # 创建游标
        cursor = conn.cursor(DictCursor)
        try:
            # 执行sql
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
    except Exception as e:
        print("发生错误")
        raise
    finally:
        conn.close()


def query_one(sql: str, params=None):
    # 获取单条数据
    conn = get_connect()
    try:
        # 创建游标，返回值是字典，默认为元组
        cursor = conn.cursor(DictCursor)
        try:
            # 执行sql
            cursor.execute(sql, params)
            return cursor.fetchone()
        finally:
            cursor.close()
    except Exception as e:
        print("发生错误")
        raise
    finally:
        conn.close()


def execute(sql: str, params=None):
    # 执行其他语句
    conn = get_connect()
    try:
        # 创建游标
        cursor = conn.cursor()
        try:
            # 执行sql
            rows = cursor.execute(sql, params)
            # 提交数据
            conn.commit()
            return rows
        finally:
            cursor.close()
    except Exception as e:
        print("发生错误")
        # 回滚数据
        conn.rollback()
        raise
    finally:
        conn.close()