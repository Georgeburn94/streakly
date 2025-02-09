# Generated by Django 4.2.18 on 2025-01-30 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('health', 'Health'), ('fitness', 'Fitness'), ('productivity', 'Productivity'), ('mindfulness', 'Mindfulness'), ('learning', 'Learning'), ('other', 'Other')], default='other', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('streak', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HabitCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='completions', to='streakly.habit')),
            ],
        ),
    ]
