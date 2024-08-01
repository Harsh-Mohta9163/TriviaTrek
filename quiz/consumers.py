# from channels.generic.websocket import WebsocketConsumer
# from django.shortcuts import get_object_or_404
# from asgiref.sync import async_to_sync
# import json
# from .models import QuizRoom

# class QuizRoomConsumer(WebsocketConsumer):
#     def connect(self):
#         self.quiz_room_id = self.scope['url_route']['kwargs']['quiz_room_id']
#         self.quiz_room = get_object_or_404(QuizRoom, id=self.quiz_room_id)
#         self.room_group_name = f'quizroom_{self.quiz_room_id}'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         if self.scope['user'] != self.quiz_room.admin:
#             self.quiz_room.members.add(self.scope['user'])
#             self.quiz_room.save()
   

#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.quiz_room.members.remove(self.scope['user'])
#         self.quiz_room.save()

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         body = text_data_json.get('command')  # Retrieve 'body' from the message
#         print(body)
#         # Create a new GroupMessage object (assuming you have a similar model)
#         if body == 'start_quiz':
#             # Handle quiz start logic
#             self.handle_quiz_start()

#             # For demonstration, sending a message back to the group
#             event = {
#                 'type': 'handle_quiz_start',
#                 'message': 'The quiz is starting!'
#             }
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 event
#             )



#     def handle_quiz_start(self,event):
#         if self.scope['user'] == self.quiz_room.admin:
#             redirect_url = f'/quiz/{self.quiz_room_id}/leaderboard/'
#         else:
#             redirect_url = f'/quiz/{self.quiz_room_id}/questions/'
        
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'quiz_start',
#                 'message': 'The quiz is starting!',
#                 'redirect_url': redirect_url
#             }
#         )


#     def quiz_start(self, event):
#         self.send(text_data=json.dumps({
#             'event': 'redirect_to_questions'
#         }))

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import QuizRoom

class QuizRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.quiz_room_id = self.scope['url_route']['kwargs']['quiz_room_id']
        self.quiz_room = get_object_or_404(QuizRoom, id=self.quiz_room_id)
        self.room_group_name = f'quizroom_{self.quiz_room_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.scope['user'] != self.quiz_room.admin:
            self.quiz_room.members.add(self.scope['user'])
            self.quiz_room.save()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        self.quiz_room.members.remove(self.scope['user'])
        self.quiz_room.save()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json.get('command')
        
        if body == 'start_quiz':
            self.handle_quiz_start()

    def handle_quiz_start(self):
        redirect_url = f'/quiz/{self.quiz_room_id}/questions/'
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'quiz_start',
                'message': 'The quiz is starting!',
                'redirect_url': redirect_url
            }
        )

    def quiz_start(self, event):
        print("hello2")
        self.send(text_data=json.dumps({
            'event': 'redirect',
            'redirect_url': event['redirect_url']
        }))
