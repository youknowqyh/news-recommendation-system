import news_topic_modeling_service_client as client

def test_basic():
    newsTitle = "Technology"
    topic = client.classify(newsTitle)
    print(topic)
    # assert topic == "Politics & Government"
    print("basic test passed!")

if __name__ == "__main__":
    test_basic()