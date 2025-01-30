from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('add/', views.add_habit, name='add_habit'),
    path('habits/', views.habit_list, name='habit_list'),
    path('mark_complete/<int:habit_id>/', views.mark_complete, name='mark_complete'),
]