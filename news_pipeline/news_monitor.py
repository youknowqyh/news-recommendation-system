import hashlib
import os
import sys
import redis 
import datetime
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

SCRAPE_NEWS_TASK_QUEUE_URL = "amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml"
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrape-news-task-queue"

NEWS_SOURCES = [
    'cnn, bbc-news, bloomberg, espn, cnbc, business-insider, abc-news, buzzfeed, bbc-sport, fox-news, the-verge, techradar, talksport, nfl-news, nhl-news, reddit-r-all'
    ]
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECONDS = 60

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQPClient = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    try:
        news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    except Exception as e:
        print(e)
        pass
    
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

        if redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            redis_client.set(news_digest, json.dumps(news))
            redis_client.expire(str(news), NEWS_TIME_OUT_IN_SECONDS)

            
            cloudAMQPClient.sendMessage(news)

    print("Fetched {} new news".format(num_of_new_news))

    cloudAMQPClient.sleep(SLEEP_TIME_IN_SECONDS)

