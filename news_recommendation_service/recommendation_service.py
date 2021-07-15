import operator
import os
import sys
import math
from flask import Flask
from flask_jsonrpc import JSONRPC

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"

SERVER_HOST = 'localhost'
SERVER_PORT = 5050

# Flask application
app = Flask(__name__)

# Flask-JSONRPC
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@jsonrpc.method('getPreferenceForUser')
def getPreferenceForUser(user_id:str)->list:
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':user_id})
    print(model)
    if model is None:
        return []
    sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]
	
    # If the first preference is close to the last one, return empty
    if math.isclose(float(sorted_value_list[0]), float(sorted_value_list[-1]), rel_tol=1e-5):
        return []
    print(sorted_list)
    return sorted_list

if __name__ == '__main__':
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)