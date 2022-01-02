import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,ImageSendMessage


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_button_message(reply_token,text,buttons):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        reply_token,
                        TemplateSendMessage(
                            alt_text=text,
                            template=buttons
                        )
                    )
        
def push_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(reply_token, TextSendMessage(text=text))

    return "OK"
def push_button_message(reply_token,text,buttons):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(  # 回復傳入的訊息文字
                        reply_token,
                        TemplateSendMessage(
                            alt_text=text,
                            template=buttons
                        )
                    )
    return "OK"
    
def send_image_url(id, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    message = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.push_message(id, message)

    return "OK"
"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Menu',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='今天想吃什麼樣的餐點呢？',
                                actions=[
                                    MessageTemplateAction(
                                        label='中式',
                                        text='中式'
                                    ),
                                    MessageTemplateAction(
                                        label='台式',
                                        text='台式'
                                    ),
                                    MessageTemplateAction(
                                        label='美式',
                                        text='美式'
                                    ),
                                    MessageTemplateAction(
                                        label='越式',
                                        text='越式'
                                    )
                                ]
                            )
                        )
                    )
        
    return "OK"
"""
