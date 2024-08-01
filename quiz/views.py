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
            # Calculate the next question number based on existing questions
            question.question_number = quiz_room.questions.count() + 1
            question.save()
            return render(request, 'quiz/partials/question_display.html', {'question': question})
    return HttpResponse(status=400)



def manage_quiz_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    members = quiz_room.members.all()  # Assuming you have a ManyToMany or ForeignKey relationship with users
    return render(request, 'quiz/manage_room.html', {
        'quiz_room': quiz_room,
        'members': members
    })


def waiting_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    return render(request, 'quiz/waiting_room.html', {'quiz_room': quiz_room})

def leaderboard(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    # Logic to fetch leaderboard data
    # Replace the placeholder data with actual user scores
    leaderboard_data = [
        {'number': 1, 'name': 'Lee Taeyong', 'points': 258.244},
        {'number': 2, 'name': 'Mark Lee', 'points': 258.242},
        {'number': 3, 'name': 'Xiao Dejun', 'points': 258.223},
        {'number': 4, 'name': 'Qian Kun', 'points': 258.212},
        {'number': 5, 'name': 'Johnny Suh', 'points': 258.208},
    ]
    return render(request, 'quiz/leaderboard.html', {'quiz_room': quiz_room, 'leaderboard_data': leaderboard_data})

def questions(request, quiz_room_id):
    print("entered")
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    questions = quiz_room.questions.order_by('question_number')
    return render(request,'quiz/questions.html', {'quiz_room': quiz_room, 'questions': questions})