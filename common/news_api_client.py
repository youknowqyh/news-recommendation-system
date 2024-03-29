import requests
from json import loads

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/'
NEWS_API_KEY = '7be565cd32a64210831fc6de6eeeb923'
TOP_HEADLINES_API = 'top-headlines'

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

# If you are in regions that are have access to newsapi.org, you can delete the following line.
proxies={'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=TOP_HEADLINES_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, pageSize=100):
    articles = []
    for source in sources:
        payload = {'apiKey' : NEWS_API_KEY,
                   'sources' : source,
                   'pageSize' : pageSize}
        response = requests.get(buildUrl(), params=payload, proxies=proxies)
        res_json = loads(response.content)
        # Extract info from response
        if (res_json is not None and res_json['status'] == 'ok'):
            articles.extend(res_json['articles'])
            
    return articles