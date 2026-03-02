from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, through='Membership', related_name='teams')

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('admin', 'Admin'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    class Meta:
        unique_together = ('user', 'team')


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_tasks',
    )
    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_tasks',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
