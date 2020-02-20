

## Chatbot Required Features

The chatbot will be with the context of public health care. It can be understood as things like the measurement against coronavirus, finding face mask/cleaning substance, summarize of news, etc. Your team can decide on what exact context that your bot can do. But technically, there are some constraints:

1. The bot should be able to differentiate at least 2 different types of queries and give 2 different types of responses.
1. The design concept of the bot should be public health care. It can be the measurement against coronavirus, finding face mask, etc.
1. The bot should use a redis server to store some persistent information.
1. The bot should use consume another service other than redis.
1. The bot should be running on Heroku.
1. The bot use git for version controls. 
1. The LINE bot should be written only with Python and its library. 
