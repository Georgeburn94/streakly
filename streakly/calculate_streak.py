import sys
import os
import django
from datetime import date, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()
from streakly.models import Habit


def calculate_streak(habit):
    """
    Calculate the current streak for a habit.
    A streak is the number of consecutive days the habit has been completed.
    """
    # Get all completions for the habit, ordered by date (newest first)
    completions = habit.completions.filter(completed=True).order_by('-date')
    
    # If there are no completions, the streak is 0
    if not completions:
        habit.streak = 0
        habit.save()
        return 0
    
    streak = 0
    today = date.today()
    
    # Check if the habit was completed today
    if completions[0].date == today:
        streak += 1
    else:
        # If not completed today, the streak is 0
        habit.streak = 0
        habit.save()
        return 0
    
    # Check previous days for consecutive completions
    for i in range(1, len(completions)):
        if completions[i].date == today - timedelta(days=i):
            streak += 1
        else:
            break
    
    habit.streak = streak
    habit.save()
    return streak

