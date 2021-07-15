# Real Time News Scraping and Recommendation System

This is a real-time news scraping and recommendation system implemented as a single-page application. It is consist of a React front-end, multiple backend services including RESTful servers and RPC servers, a MongoDB database, a news scraper as well as multiple cloud RabbitMQ message queues. It's Service-Oriented, multiple backend services commucating through jsonrpc. I built a news pipeline to scrape real-time latest news from several news sources such as CNN, BBC, ESPN. At the meantime, TF-IDF algorithm was used to dedupe news. In order to implement the functionality of recommending news according to user's preference, I developed a click log processor to record user's click behavior on different news topics. At the end, I used Tensorflow to realize news topic classification, which was also deployed as an online classifying service.

## Overview

- Implemented a single-page news browsing web application with React, Express, Node.js, Flask, RPC and JWT.
- Built a data pipeline to monitor, scrape and dedupe latest news with Redis, RabbitMQ and TF-IDF.
- Developed a click event log processor which collects users' click logs for news recommendation service.
- Deployed an online news topic classification service using a trained CNN model in Tensorflow.

## Demo

![](E:\Side Projects\news-recommend-system\repo\img\demo.png)

## Architecture

![](E:\Side Projects\news-recommend-system\repo\img\system-architecture.png)



![](E:\Side Projects\news-recommend-system\repo\img\lifecycle.png)

## System Break-down

### News Pipeline

News pipeline is composed by news monitor, web scraper and news deduper, news is sent and received between them by RabbitMQ which decouples these components. The news monitor use News API to derive latest news and store news title MD5 digest into Redis to avoid sending same news to the message queue. The web scraper use a third party package Newspaper to fetch corresponding news articles from offical news website. News depuper implements TF-IDF to calculate similarity of news to avoid storing same news from different news source into MongoDB. For similar news, only store the one published firstly.

![](E:\Side Projects\news-recommend-system\repo\img\newspipeline.jpeg)

### News Recommendation service

I built a click log processor to implement a time decay model. If a news topic is clicked, p = (1-α)p + α, if not, p = (1-α)p, Where p is the selection probability, and α is the degree of weight decrease. The result of this is that the nth most recent selection will have a weight of (1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent selection would only have half the weight of the most recent. Increasing α would bias towards more recent results more.

When some news' topic with the most probability for that user, the webpage will show a "Recommend" tag to the user.

![](E:\Side Projects\news-recommend-system\repo\img\recommendation.jpeg)

### News Classification Service

The news topic classification is implemented by Convolutional Neutral Nework(CNN) in TensorFlow and deployed online using the offline trained model. Manually label the news with 17 classes: Colleges & Schools, Environmental, World, Entertainment, Media, Politics & Government, Regional News, Religion, Sports, Technology, Traffic, Weather, Economic & Corp, Advertisements, Crime, Magazine, Other.

## Getting started

### 1. Install Redis

```
wget http://download.redis.io/releases/redis-3.2.6.tar.gz
tar xzf redis-3.2.6.tar.gz
cd redis-3.2.6
make
sudo make install
cd utils
sudo ./install_server.sh
```

### 2. Install mongodb

```
sudo apt update && sudo apt upgrade -y
sudo apt install mongodb
sudo systemctl status mongodb
sudo systemctl start mongodb
```

### 3. Install Node.js

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.4/install.sh | bash
source ~/.bashrc
nvm install node
```

### 4. Install Python

```
apt-get install -y python
pip install -r requirements.txt
```

### 5. Run

```shell
# Open multiple tabs to run 5 services

# backend server on port 4040
cd backend_server
python service.py

# Click log processor
cd news_recommendation_service
python click_log_processor.py

# Web server on port 3000
cd web_server/server
npm install
npm start

# news recommendation service on port 5050
cd news_recommendation_service
python recommendation_service.py

# news_topic_modeling_service on port 6060
cd news_topic_modeling_service/server
python server.py
```





