import requests 
import json
def classify(text):
    r = requests.post('http://localhost:6060/api', json={'id': '1', 'jsonrpc': '2.0', 'method': 'classify', 'params':[text]})
    topic = json.loads(r.text)['result']
    print("Topic: {}".format(str(topic)))
    return topic