#!flask/bin/python
from flask import Flask, jsonify
from flask import request
import sql

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 让支持jsonify中文

mysql = sql.sql()


@app.route('/login', methods=['GET'])
def login():
    if 'user_id' not in request.args:
        result = {'code': '1003', 'msg': ' login error'}
        return jsonify(result)
    result = mysql.login(request.args)
    return jsonify(result)


@app.route('/get_user_info')
def get_user_info():
    if 'user_id' not in request.args:
        result = {'code': '1030', 'msg': 'invaild params'}
    else:
        result = mysql.get_user_info(request.args)
    return jsonify(result)


@app.route('/get_slide_images')
def get_slide_images():
    result = mysql.get_slide_images()
    if not result:
        result = {'code': '1004', 'msg': 'get slide images error'}
    return jsonify(result)


@app.route('/create_group')
def create_group():
    if 'user_id' not in request.args or \
                    'group_intro' not in request.args or \
                    'money' not in request.args or \
                    'limit_num' not in request.args or \
                    'duration' not in request.args or \
                    'type' not in request.args:
        result = {'code': '1005', 'msg': 'invaild params'}
        result = jsonify(request)
    else:
        result = mysql.create_group(request.args)

    return jsonify(result)


@app.route('/get_my_groups')
def get_my_groups():
    if 'user_id' not in request.args:
        result = {'code': '1008', 'msg': 'params error'}
    else:
        result = mysql.get_my_groups(request.args)

    return jsonify(result)


@app.route('/get_recommend_groups')
def get_recommend_groups():
    if 'user_id' not in request.args:
        result = {'code': '1024', 'msg': 'params error'}
    else:
        result = mysql.get_recommend_groups(request.args)
    return jsonify(result)


@app.route('/join_group')
def join_group():
    if 'user_id' not in request.args or \
                    'group_id' not in request.args:
        result = {'code': '1027', 'msg': 'params error'}
    else:
        result = mysql.join_group(request.args)
    return jsonify(result)


@app.route('/commit_daka')
def commit_daka():
    if 'user_id' not in request.args or \
                    'group_id' not in request.args:
        result = {'code': '1011', 'msg': 'params error'}
    else:
        result = mysql.commit_daka(request.args)
    return jsonify(result)


@app.route('/commit_appeal')
def commit_appeal():
    if 'group_id' not in request.args or \
                    'user_id' not in request.args or \
                    'date' not in request.args:
        result = {'code': '1014', 'msg': 'params error'}
    else:
        result = mysql.commit_appeal(request.args)
    return jsonify(result)


@app.route('/get_my_appeal')
def get_my_appeal():
    if 'user_id' not in request.args:
        result = {'code': '1016', 'msg': 'params error'}
    else:
        result = mysql.get_my_appeal(request.args)
    return jsonify(result)


@app.route('/get_others_daka_info')
def get_others_daka_info():
    if 'user_id' not in request.args:
        result = {'code': '1023', 'msg': 'params error'}
    else:
        result = mysql.get_others_daka_info(request.args)
    return jsonify(result)


@app.route('/commit_judgement')
def commit_judgement():
    if 'user_id' not in request.args or \
                    'group_id' not in request.args or \
                    'date' not in request.args or \
                    'assessor_id' not in request.args or \
                    'is_passed' not in request.args:
        result = {'code': '1019', 'msg': 'invaild params'}
    else:
        result = mysql.commit_judgement(request.args)
    return jsonify(result)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
