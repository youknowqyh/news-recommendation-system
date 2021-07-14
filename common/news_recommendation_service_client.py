from flask_jsonrpc.proxy import ServiceProxy
server = ServiceProxy('http://localhost:5050/api')

def getPreferenceForUser(userId):
    preference = server.getPreferenceForUser(userId)['result']
    print("Preference list: {}".format(str(preference)))
    return preference