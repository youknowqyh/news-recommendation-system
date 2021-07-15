import requests 
import json
# The ServiceProxy was removed from the code base, you can copy from here and use it.
def getPreferenceForUser(userId):
    r = requests.post('http://localhost:5050/api', json={'id': '1', 'jsonrpc': '2.0', 'method': 'getPreferenceForUser', 'params':[userId]})
    preference = json.loads(r.text)['result']
    print("Preference list: {}".format(str(preference)))
    return preference
getPreferenceForUser('test')