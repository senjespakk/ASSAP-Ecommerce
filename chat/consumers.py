from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from chat.models import Thread
from django.contrib.auth.models import User

class ChatConsumer(SyncConsumer):    
    def websocket_connect(self, event):
        # get the two users
        me = self.scope['user']
        other_username = self.scope['url_route']['kwargs']['username']
        other_user = User.objects.get(username=other_username)
        # get or create incase
        thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)
        self.room_name = 'presonal_thread'
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })
        print(f'[{self.channel_name}]  - connected now')


    def websocket_receive(self, event):
        print(f'[{self.channel_name}]  - received now {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type': 'websocket.message',
                'text': event.get('text')
            }
        )
    def websocket_message(self, event):
        print(f'[{self.channel_name}] - sent now {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })
    
    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}]  - disconnected now')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)



class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.room_name = 'Broadcast'
        self.send({
            'type': 'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        print(f'[{self.channel_name}]  - connected now')


    def websocket_receive(self, event):
        print(f'[{self.channel_name}]  - received now {event["text"]}')
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, 
            {
                'type': 'websocket.message',
                'text': event.get('text')
            }
        )
    def websocket_message(self, event):
        print(f'[{self.channel_name}] - sent now {event["text"]}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })
    
    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}]  - disconnected now')
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
