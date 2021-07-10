from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = "amqps://ogzzjmml:qF4TXBuVoTFdlj9uAmlxEhQDb6Dh21-v@snake.rmq2.cloudamqp.com/ogzzjmml"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test': 'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print('test_basic passed!')

if __name__ == '__main__':
    test_basic()

#  pip install --upgrade pip enum34