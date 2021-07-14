import os
import sys
import redis
import random
import pickle
import json

from bson.json_util import dumps
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client

# from cloudAMQP_client import CloudAMQPClient
# import news_recommendation_service_client

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TABLE_NAME = 'news'
# CLICK_LOGS_TABLE_NAME = 'click_logs'

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIMEOUT_IN_SECONDS = 600

# LOG_CLICK_TASK_QUEUE_HOST = 'localhost'
# LOG_CLICK_TASK_QUEUE_NAME = "log-click-task-queue"

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
# click_queue_client = RabbitMQClient(LOG_CLICK_TASK_QUEUE_HOST, LOG_CLICK_TASK_QUEUE_NAME)


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    if page_num <= 0:
        raise ValueError('page_num should be a positive integer.')
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # The news list to be returned
    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, return empty list
        # If end_index is out of range, return all remaining news
        sliced_news_digests = news_digests[begin_index: end_index]
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        db = mongodb_client.get_db()
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))

        total_news_digests = list(map(lambda x:x['digest'], total_news))
        print(total_news_digests)
        redis_client.set(user_id, pickle.dumps(total_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIMEOUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    # topPreference = None

    # if preference is not None and len(preference) > 0:
    #     topPreference = preference[0]
    
    # for news in sliced_news:

    #     if news['class'] == topPreference:
    #         news['reason'] = 'Recommend'
    #     if news['publishedAt'].date() == datetime.today().date():
    #         news['time'] = 'today'
    return json.loads(dumps(sliced_news))