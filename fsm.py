from transitions.extensions import GraphMachine

from utils import push_text_message, send_button_message, send_image_url, send_text_message
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
        push_text_message(event.source.user_id,"您選擇了%s，請輸入“選單”"%(self.text))

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
            url="https://ifoodie.tw/explore/"+self.text+"/list/%E4%B8%AD%E5%BC%8F%E6%96%99%E7%90%86"
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
        push_text_message(event.source.user_id,"您好！若要尋找餐廳請先輸入您現在所在的城市：")
        self.go_back()

    def on_exit_chinese(self):
        print("Leaving chinese")

    def on_enter_japanese(self, event):
        print("I'm entering japanese")

        reply_token = event.reply_token
        try:
            url="https://ifoodie.tw/explore/"+self.text+"/list/%E6%97%A5%E6%9C%AC%E6%96%99%E7%90%86"
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
        push_text_message(event.source.user_id,"您好！若要尋找餐廳請先輸入您現在所在的城市：")
        self.go_back()

    def on_exit_japenese(self):
        print("Leaving japanese")
    
    def on_enter_america(self, event):
        print("I'm entering america")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list//%E7%BE%8E%E5%BC%8F%E6%96%99%E7%90%86"
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
        push_text_message(event.source.user_id,"您好！若要尋找餐廳請先輸入您現在所在的城市：")
        self.go_back()

    def on_exit_america(self):
        print("Leaving america")

    def on_enter_bbq(self, event):
        print("I'm entering bbq")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list/%E7%87%92%E7%83%A4"
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
        push_text_message(event.source.user_id,"您好！若要尋找餐廳請先輸入您現在所在的城市：")
        self.go_back()

    def on_exit_bbq(self):
        print("Leaving bbq")

    def on_enter_others(self, event):
        print("I'm entering others")
        try:
            reply_token = event.reply_token
            url="https://ifoodie.tw/explore/"+self.text+"/list/"+self.type
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
        push_text_message(event.source.user_id,"您好！若要尋找餐廳請先輸入您現在所在的城市：")
        self.go_back()

    def on_exit_others(self):
        print("Leaving others")
    
