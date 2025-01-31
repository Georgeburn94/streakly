from django.shortcuts import render, redirect, get_object_or_404
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
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    # Toggle the habit's completed status
    habit.completed = not habit.completed
    habit.save()

    # Get or create the HabitCompletion instance for today
    today = date.today()
    completion, created = HabitCompletion.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={'completed': True}
    )

    if not habit.completed:
        # If the habit is toggled to "not completed," delete the HabitCompletion for today
        completion.delete()
        # Decrease the streak by 1 if the streak is greater than 0
        if habit.streak > 0:
            habit.streak -= 1
            habit.save()
    else:
        # If the habit is toggled to "completed," ensure the HabitCompletion is marked as completed
        completion.completed = True
        completion.save()
        # Recalculate the streak when the habit is marked as completed
        calculate_streak(habit)

    return redirect('habit_list')