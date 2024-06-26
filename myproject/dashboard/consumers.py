from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync 

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('Websocket Connected... ',event)
        print("Channel layer...",self.channel_layer) 
        print("Channel name...",self.channel_name) 
       
        self.room = self.scope['url_route']['kwargs']['room']
        print("Group Name...",self.room)
        # add a channel to new or existing group
        async_to_sync(self.channel_layer.group_add)(
            self.room ,
            self.channel_name
            )
        self.send({
            'type':'websocket.accept',
        })  
    def websocket_receive(self,event):
        print('Message received from client...',event['text'])      
        print('Type of message received from client...',type(event['text']))   
        async_to_sync(self.channel_layer.group_send)(
            self.room,
            {
                'type':'chat.message',
                'message': event['text']
            }
        )  

    def chat_message(self,event):
        print('Event...',event)
        print('Actual data...',event['message'])
        print('Type of actual data...',type(event['message']))
        self.send({
            'type': 'websocket.send',
            'text': event['message']

        })


    def websocket_disconnect(self,event):
        print('Websocket disconnected...',event)   
        print("Channel layer...",self.channel_layer) # get default channel layer from project
        print("Channel name...",self.channel_name) # get default channel name from project
        # add a channel to new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            self.room,
            self.channel_name
            )
        raise StopConsumer()       

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('Websocket Connected... ',event)
        print("Channel layer...",self.channel_layer) # get default channel layer from project
        print("Channel name...",self.channel_name) # get default channel name from project
        # add a channel to new or existing group
        await self.channel_layer.group_add(
            'programmers', #group name
            self.channel_name
            )
        await self.send({
            'type':'websocket.accept',
        })  
    async def websocket_receive(self,event):
        print('Message received from client...',event['text'])      
        print('Type of message received from client...',type(event['text']))   
        await self.channel_layer.group_send(
            'programmers',
            {
                'type':'chat.message',
                'message': event['text']
            }
        )  

    async def chat_message(self,event):
        print('Event...',event)
        print('Actual data...',event['message'])
        print('Type of ctual data...',type(event['message']))
        await self.send({
            'type': 'websocket.send',
            'text': event['message']

        })


    async def websocket_disconnect(self,event):
        print('Websocket disconnected...',event)   
        print("Channel layer...",self.channel_layer) # get default channel layer from project
        print("Channel name...",self.channel_name) # get default channel name from project
        # add a channel to new or existing group
        await self.channel_layer.group_discard(
            'programmers',
            self.channel_name
            )
        raise StopConsumer()    
