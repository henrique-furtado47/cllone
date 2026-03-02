from django.contrib import admin
from .models import Team, Membership, Task


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'team', 'role')
    list_filter = ('role', 'team')
    search_fields = ('user__username', 'team__name')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'team', 'assignee', 'created_at', 'updated_at')
    list_filter = ('status', 'team')
    search_fields = ('title', 'description')
    list_editable = ('status',)