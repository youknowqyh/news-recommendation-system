import operations
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

CLICK_LOGS_TABLE_NAME = 'click_logs'
LOG_CLICK_TASK_QUEUE_URL = 'amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml'
LOG_CLICK_TASK_QUEUE_NAME = "log-click-task-queue"

click_queue_client = CloudAMQPClient(LOG_CLICK_TASK_QUEUE_URL, LOG_CLICK_TASK_QUEUE_NAME)


def test_getNewsSummariesForUser_basic():
    news = operations.getNewsSummariesForUser('test', 1)
    assert len(news) > 0
    print("basic test passed!")

def test_getNewsSummariesForUser_pagination():
    news_page_1 = operations.getNewsSummariesForUser('test', 1)
    news_page_2 = operations.getNewsSummariesForUser('test', 2)
    print(len(news_page_2))

    assert len(news_page_1) > 0
    assert len(news_page_2) > 0

    # Assert that there's no duplication in two pages
    digests_page_1_set = set(list(map(lambda x: x['digest'], news_page_1)))
    digests_page_2_set = set(list(map(lambda x: x['digest'], news_page_2)))
    print(digests_page_1_set)
    print(digests_page_2_set)
    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0
    print("pagination test passed!")


def test_logNewsClickForUser_basic():
    db = mongodb_client.get_db()
    
    db[CLICK_LOGS_TABLE_NAME].delete_many({"userId": "test"})

    operations.logNewsClickForUser('test', 'test_news')
    record = list(db[CLICK_LOGS_TABLE_NAME].find().sort([('timestamp', -1)]).limit(1))[0]

    assert record is not None
    assert record['userId'] == 'test'
    assert record['newsId'] == 'test_news'
    assert record['timestamp'] is not None

    db[CLICK_LOGS_TABLE_NAME].delete_many({'userId': 'test'})

    msg = click_queue_client.getMessage()
    assert msg is not None

    print("test_logNewsClickForUser_basic passed!")

if __name__ == "__main__":
    # test_getNewsSummariesForUser_basic()
    # test_getNewsSummariesForUser_pagination()
    test_logNewsClickForUser_basic()