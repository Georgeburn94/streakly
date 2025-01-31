from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='home'),
    path('add/', views.add_habit, name='add_habit'),
    path('mark_complete/<int:habit_id>/', views.mark_complete, name='mark_complete'),
    path('habit/<int:habit_id>/calendar/', views.habit_calendar, name='habit_calendar'),  
]