import json

from channels.generic.websocket import WebsocketConsumer
# needs the async channel layer functions to be converted.
from asgiref.sync import async_to_sync

from pprint import pprint 
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)

    def receive(self, text_data):
        pass

    def send_bidders(self,event):
        print(type(event))
        
        pprint(event)
        self.send(text_data=event["bids"])