import os
import sys
import json

from bson.json_util import dumps
from flask import Flask
from flask_jsonrpc import JSONRPC

sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'common'))
import mongodb_client

import operations

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

SERVER_HOST = 'localhost'
SERVER_PORT = 4040

@jsonrpc.method('index')
def index() -> str:
	return 'Welcome to Flask JSON-RPC'
@jsonrpc.method('add')
def add(a: int, b: int) -> int:
    """ Test method """
    print("add is called with %d and %d" % (a, b))
    return a + b
@jsonrpc.method('getNews')
def getNews() -> list:
    db = mongodb_client.get_db()
    news = list(db['news'].find())
    return json.loads(dumps(news))
@jsonrpc.method('getNewsSummariesForUser')
def getNewsSummariesForUser(user_id: str, page_num: str) -> list:
    """Get news summary from mongodb"""
    return operations.getNewsSummariesForUser(user_id, page_num)
@jsonrpc.method('logNewsClickForUser')
def logNewsClickForUser(user_id:str, news_id:str) -> None:
    """Log user news clicks"""
    print(user_id)
    return operations.logNewsClickForUser(user_id, news_id)
if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)


# class RequestHandler(pyjsonrpc.HttpRequestHandler):
#     """ Test method """
#     @pyjsonrpc.rpcmethod
#     def add(self, a, b):
#         print("add is called with %d and %d" % (a, b))
#         return a + b

#     @pyjsonrpc.rpcmethod
#     def getNews(self):
#         db = mongodb_client.get_db()
#         news = list(db['news'].find())
#         return json.loads(dumps(news))

# http_server = pyjsonrpc.ThreadingHttpServer(
#     server_address = (SERVER_HOST, SERVER_PORT),
#     RequestHandlerClass = RequestHandler
# )

# print("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))

# http_server.serve_forever()