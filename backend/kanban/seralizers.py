from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Membership, Task, Team


class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'
    read_only_fields = ['owner']


class MembershipSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)
  user_id = serializers.IntegerField(source='user.id', read_only=True)

  class Meta:
    model = Membership
    fields = ['id', 'user', 'user_id', 'username', 'team', 'role']
    extra_kwargs = {'user': {'write_only': True}}


class TeamSerializer(serializers.ModelSerializer):
  memberships = MembershipSerializer(source='membership_set', many=True, read_only=True)
  member_count = serializers.SerializerMethodField()

  class Meta:
    model = Team
    fields = ['id', 'name', 'description', 'memberships', 'member_count']

  def get_member_count(self, obj):
    return obj.membership_set.count()


class UserSearchSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email']