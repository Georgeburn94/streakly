from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitCompletion
from .forms import HabitForm
from django.utils import timezone
from .calculate_streak import calculate_streak  # Import the calculate_streak function
from datetime import date  # Import date from datetime
from django.contrib.auth.models import User


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
    # Create a new HabitCompletion instance for today
    completion, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=date.today(),
        defaults={'completed': True}
    )
    if not created:
        completion.completed = True
        completion.save()
    calculate_streak(habit)  # Call the calculate_streak function
    return redirect('habit_list')