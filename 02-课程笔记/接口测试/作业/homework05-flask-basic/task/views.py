from flask import request, jsonify

from . import task_blueprint

from database import task_db



# 创建任务
@task_blueprint.route(
    "/tasks/create",
    methods=["POST"]
)
def create_task():

    data = request.json


    task_id = str(len(task_db)+1)

    # 字典[key]
    task_db[task_id] = {

        "task_name": data.get("task_name"),

        "content": data.get("content")

    }


    return jsonify({

        "message": "任务创建成功",

        "task_id": task_id

    })



# 查看任务列表
@task_blueprint.route(
    "/tasks",
    methods=["GET"]
)
def get_tasks():

    return jsonify(task_db)



# 查看任务详情
@task_blueprint.route(
    "/tasks/<task_id>",
    methods=["GET"]
)
def get_task_detail(task_id):

    task = task_db.get(task_id)


    if task:

        return jsonify(task)


    return jsonify({

        "message": "任务不存在"

    })