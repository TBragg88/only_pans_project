"""
URL configuration for the recipes app.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # Homepage
    path('test/', views.test_view, name='test_view'),  # Test view
    path('recipes/<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
    path(
        'recipes/<slug:slug>/delete/',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('create/', views.recipe_create, name='recipe_create'),
]
