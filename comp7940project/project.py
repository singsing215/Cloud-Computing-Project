from __future__ import unicode_literals

import os
import sys
import redis
from argparse import ArgumentParser
import json
import requests
import matplotlib.pyplot as pt
import pyimgur

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
    ImageSendMessage,VideoSendMessage,PostbackTemplateAction,
    MessageTemplateAction,URITemplateAction
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
redis1 = redis.Redis(host=HOST, password=PWD, port=PORT, decode_responses=True)
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


def writeinjson(api):
    req = requests.get(api)
    with open("./name.json", "w") as f:
        json.dump(req.json(), f, ensure_ascii=False)
    return req.json()


def flight(event):
    message='Here are the latest flight information and dates for confirmed COVID19 patients:\n'
    a=writeinjson(ncovsame)
    newslist=list(a["newslist"])
    for no in newslist:
        m='Flight no: %s, date: %s\n'% (no["no"],no["date"])
        message+=m
    line_bot_api.reply_message(event.reply_token, TextSendMessage(message))


def province(q,event):
    message=''
    a=writeinjson(ncovcity)
    newslist=list(a["newslist"])
    for no in newslist:
        m='District: %s, %s: %s\n'% (no["provinceName"],q,no[q])
        message+=m
    line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    

def hubei_graph():
    a=writeinjson(ncovcity)
    newslist=list(a["newslist"])
    hubei=newslist[0]
    conf=hubei.get('confirmedCount')
    cur=hubei.get('curedCount')
    dead=hubei.get('deadCount')
    data=[conf,cur,dead]
    labels=['Confirmed','Cured','Dead']
    pt.bar(range(len(data)), data, tick_label=labels)
    pt.xlabel('Hubei'),
    pt.ylabel("Count")
    pt.savefig('send.png')
    CLIENT_ID = "135f2074e557c95"
    PATH = "send.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link

def hk_graph():
    a=writeinjson(ncovcity)
    newslist=list(a["newslist"])
    hubei=newslist[3]
    conf=hubei.get('confirmedCount')
    cur=hubei.get('curedCount')
    dead=hubei.get('deadCount')
    data=[conf,cur,dead]
    labels=['Confirmed','Cured','Dead']
    pt.bar(range(len(data)), data, tick_label=labels)
    pt.xlabel('Hong Kong'),
    pt.ylabel("Count")
    pt.savefig('send.png')
    CLIENT_ID = "135f2074e557c95"
    PATH = "send.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link

def gd_graph():
    a=writeinjson(ncovcity)
    newslist=list(a["newslist"])
    hubei=newslist[2]
    conf=hubei.get('confirmedCount')
    cur=hubei.get('curedCount')
    dead=hubei.get('deadCount')
    data=[conf,cur,dead]
    labels=['Confirmed','Cured','Dead']
    pt.bar(range(len(data)), data, tick_label=labels)
    pt.xlabel('Guangdong'),
    pt.ylabel("Count")
    pt.savefig('send.png')
    CLIENT_ID = "135f2074e557c95"
    PATH = "send.png"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
    return uploaded_image.link


ncovsame = 'http://api.tianapi.com/txapi/ncovsame/index?key=a8d66af010b307f9cf301c353d1aa0a5' 
ncovcity = 'http://api.tianapi.com/txapi/ncovcity/index?key=a8d66af010b307f9cf301c353d1aa0a5'
# Handler function for Text Message
def handle_TextMessage(event):
    if event.message.text=='1':
        print(event.message.text)
        msg = '11'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(msg))
    if event.message.text=='number':
        print(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
           text='This is a guide to get the latest Numbers of COVID19 in Chinese provinces and SAR: \n 1.Number of confirmed patient type----confirmed\n 2.Number of cured patient type----cured\n 3.Number of dead patient type----dead',
           quick_reply=QuickReply(items=[
           QuickReplyButton(action=MessageAction(label="confirmed", text="confirmed")),
           QuickReplyButton(action=MessageAction(label="cured", text="cured")),
           QuickReplyButton(action=MessageAction(label="dead", text="dead"))
           ])))
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
    if event.message.text=='Hubei':
        img_url = hubei_graph()
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
            ))
    if event.message.text=='Hongkong':
        img_url = hk_graph()
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
            ))
    if event.message.text=='Guangdong':
        img_url = gd_graph()
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
            ))
    if event.message.text=='44':
        line_bot_api.reply_message(event.reply_token,LocationSendMessage(
            title='my location',
            address='Tokyo',
            latitude=35.65910807942215,
            longitude=139.70372892916203
            ))
    if event.message.text=='6':
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(
            original_content_url='https://www.youtube.com/watch?v=8hAMDi3yzq0',
            preview_image_url='https://i.ytimg.com/an_webp/8hAMDi3yzq0/mqdefault_6s.webp?du=3000&sqp=CPW06PIF&rs=AOn4CLCxPfPorMvIWw9Typ3RwxQ8Vs2ujQ'
            ))
    if event.message.text=='video':
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://object.bigbigchannel.com.hk/2020/02/25/1582642972238.png',
                        title='How To Make Your Own Mask',
                        text='It is better to have homemade mask than none',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='view video',
                                uri='https://www.youtube.com/watch?v=8hAMDi3yzq0'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.hk01.com/di/media/images/3921597/org/823622f9fe1a3279567080bd282ac3a5.jpg/B4zaMGYvBd4Kh4M78MmCcm8t0klu951tCVlogAlZaIA?v=w1920r16_9',
                        title='Homemade Alcohol Hand Rub',
                        text='Contains detailed steps for making hand rub',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='view video',
                                uri='https://www.youtube.com/watch?v=FLLG54YfaLQ'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.ytimg.com/vi/t30dxGn-ECc/hqdefault.jpg',
                        title='How To Make Alcohol Spray',
                        text='Make a hand cleaning spray that works just as well',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='view video',
                                uri='https://www.youtube.com/watch?v=t30dxGn-ECc'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text=='7':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='https://www.youtube.com/watch?v=8hAMDi3yzq0'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text=='8':
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Are you sure?',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text=='9':
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://example.com/item1.jpg',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://example.com/item2.jpg',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text=='help':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='User Guide 1',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='1.News about COVID19',
                        text='news'
                    ),
                    MessageTemplateAction(
                        label='2.',
                        text='2'
                    ),
                    MessageTemplateAction(
                        label='3.',
                        text='3'
                    ),
                    MessageTemplateAction(
                        label='4.More...',
                        text='4'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text=='4':
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='User Guide 2',
                text='Please select',
                actions=[
                    MessageTemplateAction(
                        label='5.Where to buy mask',
                        text='44'
                    ),
                    MessageTemplateAction(
                        label='6.Viedo for DIY mask',
                        text='video'
                    ),
                    MessageTemplateAction(
                        label='7.Flight info search',
                        text='flight'
                    ),
                    MessageTemplateAction(
                        label='8.Number of COVID19',
                        text='number'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    if(event.message.text == 'news'):
        replynews(event)
    if(event.message.text[0:7] == 'editnew'):
        editnews(event)
    if(event.message.text == 'flight'):
        flight(event)
    if(event.message.text == 'confirmed'):
        province("confirmedCount",event)
    if(event.message.text == 'dead'):
        province("deadCount",event)
    if(event.message.text == 'cured'):
        province("curedCount",event)
    else : 
        print(event.message.text)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(
           text='I am not sure, need "help"?',
           quick_reply=QuickReply(items=[
           QuickReplyButton(action=MessageAction(label="help", text="help"))
           ])))

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