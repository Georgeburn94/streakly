from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_habit, name='add_habit'),
    path('mark_complete/<int:habit_id>/', views.mark_complete, name='mark_complete'),
    path('delete_habit/<int:habit_id>/', views.delete_habit, name='delete_habit'),
    path('about', views.about, name='about'),
    ]