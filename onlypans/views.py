from django.shortcuts import render


def about_view(request):
    """About page view"""
    return render(request, 'about.html')


def privacy_view(request):
    """Privacy Policy page view"""
    return render(request, 'privacy.html')


def terms_view(request):
    """Terms of Service page view"""
    return render(request, 'terms.html')
