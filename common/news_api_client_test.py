import news_api_client as client

def test_basic():
    news = client.getNewsFromSource()
    print(news)
    assert len(news) > 0

if __name__ == "__main__":
    test_basic()