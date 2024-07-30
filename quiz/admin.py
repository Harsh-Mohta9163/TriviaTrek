from django.contrib import admin
from .models import QuizRoom, Question

class QuizRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'admin', 'created_at')
    search_fields = ('room_name', 'admin__username')  # Allows searching by room name and admin username

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz_room', 'correct_option', 'score_per_question')
    list_filter = ('quiz_room',)
    search_fields = ('text', 'quiz_room__room_name')

admin.site.register(QuizRoom, QuizRoomAdmin)
admin.site.register(Question, QuestionAdmin)
