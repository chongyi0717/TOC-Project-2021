from transitions.extensions import GraphMachine

from utils import push_button_message, push_text_message, send_button_message, send_image_url, send_text_message
from linebot.models import ButtonsTemplate,MessageTemplateAction

import requests
import bs4 
import random
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_location(self, event):
        text = event.message.text
        self.text=text+"市"
        return 1

    def is_going_to_price(self, event):
        text = event.message.text
        self.price_text=text
        if text=="150以內":
            self.price=1
            return 1
        elif text=="150-600":
            self.price=2
            return 1
        elif text=="600-1200":
            self.price=3
            return 1
        elif text=="1200以上":
            self.price=4
            return 1
        return 0

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "選單"

    def is_going_to_chinese(self, event):
        text = event.message.text
        return text.lower() == "中式"

    def is_going_to_japanese(self, event):
        text = event.message.text
        return text.lower() == "日式"

    def is_going_to_america(self, event):
        text = event.message.text
        return text.lower() == "美式"

    def is_going_to_bbq(self, event):
        text = event.message.text
        return text.lower() == "燒烤"

    def is_going_to_others(self, event):
        self.type = event.message.text
        return 1

    def on_enter_location(self, event):
        print("I'm entering location")
        reply_token = event.reply_token
        buttons=ButtonsTemplate(
                                title='price',
                                text='請選擇想要的價位',
                                actions=[
                                    MessageTemplateAction(
                                        label='150以內',
                                        text='150以內'
                                    ),
                                    MessageTemplateAction(
                                        label='150-600',
                                        text='150-600'
                                    ),
                                    MessageTemplateAction(
                                        label='600-1200',
                                        text='600-1200'
                                    ),
                                    MessageTemplateAction(
                                        label='1200以上',
                                        text='1200以上'
                                    )
                                ]
                            )
        push_text_message(event.source.user_id,"您選擇了%s"%(self.text))
        send_button_message(reply_token,"Menu",buttons)
        
    def on_enter_price(self, event):
        print("I'm entering price")
        reply_token = event.reply_token
        buttons=ButtonsTemplate(
                                title='Menu',
                                text="您選擇了%s,請點選“選單”"%(self.price_text),
                                actions=[
                                    MessageTemplateAction(
                                        label='選單',
                                        text='選單'
                                    )
                                ]
                            )
        send_button_message(reply_token,"Menu",buttons)

    def on_enter_menu(self, event):
        print("I'm entering menu")
        reply_token = event.reply_token
        buttons=ButtonsTemplate(
                                title='Menu',
                                text='今天想吃什麼樣的餐點呢？若沒有你想要的選項可以自行輸入哦~',
                                actions=[
                                    MessageTemplateAction(
                                        label='中式',
                                        text='中式'
                                    ),
                                    MessageTemplateAction(
                                        label='日式',
                                        text='日式'
                                    ),
                                    MessageTemplateAction(
                                        label='美式',
                                        text='美式'
                                    ),
                                    MessageTemplateAction(
                                        label='燒烤',
                                        text='燒烤'
                                    )
                                ]
                            )
        send_button_message(reply_token,"Menu",buttons)

    def on_exit_menu(self,event):
        print("Leaving menu")

    def on_enter_chinese(self, event):
        print("I'm entering chinese")

        reply_token = event.reply_token
        try:
            url="https://ifoodie.tw/explore/"+self.text+"/list/中式料理?priceLevel="+str(self.price)+"&opening=true"
            res=requests.get(url)
            root=bs4.BeautifulSoup(res.text,"html.parser")
            titles=root.find_all("a")
            list=[]
            for title in titles:
                classes=title.get("class")
                if classes!=None:
                    for cla in classes:
                        if(cla=="jsx-3440511973" and title.get("target")=="_self"):
                            string="https://ifoodie.tw"+title.get("href")
                            if(string not in list):
                                list.append(string)
            send_text_message(reply_token,random.choice(list))
        except:
            send_text_message(reply_token,"抱歉！我們找不到您所輸入的餐廳")
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
        push_button_message(event.source.user_id,"location",buttons)
        self.go_back()

    def on_exit_chinese(self):
        print("Leaving chinese")

    def on_enter_japanese(self, event):
        print("I'm entering japanese")

        reply_token = event.reply_token
        try:
            url="https://ifoodie.tw/explore/"+self.text+"/list/日式料理?priceLevel="+str(self.price)+"&opening=true"
            res=requests.get(url)
            root=bs4.BeautifulSoup(res.text,"html.parser")
            titles=root.find_all("a")
            list=[]
            for title in titles:
                classes=title.get("class")
                if classes!=None:
                    for cla in classes:
                        if(cla=="jsx-3440511973" and title.get("target")=="_self"):
                            string="https://ifoodie.tw"+title.get("href")
                            if(string not in list):
                                list.append(string)
            send_text_message(reply_token,random.choice(list))
        except:
            send_text_message(reply_token,"抱歉！我們找不到您所輸入的餐廳")
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
        push_button_message(event.source.user_id,"location",buttons)
        self.go_back()

    def on_exit_japenese(self):
        print("Leaving japanese")
    
    def on_enter_america(self, event):
        print("I'm entering america")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list/美式料理?priceLevel="+str(self.price)+"&opening=true"
            res=requests.get(url)
            root=bs4.BeautifulSoup(res.text,"html.parser")
            titles=root.find_all("a")
            list=[]
            for title in titles:
                classes=title.get("class")
                if classes!=None:
                    for cla in classes:
                        if(cla=="jsx-3440511973" and title.get("target")=="_self"):
                            string="https://ifoodie.tw"+title.get("href")
                            if(string not in list):
                                list.append(string)
            send_text_message(reply_token,random.choice(list))
        except:
            send_text_message(reply_token,"抱歉！我們找不到您所輸入的餐廳")
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
        push_button_message(event.source.user_id,"location",buttons)
        self.go_back()

    def on_exit_america(self):
        print("Leaving america")

    def on_enter_bbq(self, event):
        print("I'm entering bbq")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list/燒烤?priceLevel="+str(self.price)+"&opening=true"
            res=requests.get(url)
            root=bs4.BeautifulSoup(res.text,"html.parser")
            titles=root.find_all("a")
            list=[]
            for title in titles:
                classes=title.get("class")
                if classes!=None:
                    for cla in classes:
                        if(cla=="jsx-3440511973" and title.get("target")=="_self"):
                            string="https://ifoodie.tw"+title.get("href")
                            if(string not in list):
                                list.append(string)
            send_text_message(reply_token,random.choice(list))
        except:
            send_text_message(reply_token,"抱歉！我們找不到您所輸入的餐廳")
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
        push_button_message(event.source.user_id,"location",buttons)
        self.go_back()

    def on_exit_bbq(self):
        print("Leaving bbq")

    def on_enter_others(self, event):
        print("I'm entering others")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list/"+self.type+"?priceLevel="+str(self.price)+"&opening=true"
            res=requests.get(url)
            root=bs4.BeautifulSoup(res.text,"html.parser")
            titles=root.find_all("a")
            list=[]
            for title in titles:
                classes=title.get("class")
                if classes!=None:
                    for cla in classes:
                        if(cla=="jsx-3440511973" and title.get("target")=="_self"):
                            string="https://ifoodie.tw"+title.get("href")
                            if(string not in list):
                                list.append(string)
            send_text_message(reply_token,random.choice(list))
        except:
            send_text_message(reply_token,"抱歉！我們找不到您所輸入的餐廳")
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
        push_button_message(event.source.user_id,"location",buttons)
        self.go_back()

    def on_exit_others(self):
        print("Leaving others")
    
