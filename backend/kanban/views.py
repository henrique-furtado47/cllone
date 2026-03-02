from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Membership, Task, Team
from .seralizers import MembershipSerializer, TaskSerializer, TeamSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response(
        {'error': 'Credenciais inválidas'},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username', '').strip()
    email = request.data.get('email', '').strip()
    password = request.data.get('password', '')
    password2 = request.data.get('password2', '')

    if not username or not password:
        return Response(
            {'error': 'Usuário e senha são obrigatórios.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if password != password2:
        return Response(
            {'error': 'As senhas não coincidem.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Este nome de usuário já está em uso.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH'])
def me_view(request):
    user = request.user
    if request.method == 'GET':
        teams = user.teams.all()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'teams': [{'id': t.id, 'name': t.name} for t in teams],
        })
    # PATCH — atualizar perfil
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.email = request.data.get('email', user.email)
    user.save()
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    })


@api_view(['POST'])
def change_password_view(request):
    user = request.user
    current = request.data.get('current_password', '')
    new_pw = request.data.get('new_password', '')
    new_pw2 = request.data.get('new_password2', '')

    if not user.check_password(current):
        return Response(
            {'error': 'Senha atual incorreta.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not new_pw or new_pw != new_pw2:
        return Response(
            {'error': 'As novas senhas não coincidem.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.set_password(new_pw)
    user.save()
    # Recriar token para manter sessão
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'message': 'Senha alterada com sucesso.'})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        user_teams = user.teams.all()
        return Task.objects.filter(
            Q(owner=user, team__isnull=True) | Q(team__in=user_teams)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer