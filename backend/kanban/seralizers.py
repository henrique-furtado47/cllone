from rest_framework import serializers

from .models import Membership, Task, Team


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'
    read_only_fields = ['owner']

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
  class Meta:
    model = Membership
    fields = '__all__'