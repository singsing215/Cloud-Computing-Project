# Coronavirus Prevention Line Chatbot
 
## Team Information

   This is GROUP E from COMP7940 Cloud Computing.

  |   NAME     |     SID   |   ACCOUNT   |            types of queries                                        |
  |------------|-----------|-------------|--------------------------------------------------------------------|
  |SU Zhanyi   |  19430051 |   zhanyis   |  show/upload the news about COVID19 with redis                     |
  |GUO Fusheng |  19413238 | singsing215 |  show latest infections number, chart and video for against COVID19|

## Introduction

This is a LINE chat robot about COVID19. The chat robot is mainly written in Python, deployed to the Heroku cloud platform, and applied to the LINE instant messaging platform. The API service uses Tian API, Imgur API, YouTube Data API. The storage database is Redis. The chat robot mainly implements three functions:
1. Query the number of COVID19 diagnoses, cures, and deaths in domestic provinces, and realize data visualization through matplotlib.
2. To realize the browsing of COVID19 news, the editing and updating of news websites
3. Provide some short videos about COVID19's anti-epidemic knowledge and realize the video search function

## Line Chatbot QR code

![QR code](http://github.com/singsing215/project-line-chatbot/raw/master/comp7940project/QRcode.PNG)

## Reference
https://developers.line.biz/en/reference

https://github.com/line/line-bot-sdk-python

https://apidocs.imgur.com

https://github.com/SMAPPNYU/youtube-data-api

https://github.com/youtube/api-samples/tree/master/python

https://developers.google.com/youtube/v3/
