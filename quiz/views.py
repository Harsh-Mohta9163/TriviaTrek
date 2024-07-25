from django.shortcuts import render

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'quiz/authenticated_home.html')
    else:
        return render(request, 'quiz/home.html')
