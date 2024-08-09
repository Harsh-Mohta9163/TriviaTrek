from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import QuizRoom,Score,Question

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
            self.update_participant_list()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        self.quiz_room.members.remove(self.scope['user'])
        self.quiz_room.save()
        self.update_participant_list()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')
        
        if command == 'start_quiz':
            self.handle_quiz_start()
        elif command == 'update_score':
            is_correct = text_data_json.get('is_correct')
            time_left = text_data_json.get('time_left')
            self.update_score(is_correct, time_left)
        
        elif command == 'remove_participant':
            print("hello9")
            user_id = text_data_json.get('user_id')
            self.remove_participant(user_id)
        elif command == 'buzz_in':
            user_id = text_data_json.get('user_id')
            username = text_data_json.get('username')

            # Send the buzz event to the leaderboard and all connected clients
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'buzz_received',
                    'user_id': user_id,
                    'username': username
                }
            )
        elif command == 'next_question':
            # Broadcast reset_buzzer event to the group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'reset_buzzer',
                }
            )

    def handle_quiz_start(self):
        if self.quiz_room.is_buzzer:
            redirect_url = f'/quiz/{self.quiz_room_id}/buzzer/'
        else:
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

    def update_score(self, is_correct, time_left):
        print("entered1")
        user = self.scope['user']
        score, created = Score.objects.get_or_create(quiz_room=self.quiz_room, user=user)
        
        if is_correct:
            # Assuming the current question is available
            current_question = Question.objects.filter(quiz_room=self.quiz_room).order_by('question_number').first()
            if current_question:
                points_awarded = current_question.score_per_question + time_left
                score.points += points_awarded
                score.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'leaderboard_update',
                'leaderboard_data': self.get_leaderboard_data()
            }
        )

    def leaderboard_update(self, event):
        
        self.send(text_data=json.dumps({
            'event': 'leaderboard_update',
            'leaderboard_data': event['leaderboard_data']
        }))

    def get_leaderboard_data(self):
        print("entered2")
        leaderboard = Score.objects.filter(quiz_room=self.quiz_room).order_by('-points')
        leaderboard_data = [
            {'number': idx + 1, 'name': score.user.username, 'points': score.points}
            for idx, score in enumerate(leaderboard)
        ]
        return leaderboard_data

    def update_participant_list(self):
        participants = [{'id': member.id, 'username': member.username} for member in self.quiz_room.members.all()]
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_update_participant_list',
                'participants': participants
            }
        )

    def send_update_participant_list(self, event):
        self.send(text_data=json.dumps({
            'event': 'update_participant_list',
            'participants': event['participants']
        }))

    def remove_participant(self, user_id):
        print("hello7")
        try:
        # Check if the user exists in the quiz room's members
            user = self.quiz_room.members.get(id=user_id)
        except user.DoesNotExist:
            print(f"User with ID {user_id} does not exist in the quiz room.")
            return  # Exit the function if the user does not exist
        # self.quiz_room.members.remove(user)
        # self.quiz_room.save()
        
        # Notify the removed user to redirect to the home page
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                'type': 'redirect_user',
                'redirect_url': '/',
                'user_id': user_id,
                'alert_message': 'You have been removed by the admin.'
            }
        )

    def redirect_user(self, event):
        print("hello6")
        self.send(text_data=json.dumps({
            'event': 'redirect_remove',
            'redirect_url': event['redirect_url'],
            'alert_message': event['alert_message'],
            'user_id': event['user_id'],
        }))

    def buzz_received(self, event):
        self.send(text_data=json.dumps({
            'event': 'buzz_received',
            'user_id': event['user_id'],
            'username': event['username']
        }))
    
    def reset_buzzer(self, event):
        # Send message to WebSocket to reset the buzzer
        self.send(text_data=json.dumps({
            'event': 'reset_buzzer',
        }))