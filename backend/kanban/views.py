from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Membership, Task, Team
from .seralizers import (MembershipSerializer, TaskSerializer, TeamSerializer,
                         UserSearchSerializer)


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
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.teams.all()

    def perform_create(self, serializer):
        team = serializer.save()
        # O criador vira admin automaticamente
        Membership.objects.create(user=self.request.user, team=team, role='admin')

    def perform_update(self, serializer):
        team = self.get_object()
        membership = Membership.objects.filter(user=self.request.user, team=team, role='admin').first()
        if not membership:
            raise PermissionDenied('Apenas administradores podem editar o time.')
        serializer.save()

    def perform_destroy(self, instance):
        membership = Membership.objects.filter(user=self.request.user, team=instance, role='admin').first()
        if not membership:
            raise PermissionDenied('Apenas administradores podem excluir o time.')
        instance.delete()

    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        """Adiciona um membro ao time. Apenas admins podem adicionar."""
        team = self.get_object()
        admin_check = Membership.objects.filter(user=request.user, team=team, role='admin').exists()
        if not admin_check:
            return Response({'error': 'Apenas administradores podem adicionar membros.'}, status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username', '').strip()
        role = request.data.get('role', 'member')

        if not username:
            return Response({'error': 'Nome de usuário é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if Membership.objects.filter(user=user, team=team).exists():
            return Response({'error': 'Usuário já é membro deste time.'}, status=status.HTTP_400_BAD_REQUEST)

        membership = Membership.objects.create(user=user, team=team, role=role)
        return Response(MembershipSerializer(membership).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        """Remove um membro do time. Apenas admins podem remover."""
        team = self.get_object()
        admin_check = Membership.objects.filter(user=request.user, team=team, role='admin').exists()
        if not admin_check:
            return Response({'error': 'Apenas administradores podem remover membros.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        membership = Membership.objects.filter(user_id=user_id, team=team).first()
        if not membership:
            return Response({'error': 'Membro não encontrado neste time.'}, status=status.HTTP_404_NOT_FOUND)

        # Não deixa remover a si mesmo se for o único admin
        if int(user_id) == request.user.id:
            admin_count = Membership.objects.filter(team=team, role='admin').count()
            if admin_count <= 1:
                return Response({'error': 'Você é o único admin. Promova outro membro antes de sair.'}, status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        return Response({'message': 'Membro removido com sucesso.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='change-role')
    def change_role(self, request, pk=None):
        """Muda o role de um membro. Apenas admins podem alterar."""
        team = self.get_object()
        admin_check = Membership.objects.filter(user=request.user, team=team, role='admin').exists()
        if not admin_check:
            return Response({'error': 'Apenas administradores podem alterar papéis.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        new_role = request.data.get('role', 'member')

        membership = Membership.objects.filter(user_id=user_id, team=team).first()
        if not membership:
            return Response({'error': 'Membro não encontrado neste time.'}, status=status.HTTP_404_NOT_FOUND)

        membership.role = new_role
        membership.save()
        return Response(MembershipSerializer(membership).data)


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def search_users(request):
    """Busca usuários por username para adicionar a times."""
    query = request.query_params.get('q', '').strip()
    if len(query) < 2:
        return Response([])
    users = User.objects.filter(username__icontains=query)[:10]
    return Response(UserSearchSerializer(users, many=True).data)