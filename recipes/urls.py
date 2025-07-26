# recipes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # Homepage
    path('recipes/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
]
