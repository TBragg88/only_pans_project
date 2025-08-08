from django.shortcuts import render
from django.http import HttpResponse


def about_view(request):
    """About page view"""
    return render(request, 'about.html')


def privacy_view(request):
    """Privacy Policy page view"""
    return render(request, 'privacy.html')


def terms_view(request):
    """Terms of Service page view"""
    return render(request, 'terms.html')


def robots_txt(request):
    """Minimal robots.txt allowing crawl."""
    content = "\n".join([
        "User-agent: *",
        "Allow: /",
    ])
    return HttpResponse(content, content_type="text/plain")
