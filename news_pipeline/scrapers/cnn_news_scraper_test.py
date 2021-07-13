import cnn_news_scraper

EXPECTED_NEWS = "CNN has obtained exclusive information about the hunt for the killers of Jovenel Moise, a banana exporter-turned-politician who was killed in a hail of gunfire in the bedroom of his private residence in the leafy Port-au-Prince district of Petion-Ville at around 1 a.m. last Wednesday, according to government statements."
CNN_NEWS_URL = "https://www.cnn.com/2021/07/13/americas/haiti-president-assassins-gun-battle-cmd-intl/index.html"

def basic_test():
    news = cnn_news_scraper.extract_news(CNN_NEWS_URL)
    # print(news)
    assert EXPECTED_NEWS in news
    print("basic test passed!")
if __name__ == "__main__":
    basic_test()