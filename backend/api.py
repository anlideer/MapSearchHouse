import flask, json
from flask import request
from flask_cors import CORS
import sys

import house_service
import user_service

house_service.get_collection()
user_service.get_collection()
server = flask.Flask(__name__)
CORS(server)    # 跨域设置

# # test service
# @server.route('/test', methods=['get'])
# def test_call():
#     resu = {'code': 200, 'message': 'hello world.'}
#     return json.dumps(resu, ensure_ascii=False)

# data: {'locationName': ''}
@server.route('/getHouseList', methods=['post'])
def getHouseList():
    data = request.data
    location_name = json.loads(data, encoding='utf-8')['locationName']
    if location_name:
        r = house_service.get_house_list(location_name)
        print(r, file=sys.stdout)
        resu = {'code': 200, 'message': 'ok', 'data': r}
        return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 10001, 'message': 'Invalid data. Usage: data: {"locationName": ""}'}
        return json.dumps(resu, ensure_ascii=False)        

# data: {'username': '', password: ''}
@server.route('/register', methods=['post'])
def register():
    data = request.data
    form_data = json.loads(data, encoding='utf-8')
    uname = form_data['username']
    pw = form_data['password']
    r = user_service.register(uname, pw)
    resu = {}
    if r == 1:
        resu = {'code': 200, 'message': 'ok'}
    else:
        resu = {'code': 10001, 'message': 'username existed'}
    return json.dumps(resu, ensure_ascii=False)

# data : {'username': '', 'paasword': ''}
@server.route('/login', methods=['post'])
def login():
    data = request.data
    form_data = json.loads(data, encoding='utf-8')
    uname = form_data['username']
    pw = form_data['password']
    r = user_service.login(uname, pw)
    resu = {}
    if r == 1:
        resu = {'code':200, 'message': 'ok'}
    else:
        resu = {'code': 10001, 'message': 'fail'}
    return json.dumps(resu, ensure_ascii=False)

# # get houses by bounds
# # data: {'bounds': []}
# @server.route('/searchHouses', methods=['post'])
# def search_houses():
#     # print('search houses', file=sys.stdout)
#     # print(request.data, file=sys.stdout)
#     data = request.data
#     bounds = json.loads(data, encoding='utf-8')['bounds']
#     if bounds:
#         r = house_service.get_houses(bounds)
#         resu = {'code': 200, 'message': 'ok', 'data': r}
#         return json.dumps(resu, ensure_ascii=False)
#     else:
#         resu = {'code': 10001, 'message': 'Invalid data. Usage: data: {"bounds": []}'}
#         return json.dumps(resu, ensure_ascii=False)

# # get all houses
# @server.route('/getAll', methods=['get'])
# def get_all():
#     resu = {'code': 200, 'message': 'ok', 'data': house_service.get_all_houses()}
#     return json.dumps(resu, ensure_ascii=False)


if __name__ == '__main__':
    server.run(debug=True, port=8888, host='0.0.0.0') # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问