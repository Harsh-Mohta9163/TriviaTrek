from django.urls import path,include
from  .views import *


urlpatterns = [
    path('',home_view,name="home"),
    path('create-quiz/', create_quiz_room, name='create_quiz_room'),
    path('quiz/<int:quiz_room_id>/create-room/', create_room, name='create_room'),
    path('quiz/<int:quiz_room_id>/add-question/', add_question, name='add_question'),
    path('quiz/<int:quiz_room_id>/manage/', manage_quiz_room, name='manage_quiz_room'),
    path('quiz/<int:quiz_room_id>/waiting_room/', waiting_room, name='waiting_room'),
    path('quiz/<int:quiz_room_id>/leaderboard/', leaderboard, name='leaderboard'),
    path('quiz/<int:quiz_room_id>/questions/', questions, name='questions'),
    path('quiz/<int:quiz_room_id>/buzzer/', buzzer, name='buzzer'),
    path('quiz/<int:quiz_room_id>/check-answer/<int:question_number>/', check_answer, name='check_answer')
]
