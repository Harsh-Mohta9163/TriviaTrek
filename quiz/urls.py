from django.urls import path,include
from  .views import *


urlpatterns = [
    path('',home_view,name="home"),
    path('create-quiz-room/', create_quiz_room, name='create_quiz_room'),
    path('create-room/<int:quiz_room_id>/', create_room, name='create_room'),
    path('add-question/<int:quiz_room_id>/', add_question, name='add_question'),
    path('manage/<int:quiz_room_id>/', manage_quiz_room, name='manage_quiz_room'),
]
