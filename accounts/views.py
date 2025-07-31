from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomLoginForm, CustomRegisterForm
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('recipe_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('recipe_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('recipe_list')
