from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from kanban import views

# Router setup for the REST API
# Configura o roteador para a API REST
router = DefaultRouter()

# Register viewsets which automatically create CRUD endpoints
# Registra os viewsets que criam endpoints CRUD automaticamente
router.register(r'tasks', views.TaskViewSet)       # /api/tasks/ endpoints for task objects
#                     endpoints para objetos de tarefa
router.register(r'teams', views.TeamViewSet)       # /api/teams/ for team objects
#                     endpoints para objetos de equipe
router.register(r'memberships', views.MembershipViewSet)  # /api/memberships/ associations
#                     endpoints para associações de membros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
]

