import flask, json
from flask import request
from flask_cors import CORS
import sys

import house_service
import user_service

house_service.get_collection()
server = flask.Flask(__name__)
CORS(server)

# test service
@server.route('/test', methods=['get'])
def test_call():
    resu = {'code': 200, 'message': 'hello world.'}
    return json.dumps(resu, ensure_ascii=False)

# get houses by bounds
# data: {'bounds': []}
@server.route('/searchHouses', methods=['post'])
def search_houses():
    # print('search houses', file=sys.stdout)
    # print(request.data, file=sys.stdout)
    data = request.data
    bounds = json.loads(data, encoding='utf-8')['bounds']
    if bounds:
        r = house_service.get_houses(bounds)
        resu = {'code': 200, 'message': 'ok', 'data': r}
        return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 10001, 'message': 'Invalid data. Usage: data: {"bounds": []}'}
        return json.dumps(resu, ensure_ascii=False)


if __name__ == '__main__':
    server.run(debug=True, port=8888, host='0.0.0.0') # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问