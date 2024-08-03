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
        command = text_data_json.get('command')
        
        if command == 'start_quiz':
            self.handle_quiz_start()
        elif command == 'update_score':
            is_correct = text_data_json.get('is_correct')
            time_left = text_data_json.get('time_left')
            self.update_score(is_correct, time_left)

        

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