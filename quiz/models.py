from django.db import models
from django.contrib.auth.models import User

class QuizRoom(models.Model):
    room_name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='quiz_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name

class Question(models.Model):
    quiz_room = models.ForeignKey(QuizRoom, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])
    score_per_question = models.IntegerField(help_text="Score awarded for this question")
    time_allotted_per_question = models.IntegerField(help_text="Time allotted per question in seconds")
    question_number = models.IntegerField(help_text="The order of the question in the quiz")

    def __str__(self):
        return self.text
