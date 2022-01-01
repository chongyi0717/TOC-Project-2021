import os
import sys
from types import DynamicClassAttribute

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,ButtonsTemplate,MessageTemplateAction
from linebot.models.messages import ImageMessage
from machine import create_machine
from utils import send_text_message,push_button_message
load_dotenv()




app = Flask(__name__, static_url_path="")

machines={}
machine=create_machine()
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
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
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    print(body)
    body_json=request.get_json()
    if body_json["destination"]!="U06ca89d886c034d5c9185af475919dd9":
        if(body_json["events"][0]["type"]=="follow"):
            buttons=ButtonsTemplate(
                                    title='請選擇城市',
                                    text='您好！若要尋找餐廳請先輸入您現在所在的城市(若選項中沒有對應的城市可自行輸入)：',
                                    actions=[
                                        MessageTemplateAction(
                                            label='台北',
                                            text='台北'
                                        ),
                                        MessageTemplateAction(
                                            label='新北',
                                            text='新北'
                                        ),
                                        MessageTemplateAction(
                                            label='高雄',
                                            text='高雄'
                                        ),
                                        MessageTemplateAction(
                                            label='台南',
                                            text='台南'
                                        )
                                    ]
                                )
            push_button_message(body_json["events"][0]["source"]["userId"],"location",buttons)
        if(body_json["events"][0]["type"]=="unfollow" or body_json["events"][0]["type"]=="leave"):
            del machines[body_json["events"][0]["source"]["userId"]]
            print("del")
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        #print(f"\nFSM STATE: {machines[event.source.user_id].state}")
        print(f"REQUEST BODY: \n{body}")
        
        if event.source.user_id not in machines:
            machines[event.source.user_id] = create_machine()

        response = machines[event.source.user_id].advance(event)
        if response == False:
            send_text_message(event.reply_token, "無法辨識您輸入的指令，請依照指示輸入指令")
            
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #machine.get_graph().draw("img/show-fsm.png", prog="dot", format="png")
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
