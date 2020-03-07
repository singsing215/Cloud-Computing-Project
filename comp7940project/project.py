from __future__ import unicode_literals

import os
import sys
import redis
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage
)
from linebot.utils import PY3

# fill in the following.
HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
PORT = "11363"
# 自己的redis
# HOST = "redis-16236.c10.us-east-1-3.ec2.cloud.redislabs.com"
# PWD = "A5aztmjp4xcnb7c5w30cet77ow48llg2gfb8mii1e87cgdbc6xr"
# PORT = "16236"

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'

def replynews(event):
        title = redis1.get('titleszy')
        summary = redis1.get('summaryszy')
        link = redis1.get('linkszy')
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://www.news.gov.hk/web/common/images/newsArticleBanner/eng/20200211000937694.png',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://www.news.gov.hk/eng/categories/wuhan/index.html', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text=title, weight='bold', size='sm'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text=summary,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='More Detail', uri=link)
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


def editnews(event):
    newnews = event.message.text.split('##')
    if(len(newnews) == 4):
        redis1.set('titleszy', newnews[1])
        redis1.set('summaryszy', newnews[2])
        redis1.set('linkszy', newnews[3])
        alerttext = 'news updated successful'
    else:
        alerttext = 'please enter correct newsformat'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(alerttext))



# Handler function for Text Message
def handle_TextMessage(event):
    if event.message.text=='1':
        print(event.message.text)
        msg = '11'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
    if event.message.text=='2':
        print(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
           text='Hello, world',
           quick_reply=QuickReply(items=[
           QuickReplyButton(action=MessageAction(label="label", text="text"))
           ])))
    if event.message.text=='3':
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url='https://cdn.hk01.com/di/media/images/715391/org/53bbb25d04815ec78b3f23e5ce6d44da.jpg/VfvDK_ih9FR05oxjDziapjpvWJ6TPVg8IQg08yEINPM?v=w1920',
            preview_image_url='https://cdn.hk01.com/di/media/images/715391/org/53bbb25d04815ec78b3f23e5ce6d44da.jpg/VfvDK_ih9FR05oxjDziapjpvWJ6TPVg8IQg08yEINPM?v=w1920'
            ))
    if event.message.text=='4':
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(
            title='my location',
            address='Tokyo',
            latitude=35.65910807942215,
            longitude=139.70372892916203
            ))
    if event.message.text=='5':
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(
            original_content_url='https://www.youtube.com/watch?v=8hAMDi3yzq0',
            preview_image_url='https://i.ytimg.com/an_webp/8hAMDi3yzq0/mqdefault_6s.webp?du=3000&sqp=CPW06PIF&rs=AOn4CLCxPfPorMvIWw9Typ3RwxQ8Vs2ujQ'
            ))
    if(event.message.text == 'news'):
        replynews(event)
    if(event.message.text[0:7] == 'editnew'):
        editnews(event)
    else : 
        print(event.message.text)
        msg = 'i dont understand'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))

# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(event.reply_token,StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id
            ))

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Nice image!"))

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Nice video!"))

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Nice file!"))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)