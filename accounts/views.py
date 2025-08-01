"""
Authentication and profile views for the accounts app.
"""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .forms import CustomLoginForm, CustomRegisterForm, UserProfileForm


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
                return JsonResponse({
                    'success': True,
                    'username': user.username,
                    'first_name': user.first_name,
                })
            
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
@require_http_methods(["GET", "POST"])
def register_view(request):
    """Handle user registration with AJAX support."""
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'username': user.username,
                    'first_name': user.first_name,
                })
            
            messages.success(
                request,
                f'Welcome to OnlyPans, {user.username}!'
            )
            return redirect('recipe_list')
        else:
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Get first error message from form
                error_message = "Please correct the errors below."
                if form.errors:
                    first_field_errors = next(iter(form.errors.values()))
                    if first_field_errors:
                        error_message = first_field_errors[0]
                
                return JsonResponse({
                    'success': False,
                    'error': error_message
                })
            
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Handle user logout with AJAX support."""
    if request.user.is_authenticated:
        # Get display name (first name or username)
        display_name = (request.user.first_name
                        if request.user.first_name
                        else request.user.username)
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logout(request)
            return JsonResponse({
                'success': True,
                'message': f'Goodbye, {display_name}!'
            })
        
        logout(request)
        messages.success(
            request,
            f'Goodbye, {display_name}! You have been logged out.'
        )
    else:
        logout(request)
        
        # Handle AJAX requests for non-authenticated users
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'You have been logged out.'
            })
    
    return redirect('recipe_list')


@login_required
def profile_view(request, username=None):
    """Display user profile page."""
    if username:
        # Viewing someone else's profile
        profile_user = get_object_or_404(User, username=username)
        is_own_profile = request.user == profile_user
    else:
        # Viewing own profile
        profile_user = request.user
        is_own_profile = True
    
    # Ensure the user has a profile (create if doesn't exist)
    from .models import UserProfile
    user_profile, created = UserProfile.objects.get_or_create(
        user=profile_user
    )
    
    # Get user's recipes
    user_recipes = profile_user.recipes.all().order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'is_own_profile': is_own_profile,
        'user_recipes': user_recipes,
        'recipe_count': user_recipes.count(),
        'average_rating': user_profile.get_average_recipe_rating(),
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    """Edit user profile page."""
    # Ensure the user has a profile (create if doesn't exist)
    from .models import UserProfile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )
    
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user_profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully!'
            )
            return redirect('profile')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = UserProfileForm(
            instance=user_profile,
            user=request.user
        )
    
    return render(request, 'accounts/profile_edit.html', {'form': form})
