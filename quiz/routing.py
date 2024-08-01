from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/quiz/<int:quiz_room_id>', consumers.QuizRoomConsumer.as_asgi()),
]
