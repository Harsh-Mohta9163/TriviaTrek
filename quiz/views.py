from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QuizRoom, Question,Score
from .forms import QuizRoomForm,QuestionForm
from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
def home_view(request):
    user=request.user
    if request.user.is_authenticated:
        return render(request, 'quiz/authenticated_home.html',{'user':user})
    else:
        return render(request, 'quiz/home.html')


@login_required
def create_quiz_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        is_buzzer = request.POST.get('is_buzzer') == 'True'  # Get the is_buzzer value
        if room_name:
            quiz_room = QuizRoom.objects.create(
                room_name=room_name, 
                admin=request.user, 
                is_buzzer=is_buzzer  # Set is_buzzer based on form input
            )
            if is_buzzer:
                return redirect('manage_quiz_room', quiz_room_id=quiz_room.id)
            return redirect('create_room', quiz_room_id=quiz_room.id)
    return redirect('home')

@login_required
def create_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    question_form = QuestionForm()
    return render(request, 'quiz/create_room.html', {'quiz_room': quiz_room, 'question_form': question_form})

@login_required
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


@login_required
def manage_quiz_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    members = quiz_room.members.all()  # Assuming you have a ManyToMany or ForeignKey relationship with users
    return render(request, 'quiz/manage_room.html', {
        'quiz_room': quiz_room,
        'members': members
    })

@login_required
def waiting_room(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    
    return render(request, 'quiz/waiting_room.html', {'quiz_room': quiz_room})

   

@login_required
def questions(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    question_number = int(request.GET.get('question_number', 1))
    current_question = quiz_room.questions.order_by('question_number').filter(question_number=question_number).first()
    user_id = request.user.id 
    user = get_object_or_404(User, id=user_id)
    print(f"user_id={user_id}")
    if current_question is None:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'quiz_finished': True})
        return render(request, 'quiz/leaderboard.html')

    context = {
        'quiz_room': quiz_room,
        'current_question': current_question,
        'user': user,  # Add this line to pass user ID to the template
        'is_final_question': current_question.question_number == quiz_room.questions.count()  # Flag for final question
    }
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('quiz/partials/quiz_display.html', context)
        return JsonResponse({
            'html': html,
            'question_number': current_question.question_number,
            'time_limit': current_question.time_allotted_per_question,
            'is_final_question': context['is_final_question']
        })

    return render(request, 'quiz/questions.html', context)

@login_required
def check_answer(request, quiz_room_id, question_number):
    print("entered")
    if request.method == 'POST':
        quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
        current_question = get_object_or_404(Question, quiz_room=quiz_room, question_number=question_number)
        data = json.loads(request.body)
        selected_option = data.get('selected_option')

        is_correct = (selected_option == current_question.correct_option)
        
        return JsonResponse({'is_correct': is_correct})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def leaderboard(request, quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    if quiz_room.is_buzzer:
        return render(request,'quiz/buzzer_leaderboard.html',{'quiz_room':quiz_room})
    else:
        # Create score objects for all members except the admin, if they don't already exist
        for member in quiz_room.members.exclude(id=quiz_room.admin.id):
            Score.objects.get_or_create(quiz_room=quiz_room, user=member)
        
        # Fetch the leaderboard data
        leaderboard = Score.objects.filter(quiz_room=quiz_room).order_by('-points')
        leaderboard_data = [
            {'number': idx + 1, 'name': score.user.username, 'points': score.points}
            for idx, score in enumerate(leaderboard)
        ]
        
        return render(request, 'quiz/leaderboard.html', {
            'quiz_room': quiz_room,
            'leaderboard_data': leaderboard_data
        })

def buzzer(request,quiz_room_id):
    quiz_room = get_object_or_404(QuizRoom, id=quiz_room_id)
    return render(request,'quiz/buzzer.html',{'quiz_room':quiz_room})