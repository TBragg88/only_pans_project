"""
Authentication views for the accounts app.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import CustomLoginForm, CustomRegisterForm


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login with AJAX support."""
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('recipe_list')
        else:
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'error': 'Invalid username or password.'
                })
            
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
            messages.success(request, f'Welcome to OnlyPans, {user.username}!')
            return redirect('recipe_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@csrf_protect
def logout_view(request):
    username = request.user.username if request.user.is_authenticated else None
    logout(request)
    if username:
        messages.success(request, f'Goodbye, {username}! You have been logged out.')
    return redirect('recipe_list')
