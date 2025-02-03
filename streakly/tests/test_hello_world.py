from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from streakly.models import Habit

class HabitViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.habit = Habit.objects.create(name="Test Habit", user=self.user)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_add_habit_view(self):
        response = self.client.get(reverse('add_habit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_habit.html')

    def test_mark_complete_view(self):
        response = self.client.get(reverse('mark_complete', args=[self.habit.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after marking complete

    def test_delete_habit_view(self):
        response = self.client.get(reverse('delete_habit', args=[self.habit.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deleting habit