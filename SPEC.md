

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
1. For the query part of finding face mask/cleaning substance, the chatbot will provide some advice on finding mask/cleaning substance, making homemade mask/cleaning substance and predicting when and where the mask/cleaning will arrive.

### Chatbot function design

1. Function in showing the lastest news about COVID19. News collects from [Department of health](https://www.coronavirus.gov.hk/eng/latest_news.html)  
   After users query the key word **COVID19NEWS**, the chatbot will return the latest news about COVID19 in Hong Kong and the link go ahead to the web page.  
   This function is use another service other than redis. The corresponding news is updated by **Department of health in Hong Kong**.  
   As the process of building the chatbot, the reply detail may change XD. (Perhaps the COVID19 disappear)  
