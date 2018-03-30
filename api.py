#!flask/bin/python
from flask import Flask, jsonify
from flask import request
import sql

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 让支持jsonify中文

mysql = sql.sql()


@app.route('/login', methods=['GET'])
def login():
    user_id = request.args['user_id']
    result = mysql.login(user_id)
    if not result:
        result = {'code': '1003', 'msg': ' login error'}
    print(result)
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
        return jsonify(request)

    result = mysql.create_group(request.args)
    return jsonify(result)
    # return str(request)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
