from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Habit(models.Model):
    # Category choices (you can customize these)
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('fitness', 'Fitness'),
        ('productivity', 'Productivity'),
        ('mindfulness', 'Mindfulness'),
        ('learning', 'Learning'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')  # Link to the user who created the habit
    name = models.CharField(max_length=100)  # Name of the habit (e.g., "Drink water")
    description = models.TextField(blank=True, null=True)  # Optional description
    completed = models.BooleanField(default=False)  # Whether the habit was completed on this date
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')  # Category of the habit
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the habit was created
    streak = models.PositiveIntegerField(default=0)  # Current streak for the habit

    def __str__(self):
        return f"{self.name} (User: {self.user.username}, Category: {self.get_category_display()})"


class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')  # Link to the habit
    date = models.DateField(auto_now_add=True)  # Date when the habit was completed
    completed = models.BooleanField(default=False)  # Whether the habit was completed on this date

    def __str__(self):
        return f"{self.habit.name} on {self.date} (Completed: {self.completed})"