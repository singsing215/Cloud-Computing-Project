

## Chatbot Required Features
This is line chatbot.

The line chatbot is the context of public health care about the coronavirus.

Specific features are as follows:
1. The bot can differentiate at least 2 different types of queries and give 2 different types of responses.
1. The bot will use a redis server to store some persistent information.
1. The bot will use consume another service other than redis.
1. The bot will be running on Heroku.
1. The bot will use git for version controls. 
1. The LINE bot will be written only with Python and its library. 


### Chatbot function design
> SU ZHANYI 19430051
1. Function in showing the lastest news about COVID19. News collects from [Department of health](https://www.coronavirus.gov.hk/eng/latest_news.html) manually update to redis server.
   After users query the key word `news`, the chatbot will return the news about COVID19 in Hong Kong and the link go ahead to the web page.  
   People can use the line chatbot to upload the news. With the comment `editnews##title##summary##link`.
1. A service with provide the youtube video with relate query, type in the key word `youtube?queryword` , then the chatbot will reply the latest three related videos.   

> GUO FUSHENG 19413238
1. For the query part of finding face mask/cleaning substance, the chatbot will provide some video on finding mask/cleaning substance, making homemade mask/cleaning substance. For the query part of getting latest number of infections, the line chatbot will answers the latest numbers of infections, cures and deaths for COVID19. Besides, user can check the same flight information of infected passengers.

