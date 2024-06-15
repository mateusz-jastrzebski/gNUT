from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .decorators import guest_required
from datetime import datetime

@guest_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            current_time = datetime.now().strftime('[%d/%b/%Y %H:%M:%S]')
            print(f"{current_time} User: {user} has logged in")
            return redirect('ups:home')
        else:
            error = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error': error})

    context = {'title': 'Authentication'}
    return render(request, 'login.html', context)

@login_required
def logout(request):
    return render(request, "login.html")
