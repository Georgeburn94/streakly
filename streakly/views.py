from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitCompletion
from .forms import HabitForm
from django.utils import timezone

# Create your views here.
def home_page_view(request):
    return render(request, 'home.html')

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habit_list.html', {'habits': habits})

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'add_habit.html', {'form': form})

@login_required
def mark_complete(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    habit.completed = True
    habit.save()
    return redirect('habit_list')