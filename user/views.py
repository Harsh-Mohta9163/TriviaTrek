from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})
