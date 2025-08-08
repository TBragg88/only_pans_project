from django.shortcuts import render


def about_view(request):
    """About page view"""
    return render(request, 'about.html')
