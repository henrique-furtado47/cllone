from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from kanban import views
from rest_framework.routers import DefaultRouter

# Router setup for the REST API
# Configura o roteador para a API REST
router = DefaultRouter()

# Register viewsets which automatically create CRUD endpoints
# Registra os viewsets que criam endpoints CRUD automaticamente
router.register(r'tasks', views.TaskViewSet, basename='task')       # /api/tasks/ endpoints for task objects
#                     endpoints para objetos de tarefa
router.register(r'teams', views.TeamViewSet, basename='team')       # /api/teams/ for team objects
#                     endpoints para objetos de equipe
router.register(r'memberships', views.MembershipViewSet)  # /api/memberships/ associations
#                     endpoints para associações de membros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/register/', views.register_view, name='register'),
    path('api/auth/me/', views.me_view, name='me'),
    path('api/auth/change-password/', views.change_password_view, name='change-password'),
    path('api/users/search/', views.search_users, name='search-users'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(
        url_name='schema',
        template_name='swagger-ui-custom.html',
    ), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include(router.urls)),
]

