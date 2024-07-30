from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QuizRoom, Question
from .forms import QuizRoomForm,QuestionForm
from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'quiz/authenticated_home.html')
    else:
        return render(request, 'quiz/home.html')

def create_quiz_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            quiz_room = QuizRoom.objects.create(room_name=room_name, admin=request.user)
            return redirect('create_room', quiz_room_id=quiz_room.id)
    return redirect('home')

def create_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    question_form = QuestionForm()
    return render(request, 'quiz/create_room.html', {'quiz_room': quiz_room, 'question_form': question_form})

def add_question(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_room = quiz_room
            question.save()
            return render(request,'quiz/partials/question_display.html', {'question': question})
            
    return HttpResponse(status=400)

def manage_quiz_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    return render(request, 'quiz/manage_room.html', {'quiz_room': quiz_room})