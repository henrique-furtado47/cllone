from rest_framework import serializers
from .models import Task, Team, Membership

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
  class Meta:
    model = Membership
    fields = '__all__'