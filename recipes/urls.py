# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # Homepage
    path('test/', views.test_view, name='test_view'),  # Test view
    path('recipes/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('create/', views.recipe_create, name='recipe_create'),
]
