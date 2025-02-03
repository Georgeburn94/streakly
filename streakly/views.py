from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Habit, HabitCompletion
from .forms import HabitForm
from django.utils import timezone
from .calculate_streak import calculate_streak  # Import the calculate_streak function
from datetime import date  # Import date from datetime
from django.contrib.auth.models import User
from calendar import monthrange
from datetime import date, timedelta

# Home page
@login_required
def home(request):
    habits = Habit.objects.filter(user=request.user).order_by('created_at')
    
    # Get the current year and month
    today = date.today()
    year = today.year
    month = today.month

    all_habits_data = []

    for habit in habits:
        # Get the number of days in the current month
        _, num_days = monthrange(year, month)

        # Create a list of dates for the current month
        dates_in_month = [date(year, month, day) for day in range(1, num_days + 1)]

        # Create a dictionary to track completed dates
        completed_dates = {
            completion.date: completion.completed
            for completion in habit.completions.filter(date__year=year, date__month=month)
        }

        # Prepare the calendar data for the habit
        calendar_data = []
        for day_date in dates_in_month:
            calendar_data.append({
                'date': day_date,
                'completed': completed_dates.get(day_date, False),
            })

        all_habits_data.append({
            'habit': habit,
            'calendar_data': calendar_data,
        })

    return render(request, 'home.html', {
        'all_habits_data': all_habits_data,
        'year': year,
        'month': month,
    })

# Form to add a new habit
@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('home')
    else:
        form = HabitForm()
    return render(request, 'add_habit.html', {'form': form})

# Mark habit complete or incomplete
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

    return redirect('home')

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect('home')

