import os
import sys
import datetime
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import news_topic_modeling_service_client

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'dedupe-news-task-queue'

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = 'news'

SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = str(task['text'])
    if text is None:
        return
    # Get recent news from mongodb
    published_at = parser.parse(task['publishedAt'])
    print(published_at)
    published_at_day_begin = published_at - datetime.timedelta(days=1)
    print(published_at_day_begin)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=2)
    print(published_at_day_end)

    db = mongodb_client.get_db()
    recent_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte':published_at_day_begin, '$lt': published_at_day_end}}))
    print(len(recent_news_list))

    if recent_news_list is not None and len(recent_news_list) > 0:
        documents = [str(news['text']) for news in recent_news_list]
        documents.insert(0, text)

        # Calculate similarity
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(documents)

        pairwise_sim = X * X.T
        print(pairwise_sim.A)
        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD :
                # Dupilicated news
                print("Dupilicated news, ignore")
                return 
    task['publishedAt'] = parser.parse(task['publishedAt'])
    # Classify news
    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if dedupe_news_queue_client is not None:
        msg = dedupe_news_queue_client.getMessage()
        if msg is not None:
            # Parse
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass 
    
        dedupe_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)