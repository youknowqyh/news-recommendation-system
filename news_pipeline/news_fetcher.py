import os
import sys
from newspaper import Article
from newspaper.configuration import Configuration

proxies={'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}


config = Configuration()
config.proxies = proxies


sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper

from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'dedupe-news-task-queue'
SCRAPE_NEWS_TASK_QUEUE_URL = 'amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml'
SCRAPE_NEWS_TASK_QUEUE_NAME = "scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print("message is broken")
        return
    
    task = msg
    article = Article(task['url'], config=config)
    article.download()
    article.parse()
    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)

    # if task['source']['name'] == 'CNN':
    #     print("Scraping CNN news")
    #     text = cnn_news_scraper.extract_news(task['url'])
    # else:
    #     print("not supported")
    # task['text'] = text

while True:
    # Fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message: scrape news from websites
            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

